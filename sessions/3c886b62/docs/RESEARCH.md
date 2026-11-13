# Research — how the three supplied links were resolved

The brief supplied three `link.amazon` short links. This document records how each was
resolved to a real Amazon product and where every subsequent value came from.

## Resolution

| Supplied link | Code | Length | Resolves to (ASIN) | Product | Department |
| --- | --- | --- | --- | --- | --- |
| <https://link.amazon/B04G1MEwY> | `B04G1MEwY` | 9 | [`B0CDY277D3`](https://www.amazon.com/dp/B0CDY277D3) | CHEFMAN | Home & Kitchen |
| <https://link.amazon/B02NbDxp3> | `B02NbDxp3` | 9 | [`B09B7SB46R`](https://www.amazon.com/dp/B09B7SB46R) | Emeril Lagasse | Home & Kitchen |
| <https://link.amazon/B00hJ57DV> | `B00hJ57DV` | 9 | [`B08DKYBTPH`](https://www.amazon.com/dp/B08DKYBTPH) | Chefman | Home & Kitchen |

## Two irregularities in the links themselves

1. **The codes are not ASINs.** Each is 9 characters and mixed case. An Amazon ASIN is 10
   characters and does not use lowercase. They are opaque short-link slugs that happen to
   begin with `B0`. Recorded as [F04](FLAGGED.md).
2. **`link.amazon` is not a documented Amazon short domain.** The links do resolve today,
   but no official page was found documenting `link.amazon` as an Amazon-operated shortener;
   Amazon's commonly documented shortener is `amzn.to`. Recorded as [F05](FLAGGED.md).

Both were handled the same way: the short links are used only as the provenance record of what
was supplied. Every product fact comes from the resolved `amazon.com` page, and every outbound
link on the site points at the canonical `/dp/<ASIN>` URL.

## Stability check

The first link was requested twice, at different points in the work. Both requests returned
`B0CDY277D3`. The redirect is therefore stable, not random or rotating.

## How the values were captured

Amazon renders the price and rating payload of a product detail page with JavaScript. A static
read of `/dp/<ASIN>` returns the page shell, the `<title>` and the footer, but not the price.
The `<title>` was still useful: it carries the full product title, the brand and the department
(the segment after the final colon).

Amazon's own search-results rendering of the same ASIN at `/s?k=<ASIN>` returns, for the single
matching product, the current price, the list price, any per-count unit price, the promotion
badge, the star rating, the ratings count, the *bought in the past month* demand signal, the
lowest alternative offer, and the canonical listing URL. That is an official Amazon page, so
those values were captured from it and it is cited on every row.

Two endpoints were tried and rejected: `/gp/aod/ajax/...` returns a 404, and `/product-reviews/
<ASIN>` redirects to the sign-in page. Neither yielded data, so the fields they would have
supplied are left blank.

## Verified values

| Product | Price | List | Rating | Ratings | Bought past month | Promotion | Lowest other offer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHEFMAN | $79.93 | $99.99 | 4.2 / 5 | 4.8K | 1K+ bought in past month | Limited time deal | $57.45 |
| Emeril Lagasse | $149.99 | $209.99 | 4.3 / 5 | 18.3K | 4K+ bought in past month | Early Black Friday Deal | $92.99 |
| Chefman | $79.91 | $119.99 | 4.4 / 5 | 16.8K | 3K+ bought in past month | Limited time deal | $49.54 |

Sources S1-S6 are listed with links in [VERIFICATION.md](VERIFICATION.md).
Full detail in [VERIFICATION.md](VERIFICATION.md).

