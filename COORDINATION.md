# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/Zone3` · Live site (GitHub Pages, source `main` `/`): https://kanlerxz87-cyber.github.io/Zone3/

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything).

## Session registry

| Session ID | Branch | Role | Claimed at (UTC) |
|---|---|---|---|
| 26634cd5 | `arena/26634cd5-zone3` | Repo review, site build, verification, integration, PR | 2026-11-13 22:36 |
| session-zone3-001 | `arena/66a80e53-zone3` | Parallel build: landing page, product table, category page, executive summary, disclosure page, flagged-review page, shared CSS/JS, data/products.json | 2026-11-13 (after 26634cd5) |

Note: session 26634cd5 is assigned exactly one branch (`arena/26634cd5-zone3`). Session arena/66a80e53-zone3 is the Arena-tracked working branch for this session. Both branches' work is preserved in the merge to `main`; conflicting shared files were resolved in favor of the verified 26634cd5 build, and session-zone3-001's dedicated pages (`executive-summary.html`, `disclosure.html`) were added.

## Task board

| Task | Status | Owner | Files in scope | Sources / verification | Irregularities |
|---|---|---|---|---|---|
| T1 — Repo review & source verification | done | 26634cd5 | `data/products.json`, `data/sources.json`, `data/flags.json` | S1–S10 + commission help pages below | F1, F2, F3, F6 |
| T2 — Site creation (landing + category pages) | done | 26634cd5 | `index.html`, `categories/**`, `analysis.html`, `flagged.html`, `sources.html`, `assets/**`, `scripts/build_site.py`, `.nojekyll`, `README.md` | — | — |
| T-02 — Resolve 3 Amazon links + collect product data | done | session-zone3-001 | `data/products.json` | All 3 link.amazon links resolved to official amazon.com/dp pages; titles/ASINs/category verified | link.amazon codes ≠ ASINs; P-003 reached checkpoint |
| T-03 — Build landing page | done | session-zone3-001 | `index.html` (superseded by 26634cd5 dashboard in merge) | n/a | none |
| T-04 — Category subpages + product table | done | session-zone3-001 | `category-air-fryers.html`, `products.html` (superseded by `categories/home-kitchen-air-fryers.html` in merge) | official sources per row | unverified blank + flagged |
| T-05 — Executive summary page | done | session-zone3-001 | `executive-summary.html` | official sources | none |
| T-06 — Affiliate disclosure page (FTC + Amazon Associates) | done | session-zone3-001 | `disclosure.html` | ftc.gov; affiliate-program.amazon.com | none |
| T-07 — Flagged for Review page | done | 26634cd5 (`flagged.html`); session-zone3-001 (`flagged-review.html`, superseded) | `flagged.html` | flags F1–F8 | F1–F8 |
| T-08 — Build verification, no broken links | done | 26634cd5 | `scripts/check_site.py` | check_site.py OK (137 links, 0 errors) on 5 pages | — |
| T-09 / T4 — Integration, PR, merge, Pages deploy | in progress | both | all | PR #3: arena/66a80e53-zone3 → main | PR #1 merged earlier (26634cd5) |

## Sources and verification performed

| ID | Source | Official | What was verified | Status |
|---|---|---|---|---|
| S1 | https://link.amazon/B04G1MEwY | Amazon | Redirects to `amazon.com/dp/B0CDY277D3`; title (brand, capacity, category, listing claims) | Fetched |
| S2 | https://link.amazon/B02NbDxp3 | Amazon | Redirects to `amazon.com/dp/B09B7SB46R`; title | Fetched |
| S3 | https://link.amazon/B00hJ57DV | Amazon | Redirects to `amazon.com/dp/B08DKYBTPH`; title | Fetched |
| S4 | https://www.amazon.com/dp/B0CDY277D3 | Amazon | Title only; body returned footer boilerplate | Partial |
| S5 | https://www.amazon.com/dp/B09B7SB46R | Amazon | Title only; body returned footer boilerplate | Partial |
| S6 | https://www.amazon.com/dp/B08DKYBTPH | Amazon | Returned "Continue shopping" interstitial; title via S3 | Not verified directly |
| S7 | https://affiliate-program.amazon.com/help/operating/agreement | Amazon Associates (updated Oct 15, 2025) | Section 5 required disclosure "As an Amazon Associate I earn from qualifying purchases." | Fetched |
| S8 | https://affiliate-program.amazon.com/help/operating/policies | Amazon Associates (updated Apr 14, 2026) | Commission Income Statement §1–3 | Fetched |
| S9 | https://affiliate-program.amazon.com/help/operating/schedule | Amazon Associates | Rate table — login-gated, NOT retrieved | Not verified |
| S10 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | FTC (dated Nov 2019) | Material connection; disclosure hard to miss, placed with endorsement | Fetched |
| S11 | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ | Amazon Associates | Standard Commission Table 1: Kitchen 4.50%; Home 3.00% | Fetched |
| S12 | https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA | Amazon Associates | Onsite Commission Table A: Kitchen 1.25%; Home 3.00% | Fetched |

Not used (non-official, for reference only, listed on Flagged page): geniuslink.com and sellersonar.com rate guides (report Kitchen 4.5%).

## Verification performed

- Every product row: brand, capacity, category, ASIN and title come from an official Amazon page or redirect. Price, rating, review count, availability and commission rate are blank and marked **Unverified** — nothing inferred.
- `scripts/check_site.py`: checks all internal links, external allow-list (amazon.com, link.amazon, affiliate-program.amazon.com, www.ftc.gov), source coverage per product row, Unverified rendering of null values, flag references, affiliate disclosure on every page. Result: **OK** on the 26634cd5 build.
- Irregularities are listed in `data/flags.json`, shown on `flagged.html`, and summarised below (F1–F8).

## Flags / irregularities (F1–F8, published on Flagged for Review)

F1 — Short-link codes do not match the ASINs they resolve to (B04G1MEwY→B0CDY277D3, B02NbDxp3→B09B7SB46R, B00hJ57DV→B08DKYBTPH). Action: confirm each short link is the intended product.
F2 — No Associate tag (`tag=`) visible in resolved links; commission cannot be attributed until tagged links are generated from the owner's Associates account. No tag was invented.
F3 — Marketplace and eligibility not confirmed: links resolve to amazon.com (US); owner location is Oslo, Norway. Action: confirm Associates account country.
F4 — Price, rating, review count, availability — all three products: blank, unverified. Action: manually record from live listings.
F5 — Commission rate for Kitchen-category products: official schedule (S9) login-gated; not used. S11/S12 give Kitchen 4.50% Standard / 1.25% Onsite; Home 3.00% both programs. Applicable rate per product unconfirmed → flagged unverified.
F6 — Product 3 direct page not verified (interstitial); title taken from S3 redirect. Action: open listing in browser.
F7 — Scope gap: platform automation (AI discovery, live pricing, content generation, click tracking) not built; static verified dashboard only.
F8 — FTC guidance dated 2019; check current FTC Endorsement Guides before publishing marketing copy.

## Task log

- **2026-11-13 22:36 UTC — 26634cd5** claimed T1–T3 and pushed (commit `494c792`); completed T1 (source retrieval) and T2 (static site via `scripts/build_site.py`); T3 as needs review (8 flags on Flagged for Review).
- **2026-11-13 — 26634cd5** T4: `check_site.py` passes (5 pages, 137 links, 0 errors). PR #1 opened (`arena/26634cd5-zone3` → `main`) and merged; post-merge Pages result recorded in PR #1 comments.
- **2026-11-13 — session-zone3-001** completed T-02 through T-07 on `arena/66a80e53-zone3`; opened PR #3 (`arena/66a80e53-zone3` → `main`): https://github.com/kanlerxz87-cyber/Zone3/pull/3. Merge in progress; PR link and merge result to be recorded here after merge.
- Merge conflict resolution: `arena/66a80e53-zone3` merged with `origin/main`; shared files resolved in favor of the verified 26634cd5 build; session-zone3-001 dedicated pages (`executive-summary.html`, `disclosure.html`) retained.

## Pages for manual review after launch

Flagged for Review: `flagged.html` (irregularities F1–F8 with source links and requested actions). These do not block the merge.
