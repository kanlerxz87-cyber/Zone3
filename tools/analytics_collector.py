#!/usr/bin/env python3
"""Legacy self-hosted analytics collector — retained for historical self-tests only.

Historical contract: data/analytics.json (0C4-T4, session 0c4c4cb6, 2026-11-17).
This implements the older five-event /e contract for provenance and the legacy test suite;
it is not the current collector and must not be enabled with the active browser runtime.
Current source of truth: data/shop/measurement.json; active browser client:
assets/measure.js; active reference endpoint: tools/analytics_endpoint.py. The current
production configuration remains OFF and has no deployed endpoint.

Historical routes:
  POST /e           validate and append an old-schema event
  GET  /stats       legacy aggregate readout
  GET  /            legacy summary

This file remains useful for compatibility tests. Do not follow the old deployment
example or set window.ZONE3_ANALYTICS_ENDPOINT on current pages; doing so beside the
canonical Z3_MEASURE runtime risks duplicate or incompatible counting.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EVENTS = {"page_view", "guide_view", "product_click", "special_link_click", "nav_click"}
HOST_RE = re.compile(r"^[A-Za-z0-9.\-]{1,253}$")
LEDGER = pathlib.Path("data/analytics-ledger.jsonl")


def clean_event(raw: object) -> dict:
    """Validate one event against data/analytics.json; raise ValueError with a reason."""
    if not isinstance(raw, dict):
        raise ValueError("body must be a JSON object")
    unknown = set(raw) - {"e", "p", "r", "t"}
    if unknown:
        raise ValueError(f"unknown field(s): {', '.join(sorted(unknown))}")
    e = raw.get("e")
    if e not in EVENTS:
        raise ValueError(f"event id must be one of: {', '.join(sorted(EVENTS))}")
    p = raw.get("p")
    if not isinstance(p, str) or not p.startswith("/"):
        raise ValueError("p must be a URL path starting with '/'")
    p = p.split("?", 1)[0].split("#", 1)[0]  # defensive re-strip
    if len(p) > 300:
        raise ValueError("p too long")
    r = raw.get("r", "")
    if r in ("", None):
        r = ""
    elif isinstance(r, str):
        r = r.split("/", 1)[0].lower()  # host only, defensively
        if not HOST_RE.match(r):
            r = ""
    else:
        raise ValueError("r must be a string host name or empty")
    t = raw.get("t")
    if not isinstance(t, str) or len(t) > 40:
        t = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {"e": e, "p": p, "r": r, "t": t, "ts": int(time.time())}


class Handler(BaseHTTPRequestHandler):
    ledger: pathlib.Path = LEDGER
    retention_s: int = 24 * 3600

    def log_message(self, fmt, *args):  # no per-request logging of anything but status
        pass

    def _code(self, n: int, body: bytes = b"", ctype: str = "application/json") -> None:
        self.send_response(n)
        if body:
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_POST(self):  # noqa: N802
        if self.path.split("?", 1)[0] != "/e":
            self._code(404, b'{"error":"not found"}')
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if n <= 0 or n > 4096:
            self._code(400, b'{"error":"empty or oversized body"}')
            return
        try:
            event = clean_event(json.loads(self.rfile.read(n).decode("utf-8")))
        except (ValueError, json.JSONDecodeError) as ex:
            self._code(400, json.dumps({"error": str(ex)}).encode())
            return
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, separators=(",", ":")) + "\n")
        self._code(204)

    def do_GET(self):  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path == "/stats":
            self._code(200, json.dumps(self.stats()).encode())
        elif path == "/":
            body = (
                "Zone3 analytics collector. POST /e with one of: "
                + ", ".join(sorted(EVENTS))
                + ". GET /stats for aggregates. Schema: data/analytics.json.\n"
            ).encode()
            self._code(200, body, "text/plain; charset=utf-8")
        else:
            self._code(404, b'{"error":"not found"}')

    def stats(self) -> dict:
        by_event: dict[str, int] = {}
        by_path: dict[str, int] = {}
        total = 0
        if self.ledger.exists():
            cutoff = int(time.time()) - self.retention_s
            for line in self.ledger.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("ts", 0) < cutoff:
                    continue
                total += 1
                by_event[rec["e"]] = by_event.get(rec["e"], 0) + 1
                by_path[rec["p"]] = by_path.get(rec["p"], 0) + 1
        return {
            "window_hours": self.retention_s // 3600,
            "total": total,
            "by_event": dict(sorted(by_event.items())),
            "by_path": dict(sorted(by_path.items(), key=lambda kv: (-kv[1], kv[0]))),
            "identifiers_retained": "none",
        }

    def prune(self) -> int:
        return prune_ledger(self.ledger, self.retention_s)


def prune_ledger(ledger: pathlib.Path, retention_s: int) -> int:
    if not ledger.exists():
        return 0
    cutoff = int(time.time()) - retention_s
    keep, dropped = [], 0
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            dropped += 1
            continue
        if rec.get("ts", 0) >= cutoff:
            keep.append(line)
        else:
            dropped += 1
    if dropped:
        ledger.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")
    return dropped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8081)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--ledger", type=pathlib.Path, default=LEDGER)
    ap.add_argument("--retention-hours", type=int, default=24)
    ap.add_argument("--prune", action="store_true", help="prune the ledger to the retention window and exit")
    a = ap.parse_args()

    Handler.ledger = a.ledger
    Handler.retention_s = max(3600, a.retention_hours * 3600)

    if a.prune:
        dropped = prune_ledger(a.ledger, max(3600, a.retention_hours * 3600))
        print(f"pruned {dropped} line(s) older than {a.retention_hours}h from {a.ledger}")
        return 0

    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"zone3 analytics collector on http://{a.host}:{a.port}/e  (ledger: {a.ledger})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
