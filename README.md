# Zone3 — Amazon Affiliate Marketing Platform

AI-powered Amazon affiliate product research, analysis, and campaign management dashboard. Static site hosted on GitHub Pages.

## What this is
A clean, simple dashboard site that collects, organizes, and analyzes three Amazon affiliate products (all air fryers, Home &amp; Kitchen category). Every table row links to its official Amazon product page; anything that could not be confirmed from an official source is left blank and flagged as unverified. No values were inferred or filled in.

## Site structure
- `index.html` — landing page / dashboard
- `products.html` — full product table with source links per row
- `category-air-fryers.html` — category subpage
- `executive-summary.html` — executive summary
- `disclosure.html` — FTC + Amazon Associates affiliate disclosure
- `flagged-review.html` — unverified items flagged for manual review
- `data/products.json` — structured product data (shared table data)
- `assets/css/style.css` — shared stylesheet
- `assets/js/app.js` — landing-page rendering

## Verified products
| ID | ASIN | Product | Official source | Affiliate link |
|----|------|---------|-----------------|----------------|
| P-001 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | amazon.com/dp/B0CDY277D3 | link.amazon/B04G1MEwY |
| P-002 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | amazon.com/dp/B09B7SB46R | link.amazon/B02NbDxp3 |
| P-003 | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | amazon.com/dp/B08DKYBTPH | link.amazon/B00hJ57DV |

## Verification policy
Every table row has a source link to an official site. Values not confirmed from an official source are left blank and flagged on the Products and Flagged for Review pages. Sources:
- Amazon product pages (amazon.com/dp/<ASIN>) — official
- Amazon Associates Commission Income Statements — affiliate-program.amazon.com
- FTC Endorsement Guides — ftc.gov

## GitHub Pages
This site is published via GitHub Pages from the `main` branch. See COORDINATION.md for the task log and PR/merge record.
