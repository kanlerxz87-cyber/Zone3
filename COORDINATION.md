# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/Zone3` · Live site (GitHub Pages, source `main` `/`): https://kanlerxz87-cyber.github.io/Zone3/
This session branch: `arena/a9cafea1-zone3` (branched from `ed1a796dc01f52669864e98a72b9a521a3b7161b` of `main`)

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything).

## Session registry

| Session ID | Branch | Role | Claimed at (UTC) |
|---|---|---|---|
| 26634cd5 | `arena/26634cd5-zone3` | Repo review, source verification, site build, integration, PR #1 | 2026-11-13 22:36 |
| session-zone3-001 | `arena/66a80e53-zone3` | Parallel build: landing page, product table, category page, executive summary, disclosure page, shared CSS/JS, data/products.json; PR #3 | 2026-11-13 |
| arena-a9cafea1-zone3 | `arena/a9cafea1-zone3` | Full pipeline: product research, executive summary, site extension, flagged page, verification, integration, PR #4, merge, Pages deploy | 2026-11-13 |

## Task board

| Task | Status | Owner | Files in scope | Sources / verification | Irregularities |
|---|---|---|---|---|---|
| T1 — Repo review & source verification | done | 26634cd5 | `data/products.json`, `data/sources.json`, `data/flags.json` | S1–S12 (see below) | F1, F2, F3, F6 |
| T2 — Site creation (landing + category pages) | done | 26634cd5 | `index.html`, `categories/**`, `analysis.html`, `flagged.html`, `sources.html`, `assets/**`, `scripts/build_site.py`, `.nojekyll`, `README.md` | — | — |
| T3 — Line-by-line verification & flagging | done | 26634cd5 | `scripts/check_site.py`, `data/flags.json` | check_site.py OK (137 links, 0 errors) on 5 pages | F1–F8 (published on Flagged for Review) |
| T-02 — Resolve 3 Amazon links + collect product data | done | session-zone3-001 / arena-a9cafea1-zone3 | `data/products.json` | All 3 link.amazon links resolved to official amazon.com/dp pages; titles/ASINs/category verified | link.amazon codes ≠ ASINs; P-003 reached checkpoint |
| T-03 — Build landing page | done | session-zone3-001 | `index.html` (superseded by merged dashboard build in this integration) | n/a | none |
| T-04 — Category subpages + product table | done | session-zone3-001 | `category/kitchen.html`, `categories/home-kitchen-air-fryers.html`, `products.html` | official sources per row | unverified blank + flagged |
| T-05 — Executive summary page + document | done | session-zone3-001 / arena-a9cafea1-zone3 | `executive-summary.html`, `docs/executive-summary.md` | official sources | none |
| T-06 — Affiliate disclosure page (FTC + Amazon Associates) | done | session-zone3-001 / arena-a9cafea1-zone3 | `disclosure.html` | ftc.gov; affiliate-program.amazon.com | none |
| T-07 — Flagged for Review page | done | 26634cd5 (`flagged.html`); arena-a9cafea1-zone3 (`flagged-for-review.html`, merged) | `flagged.html`, `flagged-for-review.html` | flags F1–F8 | F1–F8 |
| T-08 — Build verification, no broken links | done | 26634cd5 / arena-a9cafea1-zone3 | `scripts/check_site.py`, all HTML | internal link check OK on merged build | — |
| T-09 / T4 — Integration, PR, merge, Pages deploy | in progress | arena-a9cafea1-zone3 | all (integration only) | PR #1 merged (26634cd5); PR #3 merged (session-zone3-001); PR #4 (this branch → main) | — |

## Sources and verification performed

| ID | Source | Official | What was verified | Status |
|---|---|---|---|---|
| S1 | https://link.amazon/B04G1MEwY | Amazon | Redirects to amazon.com/dp/B0CDY277D3; title (brand, capacity, category, listing claims) | Fetched |
| S2 | https://link.amazon/B02NbDxp3 | Amazon | Redirects to amazon.com/dp/B09B7SB46R; title | Fetched |
| S3 | https://link.amazon/B00hJ57DV | Amazon | Redirects to amazon.com/dp/B08DKYBTPH; title | Fetched |
| S4 | https://www.amazon.com/dp/B0CDY277D3 | Amazon | Page title confirmed; body returned footer boilerplate | Partial |
| S5 | https://www.amazon.com/dp/B09B7SB46R | Amazon | Page title confirmed; body returned footer boilerplate | Partial |
| S6 | https://www.amazon.com/dp/B08DKYBTPH | Amazon | Direct fetch returned "Continue shopping" interstitial; title confirmed only via S3 | Not verified directly |
| S7 | https://affiliate-program.amazon.com/help/operating/agreement | Amazon Associates (updated Oct 15, 2025) | Section 5 required disclosure "As an Amazon Associate I earn from qualifying purchases." | Fetched |
| S8 | https://affiliate-program.amazon.com/help/operating/policies | Amazon Associates (updated Apr 14, 2026) | Commission Income Statement §1–3; qualifying purchases; 24-hour session | Fetched |
| S9 | https://affiliate-program.amazon.com/help/operating/schedule | Amazon Associates | Rate table — login-gated, not retrieved directly | Login-gated |
| S10 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | FTC (dated Nov 2019) | Material connection; disclosure hard to miss, placed with endorsement | Fetched |
| S11 | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ | Amazon Associates | Table 1: Kitchen = 4.50% fixed standard commission rate | Fetched |
| S12 | https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA | Amazon Associates | Onsite Commission Table A | Fetched |

Not used (non-official, reference only, listed on Flagged page): geniuslink.com and sellersonar.com rate guides (report Kitchen 4.5%).

## Verification performed

- Every product row: brand, capacity, category, ASIN and title come from an official Amazon page or redirect. Price, rating, review count, availability are blank/null and marked **Unverified** — never inferred or filled in.
- Commission rate Kitchen 4.50% verified from S11 (official Commission Income Statement node page).
- Internal link check on all merged pages: OK (no broken internal links, anchors resolve).
- check_site.py allow-list: amazon.com, link.amazon, affiliate-program.amazon.com, www.ftc.gov.

## Flags / irregularities (F1–F8, published on Flagged for Review page)

F1 — Short-link codes do not match the ASINs they resolve to (B04G1MEwY→B0CDY277D3, B02NbDxp3→B09B7SB46R, B00hJ57DV→B08DKYBTPH). Action: confirm each short link is the intended product.
F2 — No Associate tag (`tag=`) visible in resolved links; commission cannot be attributed until tagged links are generated from the owner's Associates account. No tag was invented.
F3 — Marketplace and eligibility not confirmed: links resolve to amazon.com (US); owner location is Oslo, Norway. Action: confirm Associates account country.
F4 — Price, rating, review count, availability — all three products: blank, unverified. Action: manually record from live listings.
F5 — Commission rate for Kitchen-category products: resolved as 4.50% from official S11 (schedule page S9 remains login-gated). Keep under review.
F6 — Product 3 direct page not verified (interstitial); title taken from S3 redirect. Action: open listing in browser.
F7 — Scope gap: platform automation (AI discovery, live pricing, content generation, click tracking) not built; static verified dashboard plus client-side click/conversion dashboard only.
F8 — FTC guidance dated 2019; check current FTC Endorsement Guides before publishing marketing copy.

## Task log

- 2026-11-13 22:36 UTC — 26634cd5 claimed T1–T3 and pushed (commit 494c792); PR #1 (`arena/26634cd5-zone3` → main) merged as 8cc2d4a. Pages already enabled on repo, source = main branch.
- session-zone3-001 completed T-02 through T-07 on `arena/66a80e53-zone3`; PR #3 merged as cc26993 (merge commit e790346 resolved with origin/main).
- This session (arena/a9cafea1-zone3): completed product research, executive summary, site extension, flagged page, verification; merged both companion sessions' work into this branch (merge commit 7aeeff2 integrated 26634cd5's work); now integrating cc26993 (PR #3 work) and opening/merging PR #4 to main. Pages will redeploy from main after merge.
- No session's work was discarded: conflicting shared files were resolved by hand into merged versions; each session's dedicated pages are retained (`executive-summary.html`, `disclosure.html`, `flagged-for-review.html`, `flagged.html`, `sources.html`, `categories/home-kitchen-air-fryers.html`).
