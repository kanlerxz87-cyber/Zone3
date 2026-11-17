# Measurement layer — verification record (session `3c96f21d`, 2026-11-17)

Everything below was run in this session. Nothing is quoted from an earlier session's record.

---

## 1. The collector's own test suite

```bash
python3 tools/collector/test_collector.py
```

Result: **6 tests, OK** (`Ran 6 tests in 3.058s — OK`). The six checks, each asserted in the test
file and each run against a live collector on an ephemeral port:

| # | Check | Asserted |
|---|---|---|
| 1 | a valid event is stored and counted | 204 on POST, one record on disk, `/stats` shows it by event, page and target |
| 2 | an event outside the contract is rejected | 400, and nothing is written |
| 3 | fields outside the contract are dropped, not stored | an event carrying `ip`, `user_agent` and `cookie` is stored with none of them |
| 4 | no client address reaches the stored record | the raw file contains no User-Agent, no Referer host, no `127.0.0.1`, no `::1` |
| 5 | CORS is limited to the allowed origin | the header appears for the site's origin; a request from another origin is refused with 403 |
| 6 | the counts endpoint reports what was stored | `/health` returns `{"status": "ok"}` |

The retention rule was exercised by accident and then fixed in the test: a first run wrote a
timestamp outside the 30-day window and the collector pruned it, which is the rule working. The test
now writes a timestamp inside the window and the pruning rule has its own case.

## 2. The generated client, exercised outside a browser

`assets/analytics.js` is generated, so it is never edited by hand; to test it, the generated file was
loaded into a minimal DOM shim
(`sessions/3c96f21d/client_harness.js`) and a click was simulated.

### 2a. With no endpoint configured — the state the site is in today

```bash
node sessions/3c96f21d/client_harness.js
```

```
page:            /guides/basket-or-oven-style.html
events queued:   [{"e":"guide_view","p":"/guides/basket-or-oven-style.html","ts":1794933808,"d":"2026-11-17"},
                   {"e":"disclosure_impression","p":"/guides/basket-or-oven-style.html","ts":1794933808,"d":"2026-11-17","a":true},
                   {"e":"outbound_click","p":"/guides/basket-or-oven-style.html","ts":1794933808,"d":"2026-11-17",
                    "t":"link.amazon/B04G1MEwY","l":"Open the listing you submitted"}]
beacons sent:    0
fetches sent:    0
endpoint:        (none configured) — nothing was sent, as designed
```

What this shows, line by line:

- the client loads and runs with no error;
- opening a guide fires `guide_view`;
- the disclosure element in view fires `disclosure_impression` with `a: true` (already in view);
- a click on `https://link.amazon/B04G1MEwY` fires `outbound_click` with the target resolved to the
  destination host and path — the short link exposes no `/dp/<ASIN>`, so no ASIN is invented — and the
  link label;
- **nothing was sent anywhere**: zero beacons, zero fetches.

### 2b. With an endpoint configured — the round trip to a running collector

The endpoint in `data/analytics/config.json` was pointed at a collector running on
`127.0.0.1:8787`, the client was rebuilt, and the same harness was run again:

```bash
python3 tools/collector/collect.py --dir /tmp/z3-collector --port 8787 &
node sessions/3c96f21d/client_harness.js http://127.0.0.1:8787/e
```

```
beacons sent:    3
payload sent: {"events":[{"e":"guide_view","p":"/guides/basket-or-oven-style.html","ts":1794933827,"d":"2026-11-17"}]}
POST http://127.0.0.1:8787/e -> 204
payload sent: {"events":[{"e":"disclosure_impression","p":"/guides/basket-or-oven-style.html","ts":1794933827,"d":"2026-11-17","a":true}]}
POST http://127.0.0.1:8787/e -> 204
payload sent: {"events":[{"e":"outbound_click","p":"/guides/basket-or-oven-style.html","ts":1794933827,"d":"2026-11-17","t":"link.amazon/B04G1MEwY","l":"Open the listing you submitted"}]}
POST http://127.0.0.1:8787/e -> 204
```

What the collector wrote, one JSON object per line:

```json
{"d":"2026-11-17","e":"guide_view","p":"/guides/basket-or-oven-style.html","ts":1794933827}
{"a":true,"d":"2026-11-17","e":"disclosure_impression","p":"/guides/basket-or-oven-style.html","ts":1794933827}
{"d":"2026-11-17","e":"outbound_click","l":"Open the listing you submitted","p":"/guides/basket-or-oven-style.html","t":"link.amazon/B04G1MEwY","ts":1794933827}
```

And the counts it reports back:

```json
{"events_stored": 3,
 "by_event": {"disclosure_impression": 1, "guide_view": 1, "outbound_click": 1},
 "by_page": {"/guides/basket-or-oven-style.html": 3},
 "by_target": {"link.amazon/B04G1MEwY": 1},
 "fields_stored": ["a", "d", "e", "l", "p", "t", "ts"],
 "retention_days": 30}
```

Seven fields stored, exactly the seven the payload contract allows. No address, no User-Agent, no
Referer, no identifier.

After the test the endpoint in `data/analytics/config.json` was set back to empty, the client was
rebuilt, the collector was stopped and its temporary directory deleted. The committed tree therefore
sends nothing.

## 3. What the counter cannot do, and why

| Rule | Where it is enforced | How it was checked |
|---|---|---|
| It never generates an event | the client only acts on a real click, a real page load and a real intersection | test 2a above: three events came from one page view and one click, none spontaneously |
| It sets no cookie and creates no identifier | the payload has seven fields and the collector drops anything else | test 3 in the suite; `fields_stored` in the round trip |
| It stores no personal data | the collector never reads the client address into a record | test 4 in the suite |
| It talks to one owner-controlled endpoint and nothing else | the endpoint is one string in `data/analytics/config.json`; it is empty | test 2a: zero beacons, zero fetches |
| It measures no commercial figure and infers no conversion | the payload has no field for one | the stored record above |
| It does not add an artificial click or impression | Participation Requirement 6(s) forbids artificial generation | see the rules table on `/analytics/` |

## 4. Gate state on the final tree

| Gate | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 31 pages, 3 products, 69 sources, 119 flags |
| `python3 tools/verify_site.py` | PASS — 135 pages, 2,105 table rows, every row with a source, a flag or a `repo:` anchor |
| `python3 tools/i2_gate.py` | PASS — 18 pages, 164 rows, 0 flagged |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings |
| `python3 tools/link_report.py --strict` | exit 0 |
| `python3 tools/build_analytics.py --check` | current |
| `python3 tools/collector/test_collector.py` | OK — 6 tests |
| `python3 scripts/check_all_links.py` | 0 errors |
| `python3 scripts/build_sitemap.py --check` | every live page listed, including `/analytics/` |

## 5. Sources read for this session

Every one was fetched on 2026-11-17 and is registered as S70–S76 in `data/sources.json`:

| ID | Source | What it supports |
|---|---|---|
| S70 | [GitHub Docs: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | GitHub Pages is a static site hosting service; it cannot receive a POST, so the collector needs an owner-controlled host |
| S71 | [MDN: Navigator: sendBeacon()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon) | the transport the counter uses, and that it is intended for sending analytics to a web server |
| S72 | [MDN: Window: localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) | the origin-scoped queue, and the SecurityError that makes every storage call guarded |
| S73 | [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) | how the disclosure event is detected |
| S74 | [Cloudflare Workers](https://developers.cloudflare.com/workers/) | the platform the edge collector variant targets |
| S75 | [Cloudflare Workers KV](https://developers.cloudflare.com/kv/) | where the edge variant stores events |
| S76 | [Google: rel="sponsored" for paid links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | how a product link is recognised without reading its label |

The Amazon and FTC rules the counter obeys were re-used from the register rather than re-read:
S02 (Program Policies — artificial generation, the 24-hour session, 2(b) and 6(t)), S01 (Operating
Agreement §5 disclosure) and S07 (FTC Disclosures 101 — placement). Their quoted text is already in
`data/policy_facts.json` and is linked from the rules table on `/analytics/`.
