# Verification log — session `cba81fa5` (2026-11-16)

Independent live re-verification round. Every row below was fetched by this session on
2026-11-16 (UTC) from the page in the **Source** column, and compared with what the site
currently publishes. Nothing here is taken from a search-result snippet, an aggregator or a
blog. Where this session did **not** re-read a page, the row says so and names the sessions
that did — that is a coverage statement, not a claim of verification.

Machine-readable copy of this register: `data/cba81fa5/sources.json` (IDs `CBA-S01…CBA-S12`).

## A. Product identity (the three submitted links)

| # | Claim on the site | Result | Source fetched 2026-11-16 |
|---|---|---|---|
| V1 | `link.amazon/B04G1MEwY` opens the CHEFMAN 6 Quart Dual Basket listing | **Confirmed** — final URL `amazon.com/dp/B0CDY277D3?…`; served title as recorded | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) → CBA-S01 |
| V2 | `link.amazon/B02NbDxp3` opens the Emeril Lagasse 26QT French Door listing | **Confirmed** — final URL `amazon.com/dp/B09B7SB46R?…` | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) → CBA-S02 |
| V3 | `link.amazon/B00hJ57DV` opens the Chefman 8 Qt TurboFry listing | **Confirmed** — final URL `amazon.com/dp/B08DKYBTPH?…&th=1` | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) → CBA-S03 |
| V4 | The submitted tokens are not ASINs and do not resolve as `/dp/` pages | **Confirmed** — `amazon.com/dp/B04G1MEwY` returned Amazon's "Page Not Found" error page (1 chunk, no product content) | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) → CBA-S04 |
| V5 | Each destination listing sits under Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | **Confirmed** for the page read (B0CDY277D3); the same path is shown on B09B7SB46R and B08DKYBTPH in the same capture set | [Best Sellers in Air Fryers, node 17659096011](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) · CBA-S05 |

**Observed destination titles (verbatim, as served 2026-11-16).** These are listing titles, not
product facts invented here; Amazon edits listing titles, and the wording differs from older
captures in the shared register:

1. `B0CDY277D3` — "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows,
   Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets,
   Digital Double Air Fryer - Black : Home & Kitchen"
2. `B09B7SB46R` — "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven
   \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking
   Accessories Included : Home & Kitchen"
3. `B08DKYBTPH` — "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for
   Crisper Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel :
   Home & Kitchen"

**Withheld on purpose.** The fetched listing and category pages also render prices, star ratings and
review counts — including for the sibling listings on those pages. None of those values is repeated in
this log, in the data files or on any page, because Participation Requirements 2(b) allows price and
availability display only when Amazon serves the link or the data comes from the Creators API / PA API,
and 6(t) allows customer reviews and star ratings only when obtained through those APIs
([Program Policies](https://affiliate-program.amazon.com/help/operating/policies), read 2026-11-16).

## B. Programme rules this site is built under

| # | Claim on the site | Result | Source fetched 2026-11-16 |
|---|---|---|---|
| V6 | Enrollment requires a site with original content that is publicly available, and third-party material needs "significant commentary, analysis, or transformation" | **Confirmed verbatim** — Participation Requirements 1 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) → CBA-S07 |
| V7 | Special Links must use the Associates ID Amazon assigned | **Confirmed verbatim** — Participation Requirements 2(a) | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) → CBA-S08 |
| V8 | The tag appears as `XXXXX-##` and must be a URL parameter on every link to an Amazon Site; product lists need additional original content; no inaccurate, overbroad, deceptive or misleading claims; prices/availability only via served link or API | **Confirmed verbatim** — Participation Requirements 2(b) | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) → CBA-S09 |
| V9 | Commission is paid ≈60 days after the end of the month; US payment minimums $10 (deposit), $10 (gift card, max $2,000), $100 (check) with a $15 check-processing fee | **Confirmed verbatim** — Commission Income Statement 5 and 6, Payment Minimum Chart | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) → CBA-S10 |
| V10 | Standard Commission Income Statement Table 1: "Physical Books, Kitchen, Automotive — 4.50%", "All Other Categories — 4.00%" | **Confirmed verbatim** | [Commission Income Statement, Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) → CBA-S11 |
| V11 | FTC: disclose any financial, employment, personal or family relationship; place it so it is hard to miss and with the endorsement itself; you cannot talk about an experience with a product you have not tried | **Confirmed verbatim** (page dated November 2019) | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) → CBA-S12 |
| V12 | A point-in-time category surface exists and is dated: Amazon's "Best Sellers in Air Fryers" page, node 17659096011, which lists Air Fryers alongside sibling nodes Air Fryer Ovens (224479505011) and Deep Fryers (289918) | **Confirmed** — page states "Our most popular products based on sales. Updated frequently." The Emeril Lagasse listing (B09B7SB46R) was displayed at position **#6** on this date. Recorded as a dated observation of a page, never as a product quality claim | [Best Sellers in Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) → CBA-S06 |

## C. Not re-read by this session (coverage statement)

| Item | Status in this round | Basis this session relies on |
|---|---|---|
| Operating Agreement §5 disclosure wording and the "Updated: October 15, 2025" header | Not re-fetched today by this session | Re-read verbatim today by sessions `ab3ed329` (A8–A9) and `59d84c55`, and on 2026-11-15 by `4f83ee7b` (R5) — three sessions, same wording. Shared register S01/S49 |
| Participation Requirements 6(t) (reviews/star ratings), 6(w) (link shorteners), 6(y) (price tracking), 6(z) (no promotion of non-Amazon retailers) | Chunk not fetched today by this session (the page is 11 chunks; this session read chunks 2 and 3) | Verbatim quotes held in `data/policy_facts.json` PF-05, PF-06, PF-32, PF-34, PF-45, PF-46, PF-47, re-read 2026-11-14/16 by sessions `3ead7ac8`, `ab3ed329`, `59d84c55` |
| Creators API `itemIdType` = ASIN (10-character alphanumeric) and the ≥10 qualifying sales prerequisite | Not re-fetched today by this session | Re-read 2026-11-16 by `ab3ed329` (A7) and 2026-11-15 by `4f83ee7b` (R6); shared register S04, S31 |
| PA-API 5 deprecation (403 AccessDeniedException) | Not re-fetched today by this session | Shared register S05, read 2026-11-13; no change reported by any later session |
| FTC Endorsement Guides FAQ (2023 revision) and the Consumer Reviews and Testimonials Rule | Not re-fetched today by this session | Shared register S44, S59, read 2026-11-14 |

## D. What changed as a result of this round

1. **Title drift confirmed again.** The Emeril Lagasse title served today carries
   "Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking
   Accessories Included", where `data/products.json` and `marketing/index.html` still quote the
   2026-11-13/14 wording ("26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan
   and rotisserie for easy family meals"). The ASIN and destination are unchanged. Recorded as
   **CBA-F-01** (listing-title drift; the site's guide copy now quotes the wording served today).
2. **A new, dated category anchor.** V12 gives the site a legitimate "current in the category"
   surface without inventing trend data, which is what `data/suggestions.json` SUG-08 asked for.
3. **Enrollment rule now quoted on the site.** V6 (original content, "significant commentary,
   analysis, or transformation") is the official basis for the anti-slop style rule — the style guide
   cites it rather than asserting taste.
4. **No value was added to any price, rating, review-count, click, conversion or revenue cell.** They
   remain blank and flagged (shared flags FLG-022/023/033 and `link_report.py`'s unresolved list).
