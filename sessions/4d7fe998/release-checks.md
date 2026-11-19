# Release checks — session `4d7fe998`

**Date:** 2026-11-19 UTC
**Branch:** `arena/4d7fe998-zone3`
**Rebased main:** `3f0d14bfad1eee800c6e6e3397e43e78b5d93839` (PR #195, including #193/#194)
**Scope:** canonical build, complete publication gates twice, hash-based idempotency, GitHub Actions/Pages/read-back, and explicit file-scope confirmation.

## Upstream baseline and live read-back

- PR [#193](https://github.com/kanlerxz87-cyber/Zone3/pull/193) merged at `2026-11-19T13:10:09Z` as `42a6952`. Publication check `44530675597` succeeded.
- PR [#194](https://github.com/kanlerxz87-cyber/Zone3/pull/194) merged at `2026-11-19T13:13:26Z` as `f29342b`. Publication check `44531216522` succeeded; the Pages API reported the `f29342b` deployment as `built` at `2026-11-19T13:13:51Z`.
- PR [#195](https://github.com/kanlerxz87-cyber/Zone3/pull/195) merged at `2026-11-19T13:17:29Z` as `3f0d14b`; it is a coordination-only CDB closeout. Publication check `44531961726` succeeded and Pages reported `3f0d14b` as `built` at `2026-11-19T13:17:58Z`.
- Cache-busted live read-back for revision `3f0d14b` confirmed the five home cards (still using submitted short links), nine guide cards including the new probe-placement guide, 17 sitemap URLs, 27 RSS entries, the brief's 5/9/36/0 status strip, six review-only paths, and current intent/product evidence surfaces. The legacy `/dashboard/` remains an older 3-product/22-source/29-flag snapshot.
- PR #194's upstream verification record reports its own complete `tools/publish.py` run twice; this is separate from and does not substitute for the branch-local checks below.

## Branch state before PR creation

- Current branch: `arena/4d7fe998-zone3`; rebased on `3f0d14b` and force-with-lease pushed as `5015056f192d16c3eadd0a8825dff6bb88d57eb6` after verifying the remote branch still pointed to `459596b635f411ecbc27494b086dd40c44483c8f`.
- Post-push `git ls-remote` matched local HEAD `5015056f192d16c3eadd0a8825dff6bb88d57eb6`. No PR for this branch existed at that point. PRs #160 and #157 were rechecked as open and left untouched.

## PR #196 merge and post-merge deployment

- PR [#196](https://github.com/kanlerxz87-cyber/Zone3/pull/196), head `d2609653008291f400e4818e9c89c8183cb013bb`, passed publication check `44534254715` and merged at `2026-11-19T13:32:02Z` as `1623c1c2b6c4b04d526130a316dd6d9344985bdd`.
- GitHub Pages API reported the merge commit `built` at `2026-11-19T13:32:31Z`.
- Cache-busted live read-back at revision `1623c1c` confirmed the executive brief’s 5/9/36/0 strip, nine-guide index and probe-placement guide, and the 17-URL sitemap. The merge contained audit/coordination/Markdown records only; no product, register or generated reader-page data changed.
- After completing the post-merge release records, `python3 tools/publish.py` was run twice again on the current tree: **41/41 commands passed both times**. All four modified audit/coordination files and `git status --porcelain -uall` were unchanged across both runs; no generated content changed.

## Branch-local canonical build and full gates

The canonical command `python3 tools/publish.py` (not `--check`) was run twice on the branch after rebasing to `3f0d14b`. Each run rebuilt the tree and executed all active/legacy structural, provenance, disclosure, sponsored-link, sitemap/feed, external-link, and analytics tests: **41 commands checked; 0 failed** on both runs.

| Run | Command | Result | Working-tree result |
|---|---|---|---|
| 1 | `python3 tools/publish.py` | **41/41 pass; 0 failed** | `git status --porcelain -uall` plus SHA-256 snapshot unchanged; 5 in-scope docs/records unchanged |
| 2 | `python3 tools/publish.py` | **41/41 pass; 0 failed** | Same status and content hashes as pre-run snapshot; no generated or other files changed |
| Idempotency | SHA-256 and `git status --porcelain -uall` snapshot before/after both runs | **PASS** | Both full rebuilds left the staged tree byte-for-byte unchanged |

Detailed gate results on the same tree:

- `tools/build_publication.py --check`: 20 publication pages current.
- `tools/check_publication.py`: **PUBLICATION PASS** — 121 current HTML pages, 19 rendered reader/workspace pages, 100 official-source table rows, 17 indexable URLs, 27 feed entries.
- `tools/verify_site.py`: **VERIFY PASS** — 162 pages / 2,622 table rows; 2,218 with official source, 443 with a flag, 117 with a repository anchor. Provenance buckets: `amazon_ftc=2021`, `flag_or_blank=91`, `repo_only=292`, `uncited=218`. It emitted 577 inherited, non-blocking advisories.
- `tools/link_report.py --strict`: 232 rows, no dangling source/flag references or uncited sources; six unreferenced flags (`FLG-001`, `FLG-002`, `FLG-003`, `FLG-007`, `FLG-027`, `I-F-01`).
- `scripts/check_all_links.py`: 208 HTML pages, 295 distinct external URLs, 0 errors.
- `scripts/mark_sponsored.py --check`, `tools/apply_sponsored.py --check`, and `tools/add_disclosure_banner.py --check`: pass; all product links carry `rel="sponsored"` and the required Associates disclosure is above the fold.
- `scripts/build_sitemap.py --check`: current, 17 indexable URLs. `tools/build_feed.py --check`: current, 27 entries.
- `tools/analytics_endpoint.py --self-test`: all checks pass. Production measurement remains disabled and the campaign ledger empty.

Structural success does not verify every historical factual claim or any account-only evidence.

## File-scope and host-state boundaries

- Only the current-status opening of `EXECUTIVE-SUMMARY.md`, this appended Part of `COORDINATION.md`, and `sessions/4d7fe998/**` are this session's changed paths.
- Product, intent, tracking, source, flag, measurement, suggestion-register and generator files remain untouched by this session. Generated reader pages are kept byte-identical by the local release builds; do not treat an upstream PR #194 page as a change made here.
- No Amazon account, Search Console, campaign-ledger or production-analytics evidence was available. Production measurement remains off, and the campaign ledger remains empty.
- PR #160 and PR #157 are not to be merged by this session.
- PR #196 passed its publication check, merged, and reached a `built` Pages status; the live brief, guide index/probe guide, and sitemap were re-read at `?revision=1623c1c`. Account-only, owner-only and hosting-policy verification remains outside repository release gates.
