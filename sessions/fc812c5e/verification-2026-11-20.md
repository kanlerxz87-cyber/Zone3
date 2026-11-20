# Verification record — session `fc812c5e` · 2026-11-20

Independent line-by-line re-verification of the live reader site against official sources.
Scope: the five submitted links, the five observed listings, the load-bearing policy clauses,
and the site surfaces the brief asks for (shop front page, category pages, guides, disclosure,
sponsored links, intent record, measurement, sitemap/feed, suggestions & decision desk,
design brief, executive summary). No reader-page content was changed in this pass; the only
files touched are this record, the dated note prepended to `EXECUTIVE-SUMMARY.md`, and the
appended Part in `COORDINATION.md`. PR #211 (`arena/ece5f73c-zone3`) owns `index.html`,
`assets/publication.css` and `tools/build_publication.py`; this session did not touch them.

## 1. Submitted links → observed destinations (re-fetched 2026-11-20)

Each `link.amazon` short link was opened and the landing `amazon.com/dp/<ASIN>` page title
was read. The mapping is unchanged from the register (`data/products.json`,
`data/publication.json`); the redirect parameters (`lv=shuf`, `plpRedirect=mhFallback`)
are recorded as observed only and are not used as product data.

| # | Submitted link | Observed ASIN | Listing title read 2026-11-20 (verbatim) | Official source |
|---|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | B0CDY277D3 | Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen | https://www.amazon.com/dp/B0CDY277D3 |
| 2 | https://link.amazon/B02NbDxp3 | B09B7SB46R | Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen | https://www.amazon.com/dp/B09B7SB46R |
| 3 | https://link.amazon/B00hJ57DV | B08DKYBTPH | Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen | https://www.amazon.com/dp/B08DKYBTPH |
| 4 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black : Home & Kitchen | https://www.amazon.com/dp/B0DHZTCNR5 |
| 5 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 : Home & Kitchen | https://www.amazon.com/dp/B0DZFD6R9Z |

Result: **5/5 titles match the register verbatim.** The observed ASINs are kept in the
`redirect_observed` / `observed_asin` fields. They are **not** recorded as the intended
products: the intent fields (`intended_asin`, `official_listing_url`,
`intent_confirmed_on`, `intent_confirmation_source`) remain blank for all five, as the
brief requires (intended and observed fields are never merged). Standing flag **FLG-003**
(the exact compliance status of the supplied short links is unresolved) and **FLG-002**
(intent unconfirmed) remain open and are published on the Flagged-for-review page. The
short links are **not** called invalid anywhere on the site.

## 2. Policy clauses re-read 2026-11-20 (official pages, verbatim)

| Clause | What it says (short quote) | What the site does | Official source |
|---|---|---|---|
| Operating Agreement §5 | "As an Amazon Associate I earn from qualifying purchases." | Disclosure strip under the masthead on every page, repeated in the footer; non-dismissible. | https://affiliate-program.amazon.com/help/operating/agreement |
| Participation Requirements 2(b) | "you must include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site." | Every product-detail CTA carries `?tag=shopnow047c-20` (the user-supplied Tracking ID); `tools/attach_tag.py --check` fails the build if any product link is untagged or carries a foreign tag. | https://affiliate-program.amazon.com/help/operating/policies |
| Participation Requirements 2(b) | "your Site may only show prices and availability if: (a) we serve the link … or (b) you obtain Product pricing and availability data via Creators API or PA API …" | No price or availability is reproduced on any reader page. The listing fetches above showed volatile prices in the page chrome; they were deliberately **not** recorded as product facts and not published. | https://affiliate-program.amazon.com/help/operating/policies |
| Participation Requirements 6(t) | "You will not display or otherwise use any of our customer reviews or star ratings … unless you have obtained a link … through Creators API or PA API …" | No star rating or review count is reproduced anywhere. Same deliberate blank as price. | https://affiliate-program.amazon.com/help/operating/policies |
| Participation Requirements 6(w) | "You will not use a link shortening service … in a manner that makes it unclear that you are linking to an Amazon Site." | Reader CTAs go directly to `amazon.com/dp/<ASIN>?tag=…` (destination clear). The supplied short links appear only in the collapsible "Listing & source" record, labelled as the observed record. | https://affiliate-program.amazon.com/help/operating/policies |
| FTC Disclosures 101 | Disclosures "likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE"; place "so it's hard to miss", with the endorsement. | The Associates statement sits above all content on every page (not footer-only), and outbound product links carry `rel="sponsored"` (machine-readable). | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |

## 3. Site surfaces checked against the brief (2026-11-20)

| Brief requirement | State found | Evidence |
|---|---|---|
| Reads like a shop, not an audit | Front page leads with the five-product shortlist (3 air fryers, 2 thermometers), filterable by category, each card with a Sponsored CTA; research surfaces sit in one "Behind the site" nav group and the footer. | `index.html`, `shop/air-fryers/`, `shop/meat-thermometers/`, live read-back https://kanlerxz87-cyber.github.io/Zone3/ |
| Findable (one site to index) | `robots.txt` allows `/`, disallows `/docs/` and `/sessions/`, names the sitemap. `sitemap.xml` lists 20 canonical URLs (front page, guide index, 11 guides, 4 shop surfaces, about, privacy, style). `feed.xml` carries 11 guide entries. Every reader page has a canonical URL, meta description and Open Graph tags. | `robots.txt`, `sitemap.xml`, `feed.xml`, `tools/build_feed.py --check` → FEED OK |
| Disclosure above the fold, every page | Strip between masthead and content on every page; repeated in footer. Gate `tools/add_disclosure_banner.py --check` passes. | `tools/add_disclosure_banner.py`, live homepage |
| Every outbound product link marked sponsored | All Amazon anchors carry `rel="sponsored noopener"`. Gates `scripts/mark_sponsored.py --check` and `tools/apply_sponsored.py --check` pass. | `index.html` (5 CTAs), gate output |
| Product-intent confirmation record | Separate fields per product; intended ASIN/URL/date/source blank for all five; observed redirect kept in its own field. | `data/publication.json` → `products[].intended_asin` (empty), `intent-record/index.html` |
| Question-shaped guides (the four suggested titles) | All four suggested working titles exist as published guides: "Basket or oven-style air fryer: what should you compare?", "A no-hype checklist for comparing air fryer capacity", "How to assess cleanup and counter-space trade-offs", "Questions to ask before buying a multi-function kitchen appliance" — plus 7 more (11 total). Titles are presented as editorial hypotheses, not popularity claims. | `guides/` (11 guides), `data/publication.json` → `guides` |
| Click & conversion measurement before scaling | Five-event taxonomy shipped (`page_view`, `outbound_click`, `guide_view`, `intent_view`, `flag_view`); production collection is **OFF** (`enabled: false`, no endpoint) because no durable HTTPS collector host exists. Campaign ledger is empty by design; no conversion, traffic or revenue figure is stated anywhere. | `assets/measure-config.js`, `data/shop/measurement.json`, `measurement/index.html` |
| Suggestions section to review before implementing | `suggestions/index.html`: 6 paths, 30 proposals, 39 questions, 50 review-only decision selects (unreviewed / shortlist / defer / reject) with browser-local save and export; a decision-record template; a suggestion-intake shape (what changes / why now / evidence needed / official basis / safe default / gate). Nothing is implemented by reading the page. | `suggestions/index.html`, `assets/publication.js`, `data/publication.json` → `suggestion_intake` |
| Design prompt | `DESIGN_PROMPT.md`: goal, 12 rails each tied to an official clause, measured current state, layout order, visual system. It is a proposal to build from, not a change that was made. | `DESIGN_PROMPT.md` |
| Executive summary | `EXECUTIVE-SUMMARY.md` with dated, scoped sections; this pass prepends its own dated note and leaves history untouched. | `EXECUTIVE-SUMMARY.md` |
| Coordination board | `COORDINATION.md` with session registry, task board, and per-session Parts; this session appends its Part and claims only `sessions/fc812c5e/**`, `EXECUTIVE-SUMMARY.md`, `COORDINATION.md`. | `COORDINATION.md` |

## 4. Build gates

`python3 tools/publish.py` (full rebuild + all checks): **49 commands, 0 failed.**
Working tree clean after rebuild (no generated drift). The structural gates do not verify
every historical factual claim; the factual claims above were verified against the official
pages in §1–§2.

## 5. Irregularities and notes

- **None new.** No product fact, price, rating, review count, commission rate, traffic or
  revenue figure was added, inferred or filled in. Every blank stays blank and flagged.
- **Info (non-blocking, doc drift):** `DESIGN_PROMPT.md` §3 lists `feed.xml` as 29 entries
  (a union count across registers); the shipped `feed.xml` carries 11 guide entries and
  `tools/build_feed.py --check` reports "11 entries (union of both registers)". The 11 is
  the correct shipped count; the brief's 29 is stale wording, not a site defect. Left
  untouched because `DESIGN_PROMPT.md` is owned by session `6b68afc8`'s brief and PR #211
  is open on adjacent files.
- **Info (naming):** the decision selects use `shortlist / defer / reject` rather than
  `Accept / Reject / Defer`. The function is identical (review-only, exportable, implements
  nothing). Not changed.
- **Standing flags (unchanged, published on the Flagged-for-review page):** FLG-003
  (short-link compliance unresolved — never called invalid), FLG-002/FLG-035 (intent
  unconfirmed), FLG-005 (per-product commission rate unassigned; public Table 1 is a
  category reference only), FLG-006 (Creators API needs qualifying sales), plus the
  account/host blockers: Associates enrolment and Special-Link validation, durable
  analytics host, Search Console verification, GitHub Pages commercial-use fit. None block
  the merge; all are listed with source links for owner review after the site is live.
