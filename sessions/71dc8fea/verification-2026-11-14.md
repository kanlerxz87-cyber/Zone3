# Independent repository and site audit — session `71dc8fea`

**Date:** 2026-11-14 UTC
**Branch:** `arena/71dc8fea-zone3`
**Initial base:** `4fd8bd641b69050c780723e00a42f045766e1c37`
**Scope:** repository/site review and local integrity checks; no shared page, source register, product data, or generator was edited by this audit.

> **Verification boundary.** This session independently inspected the repository, ran the local gates, checked GitHub Pages configuration/build metadata, and compared the current outputs with the official-source verification records already merged in `COORDINATION.md` (sessions `4575cf95`, `7b70cfb0`, and `cdc9baa4`). It did **not** make a new network fetch of Amazon or FTC pages. The official-source observations below are attributed to those dated live-fetch records, not represented as new fetches by this session. `scripts/check_all_links.py` checks internal URLs only; its documentation explicitly says it does not fetch external links.

## Executive summary

The GitHub Pages dashboard and its product/category, compliance, content, campaign, source, and review pages already exist and are published from the repository root. The local site checks pass. The supplied URLs are Amazon short links, not ASINs: the latest merged live-fetch records observed each resolving to a specific Amazon listing, but this does **not** establish that the destination was the product the submitter intended. Keep those two facts separate.

No official price, rating, review-count, per-product commission, trend/conversion, or campaign-performance value was confirmed for publication in the canonical register; those fields are blank/flagged there. No Associates tag or API credentials are configured, and the campaign metrics file is null. Accordingly, the repository is a static research/dashboard prototype with intake and build tools—not an operating, revenue-producing AI affiliate service with a connected model, account, live product feed, or conversion pipeline.

The audit also found that the repository's checks and public artifacts are **not fully consistent with the brief's strict source requirement**. The whole-tree verifier allows flags and repository anchors in place of direct official-source links, and its manifest reader does not recognize the generated pages as owned pages. Legacy `/docs/` and `/sessions/` pages are still in the sitemap and include historical price/rating material, contradicting the root executive summary's statement that none is rendered anywhere. These are logged as cross-scope requests below; this audit did not alter files owned by the site/build sessions.

## Product intake — facts kept distinct

The mapping below is from the latest merged live verification record, not a new live fetch by this session. The short-link destination is observable; the user's intended product is not established by that observation alone.

| Submitted link | Submitted token length | Observed destination in the merged verification record | Audit status | Manual source review |
|---|---:|---|---|---|
| [`link.amazon/B04G1MEwY`](https://link.amazon/B04G1MEwY) | 9 | [`B0CDY277D3`](https://www.amazon.com/dp/B0CDY277D3) — CHEFMAN 6 Quart Dual Basket Air Fryer listing | Destination observed; intended identity unconfirmed | [Creators API GetItems / ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) |
| [`link.amazon/B02NbDxp3`](https://link.amazon/B02NbDxp3) | 9 | [`B09B7SB46R`](https://www.amazon.com/dp/B09B7SB46R) — Emeril Lagasse 26QT French Door listing | Destination observed; intended identity unconfirmed | [Amazon listing](https://www.amazon.com/dp/B09B7SB46R) |
| [`link.amazon/B00hJ57DV`](https://link.amazon/B00hJ57DV) | 9 | [`B08DKYBTPH`](https://www.amazon.com/dp/B08DKYBTPH) — Chefman 8 Qt TurboFry listing | Destination observed; intended identity unconfirmed | [Amazon listing](https://www.amazon.com/dp/B08DKYBTPH) |

Amazon's [Creators API reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) defines an ASIN as a 10-character alphanumeric identifier. The nine-character submitted values therefore must not be treated as ASINs or passed into `/dp/<token>` as if they were ASINs. The earlier live verification records also say the *short links* resolve. A `Page Not Found` result for `/dp/<short-link-token>` is not evidence that the short link itself fails.

The canonical flat data (`data/products.json`) leaves product identity and commercial metrics blank and flags the unresolved intent. The separate `data/z3/products.json` records observed destination listings and titles. Those can coexist only when the pages consistently label them as **observed redirect targets**, not as confirmed intended products.

## Official policy/source references used for manual review

These are official links already in the repository's source registers and dated verification records:

| Topic | Official source |
|---|---|
| Associates participation, linking, program content, and required disclosure | [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) and [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| ASIN format | [Creators API — GetItems / ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) |
| Public standard category rates | [Associates Standard Commission Income Statement — Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| FTC disclosure guidance | [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) and [FTC Endorsements, Influencers, and Reviews](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews) |
| Current GitHub Pages configuration | [Pages API](https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages) |

The merged verification records say Table 1 is public and lists Kitchen at 4.50% as a **category rate**. That does not support assigning a per-product rate to a target whose intended identity/category has not been confirmed. The [Amazon Program Policies](https://affiliate-program.amazon.com/help/operating/policies) are also the cited source for the price/availability and rating/review display restrictions.

## Local verification performed

| Check | Result | What it establishes / does not establish |
|---|---|---|
| `python3 scripts/check_site.py` | **Pass:** 12 pages, 3 products, 48 sources, 49 flags | Checks the legacy flat-site page set and its official-source cells; not a complete official-link audit of every published HTML page. |
| `python3 tools/verify_site.py` | **Pass:** 69 pages, 1,169 table rows, 967 rows counted as official-source linked, 346 flagged, 82 repository-anchored | Its row rule also accepts GitHub links, flag IDs, or repository anchors; see release-gate finding 71-F-01. A pass is not proof that every row has a direct Amazon/FTC source. |
| `python3 tools/link_report.py --strict` | **Exit 0:** 231 dataset rows; no dangling source/flag references | Coverage counts official sources, flags, and repository anchors. It reports uncited `SRC-07` and row-unreferenced flags `FLG-001/002/003/007/027` as non-blocking advisories. |
| `python3 scripts/check_all_links.py` | **115 HTML files, 104 distinct external URL strings, 0 internal-link errors** | Checks relative paths and fragments; external URLs are collected, not fetched. |
| `python3 scripts/build_sitemap.py --check` | **Pass:** 64 pages covered; 5 extra sitemap entries | The 69-entry sitemap includes `/docs/` and `/sessions/` content, not just the current dashboard and marketing pages. |
| `python3 tools/build_site.py --out /tmp/zone3-71dc8fea-audit` | **Pass after pre-creating `data/z3/` in the temporary output:** 16 pages, 231 table rows, 22 sources, 28 flags | The first clean-output attempt failed because the builder tried to write `data/z3/build-manifest.json` without creating its parent. The normal repository build has that directory already. A separate-output `verify_site.py` run printed 112 inherited-page advisories and still exited successfully. |
| GitHub Pages API | Public legacy Pages source: `main` `/`, HTTPS enforced | The latest build status is recorded in the coordination publish record after merge; the API status is asynchronous. |

A separate local scan of the 1,169 non-archive HTML table rows found **946 rows with a direct Amazon or FTC URL in that row and 223 without one**. This is a literal host scan, not a claim that all 223 rows are unsupported product facts: the set includes blank/unverified rows, repository-status rows, and historical session/docs tables. It does show that the current machine gate is weaker than the brief's direct-source requirement and that the old published page sets need a deliberate canonical/archival policy.

## Repository irregularities found

### 71-F-01 — Generated-page ownership is not recognized by the verifier

`tools/build_site.py` writes `data/z3/build-manifest.json` with `files` values set to 12-character SHA-256 digests. `tools/verify_site.py:45–54` reads `files.values()` as relative page paths, and `check()` at lines 65–85 compares those digests to relative HTML paths. The result is that **zero** generated page paths match the manifest's `mine` set. Page-specific V2/V3 failures and row-provenance V4 failures are therefore not hard failures for those generated pages; they are treated as inherited-page advisories (or skipped for the own-page-only checks). This undermines the claimed whole-tree release gate.

**Requested resolution:** store actual generated paths separately in the manifest and have `generated_set()` consume those paths; add a regression test that proves all 16 generated pages are recognized and that a deliberately broken generated page fails the build. Create the `data/z3/` parent when using `--out`.

### 71-F-02 — The row-provenance rule does not enforce the user's official-source rule

`tools/verify_site.py:99–128` considers a row provenanced if it contains an Amazon/FTC/**GitHub** URL, a flag ID, or a `repo:` anchor. The new build gate likewise describes G1 as “row-has-source-or-flag.” This is useful for internal implementation/status rows, but it is not the same as “every factual product/policy row has an official source link.” The 946/223 scan above shows why these rules must be separated by row type: verified product/policy claims need an official source; blank values need an explicit unverified flag; repository-state claims can use a repository anchor.

**Requested resolution:** make the schema/checker distinguish product/policy facts from repository-status and blank/unverified rows, and fail if a nonblank Amazon/product/policy claim lacks an official Amazon/FTC source. Keep explicit flags for values that cannot be confirmed; do not fill them with estimates.

### 71-F-03 — Stale or overbroad product-link interpretation in the parallel `/dashboard/` register

`data/z3/flags.json` FLG-001–006 treat the short-link path as failing to select the *intended* product; FLG-007 calls the three different destinations “random” recommendations and treats `plpRedirect=mhFallback` as decisive evidence. The same dataset's `data/z3/products.json` records live destination listings, and the merged live re-fetch records confirm those mappings. What remains unconfirmed is whether those destination products are the intended items. The official sources cited for ASIN format establish that the submitted tokens are not ASINs; they do not establish that Amazon's short-link redirects are random or that the owner did not intend the destination products.

`data/z3/requirements.json` R-23 similarly says “all three identifiers are invalid.” That needs the narrower distinction: the tokens are not valid ASINs for a `/dp/` lookup, while the submitted short links were observed to resolve.

**Requested resolution:** update the parallel register and its flagged page to use the same wording as the current root data: observed target, intended identity unconfirmed. Remove “random”/“meaningless” conclusions unless an official source supports them. The relevant manual sources are the three [submitted short links](https://link.amazon/B04G1MEwY), [link 2](https://link.amazon/B02NbDxp3), [link 3](https://link.amazon/B00hJ57DV), their [Amazon destination pages](https://www.amazon.com/dp/B0CDY277D3), [destination 2](https://www.amazon.com/dp/B09B7SB46R), [destination 3](https://www.amazon.com/dp/B08DKYBTPH), and the [Creators API ASIN definition](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter).

### 71-F-04 — Public legacy pages contradict the root executive summary

`EXECUTIVE-SUMMARY.md:90–92` says there are no prices, star ratings, or review counts “anywhere on the site.” The published `/docs/` pages and `/sessions/3c886b62/` page set are included in `sitemap.xml` and contain historical price/rating tables. The root summary also describes the platform and intake as fully built/refusing all three items, while the repository shows a static dashboard/prototype and the separate `/dashboard/` data set records observed redirect destinations. The root and parallel registers must state their different meanings without contradicting one another.

The old page paths are directly reviewable at [`/docs/analysis.html`](https://kanlerxz87-cyber.github.io/Zone3/docs/analysis.html), [`/docs/content.html`](https://kanlerxz87-cyber.github.io/Zone3/docs/content.html), [`/docs/index.html`](https://kanlerxz87-cyber.github.io/Zone3/docs/index.html), and [`/sessions/3c886b62/`](https://kanlerxz87-cyber.github.io/Zone3/sessions/3c886b62/). This is especially important because the [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) restrict static price/availability and ratings/reviews displays unless their stated conditions are met. The existing FLG-028 mentions the old session pages, but its action text should be reviewed; merely relabeling a rendered rating as an observation does not itself establish policy-compliant display.

**Requested resolution:** reconcile or retire the stale outputs, decide whether to exclude them from the sitemap or replace them with clearly labeled archived/redirect pages, and make the executive summary describe exactly which current pages contain which data. Do not silently delete prior-session work; preserve it in the repository history/archive.

### 71-F-05 — “AI-powered platform” scope is not an operational runtime

The current repository contains static HTML/JS, JSON data, build/check scripts, an intake CLI, and a niche-scoring tool. `config/platform.json` has a null Associates tag and null API credentials; `data/z3/campaign-metrics.json` is all null; no model-service client, database, or running web backend was found; `assets/script.js` is not referenced by the published HTML. Thus the site describes and prototypes the workflow, but it does not currently publish tagged Special Links, query a live eligible product API, run an AI model, ingest conversions, or optimize live campaigns.

This is a delivery-scope limitation, not a missing value to infer. Keep tracking/revenue fields blank and the existing compliance flags visible. No tag, account credential, or API secret was invented.

## Cross-scope requests (logged; no shared files edited)

The current board records the `/dashboard/` build, the flat root build, and the historic `/docs/` and per-session pages under different session scopes. Per the coordination rules, this audit did not edit those owned/shared files. The following requests are for the next final integration owner:

1. Resolve 71-F-01 and 71-F-02 in `tools/build_site.py`, `tools/verify_site.py`, and their generated manifest/gates.
2. Reconcile 71-F-03 in `data/z3/flags.json`, `data/z3/requirements.json`, and the generated `/flagged/` and `/requirements/` pages.
3. Resolve 71-F-04 in `EXECUTIVE-SUMMARY.md`, `executive-summary.html`, the sitemap, and the public legacy pages; publish the resulting status on a clearly labeled Flagged for Review page with official-source links.
4. Keep 71-F-05 visible in the executive summary and requirements matrix until a compliant tag/account/API path and runtime are actually configured.

## Source and verification trail

- Latest merged live re-fetch record: `COORDINATION.md`, session `7b70cfb0` H-T1/H-T2; machine-readable copy: [`sessions/7b70cfb0/verification-2026-11-14.json`](../7b70cfb0/verification-2026-11-14.json).
- Additional live re-fetch record: `COORDINATION.md`, session `cdc9baa4` CDC-T2.
- Canonical source register: [`data/sources.json`](../../data/sources.json) (S01–S55); parallel register: [`data/z3/sources.json`](../../data/z3/sources.json) (SRC-01–SRC-22).
- Local page/data checks run by session `71dc8fea`: commands and results in the verification table above.
- GitHub Pages status and PR/merge result: recorded in the session's `COORDINATION.md` Part 71 publish record after the final merge.
