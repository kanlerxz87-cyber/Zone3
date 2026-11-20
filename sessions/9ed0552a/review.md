# Session `9ed0552a` — listing notes: a page per product

Branch `arena/9ed0552a-zone3`, base `deb67e5` (main after PR #211). 2026-11-20 UTC.

## What the reader got

Before this session the canonical shop had **no page for an individual listing**. Five products
existed as cards inside `shop/air-fryers/`, `shop/meat-thermometers/` and the comparison table, so
every product-intent URL was category-level. The retained `marketing/product-*.html` pages cover
three of the five listings, carry `noindex,follow` and use earlier chrome; they are a record of an
earlier pass, not the current shop.

Now each registered listing has its own page:

| Page | Listing | Observed ASIN |
|---|---|---|
| `/shop/air-fryers/chefman-6-quart-dual-basket-air-fryer.html` | SHOP-01 | B0CDY277D3 |
| `/shop/air-fryers/emeril-lagasse-26qt-french-door-air-fryer-oven.html` | SHOP-02 | B09B7SB46R |
| `/shop/air-fryers/chefman-turbofry-8-qt-air-fryer.html` | SHOP-03 | B08DKYBTPH |
| `/shop/meat-thermometers/thermomaven-digital-meat-thermometer.html` | SHOP-04 | B0DHZTCNR5 |
| `/shop/meat-thermometers/chef-iq-sense-wireless-meat-thermometer.html` | SHOP-05 | B0DZFD6R9Z |

Each page follows the order a buyer uses: the short answer, what the listing itself names
(format, features, care wording, listed size), where it fits and what it does not settle, four
questions to take to the model's own manual, a sponsored link to the exact listing this page
records, and the register record underneath. It reads as a page, not a row.

## How it is built

- `data/publication.json → products[].slug` and `products[].page` carry the URL slug, page
  title, meta description, short answer, four questions and the read-next guides.
- `tools/build_publication.py → product_page()` renders the page from the **same record** as the
  product card. No value is introduced that the register does not already hold with a date.
- `outputs()` emits one page per product and adds it to the local search index; the five URLs
  were added to `indexable_pages`, so `publish_pass` marks them `index,follow`, `build_sitemap`
  lists them, and `check_publication` requires the sitemap and the robots policy to agree.
- Internal links: front-page teasers ("Read the listing note"), category card headings and a new
  text link, the comparison table row headings, the guide shortlist tables, and sibling links in
  each page's aside.
- `assets/publication.css` gains three small rules for the gaps list and the sibling block.

Nothing about the earlier editions was deleted or rewritten.

## The gate

`sessions/9ed0552a/test_product_pages.py` checks, for every registered listing: the page exists
and is indexable, carries the shared masthead with the disclosure above `<main>` and in the
footer, exactly one `<h1>`, one canonical URL, a unique title and description inside the length
range, every Amazon link tagged and `rel="sponsored"`, no price/rating/review-count/test claim,
the observed ASIN printed, the intended fields still blank, and inbound links from the front
page, its category page and the comparison table, plus presence in `sitemap.xml` and the search
index. `--self-test` feeds six deliberately broken copies through the same rules and fails if any
one of them passes. Both lines are wired into `tools/publish.py`, and both were proved to fail
when the defect is reintroduced.

## Release evidence (final tree)

| Gate | Result |
|---|---|
| `python3 tools/publish.py` | **51/51 commands, 0 failed**, run three times; the last two rebuilds produced a byte-identical tree |
| `sessions/9ed0552a/test_product_pages.py` (+ `--self-test`) | PASS — 5 pages; 6/6 mutations caught |
| `tools/check_publication.py` | PASS — 129 current pages, 25 indexable URLs, 11 feed entries |
| `scripts/build_sitemap.py --check` | PASS — 25 indexable pages, no extras |
| `tools/attach_tag.py --check` | PASS — 1,703 product links tagged, no foreign tags |
| `scripts/check_all_links.py` | PASS — 216 pages, 354 external URLs, 0 errors |
| `tools/verify_site.py` | PASS — 170 pages, 2,748 table rows |
| `scripts/check_site.py` | OK — 42 pages, 5 products, 90 sources, 184 flags |

## Register changes

- `data/publication.json`: five `slug`/`page` records, five `indexable_pages` entries, one decided
  proposal **9E-P1** ("Give each registered listing its own reader-facing page") with its dated
  outcome naming this session record.
- `data/flags.json`: **9E-F01** (fixed — no per-listing page existed) and **9E-F02** (open —
  observations dated 2026-11-19 were not re-fetched on 2026-11-20; stated on every page).
- `README.md` register-facts block regenerated (25 indexable URLs, 31 proposals).

## Limits

No external site was fetched by this session (network reached GitHub/npm/PyPI only). Every page
prints the register's 19 November observation date; no same-day re-check, price, rating,
availability, commission or performance claim is made. Intended ASINs stay blank and separate
from the observed redirect. `FLG-003` remains unresolved and the supplied short links are still
not called invalid.

## Release record

Filled in `COORDINATION.md` (Part 9E) once the PR merged and Pages deployed.
