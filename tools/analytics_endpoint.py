#!/usr/bin/env python3
"""Zone3 aggregate-only self-hosted collector. GitHub Pages cannot execute this server.

POST /collect: the documented five events, approved origin, known public page, known
Amazon product token, <=2 KiB. GET /healthz: health only. GET /counts: disabled unless
Z3_ANALYTICS_READ_TOKEN is set; bearer authorization required. No IP/referrer/UA/cookie
logs, raw event rows, session IDs, or client timestamps. Disable reverse-proxy/CDN request
logs separately. Counts are not unique people, sessions, orders or conversions.

Run: python3 tools/analytics_endpoint.py --port 8787 --store /private/zone3/counts.json
Test: python3 tools/analytics_endpoint.py --self-test
"""
from __future__ import annotations

import argparse
import copy
import hmac
import json
import os
import pathlib
import re
import sys
import tempfile
import threading
import time
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVENTS = ('page_view', 'outbound_click', 'guide_view', 'intent_view', 'flag_view')
MAX_BODY = 2048
RETENTION_DAYS = 90
PATH_RE = re.compile(r'/[A-Za-z0-9/_.\-]{0,199}')
HOST_RE = re.compile(r'[a-z0-9.\-]{0,100}')
TOKEN_RE = re.compile(r'[A-Za-z0-9]{0,20}')
DEFAULT_ORIGIN = 'https://kanlerxz87-cyber.github.io'


def public_paths() -> set[str]:
    """Finite public-page allow-list; both preview and /Zone3 project-site routes."""
    paths = {'/', '/Zone3/'}
    skip = {'.git', 'archive', 'docs', 'sessions', 'node_modules', '.preview', '.local', '__pycache__'}
    for path in ROOT.rglob('*.html'):
        rel = path.relative_to(ROOT)
        if any(part in skip for part in rel.parts):
            continue
        for prefix in ('/', '/Zone3/'):
            url = prefix + rel.as_posix()
            paths.add(url)
            if url.endswith('/index.html'):
                paths.add(url[:-10])
    return paths


def product_targets() -> set[tuple[str, str]]:
    targets = set()
    registry = json.loads((ROOT / 'data/publication.json').read_text(encoding='utf-8'))
    for p in registry['products']:
        token = p['submitted_link'].rsplit('/', 1)[-1]
        targets.add(('link.amazon', token))
        for host in ('amazon.com', 'www.amazon.com'):
            targets.add((host, p['observed_asin']))
            targets.add((host, token))  # historical direct-identifier evidence links, not valid-link claims
    return targets


class Store:
    """Only {UTC day: {event: {known page: {public host|token: count}}}} is persisted."""

    def __init__(self, path: pathlib.Path, retention_days: int = RETENTION_DAYS):
        self.path = path
        self.retention_days = retention_days
        self.lock = threading.RLock()
        self.data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        if not isinstance(self.data, dict):
            raise ValueError('aggregate store must be a JSON object')
        if self._prune():
            self._write()

    def _prune(self, today: date | None = None) -> bool:
        cutoff = ((today or datetime.now(timezone.utc).date()) - timedelta(days=self.retention_days - 1)).isoformat()
        removed = [day for day in self.data if day < cutoff]
        for day in removed:
            del self.data[day]
        return bool(removed)

    def add(self, day: str, event: str, page: str, host: str, token: str) -> None:
        with self.lock:
            by_path = self.data.setdefault(day, {}).setdefault(event, {}).setdefault(page, {})
            key = f'{host}|{token}' if (host or token) else ''
            by_path[key] = by_path.get(key, 0) + 1
            self._prune()
            self._write()

    def snapshot(self) -> dict:
        with self.lock:
            if self._prune():
                self._write()
            return copy.deepcopy(self.data)

    def totals(self, day: str | None = None) -> dict:
        out: dict = {}
        for d, events in self.snapshot().items():
            if day and d != day:
                continue
            for event, pages in events.items():
                out[event] = out.get(event, 0) + sum(sum(v.values()) for v in pages.values())
        return out

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), prefix='.counts-')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as fh:
                json.dump(self.data, fh, sort_keys=True, separators=(',', ':'))
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)


def validate(payload: object, paths: set[str] | None = None, targets: set[tuple[str, str]] | None = None) -> tuple[dict | None, str]:
    """Filter extra fields; reject invalid event/path/target. Never echo attacker input."""
    if not isinstance(payload, dict):
        return None, 'body must be an object'
    if type(payload.get('v')) is not int or payload['v'] != 1:
        return None, 'unsupported version'
    event = payload.get('e')
    if not isinstance(event, str) or event not in EVENTS:
        return None, 'unknown event'
    page = payload.get('p', '/')
    if not isinstance(page, str) or not PATH_RE.fullmatch(page) or '//' in page or '..' in page:
        return None, 'bad path'
    if paths is not None and page not in paths:
        return None, 'unknown page'
    host, token = payload.get('h', ''), payload.get('t', '')
    if not isinstance(host, str) or not HOST_RE.fullmatch(host) or not isinstance(token, str) or not TOKEN_RE.fullmatch(token):
        return None, 'bad target'
    if event != 'outbound_click' and (host or token):
        return None, 'target only permitted on outbound clicks'
    if event == 'outbound_click':
        if (host, token) not in (targets if targets is not None else product_targets()):
            return None, 'unknown product target'
    return {'e': event, 'p': page, 'h': host, 't': token}, ''


class WriteCeiling:
    """A global process-wide ceiling, not a per-person identifier or bot detector."""
    def __init__(self, per_minute: int = 1200):
        self.per_minute = per_minute
        self.minute = -1
        self.count = 0
        self.lock = threading.Lock()

    def accept(self) -> bool:
        with self.lock:
            minute = int(time.monotonic() // 60)
            if minute != self.minute:
                self.minute, self.count = minute, 0
            self.count += 1
            return self.count <= self.per_minute


class PrivacyHTTPServer(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # BaseServer normally prints the client address in exception tracebacks.
        # Do not log request/identity data even on an unexpected failure.
        print("Collector request failed; no request data was logged.", file=sys.stderr)


def make_handler(store: Store, origin: str | None, read_token: str | None, paths: set[str] | None = None):
    allowed_paths = paths if paths is not None else public_paths()
    targets = product_targets()
    ceiling = WriteCeiling()

    class Handler(BaseHTTPRequestHandler):
        server_version = 'Z3Collector/2'
        sys_version = ''

        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def log_message(self, fmt, *args):
            return  # no request log; configure upstream hosting logs separately

        def _permitted_origin(self) -> str | None:
            supplied = self.headers.get('Origin', '')
            if origin is not None:
                return supplied if supplied == origin else None
            # Development preview only: the browser must match this server's host.
            try:
                candidate = urlsplit(supplied)
            except ValueError:
                return None
            if candidate.scheme in ('https', 'http') and candidate.netloc == self.headers.get('Host') and not candidate.path and not candidate.query and not candidate.fragment:
                return supplied
            return None

        def _send(self, code: int, body: bytes = b'', ctype: str = 'text/plain; charset=utf-8') -> None:
            self.send_response(code)
            permitted = self._permitted_origin()
            if permitted:
                self.send_header('Access-Control-Allow-Origin', permitted)
            self.send_header('Vary', 'Origin')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def do_OPTIONS(self):
            if self.path != '/collect':
                return self._send(404)
            return self._send(204 if self._permitted_origin() else 403)

        def do_POST(self):
            if self.path != '/collect':
                return self._send(404)
            if not self._permitted_origin():
                return self._send(403)
            if not ceiling.accept():
                return self._send(429)
            if self.headers.get('Transfer-Encoding'):
                return self._send(400)
            ctype = self.headers.get('Content-Type', '').split(';')[0].strip().lower()
            if ctype not in ('application/json', 'text/plain'):
                return self._send(415)
            try:
                length = int(self.headers.get('Content-Length', '0'))
            except ValueError:
                return self._send(400)
            if length <= 0:
                return self._send(400)
            if length > MAX_BODY:
                return self._send(413)
            try:
                payload = json.loads(self.rfile.read(length).decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError, TimeoutError):
                return self._send(400)
            record, reason = validate(payload, allowed_paths, targets)
            if record is None:
                return self._send(400, reason.encode('ascii'))
            day = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            try:
                store.add(day, record['e'], record['p'], record['h'], record['t'])
            except (OSError, ValueError):
                return self._send(503)
            return self._send(204)

        def do_GET(self):
            if self.path == '/healthz':
                return self._send(200, b'ok')
            if self.path == '/counts' and read_token:
                auth = self.headers.get('Authorization', '')
                if not hmac.compare_digest(auth.encode('utf-8'), ('Bearer ' + read_token).encode('utf-8')):
                    return self._send(401)
                body = json.dumps({'totals_by_event': store.totals(), 'daily_counts': store.snapshot(), 'retention_days': store.retention_days}).encode()
                return self._send(200, body, 'application/json')
            return self._send(404)

    return Handler


def self_test() -> int:
    failures = []
    def check(condition, label):
        print(('PASS ' if condition else 'FAIL ') + label)
        if not condition:
            failures.append(label)
    good = {'v': 1, 'e': 'page_view', 'p': '/Zone3/index.html'}
    check(validate(good)[0] is not None, 'valid page event accepted')
    for field, value in [('v', True), ('v', 2), ('e', 'conversion'), ('e', []), ('p', '/a//b'), ('p', '/a/../b'), ('p', '/?email=x'), ('p', '/x\n')]:
        check(validate({**good, field: value})[0] is None, f'invalid {field} rejected ({type(value).__name__})')
    click = {**good, 'e': 'outbound_click', 'h': 'link.amazon', 't': 'B04G1MEwY'}
    check(validate(click)[0] is not None, 'known outbound target accepted')
    check(validate({**click, 't': 'unknownUserID'})[0] is None, 'unapproved token rejected')
    check(validate({**click, 'h': 'example.org'})[0] is None, 'unapproved host rejected')
    check(validate({**good, 'h': 'link.amazon'})[0] is None, 'non-click target rejected')
    check(validate(good, {'/'})[0] is None, 'unknown public path rejected')
    extra, _ = validate({**good, 'ip': '192.0.2.1', 'referrer': 'private', 'user_id': 'test', 'd': '1999-01-01'})
    check(set(extra) == {'e', 'p', 'h', 't'}, 'extra fields never survive validation')
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp) / 'counts.json'
        store = Store(path)
        today = datetime.now(timezone.utc).date().isoformat()
        store.add(today, 'outbound_click', '/', 'link.amazon', 'B04G1MEwY')
        store.add(today, 'outbound_click', '/', 'link.amazon', 'B04G1MEwY')
        store.add(today, 'page_view', '/', '', '')
        check(store.totals(today) == {'outbound_click': 2, 'page_view': 1}, 'aggregate-only counts add correctly')
        store.data['2000-01-01'] = {'page_view': {'/': {'': 999}}}
        check('2000-01-01' not in store.snapshot(), 'retention automatically prunes old aggregates')
        stored = path.read_text()
        check(not re.search(r'ip|user.?agent|referr|cookie|visitor|user_id', stored, re.I), 'store has no identifier/raw-request fields')
        check(Store(path).totals() == store.totals(), 'atomic store reloads correctly')
    ceiling = WriteCeiling(per_minute=1)
    check(ceiling.accept() and not ceiling.accept(), 'global write ceiling enforced without client identifiers')
    print('SELF-TEST ' + ('FAIL' if failures else 'PASS') + ' · aggregate collector')
    return int(bool(failures))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--host', default='0.0.0.0')
    ap.add_argument('--port', type=int, default=8787)
    ap.add_argument('--store', type=pathlib.Path, default=pathlib.Path.home() / 'z3-analytics' / 'counts.json')
    ap.add_argument('--origin', default=DEFAULT_ORIGIN)
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not re.fullmatch(r'https://[a-zA-Z0-9.\-]+(?::\d+)?', args.origin):
        ap.error('--origin must be one explicit HTTPS origin; no wildcard')
    server = PrivacyHTTPServer((args.host, args.port), make_handler(Store(args.store), args.origin, os.environ.get('Z3_ANALYTICS_READ_TOKEN') or None))
    print(f'Aggregate collector listening on {args.host}:{args.port}; no request logs; upstream logs require separate configuration.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
