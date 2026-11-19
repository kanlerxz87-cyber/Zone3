# Verification record — session `cdb0a5ac`, 2026-11-19

Branch: `arena/cdb0a5ac-zone3` (base `6eb8c18e` = `main` at claim).
Method: official pages re-read live through the session's page-fetch tool on 2026-11-19;
repository measurements scripted against the checked-out tree (same skip set as the release
gates: `archive/`, `docs/`, `sessions/`). Every quote below was copied from the fetch result on
the date shown. Where a source was not re-read this pass, that is stated — nothing is inferred.

## 1. Official sources re-read live on 2026-11-19

| # | Source | URL | What was read (verbatim anchors) | Result |
|---|---|---|---|---|
| V1 | Google Search Central — Qualify your outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | "Mark links that are advertisements or paid placements (commonly called paid links) with the `sponsored` value." "Links marked with these `rel` attributes will generally not be followed." Page footer: "Last updated 2025-12-10 UTC." | Matches the site's `rel="sponsored"` rule on every product link (S-05 basis). Confirmed. |
| V2 | FoodSafety.gov — Cook to a Safe Minimum Internal Temperature | https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | Chart read in full: poultry 165 °F (74 °C); ground meat and sausage 160 °F (71 °C); beef/bison/veal/goat/lamb and pork steaks, roasts, chops 145 °F (63 °C) with **rest time 3 minutes**; casseroles and leftovers 165 °F (74 °C); fish 145 °F (63 °C); raw ham 145 °F + 3 minutes; "Always use a food thermometer…". Page footer: "Date Last Reviewed — November 21, 2024". | Matches the existing `food-safety` source row (checked_on 2026-11-19) and the new guide's temperature spine, quoted as read. |
| V3 | FoodSafety.gov — 4 Steps to Food Safety (Cook step) | https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety | "Use a food thermometer to be sure your food is safe. When you think your food is done, place the food thermometer in the thickest part of the food, making sure not to touch bone, fat, or gristle." Also hot-hold "140°F (60°C) or above" and microwave "165°F (74°C) or above". | New source row `food-safety-cook` (checked_on 2026-11-19) — the placement wording behind guide section 2. Confirmed. |
| V4 | FTC — Disclosures 101 for Social Media Influencers | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | "your endorsement message should make it obvious when you have a relationship ('material connection') with the brand"; "Place it so it's hard to miss"; "You can't talk about your experience with a product you haven't tried." Page dated "November 2019". | Matches the `ftc` source row and the disclosure/authorship rules the gates enforce (no first-person use claims). Confirmed. |
| V5 | Amazon Associates Program Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Header: "Updated: October 15, 2025". §1: links "must properly use the special 'tagged' link formats we provide and comply with this Agreement ('Special Links')"; Program Content defined as data/images/text/link formats etc. made available in connection with the Program. §1 incorporates the Program Policies by reference. | Matches the `amazon-agreement` source row (S01/S95) and the intent-record / Special-Link discipline. Confirmed. |

**Not re-read this pass (named, not implied):** the Associates Program Policies full text and the
FTC Endorsement-Guides topic page were re-read the same day by session `b580d790`
(`sessions/b580d790/verification-2026-11-19.md`); Google's write-high-quality-reviews,
people-first-content, Search Console and canonical pages were re-read in earlier 2026-11-19
passes. The five supplied short links were re-resolved by `b580d790` today (destinations
unchanged); this pass did not re-click them. Zone4 decision-log URLs cited in the brief's
S-rows were not re-read (they belong to the Zone4 repository; recorded as such in the
brief-status register `_meta`).

## 2. Repository measurements — 2026-11-19 (session `cdb0a5ac`)

| Measurement | Result |
|---|---|
| Published HTML pages (skipping archive/docs/sessions) | 121 (116 real pages + 5 meta-refresh redirect stubs) |
| Pages missing `<title>` or meta description | 0 among real pages; the 5 redirect stubs carry none by design (`analysis.html`, `disclosure.html`, `flagged-for-review.html`, `marketing.html`, `categories/home-kitchen-air-fryers.html`) |
| Links to `amazon.com` / `link.amazon` product hosts | 1,764 — **0** without `rel="sponsored"` |
| `affiliate-program.amazon.com` policy/source links (not paid links) | 1,215 |
| Pages carrying the Associates disclosure sentence | 121 / 121 |
| Pages with `og:image` + JSON-LD | 30 / 121 (publication layer and reader site; dashboards and redirect stubs without) |
| Question-shaped guides under `guides/` | **9** (added `where-does-the-probe-go` this pass through the publishing gate) |
| Articles under `articles/` (excluding index) | 4 |
| `feed.xml` | RSS 2.0, **27** items; `tools/build_feed.py --check` current |
| `sitemap.xml` | **17** canonical URLs = exactly the register's `indexable_pages` set; `build_sitemap.py --check` current |
| RSS autodiscovery link | 121 / 121 pages |
| "Which one is for you?" chooser | `shop/index.html`, `shop/air-fryers/index.html`, `shop/meat-thermometers/index.html` — above the table/cards; **absent from `shop/products/index.html`** (open proposal E61-P5) |
| Front page order | masthead → disclosure → editorial hero → `#products` shortlist → question router → reading room → seasonal → editor note; "Behind the site" nav group + footer both present (check_publication enforces ≥2 references from the root for every dashboard link) |
| Guide internal links | all 9 guide pages link their `shop/` pillar and ≥4 other guides; guide index links all 9 |
| Article internal links | all 4 articles link `shop/` catalogue + both category pillars + the guides index |
| "per cm" / "per centimetre" analysis | only where the brief line itself is quoted (brief-status, shop/flagged, suggestions) — **no capacity-per-centimetre analysis exists** (S-23 unimplemented; cannot be computed honestly while interior dimensions remain unverified blanks) |
| "trending" word occurrences | on 20 published pages (16 on 2026-11-17) — all dashboards/registers/quoted brief text |
| New guide page quality gates | title 63 chars (20–85 ✓), description 157 chars (60–165 ✓), one `<h1>`, `index,follow`, Article schema author = Zone3 Editorial (organization), 4 sponsored Amazon links, disclosure under masthead before `<main>`, footer disclosure, exactly one `measure.js` |

## 3. Release chain

- `python3 tools/publish.py` (full 16-builder chain + all 25 checks): **41/41 PASS**, run twice
  back-to-back on 2026-11-19 with a byte-stable tree between runs (no file changed after the
  second run).
- **Clean checkout:** a fresh local clone of the pushed branch (`b773d9a`) ran
  `python3 tools/publish.py --check`: **25/25 PASS, exit 0** — the published check suite runs
  from a clean checkout with no npm install (S-10's demand).
- During this pass the chain itself caught one real defect: `check_all_links.py` failed on the
  executive brief's link to this file before it existed — the record was written and the chain
  re-run, per "do not merge a broken site".

## 4. Explicitly not verified (left blank or flagged, never inferred)

- Prices, ratings, review counts, stock and performance figures — empty in the register and
  gated empty (`tools/check_publication.py`).
- Attribution: `shopnow047c-20` remains recorded-not-account-verified; FLG-003 stays open; the
  supplied short links' compliance status stays unresolved (not called invalid).
- Traffic, queries, conversions, orders — no Search Console or Associates report access;
  campaign ledger remains empty.
- The brief's S-row status labels cite the Zone4 decision log; that log was not re-read here
  (`data/shop/brief-status.json` `_meta` carries this caveat unchanged).
