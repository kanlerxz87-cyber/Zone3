# Verification record — session 3301d334

**Date:** 2026-11-19 (UTC)  
**Scope:** Integrate the merged C3 reader front page; order the product listing desk before buyer-question guides; build one grouped Explore menu; expand the shared footer directory on all 111 published pages; document build order.
**Source policy:** No product fact was newly inferred. Product names, submitted URLs, observed targets/ASINs and observation dates come from the existing intent/product registers and linked dated observations.

## Page-level checks

| Page content | Register/source of record | How used |
|---|---|---|
| Submitted URLs and observed ASINs | `data/products.json`; source-register records S11–S16, S23, S70–S73 and re-fetch records S76–S78 | Every card keeps the submitted link separate from the observed target. The intended ASIN is not presented as confirmed; official Amazon listing links are the source links. |
| Four guide questions | `sessions/c3be74f2/build_front_page.py` and its source-linked guide pages | Questions remain editorial working titles, not claims about search demand or popularity. |
| Disclosure | Amazon Operating Agreement, S01: https://affiliate-program.amazon.com/help/operating/agreement | Disclosure remains directly below the masthead and in the shared footer. |
| Sponsored links | Google Search Central, S90: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | Product links retain `rel="sponsored"`; repository-wide sponsored-link gate passes. |
| Dashboard navigation | `sessions/aebf0747/build_pass.py` `NAV_GROUPS` and `sessions/aebf0747/publish_pass.py` `FOOTER_GROUPS` | Root has one Explore menu; footer has a single 24-destination Dashboards group, repeated on the full published tree. |
| Decision handoff | Existing `intent-record/index.html`, `direction/questions.html`, `suggestions.html`, `decision-queue.html`, `sources/index.html` and `flagged.html` | Routes remain linked. The root table and C3-F-01 finding were preserved from merged main. |

## Validation commands and results

- `python3 scripts/check_site.py` — PASS: 42 pages, 5 products, 83 sources, 149 flags.
- `python3 tools/verify_site.py` — PASS: 152 pages, 2,522 table rows; 532 inherited repository-wide advisory items are non-blocking.
- `python3 scripts/check_all_links.py` — PASS: 198 HTML pages, 264 distinct external URLs, 0 errors.
- `python3 scripts/mark_sponsored.py --check` — PASS.
- `python3 sessions/aebf0747/publish_pass.py --check` — PASS: 111 pages, 0 changes, no missing footer targets.
- `python3 sessions/c3be74f2/build_front_page.py --check` — PASS: C3 root content current after generation.
- `python3 tools/build_feed.py --check` — PASS: 22 entries current.
- `python3 scripts/build_sitemap.py --check` — PASS: 106 pages covered.
- `python3 tools/measure_pass.py --check` — PASS: 111 pages, 0 changes.
- `node sessions/38650305/test_measure.js` — PASS: measurement client privacy/off-by-default self-tests.
- Masthead generator — root header was rendered by the shared `build_pass.masthead()` function; all relative destinations resolve.
- Footer definition — `publish_pass.FOOTER_GROUPS` contains one Dashboards group with 24 live targets; generator reports no missing footer destinations.
- CSS/Python syntax — publication stylesheet updated; `python3 -m py_compile sessions/c3be74f2/build_front_page.py sessions/aebf0747/build_pass.py sessions/aebf0747/publish_pass.py` passed.

`README.md` now places the C3 marker-bounded front-page generator after the older publication pass, so a future build restores the reader page after older generators run.

## Irregularities intentionally left for review

- **FLG-003:** exact compliance status of the supplied `link.amazon` links remains unresolved. No claim is made that these links are invalid or that an enrolled-Associates Special Link test was completed.
- Intended ASIN/listing URL confirmation, Associates account status/API eligibility, final brand/category scope, analytics endpoint hosting and Search Console ownership require account-holder input absent from this checkout.
- `assets/measure-config.js` remains disabled because no collector URL/host exists. GitHub Pages is static; no click/conversion or revenue measurement is claimed.
- No live re-fetch of the cited official pages occurred during this pass. Existing dated source records are cited for manual review; this is not a current-availability check.
- Rebase conflict: main advanced to `b0fe35b` while this branch was in progress. The complete C3 Parts and merged work were preserved; the overlapping old front-page rewrite was superseded. This session kept the C3 page and added navigation/footer/build-order changes around it. Resolution is recorded in Part 3301 of `COORDINATION.md`.
