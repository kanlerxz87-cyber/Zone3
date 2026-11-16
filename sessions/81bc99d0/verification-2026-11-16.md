# Session 81bc99d0 — independent live re-verification (2026-11-16)

Every row below was fetched **once, today, by this session** from the official page. Nothing is
carried from another session's capture. Quoted text is reproduced as observed.

| ID | Claim re-checked | Official page read (fetched 2026-11-16) | Result |
|---|---|---|---|
| 81-V01 | link.amazon/B04G1MEwY opens a live listing | https://link.amazon/B04G1MEwY | **Confirmed** — final URL `…/dp/B0CDY277D3`; page title "CHEFMAN 6 Quart Dual Basket Air Fryer Oven …" (Home & Kitchen). Destination matches the register. |
| 81-V02 | link.amazon/B02NbDxp3 opens a live listing | https://link.amazon/B02NbDxp3 | **Confirmed** — final URL `…/dp/B09B7SB46R`; title "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven …". Matches the register. |
| 81-V03 | link.amazon/B00hJ57DV opens a live listing | https://link.amazon/B00hJ57DV | **Confirmed** — final URL `…/dp/B08DKYBTPH`; title "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 …". Matches the register. |
| 81-V04 | Nine-character token is not an ASIN | https://www.amazon.com/dp/B04G1MEwY | **Confirmed** — "Page Not Found" (Amazon dog-page). Same class of result as prior sessions. |
| 81-V05 | ASIN is a 10-character identifier | Creators API GetItems (itemIds examples `B0199980K4`, `B000HZD168`; `itemIdType` default `ASIN`) | **Confirmed** — examples are 10 characters; 9-char tokens are not valid ASINs. |
| 81-V06 | Kitchen 4.50%, All Other 4.00% | Standard Commission Income Statement, Table 1 | **Confirmed as printed** — "Physical Books, Kitchen, Automotive 4.50%"; "All Other Categories 4.00%". |
| 81-V07 | Bounty rates $12 / $2 / $5 / $0.25 | Standard Commission Income Statement, Special Commission Income (a) | **Confirmed as printed** — Prime Free Trial/Paid/Young Adults/Access $12.00; Prime Video Free Trial $2.00; First Stream $5.00; Stream $0.25. |
| 81-V08 | Operating Agreement "Updated: October 15, 2025" | https://affiliate-program.amazon.com/help/operating/agreement | **Confirmed verbatim** — header reads "Updated: October 15, 2025". |
| 81-V09 | Program Policies "Updated: April 14, 2026" | https://affiliate-program.amazon.com/help/operating/policies | **Confirmed verbatim** — header reads "Updated: April 14, 2026". |
| 81-V10 | Price rule 2(b): prices only if served-link or Creators/PA API | Program Policies, Participation Requirements 2(b) | **Confirmed verbatim** — "your Site may only show prices and availability if: (a) we serve the link … or (b) you obtain Product pricing and availability data via Creators API or PA API …". |
| 81-V11 | Rating rule 6(t): reviews/star ratings only via Creators/PA API | Program Policies, Participation Requirements 6(t) | **Confirmed verbatim** — "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link … through Creators API or PA API …". |
| 81-V12 | No artificial clicks 6(s); no link shortening 6(w); no price tracking 6(y) | Program Policies 6(s), 6(w), 6(y) | **Confirmed verbatim** — each clause present with the stated wording. |
| 81-V13 | No cloaking 6(v); Program Content only for Amazon-Site products 6(z) | Program Policies 6(v), 6(z) | **Confirmed verbatim**. |
| 81-V14 | IP License §1 limited license, no data mining/robots | Program Policies, IP License §1 | **Confirmed verbatim** — "This license does not include any downloading, copying or other use of Program Content for the benefit of any third party, or any use of data mining, robots, or similar data gathering and extraction tools." |
| 81-V15 | FTC placement guidance | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers (November 2019) | **Confirmed verbatim** — "Place it so it's hard to miss"; disclosure "placed with the endorsement message itself"; footer-only is "likely to be missed". |
| 81-V16 | FTC no untried-product experience; relationship disclosure | FTC Disclosures 101 | **Confirmed verbatim** — "You can't talk about your experience with a product you haven't tried"; "financial, employment, personal, or family relationship". |
| 81-V17 | No Associates tag exists in the repo; live redirects carry none | live redirects (81-V01–V03) + repo scan | **Confirmed** — the observed redirect URLs carry no `tag`/Associate ID parameter. No tag is configured anywhere in the repo (`config/platform.json`). |

**Not re-fetched this session (no result asserted):** the 180-day/three-sale application-review window,
Onsite Table A rates, and per-ASIN commission mapping — these remain as carried with links from prior
sessions and are not claimed here as verified by this session.
