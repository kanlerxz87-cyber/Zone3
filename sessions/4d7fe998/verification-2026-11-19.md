# Verification log — session `4d7fe998`

**Date:** 2026-11-19 (UTC)
**Checkout:** `arena/4d7fe998-zone3`, re-rebased on `f29342b4ced37840ce1ff164eb2e037bd5bc7a54` (`main`, PR #194; includes PR #193)
**Review scope:** publication state, official-source boundaries, disclosure/sponsored-link policy checks, dashboard/suggestion/intent surfaces, feed/sitemap, tracking/measurement claims, and GitHub Pages suitability.
**Limit:** structural and scoped source review; not a fresh line-by-line audit of every inherited page or a substitute for account-only evidence.

## Live publication observations after PR #194

Fetched Pages after the PR #194 deployment; cache-busted with `?revision=f29342b` to avoid an older edge response:

- Home: <https://kanlerxz87-cyber.github.io/Zone3/?revision=f29342b> — five product cards in two categories. Primary “View on Amazon” CTAs still use the submitted `link.amazon` short URLs. Cards keep listing observations separate from intent and disclose that they are not hands-on reviews; no live price or rating is shown.
- Executive brief: <https://kanlerxz87-cyber.github.io/Zone3/executive-brief.html?revision=f29342b> — live register-driven strip reads 5 submitted links / 9 guides / 36 readiness questions / 0 campaign rows. Decision desk reads six paths / 26 proposals / 36 questions / 13 prompt blocks. It labels attribution unverified, production measurement off and commercial hosting for review.
- Suggestions: <https://kanlerxz87-cyber.github.io/Zone3/suggestions/?revision=f29342b> — six paths; explicit review-only wording; local save/export; no implementation action. Local HTML contains 44 answer textareas for 36 readiness questions plus eight decision-support rows.
- Guides: <https://kanlerxz87-cyber.github.io/Zone3/guides/?revision=f29342b> — nine live guide cards. All nine are in the sitemap and feed. The new guide is “Where does the probe go? Turkey, ham and roasts”; its official food-safety guidance is not a hands-on test of either listed thermometer.
- New guide: <https://kanlerxz87-cyber.github.io/Zone3/guides/where-does-the-probe-go.html?revision=f29342b> — says to check the thickest part away from bone/fat/gristle; reproduces cited FoodSafety.gov minimum-temperature/rest guidance and labels listing phrases as unverified listing claims. The upstream CDB record contains the dated official-source reads and text-level verification.
- Product-intent record: <https://kanlerxz87-cyber.github.io/Zone3/intent-record/?revision=f29342b> — all five intended-ASIN, intended-listing, confirmation-date and confirmation-source fields remain blank separately from observed redirects. It still says “Not attached to any link on this site,” which conflicts with tagged direct URLs on the product-evidence page; that does not establish account attribution.
- Product evidence: <https://kanlerxz87-cyber.github.io/Zone3/products.html?revision=f29342b> — separate SL1–SL5 table displays five direct `amazon.com/dp/<observed-ASIN>?tag=shopnow047c-20` URLs, all “Pending validation in the enrolled workflow.” The same page still contains older Product 4/5 row claims “No Associates tag, so no Special Link exists,” and older repository/config/flag statements say no tag appears. Treat these as copy contradictions, not evidence that the tagged links are approved or report.
- Legacy dashboard: <https://kanlerxz87-cyber.github.io/Zone3/dashboard/?revision=f29342b> — still shows 3 products / 22 sources / 29 flags and the older dashboard content; it is a dated legacy surface, not the current reader register.

Local inventory on the same base:

- `data/publication.json`: 5 products, 9 guides, 16 scoped official references, 26 proposals, 36 readiness questions, 6 paths and 13 design-prompt blocks.
- `review_b9008684` block: 7 design-feed entries, 7 article-slate entries, 5 traffic actions, 8 decision-support rows. (Dated text in this historical review block can retain prior guide counts; it is not the current reader count.)
- `data/shop/campaign-ledger.json`: `rows` is empty.
- `data/shop/measurement.json`: `enabled=false`, `endpoint_url=""`, `deployment_verified=false`. The active runtime/config/collector are `assets/measure.js`, `assets/measure-config.js`, `data/shop/measurement.json` and `tools/analytics_endpoint.py`; local tests are not campaign evidence.
- PR #193 labels `data/analytics.json`, `assets/track.js` and `tools/analytics_collector.py` as superseded historical code; it does not change the active OFF configuration.
- `data/special-links.json`: five direct tagged URLs with `validation_status="pending"`; URL markup is not account evidence.
- `sitemap.xml`: 17 URLs, including all nine current guide pages. `feed.xml`: 27 RSS entries, including nine current guides and five older `/site/guides/` entries (14 guide entries in total).
- The “Behind the site” header group and footer retain the research, source and decision surfaces.

## Official documents checked

| Official source | Read on / version | Relevant finding for this audit | Boundary |
|---|---|---|---|
| [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Fetched 2026-11-19; page says updated 2025-10-15; Sections 1 and 5 | Section 1 says links must properly use Amazon’s special tagged link formats. Section 5 requires a clear and prominent statement: “As an Amazon Associate I earn from qualifying purchases.” | Policy wording does not verify this owner’s account, tag assignment, or report results. |
| [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Fetched 2026-11-19; page says updated 2026-04-14; chunk 3 of 11, Participation Requirements 2(a)–(b) | 2(a) says Special Links must use the Associates ID assigned to the account. 2(b) requires the Associates ID/tag as a URL parameter on each link placed on the Site to an Amazon Site, and requires the appropriate formatting for tracking. | The policy does not identify whether `link.amazon/<code>` as supplied is compliant in this account. `FLG-003` remains unresolved; no invalidity claim is made. A visible `tag=` parameter alone is not account attribution evidence. |
| [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Fetched 2026-11-19; page dated November 2019 | Disclosures should be hard to miss, close to the endorsement, and in clear language; a footer-only disclosure may be missed. It also says not to claim product experience that did not occur. | Staff guidance, not a compliance safe harbor. |
| [FTC Endorsement Guides: What People Are Asking](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | Fetched 2026-11-19 | Endorsements must be honest and not misleading; a material connection that affects evaluation should be clearly/conspicuously disclosed. The page says context matters and the guidance is not a safe harbor. | Does not adjudicate this site’s overall legal compliance. |
| [Google: Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | Fetched 2026-11-19; last updated 2025-12-10 | Google recommends `rel="sponsored"` for advertisement/paid-placement links and permits multiple `rel` values. | Search-engine link qualification only; not Amazon approval. |
| [Google Search Console: Get started](https://developers.google.com/search/docs/monitor-debug/search-console-start) | Fetched 2026-11-19 | Ownership verification is the start of access to Search Console account data; reports include query/page performance; sitemap submission is optional and may aid discovery. | No Search Console property or report access was verified in this repo. |
| [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | Fetched 2026-11-19 | GitHub says Pages is not intended for or allowed as free web hosting to run an online business, e-commerce site, or a site primarily facilitating commercial transactions or commercial SaaS. | The reader/affiliate use is a genuine host-suitability question. This audit makes no finding that GitHub has adjudicated this site as compliant or non-compliant. |
| [Google helpful-content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Fetched 2026-11-19 | Guidance supports original, helpful, people-first content and self-assessment. | It does not establish query demand, traffic, rankings, or guide performance. |
| [FoodSafety.gov safe minimum internal temperatures](https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures) and [4 Steps to Food Safety — Cook step](https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety) | Independently re-read in upstream session `cdb0a5ac` on 2026-11-19; see [`sessions/cdb0a5ac/verification-2026-11-19.md`](../cdb0a5ac/verification-2026-11-19.md) | Supports the new probe-placement guide’s stated official minimum temperatures, rest guidance and placement advice. | This session relies on the dated upstream read-back, not a separate live fetch. It is not product-testing evidence. |

The published current publication register also links to the official Amazon Creators API GetItems documentation for the 10-character ASIN definition. No product intent is inferred from that definition or from an observed redirect.

## Checks run on the current checkout

The final branch-local canonical run was performed after rebasing on `f29342b`; `python3 tools/publish.py` was run twice. Each run reported **41 commands checked; 0 failed**. A `git status --porcelain -uall` and SHA-256 snapshot of all five in-scope changed files was unchanged after each full rebuild. The detailed record is [`sessions/4d7fe998/release-checks.md`](release-checks.md).

| Command | Result |
|---|---|
| `python3 tools/build_publication.py --check` | 20 publication pages current. |
| `python3 tools/check_publication.py` | **PUBLICATION PASS** — 121 current HTML pages, 19 rendered reader/workspace pages, 100 official-source table rows, 17 indexable URLs, 27 feed entries. |
| `python3 tools/publish.py` (twice) | **41/41 pass per run; 0 failures; byte-stable rebuilds.** Includes active and historical analytics tests. |
| `python3 tools/verify_site.py` | **VERIFY PASS** — 162 pages; 2,622 table rows; 2,218 with official source, 443 with a flag, 117 with a repository anchor. Provenance: `amazon_ftc=2021`, `flag_or_blank=91`, `repo_only=292`, `uncited=218`; 577 inherited advisory items, non-blocking. |
| `python3 tools/link_report.py --strict` | 232 register rows; no dangling source/flag references or uncited sources; six unreferenced flags (`FLG-001`, `FLG-002`, `FLG-003`, `FLG-007`, `FLG-027`, `I-F-01`). |
| `python3 scripts/check_all_links.py` | 208 HTML pages; 295 distinct external URLs; 0 errors. |
| `python3 scripts/mark_sponsored.py --check`; `python3 tools/apply_sponsored.py --check`; `python3 tools/add_disclosure_banner.py --check` | Pass; sponsored rel and above-the-fold disclosure gates are current. |
| `python3 scripts/build_sitemap.py --check`; `python3 tools/build_feed.py --check` | Pass; 17 sitemap URLs and 27 feed entries current. |
| `python3 tools/analytics_endpoint.py --self-test` | All active aggregate collector checks pass. Production measurement remains OFF. |
| `git diff --check` | Pass. |

An earlier attempted alias `python3 tools/check_links.py` does not exist; it was not retried. The correct `scripts/check_all_links.py` ran and passed as part of both canonical chains and in the detailed count check above. These are structural checks, not a fresh line-by-line factual audit of every historical page, an account-side Associates test, or proof of traffic/revenue.

## GitHub Pages status for the reviewed base

- PR [#190](https://github.com/kanlerxz87-cyber/Zone3/pull/190) merged as `eb60ee0` at 2026-11-19 12:58:17Z; its publication CI passed and the Pages build for that merge completed.
- PR [#191](https://github.com/kanlerxz87-cyber/Zone3/pull/191) merged at 13:00:47Z as `c8533cd`; its publication check and Pages build/deployment succeeded.
- PR [#193](https://github.com/kanlerxz87-cyber/Zone3/pull/193) merged at 13:10:09Z as `42a6952`; publication check run `44530675597` succeeded.
- PR [#194](https://github.com/kanlerxz87-cyber/Zone3/pull/194) merged at 13:13:26Z as `f29342b`; publication check run `44531216522` succeeded. Pages API status for `f29342b` was `built` at 13:13:51Z.
- Cache-busted live reads at `?revision=f29342b` confirmed the 5/9/36/0 executive strip, nine guides, six-path decision desk, product intent/evidence pages and the 17-URL/27-item sitemap/feed tree. The old dashboard remains stale by design/history. This is the upstream base deployment, not yet deployment verification for this session’s PR.

## Open questions that remain owner- or platform-only

1. Intended product and official intended listing for each submitted link; the four intent fields stay blank until confirmed and sourced.
2. Associates account enrollment/standing, owner ID assignment, accepted link format and report attribution; the account-only Special Link test remains necessary.
3. Amazon’s response to the exact `link.amazon` form, tracked as unresolved `FLG-003`.
4. Search Console property ownership and real query/page performance data.
5. A durable authorized collector host and host/proxy/CDN logging/privacy review; production measurement remains OFF.
6. GitHub’s assessment of whether the intended affiliate-publication use is within the Pages business-use limit, or a hosting migration before scaling.
7. Budget, accountable publisher, testing protocol, first-hand evidence, and remaining editorial choices in the 36-question decision register.

No traffic, product intent, account approval, click attribution, search demand, ranking, conversion, revenue, or hands-on performance value was filled in or claimed by this verification pass.
