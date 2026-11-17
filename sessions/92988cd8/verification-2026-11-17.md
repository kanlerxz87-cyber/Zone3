# Independent verification — 2026-11-17 (session 92988cd8)

Every row below was fetched **once, live, on 2026-11-17** by this session. The page URL is the
source. No search result, blog, aggregator or earlier session's capture was used as evidence.
Prices, star ratings and review counts appeared in several of the fetched Amazon pages; **none of
those values is recorded in this file or anywhere in this session's output** — Participation
Requirements 2(b) and 6(t) permit them only where Amazon serves the link or Creators API / PA API
supplies them (both clauses re-read verbatim today, rows V14–V15).

Rendered version of this record: `sessions/92988cd8/index.html`.

## A. The five submitted short links (the 2026-11-17 brief lists five; the register carried three)

| ID | Item | Result | Official source |
| --- | --- | --- | --- |
| V01 | `https://link.amazon/B04G1MEwY` | Landed on `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows…; breadcrumb ends Air Fryers (node 17659096011); **no `tag=` parameter** | [S11](https://link.amazon/B04G1MEwY), [S14](https://www.amazon.com/dp/B0CDY277D3) |
| V02 | `https://link.amazon/B02NbDxp3` | Landed on `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included; same breadcrumb; **no `tag=`** | [S12](https://link.amazon/B02NbDxp3), [S15](https://www.amazon.com/dp/B09B7SB46R) |
| V03 | `https://link.amazon/B00hJ57DV` | Landed on `amazon.com/dp/B08DKYBTPH` — Chefman Air Fryer 8 Qt \| TurboFry 4-in-1 with 450°F Hi-Fry Option…; same breadcrumb; **no `tag=`** | [S13](https://link.amazon/B00hJ57DV), [S16](https://www.amazon.com/dp/B08DKYBTPH) |
| V04 | `https://www.amazon.com/dp/B04G1MEwY` | **Page Not Found** (Amazon error page, title "Page Not Found") | [S08](https://www.amazon.com/dp/B04G1MEwY) |
| V05 | `https://www.amazon.com/dp/B02NbDxp3` | **Page Not Found** | [S09](https://www.amazon.com/dp/B02NbDxp3) |
| V06 | `https://www.amazon.com/dp/B00hJ57DV` | **Page Not Found** | [S10](https://www.amazon.com/dp/B00hJ57DV) |
| V07 | `https://link.amazon/B0c8moW59` **(new)** | Landed on `amazon.com/dp/B0DHZTCNR5` — ThermoMaven 1 Sec Professional Digital Meat Thermometer…; breadcrumb Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › **Meat** (node 289810); **no `tag=`**; token absent from every file in the repository before this session | [S70](https://link.amazon/B0c8moW59), [S72](https://www.amazon.com/dp/B0DHZTCNR5) |
| V08 | `https://link.amazon/B0f3GKalj` **(new)** | Landed on `amazon.com/dp/B0DZFD6R9Z` — CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes…; same Meat browse path (node 289810); **no `tag=`**; token absent from every file before this session | [S71](https://link.amazon/B0f3GKalj), [S73](https://www.amazon.com/dp/B0DZFD6R9Z) |
| V09 | `https://www.amazon.com/dp/B0c8moW59` **(new)** | **Page Not Found** — the new token is a short-link ID, not a 10-character ASIN | [S74](https://www.amazon.com/dp/B0c8moW59) |
| V10 | `https://www.amazon.com/dp/B0f3GKalj` **(new)** | **Page Not Found** — same conclusion | [S75](https://www.amazon.com/dp/B0f3GKalj) |
| V11 | All five destination URLs, parameters read | Each carries only Amazon's own routing parameters (`srctok`, `channelId`, `lv`, `plpRedirect`, `th`, `sbo`, `language`, encoding). **No `tag=` on any of the five** — a click through any link as published attributes nothing (corroborates FLG-010) | S11, S12, S13, S70, S71 |

Character counts (counted here): `B04G1MEwY`=9, `B02NbDxp3`=9, `B00hJ57DV`=9, `B0c8moW59`=9,
`B0f3GKalj`=9. ASIN rule: "Amazon Standard Identification Number: 10-Character alphanumeric unique
identifier assigned by Amazon" ([S31](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter)).

## B. Policy pages (fetched today, quoted today)

| ID | Claim tested | Result | Official source |
| --- | --- | --- | --- |
| V12 | Operating Agreement header date | **"Updated: October 15, 2025"** verbatim (chunks 0–1 of 4) | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |
| V13 | Operating Agreement §5 disclosure sentence | **Verbatim:** "You must clearly and prominently state the following … on your Site … 'As an Amazon Associate I earn from qualifying purchases.'" — identical to PF-01 and to the sentence this site prints on every page | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |
| V14 | Program Policies header date + CIS §1 windows | **"Updated: April 14, 2026"** verbatim; 24-hour session, 89-day cart completion, 180-day ship-and-pay re-read | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V15 | Participation Requirements 2(b) | **Verbatim (chunk 3):** tag "appearing as XXXXX-##, or such other format as we may designate" as a URL parameter; no dynamic per-user sub-tags; prices/availability only where "we serve the link" or via "Creators API or PA API"; expired limited-time promotion mentions must be removed | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V16 | Participation Requirements 6(s), 6(t), 6(v), 6(w), 6(y), 6(z) | **Verbatim (chunk 5):** no artificial clicks/impressions; no reviews or star ratings unless obtained through Creators API or PA API; no cloaking of the URL; no shortening "in a manner that makes it unclear that you are linking to an Amazon Site"; "must not have price tracking and/or price alerting functionality"; no non-Amazon products advertised with Program Content | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V17 | Standard Commission Table 1 + bounty table (public, no sign-in) | **As printed:** Luxury Beauty 10.00%; Physical Books, Kitchen, Automotive 4.50%; Toys/Furniture/Home… 3.00%; All Other Categories 4.00%; bounties $12.00 / $2.00 / $5.00 / $0.25. Category reference only — never assigned to a product | [S25](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| V18 | Creators API ASIN rule + partnerTag | **Verbatim:** "10-Character alphanumeric unique identifier assigned by Amazon"; `itemIdType` default `ASIN`; `partnerTag` Required: Yes | [S31](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter), [S06](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) |
| V19 | FTC Disclosures 101 | **Verbatim:** disclose "any financial, employment, personal, or family relationship"; place it so it is "hard to miss"; "You can't talk about your experience with a product you haven't tried." Page dated November 2019 | [S07](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |

## C. Not verified, and why

| Item | Why it stays blank |
| --- | --- |
| Any price, star rating, review count, sales-velocity or promotion badge | Barred as product facts by 2(b)/6(t) without an Amazon-served link or Creators/PA API — read only to confirm identity, recorded nowhere |
| Per-product commission rate | No official page maps a listing to a rate category; only category tables are published (S25) |
| Whether any destination is the submitter's intended product | A redirect shows where a link goes, not what was meant — owner input (FLG-002) |
| Whether the supplied Tracking ID is registered / approved / marketplace-correct | Requires an enrolled Associates account; no public page shows it (929-F-02) |
| Live clicks, conversions, revenue | Amazon's in-account reporting is the only compliant source; no account is connected (FLG-012) |

## D. Corrections and drift recorded (not re-flagged)

- **Title drift corroboration:** the served Emeril Lagasse title today matches the 2026-11-16
  capture already recorded as CBA-F-01 (older wording remains in `data/products.json`); the served
  Chefman 8 Qt title matches 5a56-D-02. Destinations and ASINs unchanged across every capture by
  every session, now including this one.
- **No fact was found false.** Every claim this session tested matched what the register says.
