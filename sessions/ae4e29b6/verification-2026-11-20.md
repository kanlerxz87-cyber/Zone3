# Independent re-verification — 2026-11-20

**Session:** `ae4e29b6` · **Branch:** `arena/ae4e29b6-zone3` · **Base:** `main@6a6fdc3`
**Method:** every claim below was checked against a page fetched live on 2026-11-20, or against a
row already registered in `data/sources.json` whose official URL was re-opened today. Nothing is
carried forward from a previous session's summary without being re-read.
**Rule applied throughout:** a value that could not be confirmed from an official source stays
blank and is flagged. No value is inferred from a redirect, a title, or a related-products carousel.

---

## 1. The five submitted links — what resolves, what does not

All five `https://link.amazon/<id>` links were fetched live on 2026-11-20. Each one landed on a
product detail page. This is recorded as an **observation of where the link opens**, not as
confirmation that the owner intended that product (FLG-002, FLG-035).

| # | Submitted link | Where it opens today | Destination page identifier | Breadcrumb on arrival | Intended product confirmed? |
|---|---|---|---|---|---|
| P1 | `https://link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3` | `B0CDY277D3` | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | **No** — unconfirmed, FLG-002 |
| P2 | `https://link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R` | `B09B7SB46R` | Home & Kitchen › … › Fryers › Air Fryers | **No** — unconfirmed, FLG-002 |
| P3 | `https://link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH` | `B08DKYBTPH` | Home & Kitchen › … › Fryers › Air Fryers | **No** — unconfirmed, FLG-002 |
| P4 | `https://link.amazon/B0c8moW59` | `amazon.com/dp/B0DHZTCNR5` | `B0DHZTCNR5` | Home & Kitchen › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat | **No** — unconfirmed, FLG-002 |
| P5 | `https://link.amazon/B0f3GKalj` | `amazon.com/dp/B0DZFD6R9Z` | `B0DZFD6R9Z` | Home & Kitchen › … › Thermometers & Timers › Meat | **No** — unconfirmed, FLG-002 |

**Destinations match the register.** Every destination page identifier above is identical to the
one already recorded in `data/products.json` (`redirect_observed.page_id`). Re-reading five live
pages therefore found **no drift**: the register is still accurate about where the links go.

**Listing titles, read from the arrived-at pages today.** These are the listing's own words and are
reproduced only as titles; they are not a claim about quality, and no ranking is implied.

| # | Listing title as displayed (2026-11-20) |
|---|---|
| P1 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black |
| P2 | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included |
| P3 | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel |
| P4 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black |
| P5 | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 |

**Deliberately not transcribed, though visible on the pages today:** the displayed price, the star
rating, the review count, availability, and every "customers also viewed" item. Program Policies
2(b) permits a site to show prices and availability only when Amazon serves the link carrying that
data or when it comes through the Creators/PA API (S02, re-read 2026-11-20), and 6(t) bars
review/rating republication outside the licensed feeds. Those fields stay `null` in
`data/products.json` and render as "not reproduced" on the site. Recording them here would create a
second, unlicensed store of the same data — so they are absent on purpose, not by oversight.

**Product identifiers: 9 characters submitted, 10 characters required.** Re-confirmed 2026-11-20
from the Creators API `GetItems` reference, which defines an ASIN as a **10-character alphanumeric**
unique identifier and requires `itemIdType=ASIN` with a `partnerTag` (S06/S31). The five submitted
link IDs — `B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV`, `B0c8moW59`, `B0f3GKalj` — are 9 characters, so
they are not ASIN-shaped. A direct `amazon.com/dp/<submitted-id>` request still returns Page Not
Found today (re-checked 2026-11-20 for P1; the S08 row records the same result for the set). This
is a stable irregularity, retained as FLG-001 in `data/flags.json`.

**What the short links being reachable does *not* establish.** A `link.amazon/…` link opening a
product page says nothing about (a) whether the Associates tag `shopnow047c-20` is attached
server-side on that hop, (b) whether the resulting click appears in the Associates report, or
(c) whether the owner intended that product. Only the enrolled Associates workflow can answer
(a) and (b) by testing one link and reading the tracking report (S02 §2(b); 0C4-F-04,
FLG-S05). Until then the supplied links are **not called invalid** (FLG-003 stands unresolved) and
no intent record is marked confirmed.

---

## 2. Load-bearing official sources, re-opened today

| Source | Official page | Re-read 2026-11-20 → what it still says |
|---|---|---|
| S01 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Page states **updated 2025-10-15**. §5 still requires the exact sentence *"As an Amazon Associate I earn from qualifying purchases."* §6 still treats a §5 or Program Policy breach as a material breach. §4 still declines to represent expected traffic or commission income. |
| S02 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Page states **updated 2026-04-14**. 2(b) still requires the Associates ID/tag in every Special Link URL, forbids encouraging bookmarking of Special Links and per-end-user sub-tags, restricts displayed prices/availability to Amazon-served links or Creators/PA API data, and forbids inaccurate, overbroad or deceptive claims. 1(f)/(g) still bar Amazon marks in domains/tags/usernames and child-directed sites. |
| S25 | [Standard Commission Income Statement — Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | Kitchen 4.50%, All Other Categories 4.00%. A **category** reference only; no per-product rate is asserted anywhere in the repo. |
| S06/S31 | [Creators API — GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) | ASIN = 10-character alphanumeric unique identifier; `itemIdType=ASIN`; `partnerTag` required. |
| S07 | [FTC — Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Disclose material connections clearly and conspicuously, in the same place and language as the endorsement; plain words such as *ad* or *sponsored* are acceptable. |
| S90 | [Google — Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | `rel="sponsored"` is still the marker for advertisements and paid placements. |
| S96 | [Google — Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) | Sitemap guidance unchanged: one XML sitemap listing canonical URLs, declared in `robots.txt`, submitted per site. |

`data/policy_facts.json` rows re-inspected against these pages: PF-03 (Associates ID format), PF-04
(prices only via served link or API), PF-05 (ratings/reviews only via API), PF-38 (Kitchen 4.50%),
PF-58 (no bookmark encouragement), PF-59 (no per-user sub-tags). All six still match the live
clauses. **No policy fact needed correcting this round.**

---

## 3. Site integrity gates, run on this tree

| Gate | Command | Result |
|---|---|---|
| Full release chain | `python3 tools/publish.py --check` | **31/31 PASS, 0 failed** (includes `check_all_links`, `build_shop`, `mark_sponsored`, `attach_associates_tag`, `apply_sponsored`, `add_disclosure_banner`, `build_publication`, `check_publication`, the analytics self-test and the measure JS tests). The chain prints its own caveat: structural checks do not verify every historical factual claim. |
| Disclosure presence | census of non-archive HTML | **142/157 carry the Associates sentence**; the 15 that do not are `sessions/3c886b62/*.html` — a previous session's archived prototype folder, outside this session's scope. Logged as a change request below, not edited. |
| `rel="sponsored"` coverage | reader set + shop surfaces | **0 Amazon anchors without `sponsored`** across `index.html`, all 12 `guides/*.html`, and every `shop/*/index.html` (134 Amazon anchors across 23 files inspected). |
| Associates tag on the front page | `grep -c tag=shopnow047c-20 index.html` | **5** — one per product CTA. |
| Sitemap | `sitemap.xml` | **20** `<url>` entries, matching the 20-page indexable set. |
| Feed | `feed.xml` | **11** `<item>` entries. |
| Measurement | `assets/measure-config.js`, `data/shop/measurement.json` | `{"enabled": false, "endpoint": ""}` — still OFF, as designed. The five event names remain defined and unrecorded. |
| Campaign ledger | `data/shop/campaign-ledger.json` | `"rows": []` — empty by design, no forecast, source of truth named as Associates reports (not obtained). |
| Product register | `data/products.json` | Identity/price/rating/review/commission still `null` for all five. No fill-in crept in during the intervening sessions. |

**No fix was required inside this session's scope.** Every defect found was either already flagged
or lives in a file owned by another scope.

---

## 4. Irregularities, kept visible

| Flag | What it is | Status after today's check |
|---|---|---|
| FLG-001 | Submitted link IDs are 9 characters; ASIN is defined as 10 (S06/S31). | **Open.** Unchanged; nothing today explains the discrepancy. |
| FLG-002 | The submitted link's intended product is not documented anywhere. | **Open.** Five redirects re-observed; intent still unconfirmed. |
| FLG-003 | Whether the supplied `link.amazon/…` links comply is unresolved. | **Open, not invalidated.** Only the enrolled Associates workflow can settle it by testing one link and reading the tracking report. |
| FLG-022/029/036 | Do not infer price/rating/identity from a redirect. | **Held.** No values were promoted from today's page reads. |
| 0C4-F-04 / FLG-S05 | Associates tag `shopnow047c-20` is owner-supplied and unvalidated. | **Open.** Format is plausible under PF-03; enrolment and destination validation are account-side. |
| New, this session (**AE-F-01**) | 15 archived HTML files in `sessions/3c886b62/` carry no Associates disclosure. | **Logged only.** Not published (excluded from sitemap, `robots.txt` disallows `/sessions/`), and outside this session's file scope. Recorded here so the integration session can decide whether to add a banner, archive them, or delete them. |

---

## 5. What today's pass changes for the reader

Nothing on the pages had to be retracted, and nothing was added that a buyer can act on more
safely than yesterday. That is the finding: the register survived a fresh line-by-line read of five
live listings and seven policy pages without a single correction. The gaps that remain are
account-side (enrolment, tag validation, intent, analytics host), not editorial — and they stay on
the Flagged for Review page rather than being papered over with an inference.
