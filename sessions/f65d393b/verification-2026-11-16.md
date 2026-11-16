# F65 independent verification round — 2026-11-16 (session `f65d393b`)

Every row below was fetched **live by this session on 2026-11-16** using the fetch tool.
The page URL is the source; nothing was taken from a search result, a blog, an aggregator,
or another session's record. Prices, star ratings and review counts that appeared in the
fetched Amazon page text are deliberately **not reproduced here** — they are observed for
verification only and are withheld under Program Policies 2(b) and 6(t).

## A. The three submitted short links

| # | Claim checked (as published in `data/i2/catalog.json`) | Result | Source fetched |
|---|---|---|---|
| A1 | `link.amazon/B04G1MEwY` opens `amazon.com/dp/B0CDY277D3`, title "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black" | **Confirmed** — final URL `…/dp/B0CDY277D3?…&plpRedirect=mhFallback`; served title matches verbatim | https://link.amazon/B04G1MEwY |
| A2 | `link.amazon/B02NbDxp3` opens `amazon.com/dp/B09B7SB46R`, title "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included" | **Confirmed** — final URL `…/dp/B09B7SB46R?…`; served title matches verbatim (same wording as the 2026-11-15 capture) | https://link.amazon/B02NbDxp3 |
| A3 | `link.amazon/B00hJ57DV` opens `amazon.com/dp/B08DKYBTPH`, title "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel" | **Confirmed** — final URL `…/dp/B08DKYBTPH?…`; served title matches verbatim | https://link.amazon/B00hJ57DV |
| A4 | Destination breadcrumb is `Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers` (node `17659096011`) on all three listings | **Confirmed on all three** — breadcrumb links read on each fetched page | same three fetches |
| A5 | No Associates `tag=` parameter on any destination URL | **Confirmed** — destination URLs carry only `srctok`, `channelId`, `lv`, `plpRedirect`, `th`; no `tag=` | same three fetches |
| A6 | `title_facts` for P1 ("Sync Finish", "Hi-Fry", "Auto Shutoff", "Easy View Windows", "two 3Qt baskets", "6 Quart") are present in the listing title | **Confirmed** — all six phrases appear in the served title | https://link.amazon/B04G1MEwY |
| A7 | `title_facts` for P2 ("26QT", "French-door", "24 one-touch presets", "convection", "six cooking accessories") | **Confirmed** — all five appear in the served title | https://link.amazon/B02NbDxp3 |
| A8 | `title_facts` for P3 ("8 Qt", "4-in-1: bake/dehydrate/frozen", "450°F Hi-Fry", "XL nonstick dishwasher-safe basket", "stainless steel") | **Confirmed** — all five appear in the served title | https://link.amazon/B00hJ57DV |

Identity caveat unchanged: the destinations are **observed**, not established as the
submitter's intended products (FLG-001/002/027; Q2 on the decisions page). The nine-character
tokens are not ASINs — see A10.

## B. Load-bearing official policy text

| # | Claim checked | Result (page's own wording, read 2026-11-16) | Source fetched |
|---|---|---|---|
| B1 | Operating Agreement header is current | **Confirmed** — "Updated: October 15, 2025" | https://affiliate-program.amazon.com/help/operating/agreement |
| B2 | OA §5 disclosure sentence, verbatim | **Confirmed** — "As an Amazon Associate I earn from qualifying purchases." (§5 "Identifying Yourself as an Associate") | same |
| B3 | OA §6: violating §5 is a material breach | **Confirmed** — "any violation of Section 5 and as specified in the Program Policies will be deemed a material breach of this Agreement." | same |
| B4 | OA opening paragraph contains the compensated-review prohibition | **Confirmed** — "…including the prohibition of customer reviews that are created, edited, or removed in exchange for compensation." | same |
| B5 | PP 2(b): tag required in every Special Link URL | **Confirmed** — "you must include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site." | https://affiliate-program.amazon.com/help/operating/policies |
| B6 | PP 2(b): price/availability display rule | **Confirmed** — "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…" | same |
| B7 | PP 2(b): no dynamic per-visitor sub-tags | **Confirmed** — "Under no circumstances may you associate any sub-tag, other ID or reporting … with a specific end user of your Site…" | same |
| B8 | PP 6(s): no artificial clicks | **Confirmed** — "You will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site, whether by way of a robot or software program or otherwise." | same |
| B9 | PP 6(t): reviews/star ratings only via Creators API or PA API | **Confirmed** — "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API…" | same |
| B10 | PP 6(v)/6(w): no cloaking, no unclear shortening | **Confirmed verbatim** — 6(v) "…cloak, hide, spoof, or otherwise obscure the URL…" and 6(w) "…link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site." | same |
| B11 | PP 6(y): no price tracking/alerting | **Confirmed** — "Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality." | same |
| B12 | PP 6(z): no non-Amazon products | **Confirmed** — "…advertise or promote any products that are offered on any site that is not an Amazon Site…" | same |
| B13 | Associates Program is free; no authorized paid set-up services | **Confirmed** — "The Associates Program is free to join… We have never authorized any business to provide paid set-up or consulting services to our associates…" | same |
| B14 | Standard Commission Table 1 renders publicly; Kitchen 4.50 %, All Other Categories 4.00 %, Luxury Beauty 10.00 % | **Confirmed** — full table read row for row | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ |
| B15 | Bounty table rows $12.00 / $2.00 / $5.00 / $0.25 | **Confirmed** — Prime trials/memberships $12.00, Prime Video Free Trial $2.00, First Stream $5.00, Stream $0.25 | same |
| B16 | Creators API `GetItems`: `itemIdType` defaults to `ASIN`; examples are 10 characters | **Confirmed** — Default Value `ASIN`; example `"itemIds" : ["B0199980K4" , "B000HZD168"]` | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items |
| B17 | ASIN rule: "10-Character alphanumeric unique identifier assigned by Amazon" | **Confirmed verbatim** — ItemIdType Parameter table: "Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." | same |
| B18 | FTC Disclosures 101: material-connection wording, placement, date | **Confirmed** — "financial, employment, personal, or family relationship"; "Place it so it's hard to miss"; "You can't talk about your experience with a product you haven't tried."; page dated **November 2019** | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |

## C. Deliberately not verified (and why)

| Item | Reason |
|---|---|
| Any price, star rating, review count, "bought in past month" figure as a product fact | Program Policies 2(b) and 6(t) permit those on a site only when Amazon serves them through the link or they come from Creators API/PA API. Observed values in this session's fetches are recorded nowhere. |
| Per-product commission rate | The listing's rate-card category and the account's own rates are not established (FLG-021/FLG-013). Table 1 is a category reference only. |
| Whether the destinations are the submitter's intended products | Needs owner input (FLG-002/027). |
| Whether `link.amazon` is a "Redirecting Link" under CIS 2(e) | Needs a logged-in Associates account test (FLG-003). |
| Live clicks, conversions, revenue | No Associates account or tag configured (FLG-010/FLG-012). |

**Result: every claim checked matched the official page. No value was inferred or filled;
unverifiable cells remain blank on the site.**
