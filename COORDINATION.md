# Coordination Board — Zone3 Amazon Affiliate Platform

Branch: `arena/66a80e53-zone3` (branched from `ed1a796` of `main`)
Session ID: `session-zone3-001`
Working branch: `arena/66a80e53-zone3` (single session; no branch switching per Arena session rules)

## Rules
- Claim a task by writing session ID + file scope + status before starting; commit and push the claim immediately.
- Never start a task another session has claimed.
- Keep scopes non-overlapping; each session edits only its claimed files.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding other session's work, log the handoff.
- When a task is finished: record sources, verification performed, and irregularities here; mark done.
- Never mark verified without checking against an official source; link that source.
- Shared outputs (table data, index/navigation) changed only by the final integration session once all other tasks are done.
- Flagged irregularities and unverified items do not block merge; publish on "Flagged for Review" page.

## Tasks

| ID | Task | Status | Owner | File scope | Sources / verification | Irregularities |
|----|------|--------|-------|------------|------------------------|----------------|
| T-01 | Create COORDINATION.md and claim all tasks | done | session-zone3-001 | COORDINATION.md | n/a | none |
| T-02 | Resolve 3 Amazon affiliate links to official product pages; collect product data | done | session-zone3-001 | data/products.json | All 3 links resolved via official Amazon pages (amazon.com/dp/<ASIN>). Titles + ASIN + category verified from Amazon page titles. Prices/ratings/reviews/commission NOT verifiable via fetch (Amazon blocks content) → left blank + flagged. Commission rates confirmed from official affiliate-program.amazon.com help pages but applicable rate depends on Home vs Kitchen classification + Standard vs Onsite program → flagged unverified for specific product. | link.amazon short links redirect to dp URLs; 3rd link hit Amazon checkpoint but title confirmed via link.amazon page |
| T-03 | Build landing page (index.html) with dashboard UI | in progress | session-zone3-001 | index.html, assets/css/style.css | n/a | none |
| T-04 | Build category subpages + product table with source links per row | planned | session-zone3-001 | products.html, category-air-fryers.html | official sources per row | unverified values left blank + flagged |
| T-05 | Executive summary page | planned | session-zone3-001 | executive-summary.html | official sources | none |
| T-06 | Affiliate disclosure page (FTC + Amazon Associates) | planned | session-zone3-001 | disclosure.html | ftc.gov; affiliate-program.amazon.com | none |
| T-07 | Flagged for Review page | planned | session-zone3-001 | flagged-review.html | n/a | none |
| T-08 | GitHub Pages setup, build verification, no broken links | planned | session-zone3-001 | all site files + GitHub Pages settings | GitHub Pages deploy | none |
| T-09 | Integration: PR to main, merge, confirm Pages deploy, record PR link | planned | session-zone3-001 | all | GitHub / Pages | none |

## Verified sources (official)
- Product 1: https://www.amazon.com/dp/B0CDY277D3 — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (Home & Kitchen)
- Product 2: https://www.amazon.com/dp/B09B7SB46R — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven (Home & Kitchen)
- Product 3: https://www.amazon.com/dp/B08DKYBTPH — Chefman Air Fryer 8 Qt TurboFry 4-in-1 (Home & Kitchen)
- Amazon Associates Standard Commission Table 1: https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ (Kitchen 4.50%; Home 3.00%)
- Amazon Associates Onsite Commission Table A: https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA (Kitchen 1.25%; Home 3.00%)
- FTC Endorsement Guides (affiliate disclosure): https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
