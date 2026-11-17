# Session ded63349 — independent verification round, 2026-11-17

Every load-bearing fact this session's work rests on was re-read from the official page on
2026-11-17. Prices, star ratings and review counts that appeared in the fetched Amazon text were
read **only to confirm the identity of the listing**; none is recorded as a product fact anywhere
in this repository (Participation Requirements 2(b) and 6(t) — observation D6-V02 below).

| ID | Claim / page | Observed 2026-11-17 | Result |
|---|---|---|---|
| D6-V01 | Operating Agreement header date | "Updated: October 15, 2025 (Current Associates, see what's changed)" on https://affiliate-program.amazon.com/help/operating/agreement | **matches register** (S01 / I2-S01) |
| D6-V02 | OA §5 disclosure sentence | "You must clearly and prominently state the following … on your Site …: \"As an Amazon Associate I earn from qualifying purchases.\"" — verbatim, and "any violation of Section 5 … will be deemed a material breach" (§6(a)) | **confirmed verbatim** |
| D6-V03 | Program Policies header date | "Updated: April 14, 2026." on https://affiliate-program.amazon.com/help/operating/policies | **newer than the 2026-11-16 register capture recorded no date for S02** — the register stores the clause text, not a policies header date; no conflict. Header date recorded here. |
| D6-V04 | Participation Requirements 2(b), tag parameter | "you must include your Associates ID or \"tag\" (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site" | **confirmed verbatim** |
| D6-V05 | 2(b), price/availability | "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API …" | **confirmed verbatim** |
| D6-V06 | 2(b), sub-tag ban | "Under no circumstances may you associate any sub-tag … with a specific end user of your Site … you may not dynamically assign sub-tags to users as they arrive" | **confirmed verbatim** — the five-event ledger below stores no per-user identifiers and never assigns per-user tags |
| D6-V07 | 6(s), artificial clicks | "You will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site, whether by way of a robot or software program or otherwise." | **confirmed verbatim** — the ledger counts clicks made by this site's own readers on its own pages; it never generates Amazon clicks or sessions |
| D6-V08 | 6(t), reviews/ratings | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API …" | **confirmed verbatim** |
| D6-V09 | 6(v)/6(w), cloaking and unclear links | 6(v): "You will not cloak, hide, spoof, or otherwise obscure the URL …"; 6(w): "You will not use a link shortening service … in a manner that makes it unclear that you are linking to an Amazon Site." | **confirmed verbatim** — rel="sponsored" marks the relationship without hiding the destination |
| D6-V10 | 6(y), price tracking | "Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality." | **confirmed verbatim** — the ledger records click events only; no price monitoring of any kind |
| D6-V11 | Standard Commission Table 1 | "Physical Books, Kitchen, Automotive \| 4.50%" and "All Other Categories \| 4.00%"; bounties Prime $12.00 / Prime Video Trial $2.00 / First Stream $5.00 / Stream $0.25 | **matches register** (S25 / I2-S05 row-for-row) |
| D6-V12 | ASIN is a 10-character identifier | Creators API GetItems: `itemIdType` default `ASIN`; usage example `"itemIds" : ["B0199980K4" , "B000HZD168"]` — both 10 characters | **confirmed** |
| D6-V13 | FTC Disclosures 101 | "financial, employment, personal, or family relationship"; "Place it so it's **hard to miss**"; "You can't talk about your experience with a product you haven't tried."; page footer "November 2019" | **confirmed verbatim** (I2-S06 / S07) |
| D6-V14 | link.amazon/B04G1MEwY destination | Final URL `amazon.com/dp/B0CDY277D3?lv=shuf&btn_type=ss&…&plpRedirect=mhFallback`; served title "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | **matches register** (I2-S07): same destination ASIN, same title, same `plpRedirect=mhFallback` route |
| D6-V15 | link.amazon/B02NbDxp3 destination | Final URL `amazon.com/dp/B09B7SB46R?lv=shuf&…&plpRedirect=mhFallback`; title "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen" | **matches register** (I2-S08) |
| D6-V16 | link.amazon/B00hJ57DV destination | Final URL `amazon.com/dp/B08DKYBTPH?lv=shuf&…&plpRedirect=mhFallback&th=1`; title "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen" | **matches register** (I2-S09) |
| D6-V17 | Direct listing B08DKYBTPH | Same title served on `amazon.com/dp/B08DKYBTPH` direct fetch; browse path Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers shown on all three pages | **matches register** (I2-S12) — the `plpRedirect=mhFallback` parameter also appears on the direct fetch, re-confirming the 588693c9 correction that the parameter is not evidence of a failed lookup |
| D6-V18 | Identity caveat | The three destinations open live listings; nothing official establishes that they are the products the owner intended to promote (9-character tokens are not ASINs — D6-V12) | **unchanged** — the intent record keeps `intended_asin` blank |

## What this round changes

Nothing in the register was contradicted. Two additive observations (D6-V03 policies header date
"April 14, 2026"; D6-V14–16 re-observation of the destinations on 2026-11-17) are recorded here
only; the canonical registers keep their 2026-11-16 capture dates because this session did not
re-emit the source JSON with new fetch metadata.
