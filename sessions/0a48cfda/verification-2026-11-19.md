# Session 0a48cfda — listing evidence audit, 2026-11-19

Branch `arena/0a48cfda-zone3`, base `0273fb4` (= `main` at claim). Task IDs 0A4-T1…T5 are recorded on
`COORDINATION.md` Part 0A4.

## What this pass was for

The brief asks, in its own words, for line-by-line verification against official sources and for
values that cannot be confirmed to be left blank and flagged. The reader-facing publication already
existed and already passed its gates, so re-drawing it would have been busywork. The open question
was whether the *evidence* behind the five product pages still matched the official listings.

Each listing was read directly on `amazon.com` on 2026-11-19. Nothing below is inferred from a
search result, a cached page, a seller summary or another session's notes.

## Method

1. `python3 tools/publish.py` on the untouched tree first, to establish that the baseline was green.
   Result: 25/25 commands (checks only), no drift.
2. Each of the five official listing pages opened and read, including the "Purchase options and
   add-ons" detail table, the breadcrumb and the page `<title>`.
3. Only values printed on the page were recorded. Where a field was absent, the field was left blank
   with a stated reason rather than filled from a sibling model or from the title.
4. The Programs Policies text was re-read in full at chunk 3 of 11 before changing anything
   link-related, so that any link statement quotes the clause rather than a summary of it.

## Observation log

| Product | ASIN checked | Title | Breadcrumb | Detail-table dimensions | Detail-table capacity |
|---|---|---|---|---|---|
| Shop-01 | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | CHEFMAN 6 Quart Dual Basket Air Fryer Oven … — matches the register | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | 13.38"D x 11.81"W x 10.63"H | 6 liters |
| Shop-02 | [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … | same branch | 16.9"D x 15.8"W x 14.8"H | 24.6 liters |
| Shop-03 | [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 … | same branch | 12.75"D x 13.5"W x 10"H | 8 quarts |
| Shop-04 | [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) | ThermoMaven 1 Sec Professional Digital Meat Thermometer … | n/a (no appliance branch) | **none published** | n/a |
| Shop-05 | [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes … | n/a | **none published** | n/a |

The two thermometer listings do print a detail table; it carries brand, features, colour, care and
certifications but no dimension row. That absence is a finding, not a gap in the reading.

## Findings

### F-1 — the site withheld a published fact (fixed)

`guides/cleanup-and-counter-space.html` carried the sentence "None of the three listing titles gives
width, depth or height." That was true of the titles and false of the pages: three detail tables
publish an exterior size. The sentence was replaced, the sizes were recorded under
`data/publication.json → products[].listing_dimensions`, and the size now appears on each product
card and in a "Listed size" column of the comparison table.

The record deliberately names what an exterior size is **not**: it is not the interior, not a
clearance, not a door swing and not a portion estimate. Those stay absent, with the reason stated.

### F-2 — two listings disagree with themselves on capacity (flagged, not resolved)

* Shop-01: title "6 Quart" vs detail table "Capacity: 6 liters". Six US quarts ≈ 5.7 L.
* Shop-02: title "26QT" vs detail table "Capacity: 24.6 liters". 24.6 L ≈ 26 US quarts.
* Shop-03: consistent at 8 quarts.

Both printed figures are now stored and both are published, with the field each came from named.
Published as **FLG-S33** on the shop flag register. This pass does not say which figure is correct
and does not call either listing inaccurate; that needs the model manual.

### F-3 — in-guide contents numbering was typed, not derived (fixed)

The contents block appended `<span>04</span>` for "The relevant shortlist" regardless of how many
sections existed. With this pass's new fourth section, the counter-space guide showed `04` twice;
`capacity-checklist.html` (three sections) showed `04` for what was actually entry 4 but had never
matched its own section count. The number is now `len(sections) + 1`.

### F-4 — a dangling in-page anchor on the suggestions page (fixed)

`B38-P3` and `B38-P5` list `DS-01` / `DS-03` under `evidence_needed`; `0A4-P2` initially listed a
source id. The renderer turned every `evidence_needed` entry into `href="#<id>"`, producing
`#google-page-experience`, which is not an element on the page. `scripts/check_all_links.py` caught it
as `BROKEN ANCHOR suggestions/index.html: #google-page-experience`. Now a source id renders as its
official page and an internal reference renders as plain text; both are honest, and the anchor check
is green.

## What was deliberately not done

* **The outbound links were not changed.** Program Policies 2(b) (read verbatim this pass): "you must
  include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may
  designate) as a parameter in the URL of each link you place on your Site to an Amazon Site"
  ([source](https://affiliate-program.amazon.com/help/operating/policies)). The supplied
  `link.amazon` forms carry no visible tag, but the clause also permits "such other format as we may
  designate", and only an enrolled account can show what Amazon designates. FLG-003 therefore stays
  open. The tagged direct URLs in `data/special-links.json` were **not** promoted to the buttons,
  because their destinations come from the redirects and intended product identity is unconfirmed.
* **No price, rating or review count was added.** 2(b) permits those fields only when Amazon serves
  the link or the data arrives through the Creators API. The pages visibly publish them today
  ($79.93, 4.2 stars, 4,876 ratings on Shop-01, for example); none of it was copied.
* **No counter-space arithmetic was published.** Capacity per centimetre of counter depth needs one
  consistent capacity figure and an interior measurement. F-2 removes the first and none of the five
  listings supplies the second. `E41-P1` was re-scoped to say so rather than left stating that no
  footprint existed anywhere.
* **No traffic, conversion or ranking statement.** Production collection remains off and the campaign
  ledger remains empty.

## Verification performed

| Check | Result |
|---|---|
| `python3 tools/publish.py` before any edit | 25/25 checks pass on `0273fb4` |
| `python3 tools/publish.py` after the edits, twice | 41/41 commands each run |
| Working tree after the second run | identical to after the first (no drift) |
| `git diff` size for the register edit | 78 insertions / 7 deletions in `data/publication.json` — a minimal diff, not a reformat |
| Comparison-table column counts | header 7 columns, every row 7 cells, 5 rows on `shop/products/`, 3 on `shop/air-fryers/` |
| Dangling same-page anchors on index, shop, compare, guide and flagged pages | none |
| Flag rendered | `FLG-S33` present on `shop/flagged/index.html` with its three listing sources |
| Counts | 10 guides, 18 sitemap URLs, 28 feed items, 30 proposals, 38 questions, 33 shop flags |

**Limitation.** No browser was available in this environment: the pinned Playwright Chromium could
not be downloaded (only `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`, `github.com`,
`codeload.github.com` and `api.github.com` are reachable, and the `@sparticuz/chromium` fallback
fails on missing system `libnss3`/`libnspr4`). The visual check of the new size line is therefore
structural only, not a rendered screenshot. The CSS is additive and scoped to new classes
(`.p26-dims`, `.p26-dims-empty`, `.p26-unknown`); the existing rules were not modified.

## Source list for this pass

* https://www.amazon.com/dp/B0CDY277D3 — read 2026-11-19
* https://www.amazon.com/dp/B09B7SB46R — read 2026-11-19
* https://www.amazon.com/dp/B08DKYBTPH — read 2026-11-19
* https://www.amazon.com/dp/B0DHZTCNR5 — read 2026-11-19
* https://www.amazon.com/dp/B0DZFD6R9Z — read 2026-11-19
* https://affiliate-program.amazon.com/help/operating/policies — read 2026-11-19, chunk 3 of 11
  (Program Policies, Participation Requirements 2(a) and 2(b))
* https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links — the
  `rel="sponsored"` basis already used by the site
