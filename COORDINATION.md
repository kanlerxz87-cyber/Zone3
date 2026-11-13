# COORDINATION.md — Shared task board

Repo: `kanlerxz87-cyber/Zone3` · Live site (GitHub Pages, source `main` `/`): https://kanlerxz87-cyber.github.io/Zone3/

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (listed on the Flagged for review page; does not block anything).

## Session registry

| Session ID | Branch | Role | Status | Claimed at (UTC) |
|---|---|---|---|---|
| 7f84fea4 | `arena/7f84fea4-zone3` | Integration of session 26634cd5 with this session; repo review; site; PR to `main` | in progress (T6) | 2026-11-13 |
| 26634cd5 | `arena/26634cd5-zone3` | Earlier site (PR #1, merged into `main` at 8cc2d4a). Its files are archived in `archive/26634cd5/` on this branch. | merged | 2026-11-13 22:36 |
| 66a80e53 (session-zone3-001) | `arena/66a80e53-zone3` | Parallel build: executive summary, disclosure, product table, flagged-review page, commission table citations. Merged into `main` as PR #3 (cc26993). Files archived in `archive/66a80e53/` on this branch. | merged | 2026-11-13 |
| 3c6cba43 | `arena/3c6cba43-zone3` | Own FLG-001–012 and SRC-01–010 IDs (not comparable to ours). Not read in this session beyond its COORDINATION.md. | not merged | — |
| a9cafea1 | `arena/a9cafea1-zone3` | PR #4 open. Not read in this session. | not merged | — |
| 45ec61ec | `arena/45ec61ec-zone3` | PR #2 closed. Not read in this session. | closed | — |
| 33226b37-zone3 | `arena/33226b37-zone3` | Independent re-verification of all three earlier sessions' claims; control-ASIN test; enrollment-gate and payment facts (PF-40–43, S27–S29); `research/` + `docs/` verification record; final PR. | merged | 2026-11-13 22:45 |
| c4e71983 | (branch only; no PR seen) | Not read in this session. | unknown | — |

### Branch naming decision (logged 2026-11-13, session 7f84fea4)

The brief asks for `session-<id>/<task>` branches. Arena's session branch note fixes this session to one branch, `arena/7f84fea4-zone3`, and forbids creating or pushing other branches. Task IDs (T1–T6) on this board replace the per-task branches. Earlier text on this board said the branch rule came from an "Arena session rule". That was an unsourced claim and is withdrawn. The source is the branch note in the session instructions.

## Task board

| Task | Status | Owner | Files in scope | Sources | Irregularities |
|---|---|---|---|---|---|
| T1 — Repo review and source verification | done | 7f84fea4 | `data/sources.json`, `data/products.json`, `data/policy_facts.json` | S01–S24 | FLG-001–003, 015–020 |
| T2 — Site: landing and category pages | done | 7f84fea4 | `index.html`, `executive-summary.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `flagged.html`, `sources.html`, `analysis.html` and category stubs, `assets/style.css`, `scripts/build_site.py`, `.nojekyll` | — | — |
| T3 — Line-by-line verification and flags | needs review | 7f84fea4 | `scripts/check_site.py`, `data/flags.json` | — | FLG-001–020 (published on Flagged for review) |
| T4 — Integration with session 26634cd5 (PR #1) | done | 7f84fea4 | all (integration only) | S07 mapped to S10 and others (see below) | FLG-015–020 |
| T5 — Campaign and tracking ledger | done (empty by design) | 7f84fea4 | `campaigns.html` | — | FLG-010, FLG-011 |
| T6 — Re-verify, PR, merge, Pages deploy | in progress | 7f84fea4 | this branch only | — | — |

## Integration with session 66a80e53 (PR #3, merged after this branch was first pushed)

`main` moved to cc26993 after PR #3 merged. Its files were integrated in the same way as PR #1: this branch's versions of shared files are kept, PR #3's versions are archived unchanged under `archive/66a80e53/`, and nothing is deleted. Automatic merge was not used for shared files, because it can combine two sessions' data into output neither wrote.

- **New page from PR #3:** `disclosure.html`. It is now a redirect to `content.html`, where the Associates and FTC disclosure is already checked on every page.
- **Replaced by this branch:** `executive-summary.html`, `index.html`, `README.md`, `COORDINATION.md` (merged content kept as the ID mapping), data files, scripts and CSS.
- **New sources, read 2026-11-13:** Standard Commission Table 1 (Kitchen 4.50%) as S25 and Onsite Table A (Kitchen 1.25%) as S26. These map to PR #3's S11 and S12. The Kitchen rate is shown only as a category reference, not on any product row, because the listings' category is not verified (FLG-021; PF-38, PF-39).
- **PR #3 task IDs:** T-02 to T-08 and T-09/T4 map to this board's T1–T6. PR #3's F1–F8 map as in the table below.

## Integration with session 26634cd5 (PR #1)

`main` moved to 8cc2d4a while this branch was in review. PR #1 had merged the other session's site, which added files with the same names. The merge produced add/add conflicts in 15 files. Stopping on conflicts would have left the branch unmergeable, so the integration was resolved in this branch as follows, and the other session's files were kept, not deleted:

- **Archived, unchanged:** `archive/26634cd5/` holds the other session's scripts, data, pages, CSS, README and COORDINATION.md as they were on `main` at 8cc2d4a, with `ARCHIVE_NOTE.md`. Their original files are also in git history.
- **Kept from this branch:** the generator, checker, page set and data schema. Sources, policy facts and flags were merged into them (below).
- **Old URLs:** `analysis.html` and `categories/home-kitchen-air-fryers.html` now redirect to `executive-summary.html` and `products.html`.
- **Conflict log:** add/add conflicts in COORDINATION.md, README.md, assets/style.css, data/flags.json, data/products.json, data/sources.json, flagged.html, index.html, scripts/build_site.py, scripts/check_site.py, sources.html; auto-merged analysis.html, assets/app.js, categories/home-kitchen-air-fryers.html, data/*.

### Source ID mapping (other session → this board)

| Other session | This board | Note |
|---|---|---|
| S1, S2, S3 (link.amazon) | S11, S12, S13 | Final URL and title, re-read on 2026-11-13 |
| S4, S5 (dp title) | S14, S15 | Direct title |
| S6 (dp for product 3, interstitial) | S16 | Interstitial only |
| — | S23 | Product 3 destination title via the short link |
| S7 (Operating Agreement) | S01 | Section 5 wording |
| S8 (Program Policies) | S02 | |
| S9 (commission schedule, login-gated) | S03 | Not readable |
| S10 (FTC 2019) | S07 | Dated 2019; newer guide mapped to S24 |
| — | S04, S05, S06 | Creators API docs and PA-API 5 deprecation (this branch) |
| — | S08, S09, S10 | amazon.com/dp checks for the three IDs |
| — | S17 (third-party), S18 (not accessible), S19 (footer), S20–S22 (repo and Pages checks) | Not used as facts |
| — | S24 | FTC topic page (current Endorsement Guides, 2023) |

### Flag ID mapping

| Other session (F) | This board (FLG) |
|---|---|
| F1 short-link codes do not match the ASIN | FLG-001 |
| F2 no Associate tag | FLG-010 |
| F3 marketplace and eligibility | FLG-015 |
| F4 price, rating and reviews unverified | FLG-004 |
| F5 Kitchen commission rate unverified | FLG-005 |
| F6 product 3 direct page unverified | FLG-020 (and FLG-002) |
| F7 platform automation not built | FLG-012 (and FLG-019) |
| F8 FTC guidance dated 2019 | FLG-017 |

## Verification performed (7f84fea4)

- Official pages re-read on 2026-11-13, with the text kept in `data/policy_facts.json`:
  - Operating Agreement chunks 0–3 of 4, including Schedule 1 (US only).
  - Program Policies chunks 0–9 of 11 (chunk 10 unread).
  - Creators API GetItems chunks 0–2 of 3. The ASIN is a 10-character identifier. The example ASINs in the sample are in the docs, so they are not product data.
  - FTC topic page (2023 Endorsement Guides revision).
- Product links re-resolved on 2026-11-13: each short link, the plain `amazon.com/dp/<ID>` URL for products 1 and 2, and the product 3 direct URL (interstitial). Titles are recorded as observed; prices and ratings are not present in the text returned.
- Withdrawn: PF-14 (reviews for compensation). Its text was not found in any section read.
- `scripts/check_site.py`: OK, 9 pages, 3 products, 24 sources, 20 flags.
- Limitation: the checker verifies the structure (sources present, links resolve, official hosts, no Python leaks). It does not compare quotes to source text. Quotes were checked by hand against the fetched text, and that is recorded in each fact's `section` field.
- Limitation: the Program Policies chunk 10 and the commission schedule (S03) were not read. Rates are not stated anywhere on the site.

## Integration with session 33226b37-zone3 (final PR)

Session 33226b37-zone3 worked in parallel from `ed1a796` and independently verified the same facts (its pushed branch carried a complete site built before `main` moved). To avoid clobbering the canonical site and data schema of sessions 26634cd5/66a80e53/7f84fea4, its branch was rebased onto `main` (96ad628) and reduced to non-overlapping, additive contributions. Nothing from `main` was overwritten or discarded; no generated page, script or CSS was changed. What was added:

- **`research/verification-log.md`, `research/products.md`** — the independent line-by-line verification record, with a mapping note from its local IDs to the canonical scheme.
- **`docs/executive-summary.md`** — markdown executive summary with a final-integration update.
- **`data/sources.json`** — S27 (control lookup of Amazon's documented example ASIN `B00005N5PF`: checkpoint interstitial, NOT the S08–S10 Page-Not-Found — validates that those 404s are meaningful), S28 (Account Dormancy help topic), S29 (application review help topic).
- **`data/policy_facts.json`** — PF-40 (≥3 qualifying sales within first 180 days; personal orders excluded; ≈10 posts of robust original content), PF-41 (180-day dormancy gate), PF-42 (payout ≈60 days after month end), PF-43 (US payment minimums $10/$10/$100 + $15 check fee).
- **`README.md`** — rows for `research/` and `docs/`, PF range corrected to 43.
- **Conflict note:** PR #4 (`arena/a9cafea1-zone3`, merged while this PR was open) had created its own `docs/executive-summary.md`. Resolution: main's version stays canonical; session 33226b37-zone3's summary preserved as `docs/executive-summary-33226b37.md`. Nothing discarded.
- No flags were changed; no product rows were changed.

Independent findings that corroborate existing entries (logged, not re-numbered): the S08–S10 Page-Not-Found results, the FLG-001 nine-character finding, and the S11–S13 redirect targets all reproduce exactly; the short-link redirects were re-fetched repeatedly across two sessions with identical targets (deterministic mapping — detail recorded in `research/verification-log.md` §1.5); FLG-017's FTC-2023 resolution was independently confirmed via the FTC's Endorsement Guides page.

## Merge log

| PR | Branches | Result |
|---|---|---|
| PR #1 | `arena/26634cd5-zone3` → `main` | merged 2026-11-13 (commit 8cc2d4a) |
| PR #2 | `arena/45ec61ec-zone3` | closed (not merged) |
| PR #3 | `arena/66a80e53-zone3` → `main` | merged 2026-11-13 (commit cc26993) |
| PR #4 | `arena/a9cafea1-zone3` | open (other session) |
| PR #5 | `arena/7f84fea4-zone3` → `main` | merged 2026-11-13T22:51:59Z (commit 22e6c97) |
| PR #6 | `arena/7f84fea4-zone3` → `main` | merged 2026-11-13 (commit 96ad628) |
| PR #7 | `arena/33226b37-zone3` → `main` | https://github.com/kanlerxz87-cyber/Zone3/pull/7 — merged immediately without approval per the tasking brief (merge commit recorded by GitHub); post-merge GitHub Pages build result verified via the Pages API and posted as a PR comment. |

## Task log

- **2026-11-13 — 7f84fea4**: claimed T1–T3 and pushed (commit `28e5029`). Later commits: `ed1a796` (base), `2069837` (site, data, checker, flags, PF).
- **2026-11-13 — 7f84fea4**: discovered that `main` had moved to 8cc2d4a (PR #1 merged). Logged the add/add conflicts above, resolved them on this branch, and archived the other session's files. No other branch was edited.
- **2026-11-13 — 7f84fea4**: re-read the official pages listed above. Added PF-22–37, removed PF-14, updated PF-07, PF-08, PF-13, PF-18. Added FLG-015–020.
- **2026-11-13 — 7f84fea4**: main moved to cc26993 (PR #3 merged). Integrated the same way (archive, this branch's shared files kept). Read Commission Tables 1 and A (S25, S26); added PF-38 and PF-39, FLG-021, and a reference-rate table on the Pricing page. Disclosure page is now a redirect to content.html.
- **2026-11-13 — 7f84fea4**: PR #5 (`arena/7f84fea4-zone3` → `main`): https://github.com/kanlerxz87-cyber/Zone3/pull/5 — **merged** at 2026-11-13T22:51:59Z (merge commit 22e6c97). Pages build 1367507533 for 22e6c97: **built**. Live site checked with the fetch tool: dashboard and Pricing page render.
- **2026-11-13 — 7f84fea4**: fix found on the live Pricing page: all three product rows cited S08 (product 1's page). Each row now cites its own `amazon.com/dp` check (S08, S09, S10). Shipped as a follow-up PR (see below).
- **2026-11-13 — 7f84fea4**: T6 status: done once the follow-up PR merges and the Pages build for it reports `built`.
- **2026-11-13 22:45 UTC — 33226b37-zone3**: claimed T1–T5 on its own board from base `ed1a796` (main still showed only a README at fetch time) and pushed the claim before any fetch of `main`. Completed independent verification (`research/`, `docs/`).
- **2026-11-13 — 33226b37-zone3**: discovered `main` had moved twice (PR #1 at 8cc2d4a, then PRs #3/#5/#6 at 96ad628 with the Sxx/PF/FLG schema). Its earlier add/add conflicts on COORDINATION.md and data/products.json (vs PR #1) were resolved by keeping the merged versions in full; after seeing PRs #5/#6 the branch was reset to `main` and reduced to additive contributions only. Logged here per the no-clobber rule.
- **2026-11-13 — 33226b37-zone3**: merged S27–S29 and PF-40–43 into the canonical data layer (schema-compliant), added `research/` and `docs/`, updated README and this board. `scripts/build_site.py` re-run (no page changes) and `scripts/check_site.py` passes. PR: see merge log below.
