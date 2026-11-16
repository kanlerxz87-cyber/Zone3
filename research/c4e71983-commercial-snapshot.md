# Session `c4e71983` — commercial snapshot and competitor benchmark

Captured 2026-11-13, 22:33–22:37 UTC, from official Amazon.com pages. Machine-readable copies:
`data/c4e71983-commercial-snapshot.json` and `data/c4e71983-competitors.json`.

> **Read this first.** These prices were captured by hand from Amazon search-result pages. Amazon's
> Program Policies (Participation Requirements §2(b)) permit a site to show prices only if Amazon
> serves the link, or if the price came from Creators API or PA API. **These are evidence, not
> publishable figures.** They exist to fill the gap recorded in `main`'s FLG-004, not to be rendered
> on a live page. See `c4e71983-FLG-01`.

## 1. Why this exists

`main`'s FLG-004 records price, rating and review count as unverified for all three products, and
session `7f84fea4`'s verification note states that "prices and ratings are not present in the text
returned."

They are not present on the `/dp/` pages — those returned a "shuffle" landing variant. They **are**
present on Amazon search-result pages. Querying `amazon.com/s?k=<ASIN>` returns the listing with the
full commercial block. That is the route used here.

## 2. Captured values

| Product | Rating | Ratings (shown) | Price | List | Discount | Badge | Lowest other offer | Bought past month | Captured (UTC) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0CDY277D3 — Chefman 6 Qt dual basket | Withheld | Withheld | Withheld | Withheld | 20% | Withheld | Withheld (2+ used & new) | Withheld | 22:37:14Z |
| B09B7SB46R — Emeril Lagasse 26 QT | Withheld | Withheld | Withheld | Withheld | 29% | Withheld | Withheld (2+ used & new) | Withheld | 22:33:46Z |
| B08DKYBTPH — Chefman 8 Qt TurboFry | Withheld | Withheld | Withheld | Withheld | 33% | Withheld | Withheld (3+ used & new) | Withheld | 22:37:34Z |

Discount is arithmetic from the two captured prices — it is not an Amazon-published figure.
Sources: C4E-S07, C4E-S08, C4E-S09.

## 3. Timestamp method

Amazon returns a `qid` parameter with every search-result page. It is a Unix epoch value, so decoding
it yields the true request time rather than the time this document was written:

| `qid` | Decodes to |
| --- | --- |
| 1794609434 | 2026-11-13T22:37:14Z |
| 1794609226 | 2026-11-13T22:33:46Z |
| 1794609454 | 2026-11-13T22:37:34Z |

Any future collector should record this. It makes a snapshot auditable: a reviewer can tell exactly
when a value was observed, which matters for the price-staleness problem in §6.

## 4. Competitor benchmark — official Best Sellers in Air Fryers

Node `17659096011`. Source C4E-S13. Rating counts here are **exact** (Best Sellers print full counts;
search results round them).

| Rank | Product | Brand | Capacity | Rating | Ratings | Price |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ninja Air Fryer Pro 5 Qt AF141 | Ninja | 5 Qt | 4.7 | Withheld | Withheld |
| 2 | Cosori TurboBlaze 6 Qt | Cosori | 6 Qt | 4.8 | Withheld | Withheld |
| 3 | bella Fits-anywhere 4 Qt | bella | 4 Qt | 4.5 | Withheld | Withheld |
| 4 | Chefman 4 QT Compact | Chefman | 4 Qt | 4.6 | Withheld | Withheld |
| 5 | Cuisinart TOA-55 | Cuisinart | 0.6 cu ft | 4.5 | 126 | Withheld |
| 6 | Chefman 14-Quart 6-in-1 | Chefman | 14 Qt | 4.3 | Withheld | Withheld |

**Scope limit:** positions 1–6 captured in full, 7 partially, 8–100 not enumerated. No claim is made
that any of the three promoted products is absent from the full list.

## 5. What the numbers say

**The gap is satisfaction, not price.** The category leaders rate 4.7 and 4.8; the three promoted
products rate within a narrow band. Yet the premium unit — the most expensive thing in the comparison —
shows the strongest velocity signal of the three. Buyers in this category
are not being deterred by price.

**Brand adjacency is favourable.** The category leader on volume is a
Chefman, and two of the top six are Chefman. Two of the three promoted products are Chefman.

**The premium band is thin.** Only one product in the captured top six sits above Withheld, and it has
a thin sample. The promoted premium unit has a large rating count shown. That is the least contested band in
the set and the strongest product within it.

**Two products are priced almost identically.** Despite list
prices apart. On the captured data the 8 Qt unit is the stronger of
the two, which makes it the natural "best for most people" pick with the dual-basket unit as the
"best if you cook two things at once" alternative.

**Commission consequence.** At the published Kitchen rate of 4.50%, one qualifying unit is worth
a thin per-unit commission for either Chefman and a higher figure for the Emeril Lagasse unit. The premium product is
worth nearly twice as much per conversion, and it is also the fastest-moving. That alignment — the
highest-value product is also the most popular one — is unusual and should drive placement.

Prime bounties pay $12.00 per successful trial or membership, which is more than three air fryer
sales at the Kitchen rate. Prime is a material part of the model, not an afterthought.

## 6. Volatility — the operational risk

All three products were discounted at capture and all three carried promotion badges at capture time. That is consistent with mid-November, and it means any printed price
is wrong within days.

Two rules bite at once:

1. Prices may only be shown if Amazon-served or API-sourced (§2(b)) — `c4e71983-FLG-01`.
2. References to limited-time promotions must be removed as soon as the promotion ends (§2(b)) —
   `c4e71983-FLG-02`.

A static page cannot satisfy the second. The only durable fixes are a live API feed, an
Amazon-served widget, or not showing prices at all.

## 7. What remains unverified

Best-seller rank, availability, wattage, model number, dimensions, warranty, and the exact rating
counts. These are left null in the JSON rather than estimated.

## 8. Trend analysis is not yet possible

The brief asks for trending-product identification. Trend needs a time series; this session produced
one snapshot, and Amazon's Best Sellers pages publish only the current ranking. Publishing a trend
line from a single data point would be fabrication. → `c4e71983-FLG-18`

The fix is a scheduled collector: one immutable row per ASIN per run. After eight to twelve weeks
that becomes a real series.
