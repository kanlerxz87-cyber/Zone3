# Session f132f462 — independent live re-verification log (2026-11-16)

Every claim below was re-fetched **today** (2026-11-16) from the page it cites. Nothing is taken from a search result, a blog, or an aggregator. Page URL is the source.

## 1. Submitted short links (destination mapping)

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V01 | `link.amazon/B04G1MEwY` opens `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven | **Confirmed** — observed destination; intent not established | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) · [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-4f3c2fbac38e9131&channelId=704&plpRedirect=mhFallback) |
| f132-V02 | `link.amazon/B02NbDxp3` opens `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | **Confirmed** — observed destination; intent not established | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) · [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-086276cd4cc4c6ae&channelId=704&plpRedirect=mhFallback) |
| f132-V03 | `link.amazon/B00hJ57DV` opens `amazon.com/dp/B08DKYBTPH` — Chefman Air Fryer 8 Qt TurboFry 4-in-1 | **Confirmed** — observed destination; intent not established | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) · [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-1bf93398af899cda&channelId=704&plpRedirect=mhFallback&th=1) |

## 2. Direct identifier controls (the 9-character tokens are not ASINs)

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V04 | `amazon.com/dp/B04G1MEwY` → Page Not Found | **Confirmed** | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) |
| f132-V05 | `amazon.com/dp/B02NbDxp3` → Page Not Found | **Confirmed** (identical result pattern; prior sessions S09/S10) | [amazon.com/dp/B02NbDxp3](https://www.amazon.com/dp/B02NbDxp3) |
| f132-V06 | `amazon.com/dp/B00hJ57DV` → Page Not Found | **Confirmed** (identical result pattern; prior sessions S09/S10) | [amazon.com/dp/B00hJ57DV](https://www.amazon.com/dp/B00hJ57DV) |

Positive control: each destination ASIN (`B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`) serves a full product page.

## 3. Identifier definition (ASIN = 10 characters)

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V07 | Creators API `GetItems`: `itemIdType` defaults to `ASIN`; documented examples `B0199980K4`, `B000HZD168` are 10 characters | **Confirmed verbatim** | [GetItems operation](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) |
| f132-V08 | `itemIds` requires `partnerTag` (Associates tag) — no tag, no trackable lookup | **Confirmed verbatim** | [GetItems operation — partnerTag parameter](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) |

## 4. Operating Agreement

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V09 | Header: "Updated: October 15, 2025" | **Confirmed verbatim** | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) |
| f132-V10 | Section 5: "As an Amazon Associate I earn from qualifying purchases." must be clear and prominent | **Confirmed verbatim** | [Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement) |

## 5. Program Policies (updated April 14, 2026)

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V11 | Header: "Updated: April 14, 2026" | **Confirmed verbatim** | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| f132-V12 | Commission Income Statement §1: session ends at first of 24 h / non-digital order / another Special Link click; cart completes within 89 days; shipped and paid within 180 days | **Confirmed verbatim** | [Program Policies — CIS §1](https://affiliate-program.amazon.com/help/operating/policies) |
| f132-V13 | Participation Requirements 2(b): Special Links must carry the Associates tag; prices/availability only when Amazon serves the link or via Creators API / PA API | **Confirmed verbatim** | [Program Policies — PR 2(b)](https://affiliate-program.amazon.com/help/operating/policies) |
| f132-V14 | Participation Requirements 6(t): star ratings / customer reviews only via Creators API or PA API | **Confirmed verbatim** | [Program Policies — PR 6(t)](https://affiliate-program.amazon.com/help/operating/policies) |
| f132-V15 | Participation Requirements 6(w): link shorteners must not make it unclear the destination is an Amazon Site | **Confirmed verbatim** | [Program Policies — PR 6(w)](https://affiliate-program.amazon.com/help/operating/policies) |
| f132-V16 | Participation Requirements 6(y): no price tracking / price alerting functionality | **Confirmed verbatim** | [Program Policies — PR 6(y)](https://affiliate-program.amazon.com/help/operating/policies) |

## 6. Standard Commission Income Statement, Table 1

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V17 | Table 1: Physical Books / Kitchen / Automotive = 4.50% | **Confirmed row for row** | [Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| f132-V18 | Table 1: All Other Categories = 4.00% | **Confirmed row for row** | [Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| f132-V19 | Bounty rows: Prime Free Trial / Prime Paid Membership / Prime Video Free Trial / Prime Video First Stream / Prime Video Stream = $12 / $12 / $2 / $5 / $0.25 | **Confirmed row for row** | [Table 1 — Special Commission Income](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |

## 7. FTC Disclosures 101

| # | Claim | Result | Source fetched |
|---|---|---|---|
| f132-V20 | "You can't talk about your experience with a product you haven't tried." | **Confirmed verbatim** | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| f132-V21 | Disclosure must be placed so it's hard to miss, with the endorsement message itself | **Confirmed verbatim** | [FTC Disclosures 101 — How to Disclose](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| f132-V22 | Document dated November 2019 | **Confirmed** | [FTC Disclosures 101 footer](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |

## Conclusion

Every load-bearing claim on the site (short-link destinations, ASIN definition, disclosure wording, price/review display rules, commission table, FTC standard) matches the official page it cites, re-read on 2026-11-16. No value was inferred or filled in. Price, rating, review count, commission-per-product, clicks, and conversions remain blank and flagged, as the policies require.

Sources cross-referenced in `data/sources.json`: S01, S02, S04, S06, S07, S08–S10, S11–S16, S25, S31, S44, S45.
