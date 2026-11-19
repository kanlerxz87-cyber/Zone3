# Verification record — session 3301d334

**Date:** 2026-11-19 (UTC)  
**Scope:** Root publication landing page, its generator and publication CSS, plus the shared generated footer directory (all published pages).  
**Source policy:** No new product fact was inferred. Product names, submitted URLs, observed destination URLs/ASINs and observation date are rendered from `sessions/aebf0747/intent-record.json`; related product/source records are in `data/products.json` and `data/sources.json`.

## Page-level checks

| Page content | Register/source of record | How used |
|---|---|---|
| Submitted URLs and dated observed ASINs | `data/products.json`; source links S11–S16, S23, S70–S73; re-fetch records S76–S78 | Five cards show the submitted URL as a sponsored CTA, the observed destination ASIN/date separately, and an official Amazon listing URL as the observation source. Intended ASIN remains unconfirmed. |
| Four guide titles and summaries | `sessions/aebf0747/build_pass.py` `GUIDES`; generated guide pages under `guides/` | Titles remain editorial working titles. Page says no query data/popularity claims are available. |
| Associates disclosure sentence | Amazon Operating Agreement, source S01: https://affiliate-program.amazon.com/help/operating/agreement | Kept under the masthead and repeated in the footer by `publish_pass.py`. |
| Sponsored-link marker | Google Search Central, source S90: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Every outbound product/linking card anchor carries `rel="sponsored"`; repository-wide gate passed. |
| Open questions / suggestions | Existing `direction/questions.html`, `suggestions.html`, and `intent-record/index.html` | Linked from the landing page; no owner decision was fabricated or silently applied. |
| Dashboard destinations | `sessions/aebf0747/publish_pass.py` `FOOTER_GROUPS` plus `build_pass.py` `NAV_GROUPS` | One Explore menu group collects reader/research, product/evidence, and dashboard/decision links; the shared footer has one 24-destination Dashboards group. The publication pass emitted the updated footer on all 111 generated pages; no target was missing. |

## Validation commands and results

- `python3 scripts/check_site.py` — PASS: 42 pages, 5 products, 83 sources, 148 flags.
- `python3 tools/verify_site.py` — PASS: 152 pages, 2,517 table rows; 532 repository-wide advisory items reported as non-blocking.
- `python3 scripts/check_all_links.py` — PASS: 198 pages, 263 distinct external URLs, 0 broken-link errors.
- `python3 scripts/mark_sponsored.py --check` — PASS.
- `python3 sessions/aebf0747/publish_pass.py --check` — PASS: 111 pages, 0 changes.
- `python3 tools/build_feed.py --check` — PASS: 22 entries current.
- `python3 scripts/build_sitemap.py --check` — PASS: 106 pages covered.
- `python3 tools/measure_pass.py --check` — PASS: 111 pages, 0 changes.
- `node sessions/38650305/test_measure.js` — PASS: all measurement client self-tests.
- Generator determinism — PASS: fresh `front_page()` output followed by `publish_pass.apply()` was byte-identical to committed `index.html`.
- Manual markup inspection — one `<h1>`, disclosure immediately below the masthead, one grouped Explore menu, no product photographs or unsupported pricing/ratings, and no empty cards.

## Irregularities intentionally left for review

- **FLG-003:** exact compliance status of the supplied `link.amazon` links is unresolved. This session does not label them invalid and does not claim they have been tested in the enrolled Associates workflow. Product identity is clearly labeled unconfirmed on every card.
- Intended ASIN/listing URL confirmation, account status/API eligibility, final brand/category scope, analytics-host choice and Search Console ownership require account-holder information not present in the repository.
- `assets/measure-config.js` remains disabled because no endpoint is hosted/configured. GitHub Pages is static; no conversion or traffic measurement is claimed.
- No live remote fetch of the cited official pages was performed during this pass. The relevant listing and policy source links, statuses and dated fetch records remain in the source register for manual review.
