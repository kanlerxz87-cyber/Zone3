#!/usr/bin/env python3
"""Local-only HTTP/privacy regressions. No Amazon requests and no campaign data."""
from __future__ import annotations

import http.client
import importlib.util
import json
import pathlib
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import analytics_endpoint as collector
import build_measurement

ORIGIN = 'https://kanlerxz87-cyber.github.io'
GOOD = {'v': 1, 'e': 'page_view', 'p': '/Zone3/'}


class CollectorHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = collector.Store(pathlib.Path(self.tmp.name) / 'aggregates.json')
        self.server = collector.PrivacyHTTPServer(('127.0.0.1', 0), collector.make_handler(self.store, ORIGIN, 'unit-test-only', paths={'/', '/Zone3/'}))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, method='POST', path='/collect', payload=None, headers=None):
        supplied = {'Origin': ORIGIN, 'Content-Type': 'text/plain'}
        if headers:
            supplied.update(headers)
        body = json.dumps(payload if payload is not None else GOOD).encode() if method == 'POST' else None
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        connection.request(method, path, body=body, headers=supplied)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_delivery_and_private_read(self):
        code, headers, _ = self.request()
        self.assertEqual(code, 204)
        self.assertNotIn('Set-Cookie', headers)
        self.assertEqual(headers['Access-Control-Allow-Origin'], ORIGIN)
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertEqual(self.request('GET', '/counts')[0], 401)
        code, _, body = self.request('GET', '/counts', headers={'Authorization': 'Bearer unit-test-only'})
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)['totals_by_event'], {'page_view': 1})
        self.assertEqual(self.request('GET', '/healthz')[0], 200)

    def test_unknown_and_missing_origins_do_not_count(self):
        for origin in ('https://other.example', '', 'null', 'http://['):
            with self.subTest(origin=origin):
                self.assertEqual(self.request(headers={'Origin': origin})[0], 403)
        self.assertEqual(self.store.totals(), {})

    def test_options_and_routes(self):
        self.assertEqual(self.request('OPTIONS')[0], 204)
        self.assertEqual(self.request('OPTIONS', headers={'Origin': 'https://bad.example'})[0], 403)
        self.assertEqual(self.request(path='/collect?secret=1')[0], 404)
        self.assertEqual(self.request('GET', '/stats')[0], 404)

    def test_oversized_wrong_type_and_unknown_page(self):
        self.assertEqual(self.request(payload={**GOOD, 'extra': 'x' * 2100})[0], 413)
        self.assertEqual(self.request(headers={'Content-Type': 'image/png'})[0], 415)
        self.assertEqual(self.request(payload={**GOOD, 'p': '/private/person123'})[0], 400)
        self.assertEqual(self.request(payload={**GOOD, 'v': True})[0], 400)
        self.assertEqual(self.store.totals(), {})

    def test_five_events_and_known_target_only(self):
        for event in collector.EVENTS:
            payload = {**GOOD, 'e': event}
            if event == 'outbound_click':
                payload.update(h='link.amazon', t='B04G1MEwY')
            self.assertEqual(self.request(payload=payload)[0], 204)
        self.assertEqual(self.store.totals(), {e: 1 for e in collector.EVENTS})
        bad = {**GOOD, 'e': 'outbound_click', 'h': 'link.amazon', 't': 'privatePersonId'}
        self.assertEqual(self.request(payload=bad)[0], 400)
        self.assertEqual(self.request(payload={**GOOD, 'e': 'purchase'})[0], 400)

    def test_extra_identifiers_and_client_dates_never_persist(self):
        payload = {**GOOD, 'ip': '198.51.100.1', 'email': 'not-a-person@example.invalid', 'visitor_id': 'never-retain-this', 'date': '1900-01-01'}
        self.assertEqual(self.request(payload=payload)[0], 204)
        stored = self.store.path.read_text()
        for forbidden in ('198.51.100.1', 'not-a-person', 'visitor_id', 'never-retain-this', '1900-01-01', 'email'):
            self.assertNotIn(forbidden, stored)
        self.assertIn(datetime.now(timezone.utc).date().isoformat(), stored)

    def test_read_endpoint_is_disabled_without_server_token(self):
        separate = collector.PrivacyHTTPServer(('127.0.0.1', 0), collector.make_handler(self.store, ORIGIN, None, paths={'/'}))
        thread = threading.Thread(target=separate.serve_forever, daemon=True)
        thread.start()
        try:
            connection = http.client.HTTPConnection('127.0.0.1', separate.server_port)
            connection.request('GET', '/counts')
            response = connection.getresponse()
            self.assertEqual(response.status, 404)
            response.read()
            connection.close()
        finally:
            separate.shutdown()
            separate.server_close()
            thread.join()

    def test_concurrent_aggregate_updates_do_not_drop_counts(self):
        today = datetime.now(timezone.utc).date().isoformat()
        threads = [threading.Thread(target=self.store.add, args=(today, 'page_view', '/', '', '')) for _ in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(self.store.totals(), {'page_view': 20})
        self.assertEqual(collector.Store(self.store.path).totals(), {'page_view': 20})

    def test_retention_boundary(self):
        today = datetime.now(timezone.utc).date()
        self.store.data[(today - timedelta(days=89)).isoformat()] = {'page_view': {'/': {'': 2}}}
        self.store.data[(today - timedelta(days=90)).isoformat()] = {'page_view': {'/': {'': 9}}}
        self.assertEqual(self.store.totals(), {'page_view': 2})

    def test_production_activation_requires_evidence(self):
        data = json.loads((ROOT / 'data/shop/measurement.json').read_text())
        for endpoint in ('http://example.invalid/collect', 'https://u:p@example.invalid/collect', 'https://example.invalid/collect?token=x'):
            with self.subTest(endpoint=endpoint), self.assertRaises(ValueError):
                build_measurement.config_js({**data, 'enabled': True, 'endpoint_url': endpoint})
        with self.assertRaises(ValueError):
            build_measurement.config_js({**data, 'enabled': True, 'endpoint_url': 'https://example.invalid/collect'})
        self.assertIn('"enabled": false', build_measurement.config_js(data))


if __name__ == '__main__':
    unittest.main(verbosity=2)
