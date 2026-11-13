# Verification Log

Every value on this site, line by line, with the official source that supports it.

**Rule applied:** a value is shown only if it was read from a page published by Amazon or
the U.S. Federal Trade Commission. Anything that could not be read from such a page is left
blank and listed here as unverified. Nothing is inferred, interpolated or averaged, and
nothing comes from a third-party blog, price tracker, review aggregator or model memory.

Data captured **2026-11-13** from amazon.com (US). Prices in USD.

Machine-readable version: [`data/products.json`](../data/products.json).
On the site: [Verification Log](../verification.html).

## Sources

| ID | Source | Publisher | Official | Last updated | Used for |
| --- | --- | --- | --- | --- | --- |
| `S1` | [Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | Amazon.com, Inc. | yes | — | P1 title, ASIN, brand, department, canonical URL |
| `S2` | [Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Amazon.com, Inc. | yes | — | P1 price, list price, unit price, deal badge, rating, ratings count, demand signal, other offers, listing URL |
| `S3` | [Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | Amazon.com, Inc. | yes | — | P2 title, ASIN, brand, department, canonical URL |
| `S4` | [Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | Amazon.com, Inc. | yes | — | P2 feature line, price, list price, deal badge, rating, ratings count, demand signal, other offers, listing URL |
| `S5` | [Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | Amazon.com, Inc. | yes | — | P3 title, ASIN, brand, department, canonical URL |
| `S6` | [Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | Amazon.com, Inc. | yes | — | P3 variants, price, list price, deal badge, rating, ratings count, demand signal, other offers, listing URL |
| `S7` | [Amazon Associates — Associates Program Standard Commission Income Statement (Table 1)](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | Amazon.com, Inc. (Amazon Associates Central) | yes | — | Fixed standard commission income rates by product category; bounty event rates |
| `S8` | [Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) | Amazon.com, Inc. (Amazon Associates Central) | yes | April 14, 2026 | Qualifying Purchase definition, Session windows, Qualifying Revenue definition, disqualified purchases |
| `S9` | [Amazon Associates — Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Amazon.com, Inc. (Amazon Associates Central) | yes | October 15, 2025 | Program terms, compliance and warranty obligations, incorporated Program Policies |
| `S10` | [FTC — Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | U.S. Federal Trade Commission | yes | November 2019 | Disclosure of material connection; placement and wording of disclosures |
| `S11` | [Amazon US trademark list (referenced by S8 section 2(c) on prohibited paid search placements)](https://www.amazon.com/gp/help/customer/display.html/?nodeId=200738910/) | Amazon.com, Inc. | yes | — | Context for the prohibited-paid-search disqualification |
| `S12` | [Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) | Supplied by project owner | no (supplied entry point) | — | Entry point only. The redirect target (S1/S3/S5) is the verified source for all product data. |

## P1 — CHEFMAN (`B0CDY277D3`)

- Supplied short link: <https://link.amazon/B04G1MEwY> (code `B04G1MEwY`)
- Canonical Amazon page: <https://www.amazon.com/dp/B0CDY277D3>
- Amazon listing URL: <https://www.amazon.com/CHEFMAN-Windows-Independent-Nonstick-Dishwasher/dp/B0CDY277D3>
- On the site: [B0CDY277D3](../product-chefman-6qt-dual-basket-air-fryer.html)

| Field | Value | Status | Source | Note |
| --- | --- | --- | --- | --- |
| `short_link_code` | B04G1MEwY | verified | [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) | Opaque short-link slug, NOT an ASIN (9 characters; ASINs are 10). |
| `asin` | B0CDY277D3 | verified | [S1 — Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | Resolved by following the HTTP redirect from the short link to /dp/B0CDY277D3. |
| `title` | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | verified | [S1 — Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | Read from the amazon.com page <title>. |
| `brand_from_title` | CHEFMAN | verified | [S1 — Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | Brand token as it appears in the official product title. |
| `department` | Home & Kitchen | verified | [S1 — Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | Trailing department segment of the amazon.com page <title> after the colon. |
| `canonical_url` | https://www.amazon.com/dp/B0CDY277D3 | verified | [S1 — Amazon product page — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)](https://www.amazon.com/dp/B0CDY277D3) | — |
| `amazon_listing_url` | https://www.amazon.com/CHEFMAN-Windows-Independent-Nonstick-Dishwasher/dp/B0CDY277D3 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | — |
| `current_price` | 79.93 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Shown as $79.93 on Amazon's search-results rendering of this ASIN. |
| `list_price` | 99.99 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Shown as 'List: $99.99'. |
| `unit_price` | 39.97 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Shown as '($39.97/count)'. |
| `deal_badge` | Limited time deal | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | — |
| `other_offers_low` | 57.45 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Lowest 'More Buying Choices' price shown; '(2+ used & new offers)'. |
| `rating` | 4.20 | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Shown as '4.2 out of 5 stars'. |
| `ratings_count_display` | 4.8K | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | Amazon's rounded display value, not an exact count. |
| `demand_signal` | 1K+ bought in past month | verified | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | — |
| `best_sellers_rank` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon serves BSR via JavaScript on the detail page; not readable from an official static render. Left blank by rule. |
| `associates_commission_category` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon does not publish the commission category for an individual ASIN. Candidates on the official rate table (S7) are 'Kitchen' 4.50% and 'Home' 3.00%. |
| `review_sentiment_breakdown` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon's star histogram and review text are served via JavaScript / behind sign-in. Left blank by rule. |
| `clicks` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports clicks only inside Associates Central. |
| `conversions` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports conversions only inside Associates Central. |
| `associates_tag` | *(blank — unverified)* | **unverified** | _no official source_ | No Amazon Associates tag exists in this repository. Links are untagged. |

## P2 — Emeril Lagasse (`B09B7SB46R`)

- Supplied short link: <https://link.amazon/B02NbDxp3> (code `B02NbDxp3`)
- Canonical Amazon page: <https://www.amazon.com/dp/B09B7SB46R>
- Amazon listing URL: <https://www.amazon.com/Emeril-Multi-Function-functions-dual-speed-rotisserie/dp/B09B7SB46R>
- On the site: [B09B7SB46R](../product-emeril-lagasse-26qt-french-door-air-fryer-oven.html)

| Field | Value | Status | Source | Note |
| --- | --- | --- | --- | --- |
| `short_link_code` | B02NbDxp3 | verified | [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) | Opaque short-link slug, NOT an ASIN (9 characters; ASINs are 10). |
| `asin` | B09B7SB46R | verified | [S3 — Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | Resolved by following the HTTP redirect from the short link to /dp/B09B7SB46R. |
| `title` | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | verified | [S3 — Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | Read from the amazon.com page <title>. |
| `title_feature_line` | 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | Feature line rendered by Amazon on the search-results listing for this ASIN. |
| `brand_from_title` | Emeril Lagasse | verified | [S3 — Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | — |
| `department` | Home & Kitchen | verified | [S3 — Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | — |
| `canonical_url` | https://www.amazon.com/dp/B09B7SB46R | verified | [S3 — Amazon product page — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (B09B7SB46R)](https://www.amazon.com/dp/B09B7SB46R) | — |
| `amazon_listing_url` | https://www.amazon.com/Emeril-Multi-Function-functions-dual-speed-rotisserie/dp/B09B7SB46R | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | — |
| `current_price` | 149.99 | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | — |
| `list_price` | 209.99 | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | Shown as 'List: $209.99'. |
| `unit_price` | *(blank — unverified)* | **unverified** | _no official source_ | No per-count unit price was displayed for this ASIN. |
| `deal_badge` | Early Black Friday Deal | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | — |
| `other_offers_low` | 92.99 | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | Lowest 'More Buying Choices' price shown; '(2+ used & new offers)'. |
| `rating` | 4.30 | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | — |
| `ratings_count_display` | 18.3K | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | Amazon's rounded display value, not an exact count. |
| `demand_signal` | 4K+ bought in past month | verified | [S4 — Amazon search results for B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | — |
| `best_sellers_rank` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon serves BSR via JavaScript on the detail page; not readable from an official static render. Left blank by rule. |
| `associates_commission_category` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon does not publish the commission category for an individual ASIN. Candidates on the official rate table (S7) are 'Kitchen' 4.50% and 'Home' 3.00%. |
| `review_sentiment_breakdown` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon's star histogram and review text are served via JavaScript / behind sign-in. Left blank by rule. |
| `clicks` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports clicks only inside Associates Central. |
| `conversions` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports conversions only inside Associates Central. |
| `associates_tag` | *(blank — unverified)* | **unverified** | _no official source_ | No Amazon Associates tag exists in this repository. Links are untagged. |

## P3 — Chefman (`B08DKYBTPH`)

- Supplied short link: <https://link.amazon/B00hJ57DV> (code `B00hJ57DV`)
- Canonical Amazon page: <https://www.amazon.com/dp/B08DKYBTPH>
- Amazon listing URL: <https://www.amazon.com/Chefman-TurboFry-Air-Fryer-Dishwasher/dp/B08DKYBTPH>
- On the site: [B08DKYBTPH](../product-chefman-8qt-turbofry-air-fryer.html)

| Field | Value | Status | Source | Note |
| --- | --- | --- | --- | --- |
| `short_link_code` | B00hJ57DV | verified | [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) | Opaque short-link slug, NOT an ASIN (9 characters; ASINs are 10). |
| `asin` | B08DKYBTPH | verified | [S5 — Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | Resolved by following the HTTP redirect from the short link to /dp/B08DKYBTPH. |
| `title` | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel | verified | [S5 — Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | — |
| `variants` | +1 other color/pattern | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `brand_from_title` | Chefman | verified | [S5 — Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | — |
| `department` | Home & Kitchen | verified | [S5 — Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | — |
| `canonical_url` | https://www.amazon.com/dp/B08DKYBTPH | verified | [S5 — Amazon product page — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (B08DKYBTPH)](https://www.amazon.com/dp/B08DKYBTPH) | — |
| `amazon_listing_url` | https://www.amazon.com/Chefman-TurboFry-Air-Fryer-Dishwasher/dp/B08DKYBTPH | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `current_price` | 79.91 | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `list_price` | 119.99 | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | Shown as 'List: $119.99'. |
| `unit_price` | *(blank — unverified)* | **unverified** | _no official source_ | No per-count unit price was displayed for this ASIN. |
| `deal_badge` | Limited time deal | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `other_offers_low` | 49.54 | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | Lowest 'More Buying Choices' price shown; '(3+ used & new offers)'. |
| `rating` | 4.40 | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `ratings_count_display` | 16.8K | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | Amazon's rounded display value, not an exact count. |
| `demand_signal` | 3K+ bought in past month | verified | [S6 — Amazon search results for B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | — |
| `best_sellers_rank` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon serves BSR via JavaScript on the detail page; not readable from an official static render. Left blank by rule. |
| `associates_commission_category` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon does not publish the commission category for an individual ASIN. Candidates on the official rate table (S7) are 'Kitchen' 4.50% and 'Home' 3.00%. |
| `review_sentiment_breakdown` | *(blank — unverified)* | **unverified** | _no official source_ | Amazon's star histogram and review text are served via JavaScript / behind sign-in. Left blank by rule. |
| `clicks` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports clicks only inside Associates Central. |
| `conversions` | *(blank — unverified)* | **unverified** | _no official source_ | No Associates account is connected; Amazon reports conversions only inside Associates Central. |
| `associates_tag` | *(blank — unverified)* | **unverified** | _no official source_ | No Amazon Associates tag exists in this repository. Links are untagged. |

## Totals

- 65 field checks across 3 products.
- 45 verified, 20 left blank as unverified.

## What was checked, and how

1. Each `link.amazon/<code>` short link was requested and the HTTP redirect followed to its
   destination on `amazon.com`. The destination ASIN was read from the resolved URL and
   confirmed against the product title on that page.
2. The first link was resolved twice, at different points in the work, and returned the same
   ASIN both times. That rules out a random or rotating redirect.
3. Amazon renders the price and rating payload of a product detail page with JavaScript, so a
   static read of `/dp/<ASIN>` returns the page shell but not the price. Amazon's own
   search-results rendering of the same ASIN at `/s?k=<ASIN>` does return price, list price,
   promotion badge, star rating, ratings count, the *bought in the past month* signal and the
   lowest alternative offer, for the one matching product. That is an official Amazon page and
   is cited as such.
4. Every internal link was checked by [`tools/check_links.py`](../tools/check_links.py), which
   also enforces that every row of every table marked `data-verify-source` carries a source cell.

