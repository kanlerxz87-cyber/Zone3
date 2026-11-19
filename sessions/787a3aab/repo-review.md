# Repository review — session 787a3aab, 2026-11-19

Base `0273fb4`. This review read the coordination board through Part 4d7fe998, the
canonical publication register (`data/publication.json`), the shop registers
(`data/shop/*`), the generators (`tools/build_publication.py`, `tools/build_feed.py`,
`scripts/build_sitemap.py`), the gates (`scripts/check_site.py`,
`tools/check_publication.py`), and the live site. Full line-by-line evidence is in
`verification-2026-11-19.md` in this folder.

## What already exists (and why this pass does not duplicate it)

The brief's asks are already substantially shipped on `main`:

- **Buyer-first publication, not an audit register.** Root `index.html` is the
  "Everyday Kitchen Edit" front page: hero, five product cards with format
  illustrations, question router, reading room. `shop/` holds the shortlist and the
  two category shelves (3 air fryers, 2 thermometers). Dashboard/research surfaces
  remain reachable from the footer and the single "Behind the site" nav group.
- **Question-led guides.** 10 canonical guides under `guides/` (basket-or-oven,
  capacity checklist, cleanup/counter-space, multi-function questions, instant-read
  vs wireless, holiday checklist, label words, how-do-you-know-it's-done, probe
  placement, thermometer numbers), each with title, dek, takeaway, sourced sections,
  unknowns and related reads. All four brief-suggested working titles are covered.
- **Suggestions/decision desk.** `suggestions/index.html` holds 6 paths, 28 proposals
  and 38 open questions, each with known/missing/default/discovery/owner fields and a
  local Save/Clear + JSON export. Choosing a path implements nothing.
- **Executive summary.** `executive-brief.html` (register-derived counts) +
  `EXECUTIVE-SUMMARY.md` (dated history retained).
- **Compliance machinery.** Disclosure strip under the masthead + footer on every
  indexable page; every outbound product link `rel="sponsored"`; intent record with
  blank intended fields separate from observed redirects; measurement runtime OFF
  with a tested collector; empty campaign ledger; `tools/publish.py` 41-command
  canonical chain (16 builders + 25 checks), idempotent.
- **Findability.** 18 canonical URLs in `sitemap.xml`, 28-item RSS `feed.xml`,
  unique titles/meta/canonicals, local search index, `robots.txt`.

## What this pass adds

1. A fresh, dated line-by-line verification (V01–V16) with manual-review links,
   including a same-day re-observation of all five supplied links (destinations
   unchanged 5/5; one title-wording drift flagged as 787-F-01).
2. One new question-led guide through the canonical register (guide #11):
   thermometer accuracy / ice-water check, sourced to USDA FSIS (new source
   `fsis-thermometers`) + FoodSafety.gov. It answers a question none of the 10
   existing guides answers (how to check the tool itself before trusting a reading)
   without inventing any product claim.
3. `www.fsis.usda.gov` added to the two official-hostname allowlists (USDA FSIS is a
   U.S. federal .gov publisher, same class as FoodSafety.gov).
4. Full release chain twice + idempotency, PR, merge, Pages + live verification.

## What this pass deliberately does not do

- Does not fill any `intended_*` field, add `?tag=` to reader links, enable
  analytics, add campaign rows, or publish any price/rating/review-count/tested
  figure. Each needs owner/account/host evidence this session cannot produce.
- Does not call the supplied short links invalid (FLG-003 unresolved) and does not
  rewrite dated observations to match today's live title wording (787-F-01).
- Does not create a second front door, microsite, or parallel publication layer.
- Does not claim organic traffic, rankings, conversions or revenue. No Search
  Console or first-party report exists; the new guide is a working title until
  measured queries say otherwise.

## Open owner gates (unchanged, still blocking scale — not blocking merge)

1. Confirm intended ASIN + official listing URL + date + source per product (P26-Q1).
2. Validate one Special Link per product in the enrolled Associates workflow and
   check destination + tracking report (P26-Q2 / FLG-003).
3. Choose a durable HTTPS collector host, deploy, verify delivery + logging (P26-Q3).
4. Verify Search Console ownership; obtain first-party query/Associates reports.
5. Review commercial-hosting suitability before scaling beyond GitHub Pages.
