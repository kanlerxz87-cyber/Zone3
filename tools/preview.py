#!/usr/bin/env python3
"""Development-only site preview and same-origin aggregate collector.

The production measure-config.js file is NEVER modified. This server overrides that one
response to point to /collect so the working preview can be tested end to end. Counts
are local test traffic, stored under ignored .preview/, not added to campaign ledgers.
"""
from __future__ import annotations

import argparse
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit

from analytics_endpoint import Store, PrivacyHTTPServer, make_handler

ROOT = Path(__file__).resolve().parents[1]


def handler(store_path: Path):
    collector = make_handler(Store(store_path), None, os.environ.get('Z3_ANALYTICS_READ_TOKEN') or None)

    class Preview(collector, SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def do_GET(self):
            path = unquote(urlsplit(self.path).path)
            if path in ('/collect', '/healthz', '/counts'):
                return collector.do_GET(self)
            if any(part.startswith('.') for part in Path(path).parts if part not in ('/', '')):
                return self._send(404)
            if path in ('/assets/measure-config.js', '/Zone3/assets/measure-config.js'):
                body = ('/* Development preview only. Production remains off. */\nwindow.Z3_MEASURE = '
                        + json.dumps({'enabled': True, 'endpoint': '/collect'}) + ';\n').encode()
                return self._send(200, body, 'application/javascript')
            # Support both root preview and the actual project-site base path.
            if path.startswith('/Zone3/'):
                self.path = self.path[len('/Zone3'):]
            return SimpleHTTPRequestHandler.do_GET(self)

        def do_HEAD(self):
            path = unquote(urlsplit(self.path).path)
            if any(part.startswith('.') for part in Path(path).parts if part not in ('/', '')):
                return self._send(404)
            if path.startswith('/Zone3/'):
                self.path = self.path[len('/Zone3'):]
            return SimpleHTTPRequestHandler.do_HEAD(self)

        def list_directory(self, path):
            return self._send(404)  # no directory listing or local test-store exposure

    return Preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=3000)
    parser.add_argument('--host', default='0.0.0.0')
    args = parser.parse_args()
    server = PrivacyHTTPServer((args.host, args.port), handler(ROOT / '.preview/aggregate-counts.json'))
    print(f'Zone3 Kitchen preview on {args.host}:{args.port}. Same-origin analytics is test-only; production config remains off.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
