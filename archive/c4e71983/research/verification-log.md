# Verification log

Line-by-line record of what was checked, against which official page, and what the outcome was.
Session `c4e71983`. Window: 2026-11-13 22:31–22:41 UTC.

**Rule applied:** a value is recorded only if it was read from an official page (Amazon.com,
Amazon Associates Central, or a regulator such as the FTC). If no official page would give up the
value, the field is left blank and flagged. Nothing is inferred, estimated, or carried across from a
similar product.

---

## 1. Link resolution

| Step | Input | Official page retrieved | Outcome |
| --- | --- | --- | --- |
| 1 | `https://link.amazon/B04G1MEwY` | [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | Resolves to ASIN **B0CDY277D3** — verified by URL and page title |
| 2 | `https://link.amazon/B02NbDxp3` | [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | Resolves to ASIN **B09B7SB46R** — verified by URL and page title |
| 3 | `https://link.amazon/B00hJ57DV` | [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | Resolves to ASIN **B08DKYBTPH** — verified by URL and page title |

Caveat recorded as FLAG-07: the redirects are genuine and the ASINs are confirmed by observation, but
no official Amazon document describing `link.amazon` as an Amazon-owned shortener was located.

## 2. Product fields — P1, ASIN B0CDY277D3

Source: [amazon.com/s?k=B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) (qid 1794609434 =
2026-11-13T22:37:14Z) and [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3).

| Field | Value | Status | Official source |
| --- | --- | --- | --- |
| Title | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | verified | dp page |
| Department | Home & Kitchen | verified | dp page title |
| Brand | CHEFMAN / Chefman | verified (from title) | search page |
| Capacity | 6 Quart (2 × 3 Qt) | verified (from title) | search page |
| Star rating | 4.2 out of 5 stars | verified | search page |
| Ratings shown | 4.8K | verified — **rounded by Amazon** | search page |
| Exact rating count | ␣ blank | **unverified** (FLAG-04) | review page is sign-in walled |
| Current price | $79.93 | verified at 22:37:14Z | search page |
| Price per count | $39.97 / count | verified at 22:37:14Z | search page |
| List price | $99.99 | verified at 22:37:14Z | search page |
| Promotion badge | Limited time deal | verified (FLAG-02) | search page |
| Lowest other offer | $57.45 (2+ used & new offers) | verified at 22:37:14Z | search page |
| Bought in past month | 1K+ | verified — rounded by Amazon | search page |
| Best Sellers Rank | ␣ blank | **unverified** (FLAG-03) | detail block not retrievable |
| Wattage | ␣ blank | **unverified** (FLAG-10) | not exposed |
| Model number | ␣ blank | **unverified** (FLAG-10) | not exposed |
| Affiliate tag present | **No** | fails a rule (FLAG-05) | Program Policies §2(b) |

## 3. Product fields — P2, ASIN B09B7SB46R

Source: [amazon.com/s?k=B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) (qid 1794609226 =
2026-11-13T22:33:46Z) and [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R).

| Field | Value | Status | Official source |
| --- | --- | --- | --- |
| Title | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven — 24 cooking functions, dual-speed fan and rotisserie | verified | dp page |
| Department | Home & Kitchen | verified | dp page title |
| Brand | Emeril Lagasse | verified (from title) | search page |
| Capacity | 26 QT | verified (from title) | search page |
| Star rating | 4.3 out of 5 stars | verified | search page |
| Ratings shown | 18.3K | verified — **rounded by Amazon** | search page |
| Exact rating count | ␣ blank | **unverified** (FLAG-04) | review page sign-in walled |
| Current price | $149.99 | verified at 22:33:46Z | search page |
| List price | $209.99 | verified at 22:33:46Z | search page |
| Promotion badge | Early Black Friday Deal | verified (FLAG-02) | search page |
| Lowest other offer | $92.99 (2+ used & new offers) | verified at 22:33:46Z | search page |
| Bought in past month | 4K+ | verified — rounded by Amazon | search page |
| Best Sellers Rank | ␣ blank | **unverified** (FLAG-03) | detail block not retrievable |
| Wattage / model number | ␣ blank | **unverified** (FLAG-10) | not exposed |
| Affiliate tag present | **No** | fails a rule (FLAG-05) | Program Policies §2(b) |

## 4. Product fields — P3, ASIN B08DKYBTPH

Source: [amazon.com/s?k=B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) (qid 1794609454 =
2026-11-13T22:37:34Z) and [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH).

| Field | Value | Status | Official source |
| --- | --- | --- | --- |
| Title | Chefman Air Fryer 8 Qt TurboFry 4-in-1 with 450°F Hi-Fry Option — Bake, Dehydrate, Frozen, XL Nonstick Dishwasher-Safe Basket, Stainless Steel | verified | dp page |
| Department | Home & Kitchen | verified | dp page title |
| Brand | Chefman | verified (from title) | search page |
| Capacity | 8 Qt | verified (from title) | search page |
| Star rating | 4.4 out of 5 stars | verified | search page |
| Ratings shown | 16.8K | verified — **rounded by Amazon** | search page |
| Exact rating count | ␣ blank | **unverified** (FLAG-04) | review page sign-in walled |
| Current price | $79.91 | verified at 22:37:34Z | search page |
| List price | $119.99 | verified at 22:37:34Z | search page |
| Promotion badge | Limited time deal | verified (FLAG-02) | search page |
| Lowest other offer | $49.54 (3+ used & new offers) | verified at 22:37:34Z | search page |
| Bought in past month | 3K+ | verified — rounded by Amazon | search page |
| Best Sellers Rank | ␣ blank | **unverified** (FLAG-03) | detail block not retrievable |
| Wattage / model number | ␣ blank | **unverified** (FLAG-10) | not exposed |
| Affiliate tag present | **No** | fails a rule (FLAG-05) | Program Policies §2(b) |

## 5. Category taxonomy

| Claim | Official source | Outcome |
| --- | --- | --- |
| Small Appliances is a child of Kitchen & Dining, itself a child of Home & Kitchen | [Best Sellers in Kitchen Small Appliances](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Small-Appliances/zgbs/kitchen/289913/) | verified from the breadcrumb |
| Fryers has three children: Air Fryer Ovens, Air Fryers, Deep Fryers | [Best Sellers in Fryers](https://www.amazon.com/Best-Sellers-Home-Kitchen-Fryers/zgbs/home-garden/17659095011/) | verified from the sub-category nav |
| The Air Fryers node is 17659096011 | [Best Sellers in Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) | verified |
| Node 289742 is *Coffee, Tea & Espresso Appliances*, **not** Air Fryers | [Best Sellers node 289742](https://www.amazon.com/Best-Sellers-Home-Kitchen-Air-Fryers/zgbs/home-garden/289742/) | verified — a wrong guess was caught and corrected here |

## 6. Commission rates

| Claim | Official source | Outcome |
| --- | --- | --- |
| Kitchen = 4.50% | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | verified, read from Table 1 |
| Home = 3.00% | same | verified |
| All Other Categories = 4.00% | same | verified |
| Prime free trial / paid membership bounty = $12.00 each | same | verified |
| Payment ≈ 60 days after month end; US minimums $10 / $10 / $100; $15 check fee | same | verified |
| Which rate applies to these ASINs | — | **unresolved** (FLAG-09). Amazon assigns the category internally and does not publish it. Both cases are modelled. |

## 7. Program rules

| Claim | Official source | Outcome |
| --- | --- | --- |
| Operating Agreement is dated October 15, 2025 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | verified from the page header |
| Program Policies are dated April 14, 2026 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | verified from the page header |
| Session = 24 hours; cart order within 89 days; shipped and paid within 180 days | Program Policies §1(b) | verified |
| Prices may only be shown if Amazon-served or API-sourced | Program Policies, Participation Requirements §2(b) | verified — FLAG-01 |
| Tag must appear as a URL parameter | same section | verified — FLAG-05 |
| Limited-time promotion references must be removed when the promotion ends | same section | verified — FLAG-02 |
| No training ML models on Special Links or Program Content without express prior written approval | Participation Requirements §5 | verified — FLAG-16 |
| No Special Links inside browser extensions, plug-ins or similar client software | Participation Requirements §5 | verified |
| Original content required for approval | Participation Requirements §1 | verified — FLAG-13 |
| Program Content must not be altered | Content on your Site §6(a) | verified — FLAG-08 |
| Cookie / pixel / GDPR / ePrivacy disclosure is the associate's responsibility | Responsibility for your Site §3(e) | verified — FLAG-06 |
| Amazon may monitor, record and crawl the site for compliance | Operating Agreement §12 | verified |
| Three qualifying sales within 180 days | [Associates FAQ](https://www.amazon.com/b?ie=UTF8&node=51812349011) | verified, but see FLAG-12 for the exact-quote caveat |
| Required disclosure wording: "As an Amazon Associate I earn from qualifying purchases." | [Associates FAQ](https://www.amazon.com/b?ie=UTF8&node=51812349011) | **read from the FAQ index of that official page — re-copy from the Operating Agreement before publishing** (FLAG-12) |

## 8. FTC disclosure rules

| Claim | Official source | Outcome |
| --- | --- | --- |
| Disclose any financial, employment, personal or family relationship with a brand | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | verified |
| Disclosure must be hard to miss, with the endorsement, in simple language; not on an About page, not at the end, not behind "more", not buried in hashtags | same | verified |
| You cannot talk about experience with a product you have not tried | same | verified |
| You cannot make claims a product's advertiser could not substantiate | same | verified |

## 9. Retrievals that failed

| Attempt | Result | Cost |
| --- | --- | --- |
| `/dp/ASIN` (all three) | HTTP 200 but a "shuffle" landing variant with no extractable detail block | Lost BSR, wattage, model number, full spec table |
| `/gp/aw/d/B0CDY277D3` (mobile) | Same shuffle landing | No additional data |
| `/product-reviews/B0CDY277D3` | Redirected to the Amazon sign-in wall | Lost exact rating counts |
| Best Sellers positions 7+ | Not enumerated | No claim made about absence from the full list |

## 10. Repository review

The repository at the start of this session contained one commit (`ed1a796` "Initial commit") and one
file, `README.md`, whose entire content is `# Zone3`. There were no pre-existing findings, tables,
datasets or code to review, and no other branches. Recorded as FLAG-11.

## 11. Automated checks run on the built site

| Check | Result |
| --- | --- |
| Every external URL is inside the verified allowlist | pass — 43 URLs |
| Every internal `href` / `src` resolves to a produced file | pass — 17 pages, 0 broken |
| Affiliate disclosure banner present on every page | pass — 17/17 |
| No leftover template tokens | pass |
| No Python format-string leaks into output | pass |
| All `data/*.json` files parse | pass |
