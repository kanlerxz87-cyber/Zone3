# Part 2E0 — session `2e0d5c15` (branch `arena/2e0d5c15-zone3`, base `bb3d554`; rebased onto `main@957e5ab` during the session, 2026-11-20)

## 2E0 Session registry

| Session ID | Branch | Role | Status | Claimed at (UTC) |
|---|---|---|---|---|
| 2e0d5c15 | `arena/2e0d5c15-zone3` | Register-integrity + rendering-integrity audit: correct status cells whose last sentence contradicts the registers; fix unescaped-placeholder generator bugs; remove merge debris from two published files; add reviewable proposals and questions; release gates, PR to `main`, merge, Pages deploy confirmation. Files: `data/shop/brief-status.json`, `data/flags.json`, `data/publication.json` (append-only), `scripts/build_5a56c084.py`, `tools/build_site.py`, `assets/publication.css` (one marker line), `COORDINATION.md` (this Part + two marker lines), `sessions/2e0d5c15/**`, `EXECUTIVE-SUMMARY.md` (dated section). | in progress (2E0-T4) | 2026-11-20 |

## 2E0 Board read before claiming

`main` advanced five times while this branch was open (PRs #212–#221, plus #224 during the final rebase);
the branch was rebased onto each new tip before measuring again, and **every figure in this Part was
re-measured on the tree it names**. Sessions `263214e8` (two guides), `c08695c1` (front-page integration)
and `9ed0552a` (a reader page per registered listing) landed during the session; their work is kept in
full and none of it was reverted. No open PR touched this pass's files.

## 2E0 Task board

| Task | Status | Owner | Files in scope | Sources | Irregularities |
|---|---|---|---|---|---|
| T1 — Measure the registers and the rendered tree | done | 2e0d5c15 | `sessions/2e0d5c15/**` | live fetches V1–V5 | 2E0-F01…F03 |
| T2 — Correct the status cells that close on a wrong figure | done | 2e0d5c15 | `data/shop/brief-status.json` | repository measurement | 2E0-F01 |
| T3 — Fix the two unescaped-placeholder defects at their generators | done | 2e0d5c15 | `scripts/build_5a56c084.py`, `tools/build_site.py` | repository measurement | 2E0-F02 |
| T4 — Remove merge debris from two published files | done | 2e0d5c15 | `COORDINATION.md`, `assets/publication.css` | tree-wide scan | 2E0-F03 |
| T5 — Add reviewable proposals and questions, run all gates, PR, merge, confirm Pages | in progress | 2e0d5c15 | `data/publication.json` (append-only), `data/flags.json`, `EXECUTIVE-SUMMARY.md` (dated section) | V1–V5 | — |

## 2E0 Work performed

**T1 — measured, not assumed.** On the merged tree at `main@957e5ab` + this pass: 131 published pages;
27 indexable reader URLs matching 27 sitemap `<loc>` entries exactly; 13 feed items, all sitemap-canonical;
13 guides and 4 articles; the disclosure sentence on 131 of 131 pages; `og:image` and JSON-LD on 40 pages
with all 27 indexable pages carrying both; 13 of 13 guides linking the comparison table in their own body;
139 official-source table rows; 1,248 in-page fragment links with 0 broken; 356 external URLs with 0
errors; 187 flag rows, 37 proposals and 46 questions after this pass's additions. Two read-only audit
scripts ship with the pass so three of those numbers are reproducible:
`sessions/2e0d5c15/fragment_audit.py` and `sessions/2e0d5c15/nesting_audit.py`.

**T2 — four status cells corrected.** Flag `EE-F-02` had recorded rows S-04/S-05/S-09/S-24/SG-28/SG-29 as
re-measured and fixed. Read on 2026-11-20, S-07, S-13, S-24 and SG-29 still **ended** on a figure the
registers do not hold (10/9/10 guides against 11, then 13 after that day's merges; 18 sitemap URLs against
20, then 27), and SG-29 and S-24 each contradicted an earlier sentence inside themselves. A dated
correction sentence naming the merged-tree figure was appended to each; no earlier text was rewritten,
because a dated record is that date's truth. Flag `2E0-F01` records it; question `2E0-Q1` records the
procedural gap (no gate compares a row's last sentence with its register).

**T3 — two generator bugs fixed.** The nesting audit found six pages with stray end tags. Two were not
nesting accidents: the literal strings `<token>` (`data/articles.json`, rendered by
`scripts/build_5a56c084.py`) and `<short-id>` (`tools/build_site.py`) were written into HTML unescaped, so
a browser read each as an unknown element and the word vanished from the sentence — on
`products/index.html` that sentence is the one explaining why a `/dp/` Page Not Found does not mean a short
link is broken. Both were fixed **in the generators**, and the audit now reports 4 pages, all `noindex`
legacy surfaces owned by finished passes. Flag `2E0-F02`; nothing was hand-edited.

**T4 — merge debris removed from two published files.** `COORDINATION.md` carried a stray
`>>>>>>> c126257 …` line with no matching `<<<<<<<`/`=======`, and `assets/publication.css` carried a bare
`=======` line inside the served stylesheet. Neither was caught by any release check. Both were deleted
with the surrounding content of both sessions untouched; the marker then recurred once inside this
session's own rebase, which is the argument for a mechanical check rather than another sweep. Flag
`2E0-F03`; question `2E0-Q3` asks whether the gate should refuse this class and how broadly to scope it.

**T5 — five items added for review, nothing implemented.** Proposals `2E0-P1` (a reheating/leftovers guide
built on the FSIS 165°F reheat rule and the two-hour rule) and `2E0-P2` (`BreadcrumbList` markup derived
from each guide's visible trail); questions `2E0-Q1`, `2E0-Q2` and `2E0-Q3`. Each carries its official
basis, a discovery action, a falsifier and a safe default. Choosing one on the suggestions page still
records a local preference only; `data/shop/measurement.json` remains `enabled: false` and the campaign
ledger still has zero rows.

## 2E0 Verification performed

- **Re-read 2026-11-20 (live fetch):** FoodSafety.gov *Cook to a Safe Minimum Internal Temperature* (page's
  own review date 2024-11-21; leftovers 165°F/74°C); USDA FSIS *Leftovers and Food Safety* ("be sure they
  reach 165° F as measured with a food thermometer"; 40–140°F danger zone; two-hour refrigeration rule;
  3–4 days refrigerated); USDA FSIS *Food Thermometers* (thickest part, away from bone/fat/gristle; 2–4°F
  typical accuracy; colour is not a reliable indicator); Amazon Associates *Program Policies* (header
  "Updated: April 14, 2026"; Commission Income Statement §1 and §2(e) Redirecting Link, quoted verbatim in
  the record); Google Search Central *Breadcrumb structured data*.
- **Not re-read in this pass, and not restated as verified:** Operating Agreement §5, FTC *Disclosures 101*,
  GitHub Pages limits — re-read earlier the same day by sessions `fc812c5e` and `c08695c1`, whose records
  are linked rather than duplicated. The disclosure strip, the sponsored `rel` and the index policy were
  re-checked in the built tree instead (131/131 pages carry the sentence; the gate's unsponsored-link check
  is a hard failure).
- **Gates:** `python3 tools/publish.py` → **51 of 51 PASS** on the final rebased tree; a following
  `--check` run left the working tree unchanged.
- **No claim in this Part rests on a source that was not opened, and no product, price, rating,
  destination or tracking value was added.**

## 2E0 Merge handling

`main` moved under this branch repeatedly. Each conflict was resolved the same way: upstream's register and
generated pages taken whole, then this pass's additive entries re-applied programmatically, then every
generated page rebuilt from the merged data (`tools/build_publication.py`, `scripts/build_site.py`, and the
rest of the chain) — generated HTML was never hand-merged. The board kept upstream in full with this Part
appended. The one exception is documented rather than hidden: during an intermediate rebase this session
staged `COORDINATION.md` with three conflict markers still in it; the next commit removed them and added the
tree-wide scan. No other session's work was discarded at any point.

## 2E0 Release record

- Branch: `arena/2e0d5c15-zone3`, rebased onto `main` at `bb3d554`, `8b32835`, `83e027c` and finally `957e5ab`.
- Pull request: [#222](https://github.com/kanlerxz87-cyber/Zone3/pull/222) — register correction, two rendering bugs fixed, merge debris removed, decision-desk additions.
- Merge and Pages deploy: recorded in the follow-up commit on this branch once the merge and the Pages run are confirmed.
