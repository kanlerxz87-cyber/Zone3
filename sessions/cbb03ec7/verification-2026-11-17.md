# Verification record — session cbb03ec7 (2026-11-17)

All fetches performed 2026-11-17 through the platform page-fetch tool. Every observation below
is what the page returned; nothing is inferred. Prices and star ratings visible on the served
listing pages were deliberately **not** recorded (Program Policies 2(b)/6(t) display rules —
`FLG-036`).

| # | URL fetched | Result observed | Source ID |
|---|---|---|---|
| V1 | `https://link.amazon/B0c8moW59` | Redirected to `https://www.amazon.com/dp/B0DHZTCNR5?lv=shuf&btn_type=ss&gaOptInStatus=true&…&btn_ref=srctok-633f9dc54185b50f&channelId=500&plpRedirect=mhFallback`. Served page title: "Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill BBQ Camping, Black : Home & Kitchen". Breadcrumb: Home & Kitchen (1055398) › Kitchen & Dining (284507) › Kitchen Utensils & Gadgets (289754) › Thermometers & Timers (289807) › Meat (289810). | S70 |
| V2 | `https://www.amazon.com/dp/B0DHZTCNR5` | Same title and breadcrumb as V1. Confirms the destination at its bare URL. | S71 |
| V3 | `https://www.amazon.com/dp/B0c8moW59` | Amazon "Page Not Found" error page (title field: "Page Not Found"). Token is 9 characters. | S72 |
| V4 | `https://link.amazon/B0f3GKalj` | Redirected to `https://www.amazon.com/dp/B0DZFD6R9Z?lv=shuf&sbo=…&btn_type=ss&gaOptInStatus=true&language=en_US&btn_ref=srctok-101536bcd8e0be02&channelId=500&plpRedirect=mhFallback&th=1`. Served page title: "Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3: Home & Kitchen". Same breadcrumb as V1. | S73 |
| V5 | `https://www.amazon.com/dp/B0DZFD6R9Z` | Same title and breadcrumb as V4. Confirms the destination at its bare URL. | S74 |
| V6 | `https://www.amazon.com/dp/B0f3GKalj` | Amazon "Page Not Found" error page. Token is 9 characters. | S75 |

## Checks derived from the observations (no inference)

- ASIN rule: an ASIN is a 10-character alphanumeric identifier — Creators API `GetItems`,
  `ItemIdType` (S06). Both new tokens are 9 characters → not ASINs.
- Destination identity: observed, not confirmed as the submitted product — same treatment as
  products 1–3 (`FLG-002`, `CBB-F-01`).
- Category: both new destinations sit under Thermometers & Timers › Meat, not Air Fryers
  (`CBB-F-03`).
- Tracking ID: no fetch can confirm account assignment (Associates console is login-gated);
  recorded as unverified (`CBB-F-02`).

## Cross-session corroboration

Session `974e366d` (PR #135, merged before this session's data work) independently resolved the
same two links to the same two destinations on 2026-11-17 (`data/shop/sources.json`,
`shop/products/`). Both records are kept; they are separate registers and are not merged.

## Gates re-run on the final tree (2026-11-17)

| Gate | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 30 pages, 5 products, 68 sources, 112 flags |
| `python3 tools/verify_site.py` | VERIFY PASS — 134 pages, 2,078 rows, 1,797 with official source, 72 repo anchors |
| `python3 tools/link_report.py --strict` | exit 0 |
| `python3 tools/i2_gate.py` | PASS — 18 pages, 164 rows, 0 flagged |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings, 22 inherited advisory |
| `python3 tools/build_cba81fa5_site.py --check` | already current |
| `python3 tools/build_shop.py --check` | OK — 11 pages |
| `python3 scripts/build_sitemap.py --check` | exit 0 — 97 pages, 0 extras |
| `python3 scripts/check_all_links.py` | 0 errors on 118 published HTML pages (historical `sessions/` and `archive/` snapshots excluded; their anchors may refer to retired IDs) |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 134 pages, 0 repr-shaped |
| full generator chain ×2 | idempotent (tree hash identical) |
| conflict-marker / secrets sweep | 0 / 0 |
