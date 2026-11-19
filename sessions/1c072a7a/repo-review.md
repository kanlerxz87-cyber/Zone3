# Repository review — publication consolidation, 2026-11-19

## Scope and method

Original base `3883a0b` contained 504 tracked files and competing reader layers alongside many
historical verification records. This review read the coordination board, current generators,
publication/runtime code, product/intent/source/flag/campaign data and gate definitions; executed
the inherited and new release commands; inspected real browser renders and interactions; and
fetched the bounded official sources listed in `verification-2026-11-19.md`.

This is a comprehensive **architecture/release review**, not a claim to have newly re-read every
historical assertion or inaccessible account. No synthetic sales, source reads or credentials are
substituted for missing access. Main advanced through PRs #164/#166/#167 and governance follow-ups
to `0ee4153` during implementation. The branch was rebased, not used to overwrite that history.

## Repository and build ownership

The old root could be rewritten by `scripts/build_site.py`, the cba front-door injector, the old
publication generator, the C3 pass and the C17 pass. The site also injected two different analytics
stacks. This made another independent microsite or another root post-pass the wrong long-term fix.

The current release has one canonical command, `tools/publish.py`, and one reader-content owner,
`tools/build_publication.py`, using `data/publication.json`. The retained publication entry point
calls it after legacy evidence generation. One shared chrome module/postpass supplies navigation,
disclosure, footer, search, canonical and indexing policy. Rebuilding must produce no tracked diff.
CI repeats this requirement from a fresh checkout.

All completed C3/C17/3301 source files, CSS, image and review/coordination records are retained.
Their shopper composition is rendered on a temporary page using their unchanged source renderers,
then published as `publication-prior.html` with an earlier-edition note and noindex. Its decision
handoff and C3-F-01 provenance caveat remain reachable. The sole current research nav group and
footer retain their newly added Analysis, Air-fryer category and Measurement destinations as well
as the older dashboard directory. No session's intended-product register or historical claim is
silently replaced with a redirect observation.

## Buyer experience and original contribution

The publication leads with kitchen decisions, not verification tasks. It has a consistent identity,
original generic product-format diagrams, a labelled generated kitchen still life, category shelves
for three air fryers/two thermometers, a five-product comparison, six question-shaped guides,
related reads, source notes, dates and an honest publisher byline. The seasonal guide is an editorial
planning exercise, not a holiday demand/deal claim. Search uses a public local JSON index.

The guides add shopping checklists and decision structure rather than duplicating retailer copy:
compartment versus total capacity, usable space, manual/clearance checks, part-by-part care,
actual tasks rather than preset totals, thermometer workflow and food-specific safety context.
They explicitly state what has not been established and do not invent measurements or winners.
They are modest listing-based guides, **not** hands-on reviews or demonstrated SEO success.

Current article authorship is the disclosed publisher, Zone3 Editorial. No fabricated named human,
credential, personal experience, review score, exact-model generated photograph or testing evidence
is used. New product artwork says format illustration and the source details explain the limit.
Official references: [FTC disclosure guidance](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers),
[Google review guidance](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews).

## Product identity, affiliate links and provenance

All five supplied URLs remain exact and visibly identify Amazon. Fresh redirects/title/breadcrumb
observations are recorded as 2026-11-19 observations, not owner intent. Intended ASIN, official
intended listing, confirmation date and source remain blank and separate in the inherited register.
The selected ID `shopnow047c-20` is user-supplied, not account-verified. Prices, ratings, review totals,
independent performance, certification checks and availability remain unpublished in current cards.

The disclosure sentence appears directly under the masthead and is repeated in the footer. New
links carry `rel="sponsored"`; the whole-tree sponsorship gate is retained. Do not infer full legal
or account compliance from an HTML attribute or successful redirect. [Agreement §§1/5](https://affiliate-program.amazon.com/help/operating/agreement),
[Program Policies](https://affiliate-program.amazon.com/help/operating/policies), and
[Google sponsored-link guidance](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
are linked for manual review. FLG-003 remains unresolved. The supplied short links are not called
invalid; the next permitted validation is an authorized enrolled workflow and reporting check,
not artificial clicks, self-purchases or attaching invented visitor-level tags.

Every data row in the **16 current reader/review pages** carries an official HTTPS source link;
`tools/check_publication.py` checks 51 rows, exact hostnames, source IDs, separate intent fields,
unknown figures, authorship, image labels/dimensions, disclosure, one runtime, canonical set and feed.
Code/operational observations are explicitly distinguished from the third-party rule/context linked.

### Historical provenance remains an irregularity

The integrated whole-tree verifier reports 159 pages / 2,561 rows, with 546 non-blocking advisories
under its inherited-page classification; its provenance breakdown includes 216 uncited rows and
282 repository-only rows. These are not silently waived or called freshly verified. Some official
Docs/Google references fall outside that older classifier's Amazon/FTC category, while genuine
uncited historical rows also remain. The older style lint retains 22 baseline advisories (zero new).
C3-F-01 and P26-F05 publish this limit. Retrofitting arbitrary official URLs onto repository-state
claims would be false provenance; a future focused cleanup must classify and actually research
those rows. The release is not described as universal historical claim verification.

Immutable-row union check: main's 149 flags and 83 sources were all retained unchanged; this session
adds five flags and four scoped sources, giving 154 and 87 respectively. No source ID is reused.
Current product/intent/campaign registers are not rewritten to infer missing values.

## Findability and publishing

Four existing guide URLs are updated in place and two distinct thermometer/hosting guides are added.
The canonical sitemap contains exactly 14 indexable reader URLs. Historical/research content stays
reachable with self-canonical URLs and `noindex,follow`, not falsely canonicalized to unrelated copy.
The RSS union retains other desks' entries, deduplicates canonical guides and has 24 entries.
The crawler is not told that canonicals guarantee indexing. References actually read:
[canonical guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls),
[Search Console getting started](https://developers.google.com/search/docs/monitor-debug/search-console-start).

A guide review every 14 days is an operating plan gated on evidence. Search Console ownership,
query/page reports, search demand, traffic growth and rankings are not verified. No account action
or sitemap submission is claimed. New topic selection remains an editorial hypothesis until dated
authorized query evidence exists.

## Measurement, privacy and persistence

Only `measure.js` is injected; a global guard prevents duplicate initialization. The existing default
five names are retained, not represented as names supplied by the brief. Fetch explicitly omits
credentials/Referer, strips query/hash, never writes analytics storage and respects GPC/DNT/Save-Data.
The preview sends real HTTP requests to a local same-origin collector; production config remains off.

The collector validates event/version, exact origin, finite public page and product-target lists,
content type and <=2 KiB body. It has a global write ceiling and five-second connection timeout,
server-assigned UTC day, 90-day aggregate retention, lock/atomic persistence and a disabled-by-default
private counts readout. It retains no raw event rows, IP/UA/referrer/cookie fields or visitor IDs.
Transport IP/browser headers are inevitably visible to the receiving host; upstream logging and
retention require separate verification. Origin validation is not bot authentication. The store
lock is process-local; do not run multiple workers against one JSON store.

Ten isolated HTTP/config regression tests, collector self-tests, the retained browser-stub suite,
18 extended Node regressions and real browser checks cover delivery/rejection, restart reload,
concurrency, retention boundary, unknown fields/targets, read protection, opt-outs and invalid config.
Preview events and synthetic review choices are never campaign evidence. No visitor sub-tag or
hidden conversion event is created. [Policies 2(b)](https://affiliate-program.amazon.com/help/operating/policies)
and [Pages hosting/IP-log documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
are the relevant manual-review references, not an assertion of legal approval.

Missing production host, applicable privacy/consent review, authorized reporting and account access
are published in P26-F01/F04 and the decision register. The endpoint cannot run on static Pages;
an ephemeral sandbox URL is not silently substituted as production. The campaign ledger stays empty.

## Decision readiness, automation and human handoff

The suggestions workspace has six proposals and nine explicit questions. Each separates what is
known/answered so far, what is missing, a discovery action, the blocked decision and a safe default.
A reusable design prompt carries the same constraints. Local save/clear, export and clipboard are
functional. Saving never publishes, activates collection, spends money or changes an account.

Safe build, structural provenance, sponsored-link, disclosure, feed/sitemap and privacy checks are
automated. Intent/account confirmation, link attribution, authorized API access/asset rights,
independent tests, legal basis and first-party order reports cannot be manufactured by that pipeline.
Optimization remains gated; there is no made-up traffic score, popularity ranking or revenue model.

## Hosting and release review

[GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
raise a real suitability issue for business/commercial-transaction-oriented use. This is published
as P26-F02 and in the executive/privacy/decision areas. A technically successful Pages deploy is
not policy approval, and the finding is not overstated as a blanket ban on every affiliate article.
Use suitable commercial hosting before scaling the business and a durable reviewed collector host.

Release evidence is in `release-checks.json`, `browser-checks.json`, `screenshots/` and the final
`COORDINATION.md` publish record. Browser testing includes actual Chromium at desktop/mobile sizes,
all 16 reader/review pages, keyboard/focus, search/filter/review fallback paths, both root and project
base, five events and opt-outs. Automated WCAG A/AA checks have no reported violations in that scope;
manual screen-reader review, Firefox/Safari and real-user Core Web Vitals remain unverified. No
claim is made about Amazon account attribution, Google indexation or production analytics results.
