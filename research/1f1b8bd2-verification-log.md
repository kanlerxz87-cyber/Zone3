# Independent line-by-line re-verification — session `1f1b8bd2`

**Date:** 2026-11-16 (UTC)
**Branch:** `arena/1f1b8bd2-zone3` (base `933e2f3` = `origin/main` at claim time)
**Scope:** 1F-T3 of the shared task board (`COORDINATION.md`, Part 1F). Every row below was
fetched **live on 2026-11-16 by this session** through the platform's page-fetch tool; page URL
is the source. Nothing is taken from a search result, a blog, an aggregator, or another
session's record. Values that could not be confirmed from an official page are left blank and
flagged; no value was inferred.

## A. Submitted short links and `/dp/` controls

| # | Claim checked (as published on the site) | Official source fetched 2026-11-16 | Result |
|---|---|---|---|
| 1F-V01 | `link.amazon/B04G1MEwY` opens `amazon.com/dp/B0CDY277D3` | https://link.amazon/B04G1MEwY | **Confirmed.** Final URL `amazon.com/dp/B0CDY277D3?...&plpRedirect=mhFallback`; served title "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen". Breadcrumb Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers (node `17659096011`). |
| 1F-V02 | `link.amazon/B02NbDxp3` opens `amazon.com/dp/B09B7SB46R` | https://link.amazon/B02NbDxp3 | **Confirmed.** Final URL `amazon.com/dp/B09B7SB46R?...`; served title "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen". Same Air Fryers breadcrumb. |
| 1F-V03 | `link.amazon/B00hJ57DV` opens `amazon.com/dp/B08DKYBTPH` | https://link.amazon/B00hJ57DV | **Confirmed.** Final URL `amazon.com/dp/B08DKYBTPH?...`; served title "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen". Same Air Fryers breadcrumb. |
| 1F-V04 | `amazon.com/dp/B04G1MEwY` (9-char token) → Page Not Found | https://www.amazon.com/dp/B04G1MEwY?cb=1f1b8bd2 | **Confirmed.** Served title "Page Not Found". |
| 1F-V05 | `amazon.com/dp/B02NbDxp3` → Page Not Found | https://www.amazon.com/dp/B02NbDxp3?cb=1f1b8bd2 | **Confirmed.** Served title "Page Not Found". |
| 1F-V06 | `amazon.com/dp/B00hJ57DV` → Page Not Found | https://www.amazon.com/dp/B00hJ57DV?cb=1f1b8bd2 | **Confirmed.** Served title "Page Not Found". |
| 1F-V07 | Positive control: a real 10-char ASIN serves a product page | same fetches as 1F-V01…03 (destination pages render product content) | **Confirmed** — the negative results in 1F-V04…06 are therefore meaningful. |
| 1F-V08 | No Associates tag (`tag=`) in any destination URL | destination URLs observed in 1F-V01…03 | **Confirmed** — parameters observed: `srctok`, `channelId`, `lv`, `plpRedirect`, `th`. No `tag=`. Consistent with FLG-010. |
| 1F-V09 | Mapping stability across sessions | compare with S11–S13, S23, and sessions' 2026-11-13/14/15 records | **Confirmed** — same three destinations as every prior session (fourth independent day). |

**Not published, deliberately:** the destination pages served prices and star ratings to this
fetch. Program Participation Requirements 2(b) and 6(t) (verified below) permit those on a site
only when Amazon serves them through the link or they come from Creators API/PA API. They are
recorded here only as "served, not published" and no numeric value is asserted.

## B. Policy and rate sources (all fetched 2026-11-16)

| # | Claim checked (as published on the site) | Official source fetched 2026-11-16 | Result |
|---|---|---|---|
| 1F-V10 | Operating Agreement header "Updated: October 15, 2025"; §5 disclosure sentence verbatim: "As an Amazon Associate I earn from qualifying purchases."; §6: any violation of §5 "will be deemed a material breach" | https://affiliate-program.amazon.com/help/operating/agreement (chunks 0–1) | **Confirmed verbatim** (header, §5, §6 clause all present in the served text). |
| 1F-V11 | Program Policies header "Updated: April 14, 2026" | https://affiliate-program.amazon.com/help/operating/policies (chunk 0) | **Confirmed** — served header reads "Updated: April 14, 2026." |
| 1F-V12 | Commission Income Statement §1 windows: 24-hour session; cart order ≤ 89 days after initial click-through; ship/pay within 180 days | same (chunk 0) | **Confirmed verbatim** ("24 hours elapse from that click"; "no later than 89 days after their initial click-through"; "within 180 days of the purchase, the Product is shipped to, streamed or downloaded by, and paid for by the customer"). |
| 1F-V13 | Participation Requirements 2(b): tag `XXXXX-##` as URL parameter; no dynamic per-visitor sub-tags; prices/availability only if Amazon serves the link or data comes via Creators API/PA API; no inaccurate/overbroad/deceptive claims; remove ended-promotion mentions; comparison pricing must show lowest new (and lowest used when provided) | same (chunk 3) | **Confirmed verbatim.** |
| 1F-V14 | Participation Requirements 6(s), 6(t), 6(v), 6(w), 6(y): no artificial clicks/sessions; reviews/star ratings only via Creators API or PA API; no cloaking; shorteners must not make the Amazon destination unclear; no price tracking/alerting | same (chunk 5) | **Confirmed verbatim** — all five clauses present. |
| 1F-V15 | Standard Commission Table 1 is public: "Physical Books, Kitchen, Automotive \| 4.50%"; "All Other Categories \| 4.00%"; "Luxury Beauty, Luxury Stores Beauty, Amazon Explore \| 10.00%"; bounty rows $12.00 / $2.00 / $5.00 / $0.25 | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ (chunk 0) | **Confirmed row for row** as printed. A category rate only — never assigned to a product (FLG-021/FLG-013 stand). |
| 1F-V16 | Creators API: four operations (SearchItems, GetItems, GetVariations, GetBrowseNodes); prerequisite "at least 10 qualifying sales within the past 30 days"; enrolment + registration + credentials | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction | **Confirmed verbatim.** |
| 1F-V17 | GetItems `ItemIdType`: ASIN = "Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items (chunk 1) | **Confirmed verbatim** — supports 1F-V04…06 (the nine-character tokens cannot be ASINs). |
| 1F-V18 | FTC Disclosures 101: "financial, employment, personal, or family relationship"; "Place it so it's hard to miss"; "You can't talk about your experience with a product you haven't tried"; page dated November 2019 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | **Confirmed verbatim.** |
| 1F-V19 | FTC Endorsement Guides "revised in 2023" | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews (chunk 0) | **Confirmed** — served text: "Guides Concerning Use of Endorsements and Testimonials in Advertising (Endorsement Guides), revised in 2023". |
| 1F-V20 | **New source (S59):** FTC Rule on the Use of Consumer Reviews and Testimonials "went into effect on October 21, 2024"; Q&A quotes §465.2 (fake/false reviews; influencers in the business of posting testimonials can be liable if they lie about product use), §465.4 (incentivized reviews), §465.6 (misrepresenting that a controlled site provides independent reviews), §465.7 (review suppression), §465.8 (fake social-media influence indicators); the rule's disclosure requirements relate to company insiders, influencer relationship disclosures remain under the FTC Act / Endorsement Guides | https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers (chunk 0) | **Confirmed verbatim.** Registered as **S59**; published as flag **1F-F-01** because the site's compliance citations did not include this rule. |

## C. Repository integrity (base `933e2f3`, 2026-11-16)

| # | Check | Result |
|---|---|---|
| 1F-V21 | `python3 scripts/check_site.py` (before this session's additions) | **OK** — 13 pages, 3 products, 51 sources, 78 flags |
| 1F-V22 | `python3 tools/verify_site.py` | **VERIFY PASS** — 74 pages, 1,333 rows, 1,128 with official source, 406 with flag, 86 repo-anchored, 0 advisories |
| 1F-V23 | `python3 tools/link_report.py --strict` | **exit 0** — no dangling source/flag refs; advisory lists six unreferenced-but-published flags (FLG-001/002/003/007/027, I-F-01 — non-blocking, known since cd0e6279) |
| 1F-V24 | `python3 scripts/build_sitemap.py --check` | **exit 0** — 69 pages covered, 0 extra |
| 1F-V25 | `python3 scripts/check_all_links.py` | **120 HTML pages, 105 distinct external URLs, 0 errors** |
| 1F-V26 | Conflict-marker sweep `git grep -Il -E '^(<{7}\|>{7})( \|$)'` | **0 files** |
| 1F-V27 | Secrets scan (key/secret/password/token patterns outside archives) | **0 hits** |
| 1F-V28 | Duplicate nav destinations (root + marketing pages) | **0 pages** |
| 1F-V29 | `scripts/build_site.py` idempotence | **clean** (second run: zero new diffs) |
| 1F-V30 | `scripts/build_marketing.py` idempotence at base | **FAILED** — six marketing pages differed by one nav line each (missing the Suggestions entry). Fixed in this session; recorded as **1F-F-03**. |
| 1F-V31 | GitHub Pages deployment state | repo Pages `status=built`; latest build = `933e2f3…` (2026-11-15T12:00:53Z) — current `main` is deployed. |
| 1F-V32 | Gate re-run after this session's additions (`S59`, `1F-F-01…03`, exec-summary count fix, marketing nav fix) | `check_site` **OK** (13 pages, 3 products, 52 sources, 81 flags) · `verify_site` **PASS** (74 pages, 1,337 rows, 1,132 sourced) · `link_report --strict` **exit 0** · `build_sitemap --check` **exit 0** · `check_all_links` **120 pages / 106 external URLs / 0 errors** · generators idempotent |

## D. Not re-verified here, and why

1. **Any price, star rating, review count or promotion badge as a product fact** — barred by
   Participation Requirements 2(b) and 6(t) (1F-V13, 1F-V14) absent Creators API access. The
   cells stay blank; this is a deliberate refusal, not a gap.
2. **Per-product commission rates** — public Table 1 gives category rates only; the products'
   category-to-rate and account context are not established (FLG-013/FLG-021 unchanged).
3. **Clicks, conversions, revenue** — Amazon is the system of record; no account is configured
   (FLG-010, 71-F-05 stand).
4. **Whether the observed destinations are the submitter's intended products** — no official
   source can answer this; needs the owner's confirmation (FLG-002/FLG-027).
5. **The full 55-fact policy corpus chunk by chunk** — this round re-read the clauses listed in
   §B; earlier sessions' readings of the remaining clauses stand as recorded.

## E. Sources used in this record

All fetched live on **2026-11-16** by session `1f1b8bd2`:

`https://link.amazon/B04G1MEwY` · `https://link.amazon/B02NbDxp3` · `https://link.amazon/B00hJ57DV` ·
`https://www.amazon.com/dp/B04G1MEwY` · `https://www.amazon.com/dp/B02NbDxp3` · `https://www.amazon.com/dp/B00hJ57DV` ·
`https://affiliate-program.amazon.com/help/operating/agreement` ·
`https://affiliate-program.amazon.com/help/operating/policies` ·
`https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ` ·
`https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction` ·
`https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items` ·
`https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers` ·
`https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews` ·
`https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers` (new S59) ·
the GitHub Pages API (`gh api repos/kanlerxz87-cyber/Zone3/pages/builds/latest`).

**No third-party page was used as evidence.**
