# Current-tree review and executive-summary reconciliation — 2026-11-17

## Scope

Reviewed the current publication front page, five-product shop register, suggestions/decision surfaces, and current release gates against the request. Updated the top of `EXECUTIVE-SUMMARY.md` to make the five-link status easy to find while preserving earlier sections as dated audit history. No Amazon listing was re-fetched by this pass; dated observations below are transcribed from the current checked-in register, not presented as a new live observation.

## Product register reconciliation

`data/shop/products.json` contains five submitted links and keeps each `intended_*` field blank. It records five distinct `observed_redirect_asin` values and separates them from intended product identity. `data/shop/sources.json` records the five submitted-link observations as SH-S06–SH-S10, the listing title reads as SH-S11–SH-S15, each dated 2026-11-17. Direct official listing URLs are linked from the summary. The official Creators API ItemIdType page defines an ASIN as a 10-character identifier (SH-S03).

| Submitted link | Observed target ASIN | Register source | Intent status |
|---|---|---|---|
| `B04G1MEwY` | `B0CDY277D3` | SH-S06 / SH-S11 | Unconfirmed |
| `B02NbDxp3` | `B09B7SB46R` | SH-S07 / SH-S12 | Unconfirmed |
| `B00hJ57DV` | `B08DKYBTPH` | SH-S08 / SH-S13 | Unconfirmed |
| `B0c8moW59` | `B0DHZTCNR5` | SH-S09 / SH-S14 | Unconfirmed |
| `B0f3GKalj` | `B0DZFD6R9Z` | SH-S10 / SH-S15 | Unconfirmed |

The shop register and the older three-product shared register are distinct scopes. The executive summary now says so explicitly rather than silently treating three and five as the same dataset. The two additional targets are meat thermometers, while the established reader guide cluster is air-fryers; this is a scope decision, not evidence that either product is popular or suitable.

## Current live surfaces and what remains open

- The root `index.html` is a shop-first publication front page with five product cards, four question-shaped guides, above-the-fold disclosure and footer groups linking to the dashboard, review and data surfaces.
- `shop/executive-summary/index.html`, `shop/products/index.html`, `shop/sources/index.html`, and `shop/decisions/index.html` provide a current shop-scoped summary, product/source tables and decision questions. The older `suggestions.html`, `decision-queue.html`, and `design-brief.html` remain linked from the front page footer.
- `tools/build_shop.py --check` verifies shop-page disclosures, sponsored product links, source rows, sitemap coverage and local links. It passed: 11 shop pages.
- Prices, ratings, review counts, conversion figures and forecasts remain unpublished in the shop surface. The campaign ledger is empty by design.
- No live click collector or self-hosted analytics endpoint is deployed. `data/shop/decisions.json` DEC-03 says the event taxonomy and a host were not specified; the report does not invent them. GitHub Pages hosting limitations and the relevant security logging note are cited in SH-S16.
- Search Console is not configured in this repository. Sitemap and RSS generation are checked, but there is no measured query evidence from which to claim trend/popularity or select an evidence-based next topic.
- The supplied tracking ID was not tested against an Associates account. No Associate account session/report access exists here; intended product identity and account/marketplace fit remain owner-side. FLG-S02, FLG-S04, FLG-S05, and FLG-S06 remain published on the shop Flagged page. This pass did not claim that the supplied short links are invalid; their exact compliance state remains unresolved, consistent with FLG-003.
- No product photography was added. The current decision register says approved Program Content/permission is required for imagery (DEC-05 / SH-S01).

## Suggestions prepared for review

The existing review surfaces already separate facts from proposed choices. Recommended decision sequence, now summarized at the top of `EXECUTIVE-SUMMARY.md`:

1. Decide whether the first publication scope is only air fryers or whether to add a separate meat-thermometer category.
2. In the enrolled Associates workflow, confirm intended products, generate Special Links, and test destination plus report tracking before scaling.
3. Choose a measurement host and define the requested five events before collecting click data; configure Search Console before choosing topics from measured queries.
4. Keep working article titles explicitly hypothetical until actual queries are measured.
5. Preserve blank price/rating/review cells until a policy-approved data path is available; do not infer conversion or revenue.

These are decision prompts and proposed next steps, not newly implemented features or claims of performance.

## Verification performed

- `python3 scripts/check_site.py` — OK: 30 pages, 3 products in the older shared register, 62 sources, 113 flags.
- `python3 tools/verify_site.py` — VERIFY PASS: 134 pages, 2,068 table rows; inherited advisories are non-blocking.
- `python3 tools/link_report.py --strict` — exit 0.
- `python3 tools/i2_gate.py` — PASS: 18 pages, 164 rows, 148 sourced, 16 explicit blanks, 0 flagged.
- `python3 tools/cba81fa5_lint.py` — PASS: 0 new findings, 22 inherited advisory items.
- `python3 tools/build_cba81fa5_site.py --check` — current.
- `python3 tools/build_feed.py --check` — current, 9 entries.
- `python3 scripts/build_sitemap.py --check` — current, 97 pages.
- `python3 scripts/check_all_links.py` — 0 errors across 180 HTML files / 207 external URLs.
- `python3 tools/build_shop.py --check` — OK: 11 shop pages; disclosure, sponsored links, source rows, sitemap and internal links pass.

No new Amazon fact was labeled verified in this pass. Official reference links for the five product records and remaining policy/account questions are in the dated shop source register, executive summary and flagged pages linked above.
