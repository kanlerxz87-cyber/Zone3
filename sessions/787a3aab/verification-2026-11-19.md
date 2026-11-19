# Line-by-line verification — session 787a3aab, 2026-11-19

Base: `0273fb4` (main, PR #198). Method: every load-bearing claim below was re-read
today against the official page linked in its row, or measured in this checkout with
the command shown. Nothing was inferred. Values that cannot be confirmed from an
official source stay blank in the registers and are flagged, never filled in.

Official sources re-read today (manual-review links):

- Operating Agreement (Updated October 15, 2025): https://affiliate-program.amazon.com/help/operating/agreement
- Program Policies (Updated April 14, 2026): https://affiliate-program.amazon.com/help/operating/policies
- Creators API GetItems / ItemIdType: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items
- Google, Qualify outbound links (Last updated 2025-12-10 UTC): https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- FTC, Disclosures 101 (November 2019): https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- FoodSafety.gov, Safe Minimum Internal Temperatures (Last Reviewed November 21, 2024): https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures
- USDA FSIS, Food Thermometers (Last Updated Mar 21, 2025): https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers
- Live site: https://kanlerxz87-cyber.github.io/Zone3/ (read-back 2026-11-19)

## V01 — Disclosure sentence (Operating Agreement §5) — CONFIRMED

§5 reads verbatim: "You must clearly and prominently state the following, or any
substantially similar statement previously allowed under this Agreement, on your
Site …: 'As an Amazon Associate I earn from qualifying purchases.'"
Repo: the sentence appears under the masthead (`z3:strip`) and in the footer
(`z3:footer`) on all 18 indexable pages (measured: strip index < `<main` index on
every page; 2 occurrences per page, 3 on about.html which also carries it in the
disclosure section). `scripts/check_site.py` + `tools/check_publication.py` enforce it.

## V02 — §5 violation is a material breach (§6) — CONFIRMED

§6: "any violation of Section 5 and as specified in the Program Policies will be
deemed a material breach of this Agreement." Consequence recorded in the brief-status
register; no change needed.

## V03 — Special Links, tag, sub-tags (Program Policies §2(a)–(b)) — CONFIRMED, owner gate open

§2(a): "Special Links enable accurate tracking, reporting, and accrual of commission
income. Special Links must use the Associates ID we have assigned to you."
§2(b): every link to an Amazon Site must carry the Associates ID or "tag" as a URL
parameter (format XXXXX-##); no bookmarking inducement; all Special Links accessed
directly from the Site; "Under no circumstances may you associate any sub-tag, other
ID or reporting … with a specific end user of your Site."
Repo: `data/special-links.json` holds five built Special Links
(`https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20`), all `validation_status:
pending`, with the scaling rule "Do not scale placement … until one link per product
has been opened in the enrolled Associates workflow and its destination and tracking
report confirmed." Reader-page CTAs still use the exact supplied short links and the
observed `/dp/` URLs carry no tag. That is the documented pre-validation state, not a
verified attribution claim. The supplied tag `shopnow047c-20` is recorded as
user-supplied and unverified (no account access in this session). FLG-003 stays open.

## V04 — Price/availability display rule (§2(b)) — CONFIRMED, complied with

§2(b): a Site "may only show prices and availability if: (a) we serve the link in
which that price and availability data are displayed, or (b) you obtain Product
pricing and availability data via Creators API or PA API…"
Repo: `price`, `rating`, `review_count`, `tested_performance` are null for all five
products in `data/publication.json` and `data/shop/products.json`; no reader page
shows a price, rating or review count. During today's redirect fetches the Amazon
pages themselves displayed prices/ratings; those values were deliberately not
recorded anywhere in this session. `tools/check_publication.py` fails the build if
any of the four fields is non-null.

## V05 — No misleading claims; original content (§2(b), Participation §1) — CONFIRMED

§2(b): "You must not make inaccurate, overbroad, deceptive or otherwise misleading
claims about any Product…" Participation §1: Sites "must contain original content";
third-party material needs "significant commentary, analysis, or transformation."
Repo: guides quote listing titles as listing wording, state what is not established,
and publish no "best"/winner/ranking claims. No change needed.

## V06 — rel="sponsored" (Google) — CONFIRMED

Google: "Mark links that are advertisements or paid placements (commonly called paid
links) with the `sponsored` value"; multiple rel values may be space-separated.
Repo: measured 2026-11-19 — every `link.amazon` and `amazon.com/dp` anchor on all 18
indexable pages carries `rel="sponsored noopener"` (zero unsponsored). Enforced by
`scripts/check_site.py` (whole tree) and `tools/check_publication.py` (reader pages).

## V07 — FTC disclosure placement — CONFIRMED

FTC: "Place it so it's hard to miss. The disclosure should be placed with the
endorsement message itself. Disclosures are likely to be missed if they appear only
on an ABOUT ME or profile page … or anywhere that requires a person to click MORE."
Repo: strip under the masthead on every indexable page + repeated in the footer +
repeated next to product tables. Not disclosure-page-only. Compliant in structure;
this is not legal advice and does not certify full legal compliance.

## V08 — ASIN is 10 characters (Creators API) — CONFIRMED

ItemIdType table: "ASIN | Amazon Standard Identification Number: 10-Character
alphanumeric unique identifier assigned by Amazon." All five submitted tokens are 9
characters (`B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV`, `B0c8moW59`, `B0f3GKalj`), so none
is an ASIN. `intended_asin` stays blank for all five; observed destinations are kept
in separate fields and never copied into intended fields (enforced by
`tools/check_publication.py` drift check against `data/shop/products.json`).

## V09 — Five supplied links, re-observed today — DESTINATIONS UNCHANGED (5/5)

Each supplied link was opened today; final listing, title and breadcrumb recorded:

| Submitted link | Final ASIN (today) | Title today vs register | Breadcrumb |
|---|---|---|---|
| https://link.amazon/B04G1MEwY | B0CDY277D3 | matches verbatim | …Fryers > Air Fryers |
| https://link.amazon/B02NbDxp3 | B09B7SB46R | matches verbatim | …Fryers > Air Fryers |
| https://link.amazon/B00hJ57DV | B08DKYBTPH | matches verbatim | …Fryers > Air Fryers |
| https://link.amazon/B0c8moW59 | B0DHZTCNR5 | **wording drift — see 787-F-01** | …Thermometers & Timers > Meat |
| https://link.amazon/B0f3GKalj | B0DZFD6R9Z | matches verbatim | …Thermometers & Timers > Meat |

This is a dated observation only. It does not establish owner intent (FLG-002) and
does not validate attribution (FLG-003). The supplied short links are not called
invalid; their exact compliance status remains unresolved.

## V10 — Product-intent confirmation record — CONFIRMED SEPARATE AND BLANK

`data/shop/products.json` + `data/publication.json`: for SHOP-01…05, `intended_asin`,
`official_listing_url`, `intent_confirmed_on`, `intent_confirmation_source` are all
blank; `observed_redirect_asin` / `observed_listing_url` hold the redirect targets.
The two field groups are never merged. Reader pages link the record at
`intent-record/index.html`.

## V11 — Measurement: OFF, five events, collector tested — CONFIRMED

`data/shop/measurement.json`: `enabled: false`, `endpoint_url: ""`,
`deployment_verified: false`. `assets/measure-config.js` ships
`{"enabled": false, "endpoint": ""}` — no analytics request is made. The five events
are `page_view`, `outbound_click`, `guide_view`, `intent_view`, `flag_view` (canonical
default runtime schema; the brief does not enumerate event names). Collector
(`tools/analytics_endpoint.py`) is tested by `--self-test` + `test_collector.py` +
node measure tests in the release chain. Production collection cannot be enabled
from GitHub Pages (static hosting); a durable authorized HTTPS host is an owner gate.

## V12 — Campaign ledger empty by design — CONFIRMED

`data/shop/campaign-ledger.json`: "Empty by design. No rows." No conversion score,
click estimate or revenue forecast is presented anywhere. Rows may only be added from
authorized first-party reports.

## V13 — Findability sweep (local, 2026-11-19) — CONFIRMED

- 18 indexable pages, each with a unique `<title>`, meta description and canonical
  URL (measured). The four `Moved` stub pages are `noindex,follow` redirects, not
  indexable pages.
- `sitemap.xml`: 18 URLs. `feed.xml`: 28 items (canonical guides + archived desks).
- `robots.txt`: Allow `/`, Disallow `/docs/` + `/sessions/`, Sitemap pointer present.
- `tools/publish.py --check`: 25/25 PASS on base `0273fb4` before any change.

## V14 — Live site read-back — CONFIRMED

`https://kanlerxz87-cyber.github.io/Zone3/` serves the publication front page:
masthead, disclosure strip, five product cards (supplied-link CTAs labelled
Sponsored, observed `/dp/` source links, intent/FLG-003 notes), question router and
guide cards. No price/rating reproduced. Matches the local build.

## V15 — USDA FSIS thermometer calibration (new guide source) — CONFIRMED

FSIS "Food Thermometers", Calibration section: "There are two ways to check the
accuracy of a food thermometer. One method uses ice water, and the other uses
boiling water." Ice-water method: fill a large glass with ice cubes, add drinking
water, stir well, immerse the stem a minimum of 2 inches touching neither the sides
nor the bottom, wait a minimum of 30 seconds, check without removing the stem; "It
should read 32 degrees F; if it does, the thermometer is calibrated. If not, adjust
according to manufacturer instructions." Boiling-water method: ≥2 inches, ≥30
seconds, "should read 212 degrees F at sea level", with an altitude caveat. Also:
"Most food thermometers will give an accurate reading within 2 to 4 degrees F (see
Calibration)" when placed correctly; place in the thickest part away from bone, fat
or gristle; follow the manufacturer's instructions for insertion depth. Page last
updated Mar 21, 2025. This source is added to `data/publication.json` as
`fsis-thermometers` for the new guide; `www.fsis.usda.gov` is added to the official-
hostname allowlists in `tools/check_publication.py` and `scripts/check_site.py`
(USDA FSIS is a U.S. federal .gov publisher, same class as the already-allowed
FoodSafety.gov).

## V16 — FoodSafety.gov safe minimum temperatures — CONFIRMED

Chart re-read: poultry 165°F (74°C); ground meat/sausage 160°F (71°C); beef/bison/
veal/goat/lamb/pork steaks, roasts, chops 145°F (63°C) with 3-minute rest; casseroles
and leftovers 165°F (74°C); fish 145°F (63°C). "Always use a food thermometer to
check whether meat has reached a safe minimum internal temperature." Matches the
figures quoted in the existing probe-placement guide. No change needed.

## Irregularities found in this pass

- **787-F-01 (title drift, SHOP-04):** the live ThermoMaven listing title today reads
  "…NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ,
  Stocking Stuffers Gifts for Men, Black", while the dated register observation
  (2026-11-17/19) reads "…NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED
  Screen, Highly Waterproof for Grill BBQ Camping, Black". Destination ASIN unchanged
  (B0DHZTCNR5). The register is a dated observation and is left verbatim; the drift
  is flagged here for the next re-observation pass. One existing guide quotes the
  older "Highly Waterproof" fragment as a dated title quote; it is not silently
  rewritten in this pass.
- **787-F-02 (CTA link form):** homepage/shop CTAs use the exact supplied short links
  while source links use observed `/dp/` URLs. Deliberate pre-validation state per
  the scaling rule in `data/special-links.json`; changing CTAs to tagged Special
  Links before enrolled-workflow validation would violate that rule. Owner gate.
- **787-F-03 (no new traffic evidence):** no Search Console property, Associates
  report, or production analytics delivery exists, so no organic-traffic, ranking,
  conversion or revenue claim is made. The new guide is an editorial hypothesis
  (working title), per the site's own cadence rule.
