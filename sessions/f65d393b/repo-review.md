# F65 repo review + brief-gap review — 2026-11-16 (session `f65d393b`)

Base: `origin/main` `609dc76` (PRs #99, #101, #103 merged) merged into this branch.
Read-only audit except where noted. Every gate was run on the merged tree.

## Part 1 — line-by-line repo review (F65-T2)

| # | Area | State found | Verdict |
|---|---|---|---|
| R1 | Git hygiene | Clone was **shallow (depth 1)** at session start → `git merge origin/main` failed with "refusing to merge unrelated histories". Fixed with `git fetch --unshallow origin` (same trap session 25513d33 logged). After that: merge-base resolves, merge clean, **0 line-start conflict markers** anywhere outside `archive/`. | handled |
| R2 | `scripts/check_site.py` | **OK — 13 pages, 3 products, 52 sources, 86 flags** (before this session's two flags) | pass |
| R3 | `tools/verify_site.py` | **VERIFY PASS — 83 pages, 1,482 table rows, 1,258 with official source, 439 with flag, 89 with repo anchor** | pass |
| R4 | `tools/link_report.py --strict` | exit 0 — no dangling source or flag references | pass |
| R5 | `scripts/check_all_links.py` | 129 HTML pages, 116 distinct external URLs, 0 errors | pass |
| R6 | `scripts/build_sitemap.py --check` | On the committed tree: "78 pages checked, **5 extra entries** from the other generator" (exit 0). After this session's canonical regeneration: **78 pages, 0 extra entries** — see F65-F-02 | fixed by this session |
| R7 | New `site/` build (PR #101, session 59d84c55) | 8 pages (`index`, `front-door`, `products`, `decisions`, `evidence`, `flagged`, `guides/`×2) + `site-index.json`; generator `tools/build_i2_site.py` writes only inside `site/`; gate `tools/i2_gate.py` enforces G1–G10 (§5 disclosure in top banner, IP License 2(k) disclaimer, one h1, row provenance, no unpublishable figures, no shorteners/Amazon images/iframes, internal links, no placeholders, read-date on every page). **I2 GATE PASS — 8 pages, 105 rows, 89 sourced, 16 explicit blanks, 0 flagged** | pass |
| R8 | `tools/build_i2_site.py` re-run | idempotent — no diff | pass |
| R9 | `scripts/build_site.py` + `tools/build_site.py` re-run | idempotent on root pages and the directory build — no diff | pass |
| R10 | `scripts/build_marketing.py` re-run | **NOT idempotent at base** — regenerated 6 `marketing/*.html` pages, each one line: the shared NAV now contains the "Marketing site (new)" → `site/index.html` entry added by PR #101, but the committed marketing pages predated it. Same defect class as 1F-F-03 and cd0e6279's fix. **Fixed by this session (nav-only; no copy or data changed)** → F65-F-01 | fixed by this session |
| R11 | Secrets / credentials sweep | No keys, tokens, password or Associates tag literals in any tracked file outside `archive/` | pass |
| R12 | Duplicate-nav destinations | 0 pages with a duplicated nav destination | pass |
| R13 | Disclosure coverage | Root pages: checker-enforced §5 sentence in every footer. `site/`: i2_gate G1+G2 (top banner). Directory build, `/docs/`, `sessions/3c886b62/`: banner per prior gates (verify_site V1) | pass |
| R14 | Open exposure in other sessions' scopes (corroborated, not edited) | **Still present 2026-11-16:** `docs/analysis.html` (5 price/rating literals), `docs/content.html` (4), `docs/sources.html` (3), `docs/executive-summary.html` (1), `docs/index.html` (1); `sessions/3c886b62/analysis.html` and sibling pages carry captured price/rating tables. These are the items already CR'd as AB-CR-1/AB-CR-2 and flagged as 71-F-04/AB-F-01 (High). The pages carry notices but a notice does not cure a restricted display under 2(b)/6(t). | **open — owner decision**; not edited here (other sessions' scope) |
| R15 | Board health (corroborates AB-F-03) | `COORDINATION.md` is 5,280+ lines; many 2026-11-13/14 rows still read "in progress" although their PRs merged. This session claimed before any work and did not edit other sessions' rows. | open (AB-F-03) |

## Part 2 — brief-gap review (F65-T4)

Checked on both the root build and the new `site/` build:

| Brief item | State found 2026-11-16 | Verdict |
|---|---|---|
| Suggestions section for review-before-implementation | `suggestions.html` — SUG-01…10 with compliance basis, Q1…10 (known/unknown/why/how-to-discover), D1…6 discovery actions, decision workflow; also `site/decisions.html` (proposals, open questions, discovery, **prompt pack**, workflow) | present, linked from nav + dashboard tiles + sitemap |
| Decision-making support | `decision-center.html` (known vs missing, discovery steps, prioritized recommendations, reviewable paths stored browser-locally) | present |
| Open questions / information / answers before deciding | Q1–Q10 on `suggestions.html`; Q rows on `site/decisions.html`; each row carries what is known (sourced), what is not, why it matters, how to discover it | present |
| Catchy trendy articles and topics | `content-topics.html` (editorial topic plan, rows grounded in verified facts) + `marketing/briefs.html` (3 SEO briefs), `marketing/buying-guide.html`, `marketing/comparison.html`, `site/guides/` (dual-basket vs single-basket buying guide) | present; full product articles remain honestly blocked on identity/API flags |
| AI-slop guard | Human-review gate (SUG-04/SUG-06), claim-grounding contract on `content.html`, every table row source-linked by gate (verify_site V4, i2_gate G5) | present |
| Executive summary | `EXECUTIVE-SUMMARY.md` + `executive-summary.html`; counts in sync with the register after this session's flag additions (see T5 record) | present |
| Dashboard-style UI, tables in simple format, subpages by category | Root dashboard (13 root pages, tiles + site map), category page `air-fryers.html` + `category/air-fryers.html`, and the new reader-facing `site/` (landing → products → guides → evidence → decisions → flagged) | present |
| Every table row has an official source link; blanks flagged, never inferred | verify_site: 1,258/1,482 rows official-sourced; remainder are flags/repo-anchors/blanks-by-design. i2_gate G5: 89 sourced + 16 explicit "not published" blanks | present |
| Flagged for Review page with source links | `flagged.html` (root register) + `flagged/` (directory register) + `site/flagged.html` | present |
| GitHub Pages live site | Pages source `main` `/`, status `built`; live URL https://kanlerxz87-cyber.github.io/Zone3/ | present |
| Executive summary / disclosure compliance | OA §5 sentence on every page; IP License 2(k) disclaimer where Amazon content appears | present |

## Part 2b — irregularities raised by this session

| ID | Sev | Item | Disposition |
|---|---|---|---|
| F65-F-01 | Low | The six `marketing/*.html` pages were stale relative to the shared NAV (missing PR #101's "Marketing site (new)" link) — the "generators idempotent" gate did not reproduce at base | **fixed** by regenerating the six pages (nav-only); published on `flagged.html` |
| F65-F-02 | Info | `sitemap.xml` on `main` contained 5 redirect-stub/duplicate entries (`analysis.html`, `disclosure.html`, `flagged-for-review.html`, `index.html`, `marketing.html`) swept in by `tools/build_site.py` — the root cause session 25513d33 logged as 25-F-04 | **fixed** by regenerating with the canonical writer `scripts/build_sitemap.py` (78 pages, 0 extra entries, all 8 `site/` pages listed); published on `flagged.html` |

Corroborated, not re-raised: 71-F-04 / AB-F-01 (`docs/` and `sessions/3c886b62/` price-rating
exposure — still live, see R14), AB-F-03 (board size), 1F-F-01 (FTC Reviews Rule citation),
25-F-04 (sitemap writer split — root cause now documented twice).
