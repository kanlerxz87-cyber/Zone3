# Session ed27e766 — decision and design-brief refresh

**Date:** 2026-11-17 UTC
**Branch:** `arena/ed27e766-zone3`
**Current upstream absorbed:** `6ef32c4` (PR #150 merge); the session started from the then-current `c67596a` tree after the initial five-product reconciliation.

## Scope completed

- Refreshed `data/suggestions.json`, `data/decision-queue.json`, and `data/shop/decisions.json` for the five submitted links, the requester-supplied `shopnow047c-20` value, the three-air-fryer/two-thermometer category split, canonical reader routes, and owner-side discovery steps.
- Updated `data/design-brief.json` and its renderer for the five-link/two-category prompt, current repository surfaces, source-backed evidence limits, and owner-only decisions. The recommended root + `/shop/` + `/guides/` structure remains a proposal; no route changes were made.
- Added two browser-local review choices to the generated Decision Center. The choices are not uploaded and do not record an owner decision.
- The main branch already contains the session-38650305 measurement prototype. This pass documents its five event names as a proposal, `enabled=false`, empty `endpoint_url`, and an unhosted collector. It did not edit the measurement code/config, deploy a runtime, enable collection, or claim event/conversion data.
- The shared source resolver now resolves the shop register's `SH-*` source IDs for the review and design pages; the existing Sources pages remain generated from their own registers.
- Corrected an evidence-label mismatch in the browser-local Decision Center and shop DEC-07: the former now labels SH-S11–SH-S15 as observed listing pages, not as the repository register, and the latter links all five individual observed listing pages plus the repository's two-category register.
- Reconciled two remaining queue phrasings with the five-link state: the old “0 of 3” hero metric is explicitly described as an earlier draft and the current root's five listing cards are recorded; Q13's rationale now distinguishes the three air-fryer and two thermometer observations without treating category counts as audience or demand evidence.

## Source and evidence review

This pass used the repository's official-source records checked on 2026-11-17; it did **not** independently fetch those external pages again or re-fetch any submitted product link.

- `SH-S01` — Amazon Associates Operating Agreement: source record notes the page's 2025-10-15 update, the Program Content/Special Link definition, the Section 5 disclosure wording, and Section 6 consequence.
- `SH-S02` — Amazon Associates Program Policies: source record notes sections 2(e) and 2(g) on indirect/incorrectly formatted referrals; the shop source record says its capture covered chunk 1 of 11. The broader `S02` register says the policy sections cited by the policy-facts register were read in 11 chunks.
- `SH-S03` — Creators API `ItemIdType`: the recorded definition says an ASIN is a 10-character alphanumeric identifier. This is only a token-shape fact; it does not decide whether a submitted short link is valid or compliant.
- `SH-S04` — Google Search Central: record supports `rel="sponsored"` for advertising/paid-placement links.
- `SH-S05` — FTC Disclosures 101: record supports making a disclosure hard to miss and placing it with the endorsement.
- `SH-S16` — GitHub Pages documentation: record says Pages is static hosting and logs visitor IP addresses for security.
- `SH-S06`–`SH-S15` — dated 2026-11-17 repository observations for the five submitted links and their observed listing destinations. These remain observations, not intended-product confirmations or fresh checks by this pass.

No Special Link was generated or tested in an enrolled account. `shopnow047c-20` remains requester-supplied and account-unverified. The five intended-ASIN fields remain blank. No marketplace, author, test, image right, Search Console query export, host log/retention behavior, or privacy review was inferred.

## Build and release gates

The documented build chain was run, including the flat/site/shop/measurement/brief-status/marketing/read/article generators, publication and measurement passes, feed generation, and sitemap generation. After generation, outputs outside E84 scope (`publication-pass.html` and session `aebf0747` records) were restored to avoid changing another session's publication/verification records.

| Gate | Result |
|---|---|
| `scripts/check_site.py` | PASS — 36 pages, 5 products, 75 sources, 123 flags |
| `tools/verify_site.py` | PASS — 144 pages, 2,279 table rows; 1,955 with official source, 386 with flag, 66 with repository anchor. Non-blocking provenance advisories remain in the inherited-site baseline. |
| `tools/link_report.py --strict` | PASS — 232 rows, no dangling source or flag references; existing unreferenced flags are reported as such. |
| `tools/i2_gate.py` | PASS — 20 pages, 186 rows, 170 sourced, 16 explicit blanks, 0 flagged |
| `tools/cba81fa5_lint.py` | PASS — 20 pages, 0 new findings, 22 inherited advisories |
| `scripts/cba81fa5_test_no_repr_output.py` | PASS — 144 pages, 0 repr-shaped text |
| `tools/build_shop.py` | PASS — 11 pages; disclosure, sponsored links, source rows, sitemap and local links |
| `tools/build_feed.py --check` | PASS — 9 entries, current |
| `scripts/build_sitemap.py --check` | PASS — 101 pages, 0 extra entries |
| `scripts/check_all_links.py` | PASS — 190 HTML pages, 255 distinct external URLs, 0 local-link errors |
| `tools/apply_sponsored.py --check` | PASS — every product link has `rel="sponsored"` |
| `tools/add_disclosure_banner.py --check` | PASS — §5 disclosure above the fold on published pages |
| `tools/analytics_endpoint.py --self-test` | PASS — 10 collector checks; this is a local test, not a deployment |
| `node sessions/38650305/test_measure.js` | PASS — 16 offline client checks; default config remains OFF |
| JSON validation, `py_compile`, source-ID/path checks, `git diff --check` | PASS |

## Irregularities and resolution

- After the branch was claimed, `main` advanced to `6ef32c4`. Rebasing the claim commits conflicted in the append-only `COORDINATION.md`. Resolution kept the full upstream board and appended Part 84; no upstream section was discarded. Work-in-progress JSON/Python changes were stashed and restored around the rebase.
- A first Python attempt to update the historical design brief had a syntax error and wrote nothing. The brief was later updated with a fresh, parse-checked script.
- Some generator scripts do not implement `--help`; invoking it on the shop/feed/measurement/brief-status/measure scripts ran their normal build actions. The full documented chain and the final disclosure/measurement/feed/sitemap passes were rerun. Unrelated generated outputs and other-session records were restored; only the E84-generated pages remain modified.
- The repository contains a local collector prototype despite the earlier E84 claim's assumption that no collector code existed. The review was corrected to describe the actual state (OFF/unhosted) without changing the shared analytics implementation.
- The coordination scope amendment initially said the browser-local choice UI had an export/clear path. Inspection of `build_decision_center()` showed only a clear control; the board entry was corrected. No export feature is claimed.

## Pending integration

All listed gates pass. No PR, merge, Pages deployment check, or live-site verification has been performed yet. The publish record will be appended to `COORDINATION.md` after integration.
