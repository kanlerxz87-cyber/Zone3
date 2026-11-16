# Line-by-line repository review — session `1f1b8bd2`

**Date:** 2026-11-16 (UTC) · **Branch:** `arena/1f1b8bd2-zone3` · **Base:** `933e2f3` (= `origin/main`)
**Scope:** 1F-T2 of the shared task board. Read-only against every other session's files; the only
edits made are recorded in §"Changes made" and in `COORDINATION.md` Part 1F.

## 1. What the repository contains (inventory at base)

| Layer | Owner session(s) | Contents | State found 2026-11-16 |
|---|---|---|---|
| Root flat site (13 pages) | 7f84fea4 + integrations | `index.html`, `executive-summary.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `content-topics.html`, `campaigns.html`, `flagged.html`, `sources.html`, `suggestions.html`, `decision-center.html`, `air-fryers.html` + redirect stubs (`analysis.html`, `disclosure.html`, `marketing.html`, `flagged-for-review.html`, `categories/home-kitchen-air-fryers.html`) + `404.html`, `landing-prior.html` | intact; generator reproduces all root pages byte-identically |
| Directory build (16 pages) | 3c6cba43 | `dashboard/`, `products/`, `niches/`, `pricing/`, `commission/`, `reviews/`, `content/`, `campaigns/`, `compliance/`, `agent-terms/`, `methodology/`, `requirements/`, `repo-review/`, `flagged/`, `executive-summary/`, `sources/`, `tools/`, `data/z3/` | intact; `tools/verify_site.py` PASS |
| Marketing section (7 pages) | 3d359c23, 54ce6a2b | `marketing/{index,briefs,buying-guide,comparison,product-1..3}.html` via `scripts/build_marketing.py` | **stale at base** — see finding 1F-F-03 (fixed) |
| `/docs/` sub-site | 79f85104 | 8 pages | intact (71-F-04 exposure stands, other session's scope) |
| Session sub-sites | 3c886b62, 03bbd050, 3ead7ac8, 25513d33, 71dc8fea (added this session) | `sessions/**` | intact; own checkers pass |
| Data registers | cumulative | `sources.json` 51→**52**, `flags.json` 78→**81**, `products.json` 3, `policy_facts.json` 55, `suggestions.json`, `topics.json`, `marketing.json`, `competition.json`, `commission.json` + snapshots | consistent; no dangling refs after additions |
| Generators/checkers | several | `scripts/{build_site,build_marketing,build_sitemap,check_site,check_all_links}.py`, `tools/{build_site,verify_site,link_report}.py` | all run green at base except the marketing idempotence gap (1F-F-03) |
| Records | many | `research/*-verification-log.md`, `research/*-repo-review.md`, `docs/`, `EXECUTIVE-SUMMARY.md`, `COORDINATION.md` (534 KB, 4,999 lines) | intact; exec-summary counts stale → 1F-F-02 (fixed) |

## 2. Checks run (base `933e2f3`, 2026-11-16)

| # | Check | Method | Result |
|---|---|---|---|
| R1 | Root site gate | `python3 scripts/check_site.py` | **OK** — 13 pages, 3 products, 51 sources, 78 flags |
| R2 | Whole-tree verifier | `python3 tools/verify_site.py` | **VERIFY PASS** — 74 pages, 1,333 rows, 1,128 sourced, 406 flagged, 86 repo-anchored, **0 advisories** |
| R3 | Provenance coverage | `python3 tools/link_report.py --strict` | **exit 0** — no dangling refs, no uncited sources |
| R4 | Internal + external link audit | `python3 scripts/check_all_links.py` | **120 pages, 105 external URLs, 0 errors** |
| R5 | Sitemap coverage | `python3 scripts/build_sitemap.py --check` | **exit 0** — 69 pages, 0 extra (redirect stubs excluded by design) |
| R6 | Directory session site | `python3 sessions/3c886b62/tools/check_links.py` | **OK** (per prior records; tree untouched by this session) |
| R7 | Conflict markers | line-anchored `git grep` | **0 files** |
| R8 | Secrets/credentials | pattern scan outside archives/sessions prose | **0 hits**; `.gitignore` covers `.env*` |
| R9 | Duplicate nav destinations | per-page `<nav>` href scan (root + marketing) | **0 pages** at base |
| R10 | Generator idempotence — `scripts/build_site.py` | run twice, `git status` | **clean** |
| R11 | Generator idempotence — `scripts/build_marketing.py` | run at base, `git diff` | **6 pages changed by one nav line each** → **1F-F-03**, fixed |
| R12 | Exec-summary register counts | hand-written numbers vs `data/flags.json` | **stale** (72 stated / 78 held) → **1F-F-02**, fixed |
| R13 | FTC citation coverage | `data/sources.json` vs the FTC pages fetched today | **gap**: Rule on the Use of Consumer Reviews and Testimonials not cited → **1F-F-01** (S59 added, flag published) |
| R14 | Pages deployment | GitHub Pages API | `status=built`, latest build = base commit `933e2f3` (2026-11-15T12:00:53Z) |
| R15 | Brief-deliverable reachability | existence + `index.html` link check for suggestions, decision center, executive summary, content topics, content, marketing hub/briefs/guide/comparison, flagged, products, pricing, reviews, campaigns, sources, air-fryers | **all present and linked**; `analysis.html` unlinked because it is a canonical redirect stub by design (C3-F-01 disposition) |

## 3. Irregularities raised by this session

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| 1F-F-01 | Medium (open) | The source register and compliance pages do not cite the FTC **Rule on the Use of Consumer Reviews and Testimonials** (16 CFR Part 465, effective 2024-10-21 per the FTC's own Q&A) — directly relevant to this site's comparison/buying-guide/review content (fake reviews, incentivized reviews, §465.6 fake-"independent" site rule). | **Published for review** — source **S59** added (fetched 2026-11-16), flag on `flagged.html` with change request. Non-blocking. |
| 1F-F-02 | Low (fixed) | `EXECUTIVE-SUMMARY.md` current-state counts (§2, §6) were stale: 72 flags stated vs 78 held — reproduces 54C-F-02's drift prediction. | **Fixed**: §2/§6 updated to post-addition register values (81 flags: 3/13/22/26/17; 52 sources; 55 policy facts). Dated historical gate bullets left untouched. Change request to generate counts stands. |
| 1F-F-03 | Low (fixed) | The six generated `marketing/*.html` pages were stale vs `scripts/build_marketing.py` (missing the Suggestions nav entry), so the "generators idempotent" gate claim from sessions 25/54C no longer reproduced at base. | **Fixed** by regenerating the six pages — the same navigation-only sync session cd0e6279 performed for the Decision Center. No copy/data changed. |

Carried forward (not raised anew; see their own registers): 71-F-01/02/04 (verifier manifest bug,
provenance-gate strictness, `/docs/` + session-archive price/rating exposure), FLG-001/002/003/010
(product intent, link model, missing tag), FLG-022 (price/rating display), FLG-027 (identity vs
intent), 54C-F-05/06 (source-ID aliases; S46–S48 note literals), the six unreferenced-but-published
flag IDs from `link_report --strict`.

## 4. Changes made by this session (all logged in `COORDINATION.md` Part 1F)

| File | Change | Why |
|---|---|---|
| `data/sources.json` | +S59 (FTC Consumer Reviews Rule Q&A) | 1F-F-01 |
| `data/flags.json` | +1F-F-01, +1F-F-02, +1F-F-03 (with `repo_evidence` where source-less) | brief requires irregularities published on Flagged for review |
| `EXECUTIVE-SUMMARY.md` | §2/§6 counts corrected; §7 adds the 2026-11-16 re-verification bullet | 1F-F-02 |
| `marketing/*.html` (6) | regenerated (one nav line each) | 1F-F-03 |
| root pages `index/flagged/sources/executive-summary.html` | regenerated from data by `scripts/build_site.py` | publish the above |
| `sitemap.xml` | regenerated by `scripts/build_sitemap.py` (no URL-set change) | routine |
| `sessions/71dc8fea/verification-2026-11-14.md` | taken over verbatim from stale PR #71 | 60-minute takeover rule |
| `research/1f1b8bd2-*` (2 files) | this session's records | board scope |
| `COORDINATION.md` | Part 1F + Part 71 takeover | append-only |

## 5. Verdict

The tree at `933e2f3` is internally consistent: every published fact row carries an official
source link or an explicit flag/repo anchor, all five gates pass, links resolve, and the deployed
Pages build matches `main`. Three defects were found and two were fixed here (1F-F-02, 1F-F-03);
the third (1F-F-01) is published for owner review as the brief requires. No value was inferred,
and no cell that lacks an official source was filled.
