# Niche and competition analysis

Session `c4e71983`. Data captured 2026-11-13, 22:33–22:39 UTC from official Amazon pages.

## 1. Niche identification — discovered, not chosen

The platform was asked to identify profitable niches. It did so by resolving the three supplied links
rather than by prediction. All three resolve to Amazon.com air fryers.

| Level | Value | Official source |
| --- | --- | --- |
| Department | Home & Kitchen | product page title |
| L2 | Kitchen & Dining | [Best Sellers breadcrumb](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Small-Appliances/zgbs/kitchen/289913/) |
| L3 | Small Appliances | same |
| L4 | Fryers | [Best Sellers in Fryers](https://www.amazon.com/Best-Sellers-Home-Kitchen-Fryers/zgbs/home-garden/17659095011/) |
| L5 | Air Fryers | [Best Sellers in Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) |

Sibling sub-categories under Fryers: Air Fryer Ovens, Air Fryers, Deep Fryers.

**Correction logged:** the best-seller node `289742` — a plausible guess for Air Fryers — is in fact
*Coffee, Tea & Espresso Appliances*. It was fetched, found wrong, and discarded. The correct node is
`17659096011`.

## 2. The catalogue

| ID | ASIN | Sub-category | Capacity | Price | List | Rating | Ratings shown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | B0CDY277D3 | Dual Basket | 6 Qt (2 × 3 Qt) | $79.93 | $99.99 | 4.2 | 4.8K |
| P2 | B09B7SB46R | Air Fryer Toaster Oven | 26 QT | $149.99 | $209.99 | 4.3 | 18.3K |
| P3 | B08DKYBTPH | Large Capacity | 8 Qt | $79.91 | $119.99 | 4.4 | 16.8K |

Sub-categories are derived from what the official product titles actually say, not from an external
taxonomy.

## 3. Competition — official Best Sellers, ranks 1–6

| Rank | Product | Brand | Capacity | Rating | Ratings | Price |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ninja Air Fryer Pro 5 Qt AF141 | Ninja | 5 Qt | 4.7 | 10,984 | $89.99 |
| 2 | Cosori TurboBlaze 6 Qt | Cosori | 6 Qt | 4.8 | 22,768 | $99.99 |
| 3 | bella Fits-anywhere 4 Qt | bella | 4 Qt | 4.5 | 4,015 | $39.99 |
| 4 | Chefman 4 QT Compact | Chefman | 4 Qt | 4.6 | 7,552 | $57.91 |
| 5 | Cuisinart TOA-55 | Cuisinart | 0.6 cu ft | 4.5 | 126 | $129.95 |
| 6 | Chefman 14-Quart 6-in-1 | Chefman | 14 Qt | 4.3 | 52,301 | $99.95 |

Source: [Best Sellers in Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/).
Rating counts on this page are exact — unlike Amazon search results, which round them.

**Scope limit:** positions 1–6 were captured in full; position 7 partially; 8–100 not enumerated. No
claim is made that any target product is absent from the full list.

## 4. Findings

**a. The gap is satisfaction, not price.** Category leaders rate 4.7 and 4.8. These three rate
4.2–4.4. Meanwhile the $149.99 unit — the most expensive thing on this page — shows the strongest
velocity signal in the catalogue. Buyers are not being deterred by price here.

**b. Brand adjacency is favourable.** The category leader on volume (#6) and two of the top six are
Chefman, which is also the brand of two of the three promoted products. Brand familiarity in the
category helps.

**c. The premium band is thin.** Only one product in the captured top six sits above $130, and it has
just 126 ratings. The $149.99 promoted unit has 18.3K ratings shown. That is the least contested
band and the strongest product within it.

**d. Two products are priced identically.** At $79.91 and $79.93 they are two cents apart, despite
list prices $20 apart. The differentiator is features and ratings, not cost — and P3 (4.4 stars,
16.8K ratings) is objectively the stronger of the two on the captured data. That makes it the natural
"best for most people" pick, with P1 as the "best if you cook two things at once" alternative.

## 5. Pricing

All three products were discounted at capture, two with a *Limited time deal* badge and one with an
*Early Black Friday Deal* badge — consistent with mid-November. Discount depth vs list:

| Product | Price | List | Discount |
| --- | --- | --- | --- |
| B0CDY277D3 | $79.93 | $99.99 | 20% |
| B09B7SB46R | $149.99 | $209.99 | 29% |
| B08DKYBTPH | $79.91 | $119.99 | 33% |

(Discount is calculated from the two captured prices; it is arithmetic, not an Amazon-published figure.)

**Operational consequence:** any price printed on a page will be wrong within days. Combined with
FLAG-01 (hand-captured prices are not permitted) and FLAG-02 (promotion references must be removed
when the promotion ends), this is the single biggest operational risk in the niche.

## 6. Keyword and content direction — explicitly not measured data

**No search-volume figures appear in this project, on purpose.** No official source publishes keyword
volume for Amazon or Google search. Numbers quoted for "air fryer" search volume on third-party blogs
are that vendor's estimate. A fabricated figure in a table is indistinguishable from a measured one,
so the columns that would hold it are empty.

What *can* be said from the official data that was captured:

- **Intent clusters are visible in the official titles.** Capacity ("6 Quart", "26QT", "8 Qt"),
  function count ("4-in-1", "24 cooking functions", "9-in-1") and feature hooks ("Sync Finish",
  "Hi-Fry", "rotisserie") are the exact phrases a buyer sees on Amazon, and they come from an
  official source.
- **The comparison structure is pre-built.** Three products, three tiers, one category — "versus"
  content needs no further product research.
- **Sub-category pages map to distinct jobs to be done.** Dual basket (cook two things at once),
  toaster oven (replace three appliances with one), large capacity (feed more people at once).

Once the site is live, real query data arrives from Google Search Console and Amazon's own reports.
Until then, keyword priority is a hypothesis to test, not data.

## 7. Trend analysis — not yet possible

The brief asks for trending-product identification. Trend requires a time series. This session
produced a single snapshot, and Amazon's Best Sellers pages publish only the current ranking (they
describe themselves as "Our most popular products based on sales. Updated frequently"). Publishing a
trend line from one data point would be fabrication. → **FLAG-18**

The collector described on the Automation Architecture page is what builds that series: an
append-only row per ASIN per scheduled run.
