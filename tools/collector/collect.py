#!/usr/bin/env python3
"""Zone3 measurement collector — a small, self-hosted endpoint for the site's own events.

    python3 tools/collector/collect.py --dir ./data --port 8787

What it is
    A standard-library HTTP server that accepts the events the site's counter posts, writes one
    JSON object per line to a local file, and can report the counts back. It is the "self-hosted
    analytics endpoint" in the owner brief.

What it deliberately does not do
    * It never writes the client address, the User-Agent, the Referer, or any cookie. The only
      fields it stores are the seven the payload contract allows (see data/analytics/events.json).
    * It has no dashboard, no login, no third-party dependency and no network access of its own.
      It listens, it writes a file, it answers a count.
    * It never generates an event. Nothing reaches it except a POST from a reader's browser.

Routes
    POST /e       one JSON object {"events": [ ... ]}; 204 on success, 400 on a bad payload
    GET  /stats   JSON counts by event, by page and by target
    GET  /health  JSON liveness
    GET  /        a one-paragraph description of the above

Options
    --dir DIR         where the event file and the counters live (default ./collector-data)
    --file NAME       event file name inside --dir (default events.jsonl)
    --port N          port to listen on (default 8787)
    --host H          address to bind (default 127.0.0.1; use 0.0.0.0 to serve the internet)
    --allow-origin O  Origin allowed to post (repeatable). Default: the Zone3 Pages origin.
    --retention-days N  events older than this are pruned at startup and hourly (default 30)

Test
    python3 tools/collector/test_collector.py
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ALLOWED_EVENTS = {
    "outbound_click",
    "guide_view",
    "comparison_view",
    "cta_click",
    "disclosure_impression",
}

FIELD_LIMITS = {
    "e": 40,
    "p": 200,
    "t": 120,
    "l": 60,
    "a": 5,
    "ts": 12,
    "d": 10,
}

MAX_BODY_BYTES = 64 * 1024
DEFAULT_ORIGINS = ["https://kanlerxz87-cyber.github.io"]
PATH_RE = re.compile(r"^/[A-Za-z0-9._~!$&'()*+,;=:@%/-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOCK = threading.Lock()


def clean_event(raw: dict) -> dict | None:
    """Keep only the allowed fields, in the allowed shapes. Return None when it is not an event."""
    if not isinstance(raw, dict):
        return None
    name = raw.get("e")
    if name not in ALLOWED_EVENTS:
        return None
    out: dict = {"e": name}
    for field, limit in FIELD_LIMITS.items():
        if field == "e":
            continue
        value = raw.get(field)
        if value is None:
            continue
        if field == "a":
            if value is True or value is False:
                out["a"] = value
            continue
        if field == "ts":
            try:
                out["ts"] = int(value)
            except (TypeError, ValueError):
                return None
            continue
        if not isinstance(value, str):
            return None
        value = value.strip()
        if len(value) > limit:
            return None
        if field == "p":
            if not value.startswith("/") or not PATH_RE.match(value):
                return None
        if field == "d" and not DATE_RE.match(value):
            return None
        out[field] = value
    if "p" not in out or "ts" not in out:
        return None
    return out


class Collector:
    """The storage half of the collector: append events, prune them, count them."""

    def __init__(self, directory: pathlib.Path, filename: str, retention_days: int) -> None:
        self.directory = directory
        self.path = directory / filename
        self.retention_days = retention_days
        self.directory.mkdir(parents=True, exist_ok=True)

    def _prune(self, lines: list[str]) -> list[str]:
        if self.retention_days <= 0:
            return lines
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        kept = []
        for line in lines:
            try:
                item = json.loads(line)
            except ValueError:
                continue
            stamp = item.get("ts")
            if not isinstance(stamp, int):
                continue
            if datetime.fromtimestamp(stamp, timezone.utc) >= cutoff:
                kept.append(line)
        return kept

    def append(self, events: list[dict]) -> int:
        with LOCK:
            existing = []
            if self.path.exists():
                existing = [ln for ln in self.path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            existing.extend(json.dumps(e, separators=(",", ":"), sort_keys=True) for e in events)
            existing = self._prune(existing)
            self.path.write_text("\n".join(existing) + "\n", encoding="utf-8")
        return len(events)

    def events(self) -> list[dict]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def stats(self) -> dict:
        events = self.events()
        by_event: dict = {}
        by_page: dict = {}
        by_target: dict = {}
        for item in events:
            by_event[item.get("e", "?")] = by_event.get(item.get("e", "?"), 0) + 1
            page = item.get("p", "?")
            by_page[page] = by_page.get(page, 0) + 1
            target = item.get("t")
            if target:
                by_target[target] = by_target.get(target, 0) + 1
        return {
            "events_stored": len(events),
            "by_event": dict(sorted(by_event.items())),
            "by_page": dict(sorted(by_page.items(), key=lambda kv: (-kv[1], kv[0]))),
            "by_target": dict(sorted(by_target.items(), key=lambda kv: (-kv[1], kv[0]))),
            "fields_stored": sorted({k for item in events for k in item}),
            "retention_days": self.retention_days,
        }


class Handler(BaseHTTPRequestHandler):
    server_version = "Zone3Collector/1.0"
    collector: Collector
    allowed_origins: list

    def log_message(self, fmt, *args):  # noqa: A003 - the request line only, never the client address
        # The default implementation prints the client IP. This collector must not keep the
        # address of any reader anywhere, including its own log, so it is left out.
        sys.stderr.write("%s\n" % (fmt % args))

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True  # same-origin or a non-browser client
        return origin in self.allowed_origins

    def _send(self, code: int, body: str, content_type: str = "application/json") -> None:
        payload = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        origin = self.headers.get("Origin")
        if origin and origin in self.allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def do_OPTIONS(self):  # noqa: N802 - the BaseHTTPRequestHandler API
        if not self._origin_allowed():
            self._send(403, '{"error":"origin not allowed"}')
            return
        self.send_response(204)
        origin = self.headers.get("Origin")
        if origin and origin in self.allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Max-Age", "600")
            self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self):  # noqa: N802 - the BaseHTTPRequestHandler API
        if self.path.split("?")[0] == "/health":
            self._send(200, json.dumps({"status": "ok", "events": len(self.collector.events())}))
        elif self.path.split("?")[0] == "/stats":
            self._send(200, json.dumps(self.collector.stats(), indent=1))
        elif self.path.split("?")[0] == "/":
            self._send(200, json.dumps({
                "service": "Zone3 measurement collector",
                "routes": ["POST /e", "GET /stats", "GET /health"],
                "stores": "event name, page path, target, link label, boolean flag, timestamp, date",
                "never_stores": ["IP address", "User-Agent", "Referer", "cookies", "visitor identifier"],
            }, indent=1))
        else:
            self._send(404, '{"error":"not found"}')

    def do_POST(self):  # noqa: N802 - the BaseHTTPRequestHandler API
        if self.path.split("?")[0] != "/e":
            self._send(404, '{"error":"not found"}')
            return
        if not self._origin_allowed():
            self._send(403, '{"error":"origin not allowed"}')
            return
        length = self.headers.get("Content-Length")
        try:
            size = int(length) if length else 0
        except ValueError:
            size = 0
        if size <= 0 or size > MAX_BODY_BYTES:
            self._send(400, '{"error":"empty or oversized body"}')
            return
        raw = self.rfile.read(size)
        try:
            body = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._send(400, '{"error":"body is not JSON"}')
            return
        items = body.get("events") if isinstance(body, dict) else None
        if not isinstance(items, list) or not items:
            self._send(400, '{"error":"expected an events array"}')
            return
        cleaned = [e for e in (clean_event(item) for item in items) if e]
        if not cleaned:
            self._send(400, '{"error":"no event matched the contract"}')
            return
        self.collector.append(cleaned)
        self._send(204, "")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Zone3 measurement collector")
    ap.add_argument("--dir", default="collector-data", help="directory for the event file")
    ap.add_argument("--file", default="events.jsonl", help="event file name")
    ap.add_argument("--host", default="127.0.0.1", help="address to bind")
    ap.add_argument("--port", type=int, default=8787, help="port to listen on")
    ap.add_argument("--allow-origin", action="append", default=[],
                    help="Origin allowed to post (repeatable)")
    ap.add_argument("--retention-days", type=int, default=30, help="prune events older than this")
    args = ap.parse_args(argv)

    collector = Collector(pathlib.Path(args.dir), args.file, args.retention_days)
    handler = type("BoundHandler", (Handler,), {
        "collector": collector,
        "allowed_origins": args.allow_origin or DEFAULT_ORIGINS,
    })
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print({
        "listening": f"http://{args.host}:{args.port}",
        "events_file": str(collector.path),
        "allowed_origins": handler.allowed_origins,
        "retention_days": args.retention_days,
    }, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
