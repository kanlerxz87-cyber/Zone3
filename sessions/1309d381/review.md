# Repository review — session `1309d381` (2026-11-20)

## Scope and method

This is a local review of the current publication, decision registers, automation configuration and build gates after the required rebase onto `bb3d554` (PR #212). The repository was inspected directly; this session did **not** fetch Amazon or Google pages live. Official-source dates below are the dates already recorded in the repository, not a claim of a new re-read. A separate, merged verification record from session `fc812c5e` re-fetched the five submitted links and re-read the Amazon disclosure/link clauses on 2026-11-20: [`sessions/fc812c5e/verification-2026-11-20.md`](../fc812c5e/verification-2026-11-20.md).

No account, API, Search Console, analytics-host, or Associates report access is available from the repository. No private credentials or account screenshots were requested or stored.

## What already exists

- **Reader-facing publication:** the root page and category/shop pages lead with products and buyer questions. The current catalogue has five submitted links (three air fryers and two meat thermometers); 11 question-led guides are registered. Session `fc812c5e` reports that all four titles proposed in the user brief are already published as guides, and labels them editorial hypotheses rather than demand claims.
- **Decision desk:** `suggestions/index.html` is generated from `data/publication.json`. At this base it contains six selectable paths, 30 proposals, 39 decision questions, a copy-ready design prompt and a browser-local review/export flow. A selection does not publish or implement changes.
- **Affiliate evidence:** all five product-intent records have blank intended ASIN, official listing URL, confirmation date and source fields; observed redirect destinations stay separate. The tracking ID is owner-supplied and unvalidated. The current site and the merged verification record explicitly leave `FLG-003` unresolved; they do not call the supplied short links invalid.
- **Trust and publication mechanics:** the current generated pages include the Associates disclosure and sponsored product links; `tools/publish.py` is the full build/release chain for the static publication. It runs deterministic builders and checks; its header states that it does not call remote APIs or access accounts.
- **Measurement:** `data/shop/measurement.json` defines five events, but `enabled` is `false` and `endpoint_url` is empty. `data/shop/campaign-ledger.json` has zero rows. There is no production click collection, Search Console report, authorized Associates report, conversion score, or revenue forecast recorded here.

## AI and data-permission finding

The repository's official-source register links Amazon Associates Program Policies (S02) at <https://affiliate-program.amazon.com/help/operating/policies>. The existing policy-fact record `data/policy_facts.json` PF-22–PF-25, last recorded as read 2026-11-13, quotes restrictions on automated data mining and on aggregating, analyzing, extracting or repurposing Product Advertising Content through Creators API, PA API or Data Feeds, including direct model training/fine-tuning, absent express prior written approval. It also records a restriction on third-party use of Program Content to develop or improve language/multimodal or machine-learning models. Those lines are an existing repository record; they were **not** independently re-fetched in this session.

No express written approval, product-data API access, or model-use permission is recorded. Therefore this review recommends **not enabling Amazon-product-content analysis, training, automated product scoring, or AI-written product claims**. Safe work in this pass is limited to the review workflow, data-permission question, design prompt, deterministic build gates and source-linked summaries. Generated text is not treated as verification.

## Missing information that blocks a responsible “AI affiliate platform” decision

1. **Product intent:** owner-confirmed intended ASIN, official listing URL, confirmation date and source for each of the five submissions. Do not infer these from observed redirects. See `P26-Q1` and the intent-record page.
2. **Account and attribution:** confirmation that the site and `shopnow047c-20` belong to the intended enrolled Associates account, plus one enrolled-workflow Special Link and report check per intended product. See `P26-Q2`, `P27-Q6`, and `FLG-003`.
3. **AI permission/data scope:** express written Amazon approval, if needed, stating the permitted inputs and operations; whether any API/data-feed use is allowed for analysis or model-related work; and a documented model/vendor data-handling boundary. New question `1309-Q1` will collect the answer without storing credentials.
4. **Real demand and outcomes:** verified Search Console query/page reports and authorized Associates reports with reporting dates and provenance. Without them, “trending,” “high-converting,” commission potential, and optimization scores remain unsubstantiated. See `P26-Q4`, `P26-Q5`, and `E61-Q1`.
5. **Production collection:** a durable host and an approved logging/retention/privacy configuration before the five-event prototype can be switched on. GitHub Pages is static; a successful Pages build does not deploy the collector.
6. **Editorial authority:** a named human editor and a review/sign-off rule before AI-assisted drafts are published as editorial content. The project does not claim hands-on testing or a named human reviewer.

The suggestion register records who can supply each answer, a discovery action, and a safe default. The AI-specific proposal is review-only: it does not enable a model, ingest product data, replace links, or publish new guides.

## Irregularity found for this pass

- **RSS count drift:** the checked-in `feed.xml` has 11 `<item>` entries, but `DESIGN_PROMPT.md` section 3 says 29 and the README's generated facts block says 4. These are stale/mis-scoped repository counts, not traffic evidence. The 29 figure is noted in the prior review as a broader register-union count, not the shipped RSS item count. This pass will correct the design-brief wording and regenerate the README fact block from the feed builder.

## Official sources for manual review

- Amazon Associates Program Policies (S02; PF-22–PF-25 cite this source): <https://affiliate-program.amazon.com/help/operating/policies>
- Amazon Associates Program Operating Agreement (S01): <https://affiliate-program.amazon.com/help/operating/agreement>
- Amazon Creators API introduction (S04): <https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction>
- Google Search Console setup and query reporting: <https://developers.google.com/search/docs/monitor-debug/search-console-start>
- Google people-first content guidance: <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- GitHub Pages hosting limits: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>

No new product-level fact, price, rating, review count, commission rate, trend, conversion or revenue claim is added by this review.
