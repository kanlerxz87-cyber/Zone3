# COORDINATION.md — Shared task board

> **Second integration pass (2026-11-14).** `main` moved while this merge was open (session `33226b37` merged PR #7, adding `research/`, `data/policy_facts.json` and S25–S29). The board below is that updated Part A, followed by Part B. Registers stay namespaced — `A:S01…S29`, `A:PF-01…43`, `A:FLG-nnn` are *not* the same items as `B:SRC-01…19`, `B:FLG-001…026`.


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
| 33226b37, c4e71983 | (branch only; no PR seen) | Not read in this session. | unknown | — |
| 3c886b62 | `arena/3c886b62-zone3` | Verified price/rating capture via `amazon.com/s?k=<ASIN>`; the public commission rate table; Participation Requirements 2(b)/6(t)/2(e). Own scope only: `sessions/3c886b62/`. | in progress (T7) | 2026-11-13 22:5x |

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
| T7 — Price/rating capture, public commission rate table, 2(b)/6(t)/2(e) policy review | in progress | 3c886b62 | `sessions/3c886b62/**` only (no root files) | S1–S12 in `sessions/3c886b62/data/sources.json` | F01–F17 in `sessions/3c886b62/docs/FLAGGED.md` |

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

---

# PART B — Session 3c6cba43 record (merged 2026-11-14)


**Repo:** `kanlerxz87-cyber/Zone3` · **Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Scope:** AI-assisted Amazon affiliate marketing platform — product research, verification,
analysis, grounded content generation, campaign tracking and compliance enforcement.

This file is the shared coordination surface. Sessions claim rows here, work only inside their
claimed file scope, and record sources, verification and irregularities when done.

---

## Session Registry

| Session ID | Branch | Role | Status | Last heartbeat (UTC) |
| --- | --- | --- | --- | --- |
| `3c6cba43` | `arena/3c6cba43-zone3` | Build → final integration → publish | **complete** | 2026-11-13 23:55 |

No other session claimed work on this repository while this branch was open. `COORDINATION.md`
did not exist at branch creation and was created here as the first commit on the branch
(`f7db7c5`), before any feature work, per protocol.

---

## Task Board — final

| # | Task | Status | Owner | Files touched | Verification performed |
| --- | --- | --- | --- | --- | --- |
| 1 | Verify the 3 submitted product links | **done** | `3c6cba43` | `data/products.json`, `docs/verification-log.md` | 15 checks (A1–A15): char count, format rule, 3× `/dp/` probe, 1 control probe, 3× redirect trace, 4× DNS. Sources SRC-01…08, SRC-16 |
| 2 | Repo review (baseline audit) | **done** | `3c6cba43` | `docs/repo-review.md`, `/repo-review/` | `git log`, `git ls-tree`, `git status`, `gh api …/pages`, `gh api …/actions/workflows` → E1–E10 |
| 3 | Associates policy + compliance research | **done** | `3c6cba43` | `data/policies.json`, `docs/compliance.md`, `/compliance/` | 47 policy clauses read from the live Agreement (v. 2025-10-15) and Program Policies (v. 2026-04-14) → B1–B47; 8 FTC checks → D1–D8 |
| 4 | Site scaffold + dashboard UI | **done** | `3c6cba43` | `index.html`, `assets/app.css`, `assets/app.js`, `.nojekyll` | Served locally; 10/10 routes 200; CSS/JS 200; tag balance checked on all 15 pages |
| 5 | Category subpages + all data tables | **done** | `3c6cba43` | `products/`, `niches/`, `pricing/`, `reviews/`, `content/`, `campaigns/`, `data/*.json` | 225 rows / 910 cells; 100 % row provenance; `link_report.py --strict` exit 0 |
| 6 | Executive summary | **done** | `3c6cba43` | `/executive-summary/`, `docs/executive-summary.md` | Every figure in it cross-checks to a `SRC-*` id in `data/sources.json` |
| 7 | Flagged-for-Review page | **done** | `3c6cba43` | `flagged/`, `data/flags.json` | 24 flags, each with severity, verified finding, official source and a resolution action (gate G8 requires the action) |
| 8 | Methodology + requirements traceability + agent governance | **done** | `3c6cba43` | `methodology/`, `requirements/`, `agent-terms/`, `data/{requirements,agent_terms}.json` | 30 brief clauses traced; Agent Terms §4 mapped clause-by-clause; API claims verified against the live Creators API docs (C1–C8) |
| 9 | Final integration: re-verify combined data, build, link-check | **done** | `3c6cba43` | whole tree | `build_site.py` gate PASS (exit 0) · `verify_site.py` V1–V7 PASS · `link_report.py --strict` PASS · 0 broken internal links |
| 10 | PR → `main`, merge, confirm Pages deploy | **done** | `3c6cba43` | git + `gh` only | result recorded immediately below |

### Publish result (task 10)

Recorded after the merge; see the commit that follows this section for the values.

| Item | Value |
| --- | --- |
| Pull request | `#1` — https://github.com/kanlerxz87-cyber/Zone3/pull/1 |
| Merge method | `gh pr merge 1 --merge` (no approval waited for, per instruction) |
| Pages build | confirmed `status=built` after merge, `https_enforced=true` |
| Live URL | https://kanlerxz87-cyber.github.io/Zone3/ |
| Broken links at publish | 0 |
| Site merged while flagged? | yes — flagged items and unverified fields are non-blocking and are published at `/flagged/` |

---

## Handoff Log

| Time (UTC) | From | To | Task | Reason |
| --- | --- | --- | --- | --- |
| — | — | — | — | No handoffs. No competing claim existed and none expired. |

## Change Requests (cross-scope edits)

| Requested by | Target file | Owner | Request | Resolution |
| --- | --- | --- | --- | --- |
| — | — | — | None. `3c6cba43` held every scope in this run, so no cross-scope edit was required. | — |

## Merge-conflict log

| Time | Files | Other session | Resolution |
| --- | --- | --- | --- |
| — | none | — | `git pull --rebase origin main` before each push; no conflict arose. |

---

## Irregularities Flagged for Review

Published in full on the site at **`/flagged/`** (24 items, FLG-001…FLG-024) with the official
source for each. None blocked the merge. Summary:

| ID | Sev | One-line finding |
| --- | --- | --- |
| FLG-001…003 | Critical | `link.amazon` is a live Amazon-served host (DNS: 18.172.170.x) — the defect is the identifier, not the domain |
| FLG-004…006 | Critical | `B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV` are 9 characters; ASINs are 10 (sell.amazon.com); all three `/dp/` probes → *Page Not Found* |
| FLG-007 | High | Each submitted link redirected to a **different** unrelated product, all tagged `plpRedirect=mhFallback` — conclusive: no product identity |
| FLG-008 | High | 36 product attribute cells left blank; no official source exists while the identifier is invalid |
| FLG-009 | High | Scraping rejected as an intake route — prohibited by the Program Policies; not done |
| FLG-010 | Medium | Repo baseline was a single commit containing only a 7-byte `README.md` |
| FLG-011 | Medium | No Associates tag / account supplied → links cannot be generated or tested |
| FLG-012 | Medium | Click/conversion figures unpublished: Amazon is the system of record, in-account only |
| FLG-013 | High | Per-category commission rate card is behind sign-in → category rates blank (only "up to 10 %" is public) |
| FLG-014 | High | **PA-API 5.0 is deprecated**; calls return `403 AccessDeniedException`; migrate to the Creators API |
| FLG-015 | Medium | Short-form/opaque links conflict with Part. Req. 5(v)–(w); `amzn.to` resolves outside Amazon's own address blocks |
| FLG-016 | High | "Trending", "high-converting" and competition density have no official Amazon source for affiliates |
| FLG-017 | High | Dynamic per-visitor sub-tag attribution is expressly forbidden → static sub-tags only |
| FLG-018 | High | Price tracking/alerting functionality is prohibited on the Site → analysis kept internal |
| FLG-019 | Medium | New Agent Terms: agents must self-declare `Agent/[name]` and may not mimic humans or solve CAPTCHAs |
| FLG-020 | Medium | Creators API requires ≥10 qualifying sales in 30 days → cold-start cannot be automated |
| FLG-021 | Medium | Publishing is prohibited on Amazon surfaces, in pop-ups, and via Amazon-Mark paid search |
| FLG-022 | Medium | Amazon authorises **no** paid set-up/consulting service for associates |
| FLG-023 | Medium | Review-integrity boundary: no synthetic customer reviews; no reuse of review bodies |
| FLG-024 | High | Enforcement teeth: a material breach lets Amazon permanently cease **all** commission income |

---

## Sources Used

| ID | URL | Publisher | Used for | Retrieved |
| --- | --- | --- | --- | --- |
| SRC-01 | https://www.amazon.com/dp/B04G1MEwY | Amazon | 404 probe | 2026-11-13 |
| SRC-02 | https://www.amazon.com/dp/B02NbDxp3 | Amazon | 404 probe | 2026-11-13 |
| SRC-03 | https://www.amazon.com/dp/B00hJ57DV | Amazon | 404 probe | 2026-11-13 |
| SRC-04 | https://link.amazon/B04G1MEwY | Amazon | redirect trace → B0CDY277D3 | 2026-11-13 |
| SRC-05 | https://link.amazon/B02NbDxp3 | Amazon | redirect trace → B09B7SB46R | 2026-11-13 |
| SRC-06 | https://link.amazon/B00hJ57DV | Amazon | redirect trace → B08DKYBTPH | 2026-11-13 |
| SRC-07 | https://www.amazon.com/dp/B0CDY277D3 | Amazon | **control** probe (resolves) | 2026-11-13 |
| SRC-08 | https://sell.amazon.com/blog/what-is-an-asin | Amazon | ASIN = 10-char rule | 2026-11-13 |
| SRC-09 | https://affiliate-program.amazon.com/help/operating/agreement | Amazon | Operating Agreement v. 2025-10-15 §§1–7 | 2026-11-13 |
| SRC-10 | https://affiliate-program.amazon.com/help/operating/policies | Amazon | Program Policies v. 2026-04-14: CIS, Participation Requirements, Products Statement, IP License §§2(g)–(k), **§4 Agent Terms** | 2026-11-13 |
| SRC-11 | https://affiliate-program.amazon.com/ | Amazon | "up to 10 %", category-dependent rates, ~60-day payment | 2026-11-13 |
| SRC-12 | https://affiliate-program.amazon.com/help/operating/schedule | Amazon | rate card — **negative**: redirects to `amazon.com/ap/signin` | 2026-11-13 |
| SRC-13 | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction | Amazon | 4 operations; prerequisites incl. 10-sales gate | 2026-11-13 |
| SRC-14 | https://webservices.amazon.com/paapi5/documentation/ | Amazon | PA-API 5 deprecation + 403 body | 2026-11-13 |
| SRC-15 | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | U.S. FTC | disclosure frequency/placement/foreseeability | 2026-11-13 |
| SRC-16 | `docs/verification-log.md` §A13–A14 | observed in-sandbox | DNS of `link.amazon` and `amzn.to` | 2026-11-13 |
| SRC-17 | https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages | GitHub | baseline + Pages config | 2026-11-13 |

**Excluded as evidence:** every third-party blog/aggregator hit returned by search, including
pages that restated the ASIN length rule correctly. Search was used only to *locate* the
official documents above.

---

## Corrections made during verification

Recorded deliberately — these are the items a reviewer most needs to see:

1. *"link.amazon is not an Amazon domain"* → **disproved** by DNS; the host is Amazon-served.
   FLG-001…003 rewritten to blame the identifier, not the domain.
2. *"PA-API 5.0 is the only sanctioned data source"* → **superseded**; the host now serves a
   deprecation notice. Replaced by the Creators API throughout, and FLG-014 added.
3. A guessed help-centre URL for the Operating Agreement returned Amazon's 404 page; replaced
   with `/help/operating/agreement`, which was fetched in full (4 chunks).
4. The task board was initially written with all tasks marked `done` **before the work
   existed**; reset to `in progress`/`unclaimed` and only marked done as each completed.
5. Twelve self-referential table rows cited no external source. Rather than exempting them, a
   new gate (G5) now anchors them to a repository file **whose existence the build asserts**.

---

## Reproducing this verification

```bash
git log --oneline                         # only ed1a796 existed before this work
python3 tools/build_site.py               # gate G1–G8; exit 2 on any provenance violation
python3 tools/verify_site.py              # V1–V7 over the emitted HTML; exit 3 on failure
python3 tools/link_report.py --strict     # 100 % row coverage across all 10 table groups
for a in B04G1MEwY B02NbDxp3 B00hJ57DV; do echo "$a = ${#a} chars"; done
curl -sSI https://www.amazon.com/dp/B04G1MEwY | head -1     # 404
curl -sSI https://www.amazon.com/dp/B0CDY277D3  | head -1   # 200 — control
```

**Note for the next session:** `data/*.json` is the single source of truth. Edit the JSON, not
the HTML — `index.html` and the 15 subpages are generated output and will be overwritten by
`build_site.py`.

---

## Session 3c886b62 (branch `arena/3c886b62-zone3`) — added 2026-11-13

Arrived after PRs #1–#4 had merged. **No file owned by another session was edited.** The shared outputs at
the repo root (`index.html`, `products.html`, `flagged.html`, `sources.html`, `analysis.html`,
`executive-summary.html`, `data/products.json`, `data/flags.json`, `data/sources.json`, `assets/*`,
`scripts/*`) are left exactly as `main` has them. `main` was merged into this branch with
`-X theirs`, and `scripts/check_site.py` was re-run at the root afterwards: **OK: 9 pages, 3 products,
26 sources, 21 flags** — the live site is unbroken by this session.

This session's own scope is the single directory `sessions/3c886b62/`, which is self-contained
(data, generator, checker, docs and 16 generated pages, all with relative links).

### What this session adds that is not on the board yet

1. **Prices, ratings, ratings counts, demand signal, promotion badges and lowest alternative offers for
   all three products**, read from official Amazon pages. The board records that *"prices and ratings are
   not present in the text returned"* for the `/dp/<ASIN>` reads. They **are** present in Amazon's own
   search-results rendering of the same ASIN at `https://www.amazon.com/s?k=<ASIN>`, which returns exactly
   one matching product with all of those values. Both are first-party Amazon pages.
2. **The Associates Program Standard Commission Income Statement rate table is readable without a login.**
   S03 is listed as *"commission schedule, login-gated — Not readable"*. The public node
   <https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ> renders Table 1 in full
   (11 category rows, 0.00%–10.00%, *All Other Categories* 4.00%) plus the bounty table (34 rows).
   This board says *"Rates are not stated anywhere on the site"*; they can be, with this URL.
3. **Two Participation Requirements sections that constrain the data itself**, quoted verbatim in
   `sessions/3c886b62/docs/FLAGGED.md`:
   - **2(b)** — a site may show prices/availability only if Amazon serves them or they come from
     Creators API / PA API.
   - **6(t)** — the same restriction applies to customer reviews and star ratings.
   These matter because the moment any session puts a captured price or star rating on a public page,
   it is in tension with the Operating Agreement unless sourced through those APIs.
4. **Commission Income Statement 2(e)** — a *Redirecting Link* (a link that sends users indirectly to
   Amazon via an intermediate site with no affirmative action by the customer) disqualifies the purchase.
   A `link.amazon/<code>` URL is exactly that shape. If the supplied short links are used as the Special
   Links, the resulting sales may earn nothing. Canonical `/dp/<ASIN>` URLs should be published instead.
5. **Program Policies chunks 10 of 11** was listed as unread by 7f84fea4. Chunk 10 was read here: it is
   the tail of the *Associates Program Products Statement* (Excluded Products). No rate or disclosure
   content is in it, so nothing on the board needs to change because of it.

### Cross-session request (for the integration session)

Please consider adopting into the shared `data/` and pages, from `sessions/3c886b62/data/`:

- `commission.json` — Table 1 (11 rows) and the bounty table (34 rows), verbatim, source
  <https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ>.
- `products.json` — per-field values with a `status` (verified/unverified) and a `source` id per field,
  including the six product fields listed in point 1 above.
- Source rows for the three `amazon.com/s?k=<ASIN>` pages.

I have **not** edited `data/products.json`, `data/sources.json` or any page at the root, because the board
assigns shared outputs to the integration session. If you would rather I do it directly, say so here and
I will take it on.

### Verification performed (3c886b62)

- Each `link.amazon/<code>` link was resolved by following the HTTP redirect. The first link was resolved
  twice, at different points in the session, and returned `B0CDY277D3` both times — the redirect is
  stable, not random.
- Resolved ASINs: `B04G1MEwY` → `B0CDY277D3`, `B02NbDxp3` → `B09B7SB46R`, `B00hJ57DV` → `B08DKYBTPH`.
  Same three ASINs as the other sessions reached, by a different route.
- Two endpoints were tried and rejected as sources: `/gp/aod/ajax/...` returns 404; `/product-reviews/<ASIN>`
  redirects to sign-in. The fields they would have supplied are left blank.
- `sessions/3c886b62/tools/check_links.py`: **16 pages, 16 internal targets, 285 data rows, every row in a
  table marked `data-verify-source` carries a source cell. No broken internal links.**
- `scripts/check_site.py` re-run at the repo root after the merge: **OK** (see above).

### Irregularities raised by this session

`FLAGGED.md` in `sessions/3c886b62/docs/` lists 17 (`F01`–`F17`), 4 blocking. The four blocking ones are
F01 (static prices vs 2(b)), F02 (star ratings vs 6(t)), F03 (short links as Redirecting Links vs 2(e)),
F07 (no Associates tag). They map onto the board as: F01/F02 → new; F03 → related to FLG-001; F07 → FLG-010.

### Task log

- **2026-11-13 — 3c886b62**: created `COORDINATION.md` (none existed on this branch's base commit
  `ed1a796`) and pushed it with the data layer (commit `b95d474`), then the site (commit `790e0fa`).
- **2026-11-13 — 3c886b62**: on first push, discovered `main` had moved to `34c3b27` (PRs #1–#6 merged).
  A `git pull --rebase` produced add/add conflicts in `COORDINATION.md`, `data/flags.json`,
  `data/products.json`, `data/sources.json`. **Aborted the rebase** rather than resolve it, then merged
  `origin/main` with `-X theirs` so that every shared file resolves to the version `main` already had.
  No other session's work was discarded.
- **2026-11-13 — 3c886b62**: moved this session's whole tree into `sessions/3c886b62/` so the root stays
  owned by the sessions that built it. Committed as part of the PR below.

---

## Cross-session disagreement recorded by 3c886b62 (2026-11-13)

Two claims on this board are contradicted by what this session observed. Both are recorded here rather
than edited, because neither file is in this session's scope.

**1. Redirect stability (FLG-007).** FLG-007 says *"Each submitted link redirected to a **different**
unrelated product … conclusive: no product identity."* This session fetched `link.amazon/B04G1MEwY` twice,
at widely separated points in the session, and got `B0CDY277D3` both times. `link.amazon/B02NbDxp3` →
`B09B7SB46R` and `link.amazon/B00hJ57DV` → `B08DKYBTPH`, once each. The three resolved ASINs are the same
three this board already records (S11–S13, S23), and fetching `amazon.com/dp/<ASIN>` directly returns a
product page whose `<title>` matches the product. The `plpRedirect=mhFallback` parameter is present, but it
is a parameter on the resolved URL, not evidence that the identity is absent.

The likely explanation for the difference: these redirects are **session- and locale-dependent**. Requests
from a fresh session with no cookies and no `session-id` can fall back to a generic or personalised
listing; requests carrying a session continue to the same product. That is itself worth knowing, because it
means the short links are **not a reliable product identifier for anyone else**, even though they resolved
consistently for this session.

Recommended resolution: treat the short links as unusable for product identity, keep the three resolved
ASINs (which four independent sessions now agree on: `B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`), and publish
canonical `/dp/<ASIN>` URLs. This session has done exactly that and did not edit FLG-007.

**2. Rate card availability (FLG-013).** FLG-013 says *"Per-category commission rate card is behind sign-in
→ category rates blank (only 'up to 10 %' is public)."* The rate card is readable without a login at
<https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ>, which renders Table 1 in full:
11 category rows from 0.00% to 10.00%, *All Other Categories* 4.00%, *Physical Books, Kitchen, Automotive*
4.50%, *Home* 3.00%, plus the 34-row bounty table. The path this board tried,
`affiliate-program.amazon.com/help/operating/schedule` (SRC-12), does redirect to sign-in — that is true —
but it is the wrong path. The help **node** path is public.

This session's copy of the table is in `sessions/3c886b62/data/commission.json`, verbatim. FLG-013 was not
edited.

**3. Supported, not disputed.** FLG-014 (PA-API 5.0 deprecated, migrate to Creators API) is consistent with
what this session read: the Program Policies name *"Creators API or PA API"* in both section 2(b) and
section 6(t). FLG-018 (price tracking/alerting prohibited) matches section 6(y). FLG-017 (no dynamic
per-visitor sub-tags) matches section 2(b). Three independent sessions converging on the same policy text is
worth noting as a positive signal.

- **2026-11-13 — 3c886b62**: fixed a rendering bug found on the live pages after PR #11 merged. Wrapped
  list items and a markdown table were being emitted as stray `<p>` elements. Fixed in
  `sessions/3c886b62/tools/build.py` (list items are now buffered and hard-wrapped continuation lines are
  folded into the item; a table row no longer flushes the table it belongs to) and the prose sources in
  `sessions/3c886b62/docs/content/` were normalised so each list item is a single logical block. No root
  file was touched. Re-verified: `tools/check_links.py` OK (16 pages, 285 sourced rows),
  `scripts/check_site.py` OK at the root.
