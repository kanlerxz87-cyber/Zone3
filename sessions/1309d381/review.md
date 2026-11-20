# Repository review — session `1309d381` (2026-11-20)

## Scope and method

This is a local review of the current publication, decision registers, automation configuration and build gates after PR #215 (13 guides) and the c08695c1 integration PRs #219/#221. Its deployment check passed. The latest fetched `origin/main` is `83e027c` (PR #221); no Amazon or Google page was fetched by this session. The repository was inspected directly; this session did **not** fetch Amazon or Google pages live. Official-source dates below are the dates already recorded in the repository, not a claim of a new re-read. A separate, merged verification record from session `fc812c5e` re-fetched the five submitted links and re-read the Amazon disclosure/link clauses on 2026-11-20: [`sessions/fc812c5e/verification-2026-11-20.md`](../fc812c5e/verification-2026-11-20.md).

No account, API, Search Console, analytics-host, or Associates report access is available from the repository. No private credentials or account screenshots were requested or stored.

## What already exists

- **Reader-facing publication:** the root page and category/shop pages lead with products and buyer questions. The current catalogue has five submitted links (three air fryers and two meat thermometers); 13 question-led guides are registered after PR #215. Session `fc812c5e` reports that all four titles proposed in the user brief are already published as guides, and labels them editorial hypotheses rather than demand claims.
- **Decision desk:** `suggestions/index.html` is generated from `data/publication.json`. On the merged tree the implementation contains six selectable paths, 38 proposals, 47 decision questions, 14 copy-ready design-prompt blocks and a browser-local review/export flow (upstream sessions 2e0d5c15 and 9ed0552a added four proposals and five product pages while this branch was open). The existing 263-Q3/263-P3 entries cover safe automation generally; this session adds a separate AI/data-permission question and proposal rather than replacing them. A selection does not publish or implement changes.
- **Affiliate evidence:** all five product-intent records have blank intended ASIN, official listing URL, confirmation date and source fields; observed redirect destinations stay separate. The tracking ID is owner-supplied and unvalidated. The current site and the merged verification record explicitly leave `FLG-003` unresolved; they do not call the supplied short links invalid.
- **Trust and publication mechanics:** the current generated pages include the Associates disclosure and sponsored product links; `tools/publish.py` is the full build/release chain for the static publication. It runs deterministic builders and checks; its header states that it does not call remote APIs or access accounts.
- **Measurement:** `data/shop/measurement.json` defines five events, but `enabled` is `false` and `endpoint_url` is empty. `data/shop/campaign-ledger.json` has zero rows. There is no production click collection, Search Console report, authorized Associates report, conversion score, or revenue forecast recorded here.

## AI and data-permission finding

The repository's official-source register links Amazon Associates Program Policies (S02) at <https://affiliate-program.amazon.com/help/operating/policies>. The existing policy-fact record `data/policy_facts.json` PF-22–PF-25, last recorded as read 2026-11-13, quotes restrictions on automated data mining and on aggregating, analyzing, extracting or repurposing Product Advertising Content through Creators API, PA API or Data Feeds, including direct model training/fine-tuning, absent express prior written approval. It also records a restriction on third-party use of Program Content to develop or improve language/multimodal or machine-learning models. Those lines are an existing repository record; they were **not** independently re-fetched in this session.

No express written approval, product-data API access, or model-use permission is recorded. Therefore this review recommends **not enabling Amazon-product-content analysis, training, automated product scoring, or AI-written product claims**. Safe work in this pass is limited to the review workflow, data-permission question, design prompt, deterministic build gates and source-linked summaries. Generated text is not treated as verification.

## Missing information that blocks a responsible “AI affiliate platform” decision

1. **Product intent:** owner-confirmed intended ASIN, official listing URL, confirmation date and source for each of the five submissions. Do not infer these from observed redirects. See `P26-Q1` and the intent-record page.
2. **Account and attribution:** confirmation that the site and `shopnow047c-20` belong to the intended enrolled Associates account, plus one enrolled-workflow Special Link and report check per intended product. See `P26-Q2`, `P27-Q6`, and `FLG-003`.
3. **AI permission/data scope:** express written Amazon approval, if needed, stating the permitted inputs and operations; whether any API/data-feed use is allowed for analysis or model-related work; and a documented model/vendor data-handling boundary. Question `AI-1309-Q1` is now in the in-scope suggestion register, with the proposed answer format excluding credentials.
4. **Real demand and outcomes:** verified Search Console query/page reports and authorized Associates reports with reporting dates and provenance. Without them, “trending,” “high-converting,” commission potential, and optimization scores remain unsubstantiated. See `P26-Q4`, `P26-Q5`, and `E61-Q1`.
5. **Production collection:** a durable host and an approved logging/retention/privacy configuration before the five-event prototype can be switched on. GitHub Pages is static; a successful Pages build does not deploy the collector.
6. **Editorial authority:** a named human editor and a review/sign-off rule before AI-assisted drafts are published as editorial content. The project does not claim hands-on testing or a named human reviewer.

The suggestion register records who can supply each answer, a discovery action, and a safe default. The AI-specific proposal is review-only: it does not enable a model, ingest product data, replace links, or publish new guides.

## RSS count drift and fix

The starting tree had 13 XML channel items in `feed.xml`, a stale README fact of 4, and a `DESIGN_PROMPT.md` count of 29 that described a broader register union from an earlier snapshot. Current feed-builder inputs contain 31 post-retirement candidates; the sitemap filter omits 18 destinations, leaving 13 actual XML items. These are repository counts, not traffic or demand evidence.

This pass clarifies the distinction in section 3 of `DESIGN_PROMPT.md`, updates the generated README label/count, and adds `tools/check_feed_readme.py` to validate the XML item count, the README sentinel block, the candidate union and sitemap filtering, and every measured row of design section 3 — page tree, canonical/OG/description coverage, sitemap URLs, guides, the four decision-desk figures, and the source and flag registers. `tools/publish.py` now rebuilds the publication after the final feed generation; `tools/build_publication.py --check` also fails on stale README facts rather than only printing a warning. Current check output: 13 published RSS items, 31 candidates, 18 sitemap exclusions, 131 HTML pages, 27 indexable URLs, 13 guides, 38 proposals, 47 questions, 14 brief blocks. Negative tests (README count, OG ratio, flag count, proposal count, guide count, each edited one at a time) all exited 1 with the stale row named and were reverted.

## Official sources for manual review

- Amazon Associates Program Policies (S02; PF-22–PF-25 cite this source): <https://affiliate-program.amazon.com/help/operating/policies>
- Amazon Associates Program Operating Agreement (S01): <https://affiliate-program.amazon.com/help/operating/agreement>
- Amazon Creators API introduction (S04): <https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction>
- Google Search Console setup and query reporting: <https://developers.google.com/search/docs/monitor-debug/search-console-start>
- Google people-first content guidance: <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- GitHub Pages hosting limits: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>

No new product-level fact, price, rating, review count, commission rate, trend, conversion or revenue claim is added by this review.

## Release and deployment (2026-11-20)

- Branch `arena/1309d381-zone3`; `main` was at `c7db696` (PRs #222, #224, #225, #226) when this pass merged it. The board was rebuilt as upstream's file verbatim plus this Part, generated pages were taken from upstream and rebuilt by the chain, and `data/publication.json` was reconstructed with upstream's rows plus this session's four additive entries by id — no upstream row was dropped or rewritten.
- PR [#227](https://github.com/kanlerxz87-cyber/Zone3/pull/227) merged into `main` on 2026-11-20T06:15:27Z as `2ebb5a9c0d83b1717b34f8e6859c9baa32d7503d`.
- Checks: PR run [44686357940](https://github.com/kanlerxz87-cyber/Zone3/actions/runs/44686357940) passed; on the merge push, `Publication checks` [44686520931](https://github.com/kanlerxz87-cyber/Zone3/actions/runs/44686520931) and `pages build and deployment` [44686519931](https://github.com/kanlerxz87-cyber/Zone3/actions/runs/44686519931) both succeeded.
- Merged-tree gates: `python3 tools/publish.py` — 53/53 commands, 0 failed, twice, byte-identical tree; `check_publication.py` — 131 HTML pages, 29 reader/workspace pages, 141 official-source rows, 27 indexable URLs, 13 feed items; `check_feed_readme.py` — every measured design row current.
- Live read-back at `?revision=2ebb5a9`: `AI-1309-P1` renders with `AI-1309-Q1` as its evidence anchor, and the executive brief shows the AI-permission row as "Disabled pending a specific approval" alongside 5 / 13 / 47 / 0.
- The first post-merge gate run is the strongest evidence for the new check: it failed on the merged tree because the brief still said 126 pages when the tree had 131, which is exactly the staleness this pass set out to catch.

No traffic, ranking, conversion, commission or revenue claim was added. No account, API, model or tracking configuration changed. Product intent, Associates account/API approval, Search Console access and `FLG-003` remain open.
