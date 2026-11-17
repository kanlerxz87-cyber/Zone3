#!/usr/bin/env python3
"""Self-hosted, privacy-preserving collector for Zone3 page and outbound-click events (build 38650305).

It is NOT hosted by this repository. GitHub Pages serves static files only, so the owner must run
this script on a host they control, then set endpoint_url in data/shop/measurement.json and rebuild
(python3 tools/build_measurement.py).

Standard library only.

  python3 tools/analytics_endpoint.py --port 8787 --store ~/z3-analytics/counts.json
  python3 tools/analytics_endpoint.py --self-test          # offline test, exit 1 on failure

Endpoints
  POST /collect   JSON or text/plain body: {"v":1,"e":<event>,"p":<path>,"h":<host>,"t":<token>}
                  204 on success, 400 on a rejected field, 413 when the body is over 2 KB.
  GET  /counts    Daily totals. Enabled only when the environment variable Z3_ANALYTICS_READ_TOKEN
                  is set; requires header "Authorization: Bearer <token>". Otherwise 404.
  GET  /healthz   200 "ok".

What is stored: per UTC day, per event name, per page path, per link host and token, a count. Nothing
else. The server does not write request logs, does not read or store the client IP address, the user
agent or the referrer, and ignores any client-supplied date.
"""
from __future__ import annotations

import argparse
import hmac
import json
import os
import pathlib
import re
import sys
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EVENTS = ("page_view", "outbound_click", "guide_view", "intent_view", "flag_view")
MAX_BODY = 2048
PATH_RE = re.compile(r"^/[A-Za-z0-9/_.\-]{0,199}$")
HOST_RE = re.compile(r"^[a-z0-9.\-]{0,100}$")
TOKEN_RE = re.compile(r"^[A-Za-z0-9]{0,20}$")
DEFAULT_ORIGIN = "https://kanlerxz87-cyber.github.io"
_lock = threading.Lock()


class Store:
    """Aggregate counts only: {day: {event: {path: {host|token: count}}}}."""

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.data: dict = {}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8") or "{}")

    def add(self, day: str, event: str, page: str, host: str, token: str) -> None:
        with _lock:
            by_path = self.data.setdefault(day, {}).setdefault(event, {}).setdefault(page, {})
            key = f"{host}|{token}" if (host or token) else ""
            by_path[key] = by_path.get(key, 0) + 1
            self._write()

    def totals(self, day: str | None = None) -> dict:
        out: dict = {}
        for d, events in self.data.items():
            if day and d != day:
                continue
            for ev, pages in events.items():
                out[ev] = out.get(ev, 0) + sum(sum(v.values()) for v in pages.values())
        return out

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), prefix=".counts-")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, indent=1, sort_keys=True)
        os.replace(tmp, self.path)


def validate(payload: object) -> tuple[dict | None, str]:
    """Return (clean_record, '') or (None, reason). Only the allow-listed fields survive."""
    if not isinstance(payload, dict):
        return None, "body must be a JSON object"
    if payload.get("v") != 1:
        return None, "unsupported version"
    e = payload.get("e")
    if e not in EVENTS:
        return None, "unknown event"
    p = payload.get("p", "/")
    if not isinstance(p, str) or not PATH_RE.match(p) or "//" in p:
        return None, "bad path"
    h = payload.get("h", "")
    if not isinstance(h, str) or not HOST_RE.match(h):
        return None, "bad host"
    t = payload.get("t", "")
    if not isinstance(t, str) or not TOKEN_RE.match(t):
        return None, "bad token"
    return {"e": e, "p": p, "h": h, "t": t}, ""


def make_handler(store: Store, origin: str, read_token: str | None):
    class Handler(BaseHTTPRequestHandler):
        server_version = "Z3Collector/1"
        sys_version = ""

        def log_message(self, fmt, *args):  # no request logging: no IP addresses, no user agents
            return

        def _send(self, code: int, body: bytes = b"", ctype: str = "text/plain") -> None:
            self.send_response(code)
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def do_OPTIONS(self):  # noqa: N802
            self._send(204)

        def do_POST(self):  # noqa: N802
            if self.path.split("?")[0] != "/collect":
                return self._send(404)
            try:
                n = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                return self._send(400)
            if n <= 0:
                return self._send(400)
            if n > MAX_BODY:
                return self._send(413)
            raw = self.rfile.read(n)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return self._send(400)
            rec, why = validate(payload)
            if rec is None:
                return self._send(400, why.encode())
            day = datetime.now(timezone.utc).strftime("%Y-%m-%d")  # server clock only
            store.add(day, rec["e"], rec["p"], rec["h"], rec["t"])
            return self._send(204)

        def do_GET(self):  # noqa: N802
            path = self.path.split("?")[0]
            if path == "/healthz":
                return self._send(200, b"ok")
            if path == "/counts" and read_token:
                auth = self.headers.get("Authorization", "")
                if not hmac.compare_digest(auth, f"Bearer {read_token}"):
                    return self._send(401)
                body = json.dumps({"totals_by_event": store.totals()}, indent=1).encode()
                return self._send(200, body, "application/json")
            return self._send(404)

    return Handler


def self_test() -> int:
    """Offline checks: allow-list, field filtering, aggregate-only storage, no identifiers stored."""
    failures: list[str] = []

    def check(cond: bool, label: str) -> None:
        print(("PASS " if cond else "FAIL ") + label)
        if not cond:
            failures.append(label)

    ok, _ = validate({"v": 1, "e": "page_view", "p": "/Zone3/index.html"})
    check(ok is not None, "valid page_view accepted")
    check(validate({"v": 1, "e": "visitor_profile", "p": "/"})[0] is None, "unknown event rejected")
    check(validate({"v": 1, "e": "page_view", "p": "/a//b"})[0] is None, "double-slash path rejected")
    check(validate({"v": 1, "e": "page_view", "p": "/x?user=1"})[0] is None, "query string in path rejected")
    check(validate({"v": 2, "e": "page_view", "p": "/"})[0] is None, "wrong version rejected")
    check(validate({"v": 1, "e": "outbound_click", "p": "/", "h": "link.amazon", "t": "B0CDY277D3"})[0] is not None,
          "outbound_click with host and token accepted")
    check(validate({"v": 1, "e": "outbound_click", "p": "/", "t": "bad token!"})[0] is None,
          "token with punctuation rejected")
    rec, _ = validate({"v": 1, "e": "page_view", "p": "/", "ip": "203.0.113.9", "ua": "x", "ref": "y", "d": "1999-01-01"})
    check(rec == {"e": "page_view", "p": "/", "h": "", "t": ""}, "extra fields (ip, ua, ref, date) dropped")

    with tempfile.TemporaryDirectory() as tmp:
        store = Store(pathlib.Path(tmp) / "counts.json")
        store.add("2026-11-17", "outbound_click", "/Zone3/guides/x.html", "link.amazon", "B04G1MEwY")
        store.add("2026-11-17", "outbound_click", "/Zone3/guides/x.html", "link.amazon", "B04G1MEwY")
        store.add("2026-11-17", "page_view", "/Zone3/index.html", "", "")
        check(store.totals("2026-11-17") == {"outbound_click": 2, "page_view": 1}, "daily totals aggregate correctly")
        stored = (pathlib.Path(tmp) / "counts.json").read_text(encoding="utf-8")
        check(not re.search(r"ip|user.?agent|referr|cookie|visitor", stored, re.I),
              "stored file contains no IP, user-agent, referrer, cookie or visitor key")

    if failures:
        print(f"SELF-TEST FAIL · {len(failures)} check(s) failed")
        return 1
    print("SELF-TEST PASS · collector allow-list, field filter and aggregate-only store")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--store", default=str(pathlib.Path.home() / "z3-analytics" / "counts.json"))
    ap.add_argument("--origin", default=DEFAULT_ORIGIN, help="allowed CORS origin (the public site)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    store = Store(pathlib.Path(args.store))
    read_token = os.environ.get("Z3_ANALYTICS_READ_TOKEN") or None
    srv = ThreadingHTTPServer((args.host, args.port), make_handler(store, args.origin, read_token))
    print(f"collector on {args.host}:{args.port}; store={args.store}; read endpoint={'on' if read_token else 'off'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
