# Release checks — session `4d7fe998`

**Date:** 2026-11-19 UTC
**Branch:** `arena/4d7fe998-zone3`
**Rebased main:** `f29342b4ced37840ce1ff164eb2e037bd5bc7a54` (PR #194, including #193)
**Scope:** canonical build, complete publication gates twice, hash-based idempotency, GitHub Actions/Pages/read-back, and explicit file-scope confirmation.

## Upstream baseline and live read-back

- PR [#193](https://github.com/kanlerxz87-cyber/Zone3/pull/193) merged at `2026-11-19T13:10:09Z` as `42a6952`. Publication check `44530675597` succeeded.
- PR [#194](https://github.com/kanlerxz87-cyber/Zone3/pull/194) merged at `2026-11-19T13:13:26Z` as `f29342b`. Publication check `44531216522` succeeded; the Pages API reported the `f29342b` deployment as `built` at `2026-11-19T13:13:51Z`.
- Cache-busted live read-back for revision `f29342b` confirmed the five home cards (still using submitted short links), nine guide cards including the new probe-placement guide, 17 sitemap URLs, 27 RSS entries, the brief's 5/9/36/0 status strip, six review-only paths, and current intent/product evidence surfaces. The legacy `/dashboard/` remains an older 3-product/22-source/29-flag snapshot.
- PR #194's upstream verification record reports its own complete `tools/publish.py` run twice; this is separate from and does not substitute for the branch-local checks below.

## Branch-local canonical build and full gates

The canonical command `python3 tools/publish.py` (not `--check`) was run twice on the branch after rebasing to `f29342b`. Each run rebuilt the tree and executed all active/legacy structural, provenance, disclosure, sponsored-link, sitemap/feed, external-link, and analytics tests: **41 commands checked; 0 failed** on both runs.

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
- The branch PR, its checks, merge (only if checks pass), post-merge Pages deployment, and live summary read-back will be recorded after the local gates.
