# Verification record — session 38650305 (2026-11-17)

Branch `arena/38650305-zone3`, base `d192053` (`main`). Everything here was run in this checkout, and again in a fresh clone of the pushed branch.

## 1. Official sources read (fetched 2026-11-17)

| # | Source | What it supports | Where used |
|---|---|---|---|
| 1 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (updated April 14, 2026), Participation Requirements 2(a) and 2(b) | 2(a): Special Links must use the Associates ID assigned to you. 2(b): you must include your Associates ID or tag in the URL of each link to an Amazon Site; "Under no circumstances may you associate any sub-tag, other ID or reporting provided in connection with the Associates Program with a specific end user of your Site (e.g., you may not dynamically assign sub-tags to users as they arrive on your Site for purposes of monitoring such users' behavior)." 2(b) also limits showing prices and availability to the Amazon-served link or the Creators API / PA API. | Measurement design (no visitor ID); M38-F-01, M38-F-02, M38-F-04 |
| 2 | [GitHub Docs: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | "GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository". "When a GitHub Pages site is visited, the visitor's IP address is logged and stored for security purposes". | Collector is not hosted here (M38-F-04, M38-F-15) |
| 3 | [Google Search Console](https://search.google.com/search-console/about) | Sign-in via a Google account is required ("Start now" leads to a Google ServiceLogin). | Search Console blocked (M38-F-03) |
| 4 | [Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Section 5 disclosure sentence (already in use). | Disclosure unchanged (verified by gate V1) |

Not re-read in this session: the Operating Agreement beyond Section 5, the Creators API documentation, and the Zone4 decision log's individual rows. The brief's status labels are quoted, not verified (M38-F-16).

## 2. Repository measurements (2026-11-17)

Script: `sessions/38650305/measure_pages.py`; output: `sessions/38650305/measure_pages.out.txt`.

- 104 published HTML pages (excluding `archive/`, `docs/`, `sessions/`).
- Title present: 104/104. Meta description present: 104/104 (S-04 measured as met). Six pages carry the publish pass's generic description (M38-F-05).
- Links to amazon.* or link.amazon*: 1,447. Without `rel="sponsored"`: 0 (S-05 measured as met).
- og:image: 11/104. JSON-LD: 11/104 (S-09 partly).
- Images: `assets/img/hero-kitchen.jpg`, `capacity.jpg`, `counter.jpg`. Hero image is a generated-style kitchen illustration; capacity caption says "Our own illustration" (S-18 conflict, M38-F-10).
- "which one is for you": 0 pages (S-19 not found, M38-F-11). "per centimetre" / "per cm": 0 pages (S-23 not found, M38-F-11).
- Articles (5 files incl. index) link to a buying page and a category page; the 4 question guides in `guides/` do not (S-24 partly, M38-F-12).
- `DESIGN_PROMPT.md`: not present in this checkout (S-14 not found, M38-F-09).

## 3. Build and gate results

| Check | Result |
|---|---|
| `tools/verify_site.py` | PASS (advisory provenance notes on new register pages; non-blocking, see §5) |
| `scripts/check_site.py` | OK, 30 pages, 3 products, 62 sources, 113 flags |
| `tools/i2_gate.py` | PASS |
| `tools/cba81fa5_lint.py` | PASS, 0 new, 22 inherited |
| `tools/build_shop.py --check` | PASS (after allowlist fix, §4) |
| `tools/build_feed.py --check` | current, 9 entries |
| `scripts/build_sitemap.py --check` | 99 pages, 0 extra |
| `scripts/check_all_links.py` | 0 errors (182 pages, 219 URLs) |
| `tools/link_report.py --strict` | 0 |
| `sessions/aebf0747/publish_pass.py --check` | 0 changed |
| `tools/measure_pass.py --check` | 0 changed |
| `tools/build_measurement.py --check` | current |
| `tools/build_brief_status.py --check` | current, 23 rows |
| `tools/build_cba81fa5_site.py --check` | current |
| `tools/analytics_endpoint.py --self-test` | PASS (10 checks) |
| `sessions/38650305/test_measure.js` (Node, stubbed browser globals) | PASS (16 checks) |
| `scripts/cba81fa5_test_no_repr_output.py` | PASS, 136 pages |

Live HTTP checks of the collector (local, temporary store): `/healthz` 200; valid `POST /collect` 204; unknown event 400; `/counts` 404 when no read token is set. The stored file held one aggregate row, with no IP address (grep for the test IP: 0 matches).

Clean-checkout run: see §6.

## 4. Changes to shared tools (logged)

- `tools/build_shop.py`: `search.google.com` added to `OFFICIAL_HOSTS`, so the Search Console sign-in page can be cited. The gate had rejected it.
- `sessions/aebf0747/publish_pass.py`: two footer links added (measurement, brief status).
- Chain order (now required): `tools/build_shop.py` → `sessions/aebf0747/publish_pass.py` → `tools/measure_pass.py` → `scripts/build_sitemap.py`. The new generators (`tools/build_measurement.py`, `tools/build_brief_status.py`) apply the same post-passes in memory, so their `--check` is exact.

## 5. Advisory notes (non-blocking)

`verify_site.py` reports V4 notes on the new register pages. The provenance rule counts Amazon and FTC links as official, and Google and GitHub links as repository-only. The brief's rows that cite Google developer pages therefore appear as "no official link". These are recorded as advisory by the existing gate and do not block.

## 6. Clean checkout

Recorded in the COORDINATION Part 38 log after the final push (the fresh clone of the pushed commit ran every gate listed in §3; `build_shop --check` failed there before the allowlist fix and passed after it).

## 7. Not done (blocked, see flags)

Special Link validation (needs an Associates account), Search Console (needs a Google account), reader capture (needs a decision and a privacy notice), collector hosting (needs a host), the five event definitions (need owner confirmation), image decision (S-18), and the brand name (DEC-04).
