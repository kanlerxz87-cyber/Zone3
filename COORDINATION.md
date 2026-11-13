# Coordination — Zone3 Amazon Affiliate Platform

Branch: `arena/a9cafea1-zone3` (branched from `ed1a796dc01f52669864e98a72b9a521a3b7161b` of `main`)
Session: single session working the full pipeline on this branch.
Rule: each session edits only files in its claimed scope; log cross-session requests here instead of editing others' files.

## Tasks

| # | Task | Status | Owner | Files / Scope | Sources | Notes |
|---|------|--------|-------|---------------|---------|-------|
| 1 | Repo review; flag irregularities | done | session-arena-a9cafea1-zone3 | README.md, COORDINATION.md | n/a | Repo near-empty (only README.md). Irregularities logged below. |
| 2 | Product research — verify 3 Amazon links against official sources | done | session-arena-a9cafea1-zone3 | data/products.json | Amazon.com link.amazon redirects; amazon.com /dp pages; Associates Central | All 3 links verified as redirects to real Amazon product pages. Prices/ratings/reviews blocked by Amazon bot protection — left blank + flagged. |
| 3 | Executive summary | done | session-arena-a9cafea1-zone3 | docs/executive-summary.md | Amazon Associates Central (commission statement, policies, operating agreement) | |
| 4 | Site creation — landing page, category subpages, dashboard table | in progress | session-arena-a9cafea1-zone3 | index.html, products.html, category/kitchen.html, analysis.html, disclosure.html, flagged-for-review.html, dashboard.html, assets/ | task 2 outputs | GitHub Pages static site |
| 5 | Flagged for Review page (unverified items + irregularities) | planned | session-arena-a9cafea1-zone3 | flagged-for-review.html | task 1, 2, 4 | Publish unverified items here |
| 6 | Verification — every table row has official source link; no broken links | planned | session-arena-a9cafea1-zone3 | all site files | official sources | Link check before publish |
| 7 | GitHub Pages setup + deploy confirmation | planned | session-arena-a9cafea1-zone3 | repository settings | GitHub Pages docs | |
| 8 | Pull request to main + merge + record result | planned | session-arena-a9cafea1-zone3 | GitHub PR | all prior tasks | Do not merge a broken site |

## Log

- Session started on branch `arena/a9cafea1-zone3`. Repo contains only `README.md` ("# Zone3"). Task 1 claimed and committed (b9c1485).
- Task 1 done: repo review complete. Irregularity: repo is near-empty (only README.md, no code, no config).
- Task 2 done: all three `link.amazon` short links resolved on the amazon.com domain:
  - B04G1MEwY → https://www.amazon.com/dp/B0CDY277D3 (CHEFMAN 6 Quart Dual Basket Air Fryer Oven, Home & Kitchen)
  - B02NbDxp3 → https://www.amazon.com/dp/B09B7SB46R (Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven, Home & Kitchen)
  - B00hJ57DV → https://www.amazon.com/dp/B08DKYBTPH (Chefman Air Fryer 8 Qt TurboFry 4-in-1, Home & Kitchen)
  Irregularity: short-link ASINs return 404 on direct /dp/ lookup across amazon.com/.co.uk/.de/.ca/.in/.com.au; short-link ASIN ≠ destination ASIN. Product price/rating/review/availability blocked by Amazon bot-protection checkpoint — left blank, flagged for review.
- Verified official sources: Associates Commission Income Statement (Kitchen = 4.50%): https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ ; Program Policies incl. FTC disclosure compliance: https://affiliate-program.amazon.com/help/operating/policies ; Operating Agreement §5 disclosure "As an Amazon Associate I earn from qualifying purchases": https://affiliate-program.amazon.com/help/operating/agreement
- Next: task 3 executive summary, then task 4 site build.
