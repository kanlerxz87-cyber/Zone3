#!/usr/bin/env python3
"""Round-trip test for the Zone3 measurement collector.

    python3 tools/collector/test_collector.py

What it proves, line by line:
    1. a valid event is accepted, written to disk and counted;
    2. an event outside the contract is rejected and nothing is written;
    3. fields the contract does not allow are dropped, not stored;
    4. no client address, User-Agent or Referer ends up in the stored record;
    5. the response carries no CORS header for an origin that is not allowed, and does for one
       that is;
    6. the counts endpoint reports what was stored.

Standard library only. It starts the collector on an ephemeral port in a temporary directory.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from collect import Collector, Handler  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402

# A timestamp inside the collector's retention window, so the pruning rule (which is itself
# under test) does not remove the events this test writes.
NOW = int(time.time())
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


class CollectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.collector = Collector(pathlib.Path(self.tmp.name), "events.jsonl", 30)
        handler = type("BoundHandler", (Handler,), {
            "collector": self.collector,
            "allowed_origins": ["https://kanlerxz87-cyber.github.io"],
        })
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self.server.server_address[1]
        self.thread = __import__("threading").Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def post(self, payload: dict, headers: dict | None = None):
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/e",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", **(headers or {})},
            method="POST",
        )
        return urllib.request.urlopen(request, timeout=10)

    def get(self, path: str, headers: dict | None = None):
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}", headers=headers or {}, method="GET")
        return urllib.request.urlopen(request, timeout=10)

    def test_valid_event_is_stored_and_counted(self):
        response = self.post({"events": [{
            "e": "outbound_click",
            "p": "/guides/basket-or-oven-style.html",
            "t": "B0CDY277D3",
            "l": "Open the listing you submitted",
            "ts": NOW,
            "d": TODAY,
        }]})
        self.assertEqual(response.status, 204)
        stored = self.collector.events()
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["t"], "B0CDY277D3")
        stats = json.loads(self.get("/stats").read().decode("utf-8"))
        self.assertEqual(stats["events_stored"], 1)
        self.assertEqual(stats["by_event"]["outbound_click"], 1)
        self.assertEqual(stats["by_target"]["B0CDY277D3"], 1)

    def test_event_outside_the_contract_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.post({"events": [{"e": "not_an_event", "p": "/", "ts": NOW}]})
        self.assertEqual(caught.exception.code, 400)
        self.assertEqual(self.collector.events(), [])

    def test_unknown_fields_are_dropped_not_stored(self):
        self.post({"events": [{
            "e": "guide_view",
            "p": "/guides/index.html",
            "ts": NOW,
            "ip": "203.0.113.9",
            "user_agent": "some browser",
            "cookie": "session=abc",
        }]})
        stored = self.collector.events()
        self.assertEqual(len(stored), 1)
        for banned in ("ip", "user_agent", "cookie"):
            self.assertNotIn(banned, stored[0])

    def test_no_client_address_is_stored(self):
        self.post({"events": [{"e": "guide_view", "p": "/guides/index.html", "ts": NOW}]},
                  headers={"User-Agent": "probe-agent/1.0", "Referer": "https://example.invalid/x"})
        raw = (pathlib.Path(self.tmp.name) / "events.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("probe-agent", raw)
        self.assertNotIn("example.invalid", raw)
        self.assertNotIn("127.0.0.1", raw)
        self.assertNotIn("::1", raw)

    def test_cors_is_limited_to_the_allowed_origin(self):
        allowed = self.post({"events": [{"e": "cta_click", "p": "/", "t": "/guides/", "ts": NOW}]},
                             headers={"Origin": "https://kanlerxz87-cyber.github.io"})
        self.assertEqual(allowed.headers.get("Access-Control-Allow-Origin"),
                         "https://kanlerxz87-cyber.github.io")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.post({"events": [{"e": "cta_click", "p": "/", "t": "/guides/", "ts": NOW}]},
                      headers={"Origin": "https://not-allowed.invalid"})
        self.assertEqual(caught.exception.code, 403)
        self.assertIsNone(caught.exception.headers.get("Access-Control-Allow-Origin"))

    def test_health_reports_liveness(self):
        payload = json.loads(self.get("/health").read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")


if __name__ == "__main__":
    unittest.main(verbosity=2)
