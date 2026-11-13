# Zone3 — Amazon Affiliate Marketing Platform

Static dashboard for three supplied Amazon affiliate products. Published with GitHub Pages from `main` (root).

**Live site:** https://kanlerxz87-cyber.github.io/Zone3/

**Data:** `data/products.json`, `data/sources.json`, `data/flags.json`

**Build:** `python3 scripts/build_site.py` (generates the HTML pages)

**Check:** `python3 scripts/check_site.py` (broken links, source coverage, unverified values flagged)

**Coordination board:** `COORDINATION.md`

## What this is

A clean, simple dashboard site that collects, organizes, and analyzes three Amazon affiliate products (all air fryers, Home & Kitchen category). Every table row links to its official Amazon product page; anything that could not be confirmed from an official source is left blank and flagged as unverified. No values were inferred or filled in.

## Verified products

| ID | ASIN | Product | Official source | Affiliate link |
|----|------|---------|-----------------|----------------|
| P-001 / P1 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | amazon.com/dp/B0CDY277D3 | link.amazon/B04G1MEwY |
| P-002 / P2 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | amazon.com/dp/B09B7SB46R | link.amazon/B02NbDxp3 |
| P-003 / P3 | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | amazon.com/dp/B08DKYBTPH | link.amazon/B00hJ57DV |

All three are Home & Kitchen → Kitchen. Standard US commission: 4.50% (verified from the official Amazon Associates Commission Income Statement).

## Site structure

- `index.html` — landing page / dashboard (with executive summary)
- `products.html` — full product table; every row with official source links
- `category/kitchen.html` — category subpage (Home & Kitchen / air fryers)
- `categories/home-kitchen-air-fryers.html` — alternate category table with listing claims and comparison
- `analysis.html` — analysis & findings, verification log, compliance checklist
- `dashboard.html` — client-side click/conversion dashboard (no server, no manual input)
- `disclosure.html` — dedicated FTC + Amazon Associates affiliate disclosure
- `flagged-for-review.html` — unverified items and irregularities with source links
- `executive-summary.html` — dedicated executive summary (session arena/66a80e53-zone3)
- `docs/executive-summary.md` — executive summary document
- `sources.html` — every official source used (S1–S12)
- `scripts/build_site.py` — static site generator
- `scripts/check_site.py` — build-time link/source verification

## Verification policy

Every table row has a source link to an official site. Values not confirmed from an official source are left blank and flagged on the Flagged for Review page. No values were inferred or filled in.

## Commission disclosure

As an Amazon Associate I earn from qualifying purchases. See `disclosure.html`.

## Coordination

See `COORDINATION.md` for the shared task board, session claims, sources, verification notes and flagged irregularities.
