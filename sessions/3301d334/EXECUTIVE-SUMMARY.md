# Executive summary — Zone3 front-page pass

**Date:** 2026-11-19 (UTC)  
**Branch:** `arena/3301d334-zone3`  
**Deliverable:** [Zone3 publication front page](../../index.html)  
**Public URL (after deployment):** https://kanlerxz87-cyber.github.io/Zone3/

## What changed

The home page now opens as a reader-facing kitchen-buying publication rather than a verification dashboard. It leads with a practical comparison promise, presents the five supplied links in two clearly separated groups, and gives priority to four question-shaped buyer guides. Each listing card distinguishes the *observed destination* from the *owner's unconfirmed intended product*, links to the dated official Amazon listing used as its source, and leaves the submitted link clearly labeled. The page adds a compact “what is known / what is open” decision path to the product-intent record, open questions and suggestions queue.

The masthead keeps only reader tasks prominent (Home, Shop, Guides, Compare). An **Explore** menu groups research, product evidence, dashboard/decision surfaces and site files. The shared footer now provides the full directory, including one Dashboards group with 24 report, tracking and decision destinations. The affiliate disclosure stays directly below the masthead and repeats in the footer. Amazon-facing links carry `rel="sponsored"`.

No product photography, prices, ratings, reviews, bestseller rank, search-volume, conversion or revenue claims were added. The design uses typography and layout rather than generated product imagery.

## What the repository supports

- Five submitted short links are in the intent register. The observed destinations were recorded on **2026-11-17**; the ASINs observed are not treated as proof of owner intent.
- Three observed destinations are in the air-fryer guide scope; two thermometer listings remain outside that scope with a category decision open.
- Four buyer guides are published as working titles, not as claims about query popularity.
- Every card's observed target links directly to the Amazon listing cited in the existing source register.
- The Associates disclosure, sponsored-link convention, source register, flags, executive summary, campaign ledger, measurement status, decision queue and suggestions remain available.

## Decisions and evidence still missing

1. **Intended product per link:** the owner has not supplied/confirmed the intended ASIN and official listing URL for any of the five links. Keep intent fields separate from observed redirects.
2. **Special Links and tracking:** the enrolled Associates workflow has not been used to test one link per intended product. FLG-003 remains unresolved. This report does **not** claim the supplied short links are invalid.
3. **Account and API eligibility:** enrollment state, qualifying-sale/API eligibility and credentials are not available in the repository. Do not automate prices, reviews, availability or commissions without an authorized source.
4. **Analytics and search evidence:** the static GitHub Pages site cannot host a POST collector. The self-hosted endpoint has no host/URL, so measurement is deliberately disabled; Search Console ownership is not connected. There are no measured query, click or conversion results to guide topic selection.
5. **Editorial scope and brand:** the two thermometer listings are outside the air-fryer guide cluster; the brand name and final product scope remain owner decisions.

See the live **[Suggestions & decisions](../../suggestions.html)** page and **[Open questions](../../direction/questions.html)** page for proposals, decision paths and discovery steps. Items that need owner-side accounts or confirmation are not presented as completed.

## Verification performed for this pass

- `python3 scripts/check_site.py` — PASS (42 gated pages; 5 products; 83 sources; 148 flags).
- `python3 tools/verify_site.py` — PASS (152 pages; 2,517 table rows). It also reports 532 inherited advisory items elsewhere in the repository; they are non-blocking and are not claims newly verified by this page.
- `python3 scripts/check_all_links.py` — PASS (198 HTML pages; 263 distinct external URLs; 0 link errors).
- `python3 scripts/mark_sponsored.py --check` — PASS.
- `python3 sessions/aebf0747/publish_pass.py --check` — PASS (111 pages; 0 changes needed).
- `python3 tools/build_feed.py --check` — PASS (22 entries current).
- `python3 scripts/build_sitemap.py --check` — PASS (106 pages covered).
- `python3 tools/measure_pass.py --check` — PASS (111 pages; 0 changes needed).
- `node sessions/38650305/test_measure.js` — PASS (counter-off-by-default, GPC/DNT behavior and event-shape checks).
- Regenerating the front page in memory from `sessions/aebf0747/build_pass.py` and applying the shared publication pass produced an exact match to `index.html`.

This pass did not re-fetch Amazon/FTC/Google pages. Claims on the page are limited to the project's existing dated observations and linked sources; the listed official pages are available for manual review below. A successful build/source-link gate is not a claim of current product availability, owner intent or affiliate-link compliance.

## Official source links for manual review

- Amazon Associates **Operating Agreement** (disclosure and Special Links): https://affiliate-program.amazon.com/help/operating/agreement — source register S01.
- Amazon Associates **Program Policies** (link and product-content rules): https://affiliate-program.amazon.com/help/operating/policies — S02.
- Amazon Creators API **Introduction / prerequisites**: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction — S04.
- FTC **Disclosures 101 for Social Media Influencers**: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers — S07.
- Google Search Central **Qualify your outbound links** (`rel="sponsored"`): https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links — S90.
- Dated product-link and destination observations are linked per card and in [`data/products.json`](../../data/products.json), [`data/sources.json`](../../data/sources.json) and the [source register](../../sources/index.html). Relevant source IDs include S11–S16, S23, S70–S73 and S76–S78.
