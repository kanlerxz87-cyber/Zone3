# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/Zone3` · Live site (GitHub Pages, source `main` `/`, legacy build): https://kanlerxz87-cyber.github.io/Zone3/

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for review page; does not block anything).

## Session registry

| Session ID | Branch | Role | Claimed at (UTC) | Last heartbeat (UTC) |
|---|---|---|---|---|
| 7f84fea4 | `arena/7f84fea4-zone3` | Repo review, source verification, site build, integration, PR, merge | 2026-11-13 22:55 | 2026-11-13 23:20 |

### Branch note (read first)

- The brief asks for `session-<id>/<task>` branches. The Arena session rule for this run fixes the working branch to `arena/7f84fea4-zone3`. This session creates and pushes no other branch, so every task is done on this one branch.
- Other session branches exist on the remote and were read only (no edits, no pushes): `arena/26634cd5-zone3`, `arena/3c6cba43-zone3`, `arena/a9cafea1-zone3`. Each also created a `COORDINATION.md` and claimed overlapping tasks on its own branch. **Merging them into `main` later will conflict** in this file and in the site files. The integration session that merges them must reconcile the task board, the data files and the site, then re-run `scripts/check_site.py` (see FLG-008).

## Task board

| Task | Status | Owner | Files in scope |
|---|---|---|---|
| T1 — Repo review (baseline audit, irregularities) | done | 7f84fea4 | `COORDINATION.md`, `README.md` |
| T2 — Source verification (official sources, line by line) | done | 7f84fea4 | `data/sources.json`, `data/products.json`, `data/policy_facts.json`, `data/flags.json` |
| T3 — Site build (landing dashboard, category pages, flagged page, sources page) | done | 7f84fea4 | `index.html`, `executive-summary.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `flagged.html`, `sources.html`, `assets/style.css`, `.nojekyll` |
| T4 — Generator and verification script | done | 7f84fea4 | `scripts/build_site.py`, `scripts/check_site.py` |
| T5 — Executive summary | done | 7f84fea4 | `executive-summary.html` (the summary is on the site; no separate file) |
| T6 — Integration: build, link check, PR → `main`, merge, Pages deploy confirmation | in progress | 7f84fea4 | all (integration only) |

## Task results

### T1 — Repo review (done)

- **What was reviewed:** `main` at `ed1a796`: one commit, one file (`README.md`, 7 bytes, `# Zone3`). No licence, `.gitignore`, data, code or site. Pages was already enabled on `main` at `/` with the legacy build (checked with `gh api repos/kanlerxz87-cyber/Zone3/pages`).
- **Sources:** S20 (commit), S21 (branches), S22 (Pages API). See `data/sources.json`.
- **Verification:** `git log`, `git ls-remote origin`, `git fetch` of all `arena/*` refs, `gh api` for Pages, and a byte count of `README.md`.
- **Irregularities:** FLG-008 (overlapping session branches), FLG-009 (no licence, single-file baseline), FLG-007 (another branch cites PA-API 5 as the sanctioned source; the official notice says it is deprecated).

### T2 — Source verification (done)

- **Official sources read (2026-11-13):** S01 Operating Agreement; S02 Program Policies (Participation Requirements, Commission Income Statement, Products Statement); S04 Creators API introduction; S05 PA-API 5 deprecation notice; S06 Creators API GetItems; S07 FTC Disclosures 101; S19 Associates link on amazon.com.
- **Not accessible:** S03 commission schedule (redirected to sign-in); S18 Seller Central ASIN page (error page).
- **Third-party (flag only, never a fact):** S17.
- **Product checks:** each of the three identifiers was typed as `amazon.com/dp/<ID>` (S08–S10). Each submitted `link.amazon` link was fetched twice (S11–S13) and each landing page's title was read (S14–S16). Identifier lengths were computed with Python (9, 9, 9 characters; the redirect IDs are 10 characters).
- **Quotes:** 21 verbatim policy quotes in `data/policy_facts.json` (PF-01 to PF-21), each with its section number.
- **Irregularities:** FLG-001 to FLG-007, FLG-010 to FLG-014.

### T3 — Site build (done)

- **Pages:** dashboard, executive summary, Products, Pricing and commission, Reviews and competition, Content and compliance, Campaigns and tracking, Flagged for review (14 flags), Sources (22 sources).
- **Verification:** `scripts/check_site.py` passes (9 pages, 3 products, 22 sources, 14 flags). Each page was served locally and returned HTTP 200.
- **Irregularities:** none new (all are in the flags register).

### T4 — Generator and checker (done)

- `scripts/build_site.py` (standard library only) writes every page from `data/*.json`. A null value renders as a blank cell labelled *Unverified*.
- `scripts/check_site.py` fails on: a product without an official source; a value without an official source; a table row whose Source column has no official link; a broken internal link or anchor; a non-https link; a missing disclosure line; a missing navigation bar; an executive-summary finding without a source link; a Python `None` leak.
- **Negative test (done):** a copy of the data with a product's only source set to a non-official link and a price with no official source was run through the checker. It failed on both (the checker caught both defects). Two real defects were found and fixed this way: the redirect-table row cited a non-official source, and the checker had not required an official source per value.

### T5 — Executive summary (done)

- The summary is `executive-summary.html`. It contains the bottom line, key findings (each with a source link), what was built, what is not done and why, and owner items. No separate markdown file was created.

### T6 — Integration (in progress)

- Steps: `scripts/build_site.py` → `scripts/check_site.py` → commit → push `arena/7f84fea4-zone3` → open PR to `main` → merge with `gh pr merge --merge` → confirm the Pages build status with `gh api repos/kanlerxz87-cyber/Zone3/pages/builds/latest` (must be `built`).
- The PR link and merge result are recorded in the task log below and in the PR itself.

## Irregularities for review (summary; full detail on the Flagged for review page)

| Flag | Severity | Item |
|---|---|---|
| FLG-001 | Critical | The three submitted identifiers are 9 characters, not 10-character ASINs; `amazon.com/dp/<ID>` returns Page Not Found. |
| FLG-002 | High | Each short link lands on a different product (not confirmed as the submitted one). Parameters `lv=shuf` and `plpRedirect=mhFallback`. |
| FLG-003 | Critical | link.amazon is not documented in the Associates policies read; possible Redirecting Link (Commission Income Statement §2(e)). Cross-session note: branch `arena/3c6cba43-zone3` (FLG-001 there) asserts link.amazon is not an Associates short-link domain. This session could not confirm either claim from an official source. |
| FLG-004 | High | Product name, brand, price, rating, reviews, competitor count, rank and availability unverified for all 3. |
| FLG-005 | High | Commission schedule not accessible (sign-in redirect). No rate stated. |
| FLG-006 | High | Creators API needs enrolment and ≥10 qualifying sales in 30 days. |
| FLG-007 | Medium | Other branch cites PA-API 5 as sanctioned; the official notice says it is deprecated. |
| FLG-008 | Medium | Overlapping session branches; merge conflicts expected. |
| FLG-009 | Medium | Baseline repo: no licence, single README. |
| FLG-010 | Medium | No Associates tag supplied; no Special Links created. |
| FLG-011 | Medium | No click or conversion data; campaigns ledger is empty on purpose. |
| FLG-012 | Medium | No SEO articles, comparisons or buying guides (blocked by unverified product facts). |
| FLG-013 | Low | Disclosure placement (footer) needs owner review; enrolment not checked. |
| FLG-014 | Low | Source pages show different copyright years in footers. |

## Task log

- **2026-11-13 22:55 UTC — 7f84fea4** claimed T1–T6 on `arena/7f84fea4-zone3`. Claim commit `28e5029` pushed before any other work.
- **2026-11-13 23:00–23:20 UTC — 7f84fea4** completed T1–T5: read-only checks (sources, product identifiers, redirects), data files, generator, checker, and the site. Checker negative test run and fixed. Local preview on port 8080 returned HTTP 200 for every page.
- **2026-11-13 — 7f84fea4** T6 (PR, merge, Pages confirmation): in progress; the result is recorded in the PR and in the final session report.
