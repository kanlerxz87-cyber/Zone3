# Verification record — session `9ed0552a`, 2026-11-20

This record covers the five listing pages added by 9E-T2. It is deliberately narrow: it records
**what each new page asserts, where the assertion already lived, and what was not checked today.**

## 1. What this session could and could not fetch

The sandbox's outbound network reached `github.com`, `codeload.github.com`, `api.github.com`,
`registry.npmjs.org`, `pypi.org` and `files.pythonhosted.org` only. **`amazon.com`,
`link.amazon`, `affiliate-program.amazon.com`, `ftc.gov`, `developers.google.com`,
`foodsafety.gov` and `fsis.usda.gov` were not reachable from this session and were not
requested.** No page in this session claims a fresh read of any of them.

Consequence, stated on the pages themselves:

- Each listing page prints **"Listing checked 19 Nov 2026"**, which is the `observed_on` value in
  `data/publication.json`, written by the sessions that did open the pages (`b580d790`,
  `d3493182`, `0a48cfda`, `1c072a7a`).
- No price, star rating, review count, availability, rank, commission or performance value is
  printed, because none is held in the register and none may be inferred.
- Published on the Flagged-for-review page as **9E-F02** (open — limitation stated on the page).

## 2. Claim-by-claim provenance for the new pages

Every rendered sentence is generated from a register field. The table maps the value to the
field and to the official URL recorded with it. **The dates are the register's dates, not
today's.**

| Value on the page | Register field | Official URL recorded with it | Recorded |
|---|---|---|---|
| Listing title wording, brand, format, features | `products[].listing_title`, `brand`, `format_text`, `features` | `https://www.amazon.com/dp/<observed_asin>` | 2026-11-19 |
| Observed ASIN | `products[].observed_asin` | same | 2026-11-19 |
| Exterior size and capacity as listed (SHOP-01–03) | `products[].listing_dimensions.as_listed`, `.capacity_as_listed` | same | 2026-11-19 |
| Capacity mismatch note (SHOP-01, SHOP-02) | `products[].listing_dimensions.capacity_note` | same | 2026-11-19 |
| "No dimensions published" (SHOP-04, SHOP-05) | `products[].listing_dimensions.status` / `.scope` | same | 2026-11-19 |
| Care wording in the title (SHOP-01, SHOP-03) | `products[].cleanup_title_wording` | same | 2026-11-19 |
| "Fits you if / Not for you if / the question" | `DECISION[...]` in `tools/build_publication.py` | editorial, derived from format wording | unchanged from 2026-11-19 |
| Observation scope | `products[].observation_scope` | same | 2026-11-19 |
| Disclosure sentence | `chrome.DISCLOSURE` | `https://affiliate-program.amazon.com/help/operating/agreement` (S01, §5) | 2026-11-19 |
| Sponsored-link rule (`rel="sponsored"`) | S90 | `https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links` | 2026-11-19 |
| Associates tag on product links | `data/shop/config.json → associates_tracking_id` | `https://affiliate-program.amazon.com/help/operating/policies` §2(b) | 2026-11-19 |

The five observed listing URLs the pages link to, for manual review:

| Product | Observed ASIN | Official listing URL | Supplied link (unchanged) |
|---|---|---|---|
| SHOP-01 Chefman 6-quart dual-basket | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | https://link.amazon/B04G1MEwY |
| SHOP-02 Emeril Lagasse 26QT French-door | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | https://link.amazon/B02NbDxp3 |
| SHOP-03 Chefman TurboFry 8 Qt | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | https://link.amazon/B00hJ57DV |
| SHOP-04 ThermoMaven digital | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | https://link.amazon/B0c8moW59 |
| SHOP-05 CHEF iQ Sense wireless | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | https://link.amazon/B0f3GKalj |

## 3. What was verified mechanically today

Run on the final tree, after `python3 tools/publish.py` (51 commands, 0 failed, twice,
byte-identical rebuild):

| Gate | Output |
|---|---|
| `sessions/9ed0552a/test_product_pages.py` | PASS — 5 listing pages present, indexable, sourced, tagged, sponsored and reachable |
| `sessions/9ed0552a/test_product_pages.py --self-test` | PASS — 6 deliberately broken copies each caught (unsponsored link, untagged link, a price, removed disclosure, second heading, unconfirmed-intent text erased) |
| `tools/check_publication.py` | PASS — 129 current HTML pages, 25 indexable URLs, 11 feed entries |
| `scripts/build_sitemap.py --check` | PASS — 25 indexable pages; no noindex pages or extras |
| `tools/attach_tag.py --check` | PASS — 1,703 product links carry `tag=shopnow047c-20`; no foreign tags |
| `scripts/check_all_links.py` | PASS — 216 HTML pages, 354 distinct external URLs, 0 errors |
| `tools/verify_site.py` | PASS — 170 pages, 2,748 table rows, V1–V7 |
| `scripts/check_site.py` | OK — 42 pages, 5 products, 90 sources, 184 flags |
| `tools/link_report.py --strict` | PASS — no dangling source/flag references |
| `sessions/5d460e79/test_counts.py` | PASS — no typed numerals in the generator's prose |

Structural gates prove structure, not truth. They confirm that each page carries a visible
disclosure, a tagged and sponsored outbound link, one heading, one canonical URL, a unique title
and description, the observed ASIN, an explicit blank for the intended fields, and inbound links
from three other pages. They do **not** confirm that an Amazon listing still says what it said on
19 November.

## 4. Blanks left blank

- `intended_asin`, `official_listing_url`, `intent_confirmed_on`, `intent_confirmation_source`
  remain `""` for all five products (FLG-002, FLG-003, P26-Q1, P26-Q2).
- `price`, `rating`, `review_count`, `tested_performance` remain `null`.
- Dimensions for SHOP-04 and SHOP-05 remain empty, because the listings' detail tables did not
  print them when read on 2026-11-19.
- No commission rate is attached to any product.

## 5. Manual review links

- Amazon Associates Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement
- Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- FTC, Disclosures 101: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Google, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- Google, write high quality reviews: https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews
- The five listing URLs in the table above.

Nothing in this record is a certification by Amazon, the FTC or Google.
