# Requirements

The project brief, decomposed into a tracked list. R01–R21 come from the brief verbatim;
R22–R30 are the delivery requirements for this session.

**14 implemented**, **12 partial**, **4 blocked**, out of 30.

On the site: [Requirements](../requirements.html). Machine-readable version:
[`data/requirements.json`](../data/requirements.json).

## The brief

> Build an AI-powered Amazon affiliate marketing platform that automates product research, identifies trending and high-converting products, analyzes pricing, reviews, competition, and commission potential, and generates SEO-optimized product articles, comparisons, and buying guides. The agent should identify profitable niches, create engaging marketing content, publish and manage affiliate links, track clicks and conversions, and continuously optimize campaigns to maximize affiliate revenue. Prioritize automation, scalability, data-driven decisions, and compliance with Amazon Associates policies and disclosure requirements.

## Matrix

| ID | Requirement | Status | Evidence | Gap | Flags |
| --- | --- | --- | --- | --- | --- |
| `R01` | Automate product research | Partial | tools/build.py regenerates every page from data/*.json; docs/RESEARCH.md records the resolution method. | No scheduled crawler or API-driven refresh runs on GitHub Pages (static host). | [F10](FLAGGED.md) |
| `R02` | Identify trending products | Partial | Amazon's own 'N bought in past month' demand signal captured for all three products (S2, S4, S6). | Best Sellers Rank was not readable from any official static render, so it is left blank. | [F12](FLAGGED.md) |
| `R03` | Identify high-converting products | Blocked | Conversion rate is a report inside Associates Central. | No Associates account is connected, so no conversion data exists. Field left blank by rule. | [F15](FLAGGED.md), [F07](FLAGGED.md) |
| `R04` | Analyze pricing | Partial | Current price, list price, unit price, lowest other offer and discount depth are captured and tabulated on analysis.html. | Live price tracking and price alerting are prohibited by Participation Requirements 6(y) unless Amazon agrees. | [F09](FLAGGED.md), [F16](FLAGGED.md), [F01](FLAGGED.md) |
| `R05` | Analyze reviews | Partial | Star rating and ratings volume captured for all three products (S2, S4, S6). | Star histogram and review text are JavaScript-only and behind sign-in; sentiment is not captured. | [F14](FLAGGED.md) |
| `R06` | Analyze competition | Partial | Internal three-way comparison on comparison.html across price, rating, volume, demand and commission band. | No wider competitor set was captured, because only the three supplied links are in scope and no other official source was used. | — |
| `R07` | Analyze commission potential | Partial | The full official rate table is reproduced on commission.html (S7) with the qualifying-purchase and payment rules (S8). | Amazon does not publish the commission category per ASIN, so the per-product rate is left blank rather than guessed. | [F06](FLAGGED.md) |
| `R08` | Generate SEO-optimized product articles | Partial | One article-style page per product with title, meta description, canonical Amazon link, structured spec table and sources. | Articles are authored, not machine-generated on a schedule; no LLM is wired in. | [F10](FLAGGED.md) |
| `R09` | Generate comparisons | Implemented | comparison.html — side-by-side table of all three products with a source link per row. | — | — |
| `R10` | Generate buying guides | Implemented | category-home-kitchen.html carries an air-fryer buying guide built only from values verified on Amazon. | — | — |
| `R11` | Identify profitable niches | Partial | Niche identified as Home & Kitchen > Air Fryers, all three supplied products land there (S1, S3, S5). | Profitability per unit cannot be verified without the per-ASIN commission category. | [F06](FLAGGED.md), [F07](FLAGGED.md) |
| `R12` | Create engaging marketing content | Partial | Content pages, category guide and comparison are written; product pages carry the Amazon listing deep link. | No A/B testing or content variants, because no traffic or conversion data exists to test against. | [F15](FLAGGED.md) |
| `R13` | Publish and manage affiliate links | Partial | Every link is held once in data/products.json and rendered from there, so a tag can be applied in one place. | No Associates tag exists, so links are untagged. The supplied short links should not be used as the live Special Links. | [F07](FLAGGED.md), [F03](FLAGGED.md), [F05](FLAGGED.md) |
| `R14` | Track clicks | Blocked | Clicks are reported only inside Associates Central. | No Associates account connected. Field left blank by rule. | [F15](FLAGGED.md), [F07](FLAGGED.md) |
| `R15` | Track conversions | Blocked | Conversions are reported only inside Associates Central. | No Associates account connected. Field left blank by rule. | [F15](FLAGGED.md), [F07](FLAGGED.md) |
| `R16` | Continuously optimize campaigns to maximize affiliate revenue | Blocked | Optimisation loop is specified in docs/REQUIREMENTS.md with its inputs and decision rules. | A loop needs clicks and conversions, which do not exist yet, plus a runtime, which a static host does not provide. | [F15](FLAGGED.md), [F10](FLAGGED.md), [F12](FLAGGED.md) |
| `R17` | Prioritize automation | Partial | Site is fully generated from a JSON data layer by tools/build.py; no page is hand-edited. | No scheduler or runtime on GitHub Pages to execute the automation. | [F10](FLAGGED.md) |
| `R18` | Prioritize scalability | Partial | Adding a product is a single JSON entry; the generator emits its category page, product page and every table row. | Ingestion of new products is still manual. | [F10](FLAGGED.md) |
| `R19` | Prioritize data-driven decisions | Implemented | Every value carries a source id and a verified/unverified status; unverified values render blank and are listed on flagged.html. | — | — |
| `R20` | Compliance with Amazon Associates policies | Implemented | compliance.html maps each obligation to the exact policy text with a link (S8, S9). | Two blocking conflicts remain open on the data itself: F01 (prices) and F02 (star ratings). | [F01](FLAGGED.md), [F02](FLAGGED.md), [F03](FLAGGED.md), [F07](FLAGGED.md), [F08](FLAGGED.md), [F09](FLAGGED.md), [F11](FLAGGED.md) |
| `R21` | Compliance with disclosure requirements | Implemented | Site-wide disclosure banner and a dedicated compliance page citing the FTC (S10) and Participation Requirements 3(b) (S8), which names the FTC Endorsement Guides. | The Amazon affiliate disclosure text must also be enabled once a tag exists (it is currently worded to match the untagged state). | [F07](FLAGGED.md) |
| `R22` | Create an executive summary outlining important details | Implemented | EXECUTIVE_SUMMARY.md and executive-summary.html. | — | — |
| `R23` | Review the repo line by line, verify from official sources, link for manual review, flag irregularities | Implemented | docs/RESEARCH.md, docs/VERIFICATION.md, docs/FLAGGED.md. Repository contained only README.md at the base commit. | — | [F17](FLAGGED.md) |
| `R24` | GitHub Pages live site with a clean landing page and subpages organized by category | Implemented | https://kanlerxz87-cyber.github.io/Zone3/ — index.html plus categories.html, category-home-kitchen.html and one page per product. | — | — |
| `R25` | Clean, user friendly, simple, easy to use UI like a simple dashboard | Implemented | Single sidebar dashboard shell, one stylesheet, no framework, no client-side router. | — | — |
| `R26` | Contain all entries and findings in a simple, easy to read table format | Implemented | Products, commission table, requirements matrix, flags, sources and verification log are all tables. | — | — |
| `R27` | Every table row must have a source link to an official site | Implemented | Every data row carries a Source cell linking to amazon.com, affiliate-program.amazon.com or ftc.gov. Verified by tools/check_links.py. | — | — |
| `R28` | If a value cannot be confirmed from an official source, leave it blank and flag it as unverified | Implemented | Null-valued fields render as an explicit 'Unverified' cell, never as a guess. See docs/VERIFICATION.md. | — | — |
| `R29` | Publish flagged irregularities on a clearly labeled Flagged for Review page with source links | Implemented | flagged.html renders data/flags.json with a source link or an explicit 'no official source' note per item. | — | — |
| `R30` | Open a pull request, merge it, confirm GitHub Pages deploys, record the result in COORDINATION.md | Implemented | Recorded in COORDINATION.md task T12 after the deploy check. | — | — |

Four requirements are marked blocked: track clicks, track conversions, identify high-converting products,
and continuously optimize campaigns. All four fail for the same two reasons, and both are fixable.

### Why they are blocked

**No Associates account is connected.** Amazon reports clicks, conversions and the realised per-order
commission rate only inside Associates Central. Without that data there is nothing to optimise against,
so the requirement is genuinely blocked rather than deprioritised.

**GitHub Pages has no runtime.** It serves static files. There is no server, database, scheduler or model
endpoint, so nothing can run on a schedule and nothing can be generated per request.

### The shape that fits

The site is already built to be generated. `tools/build.py` reads `data/*.json` and writes every page, so
the whole site is a pure function of the data layer. That means automation only has to produce JSON; it
does not have to produce HTML.

**Ingest, scheduled.** A GitHub Actions workflow on a cron runs a collector that calls the Product
Advertising API or Creators API for each ASIN in the catalogue, writes the response into
`data/products.json` with a fresh capture timestamp and the source id, and opens a pull request. The
price and rating columns then satisfy Participation Requirements 2(b) and 6(t) because they came from the
API, and the staleness problem disappears because the refresh is automatic.

**Attribute, from reports.** A second scheduled job ingests the Associates Central reports into a
time-series store, keyed by the sub-tag in each link. Amazon permits additional sub-tags for exactly this
purpose, and prohibits assigning them dynamically per user, so the sub-tags must be per-placement and
static.

**Decide, on rules.** With clicks and conversions per placement, the optimisation loop becomes a small set
of explicit rules: demote any product whose conversion rate falls below a threshold over a trailing
window, promote any content placement whose earnings per hundred clicks exceeds the catalogue median, and
retire any page whose promotion badge has expired. Each rule writes a proposed change to the data layer as
a pull request, so a human approves before anything ships. That keeps the decision auditable, which
matters because a wrongly automated price claim is a policy breach.

**Generate content, with a human gate.** Article, comparison and buying-guide generation can be templated
from the same verified data layer, because every claim on those pages is already a field in
`data/products.json`. The safe pattern is generation into a pull request with the source id inline on
every claim, never direct publication, so that a hallucinated value is caught at review rather than
published.

### Sequencing

Fix the blocking flags first. Nothing in this design works until an Associates tag exists and API
credentials are in place, because without them the ingest job has no data source and the reports job has
no reports. The order is: tag, then API credentials, then ingest, then attribution, then the optimisation
rules, then content generation.

### What deliberately stays manual

Publishing. Every automated change lands as a pull request. Amazon holds the Associate solely responsible
for the accuracy of everything on the site and can terminate the account without notice for a breach, so
automated direct publication is a bad trade at any traffic level.

