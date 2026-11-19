# Zone3 Kitchen

A buyer-first kitchen publication: source-linked product introductions, practical question-led
guides, and a separate review/research workspace. Plain HTML, CSS and JavaScript;
no third-party front-end dependency, scraped product imagery or invented reviewer.

Counts are never typed into this file by hand. The block below is generated from the registers by
`python3 tools/build_publication.py` (region `z3:register-facts`) and is checked in CI, so a page,
this README and a register cannot disagree about how big the site is. Before this rule the headline
here carried a guide count three short of the register's, and the ownership bullet below it was retyped
by hand each time the desk grew — both are the same defect, recorded as `E41-F01` and closed by the gate
that reads this file.

<!-- z3:register-facts -->
| Register | Now | File |
|---|---|---|
| Question-led guides | 11 | `data/publication.json → guides` |
| Indexable reader URLs | 20 | `data/publication.json → indexable_pages` |
| Supplied product links | 5 | `data/publication.json → products` |
| Open decision-readiness questions | 39 | `data/publication.json → questions` |
| Suggestions on the desk | 30 | `data/publication.json → proposals` |
| Paths a reviewer can choose | 6 | `data/publication.json → paths` |
| Design-brief blocks | 13 | `data/publication.json → design_prompt` |
| Scoped official references | 17 | `data/publication.json → sources` |
| RSS entries across all editorial desks | 4 | `feed.xml` |
| Campaign ledger rows | 0 | `data/shop/campaign-ledger.json` (empty by design) |
<!-- /z3:register-facts -->

**Site:** https://kanlerxz87-cyber.github.io/Zone3/ · **Current executive brief:**
[`executive-brief.html`](executive-brief.html) · **Review proposals:**
[`suggestions/index.html`](suggestions/index.html) · **This session's repo review:**
[`sessions/222cfe13/repo-review-2026-11-19.md`](sessions/222cfe13/repo-review-2026-11-19.md) · **Release record:**
[`COORDINATION.md`](COORDINATION.md#session-1c072a7a--publication-consolidation-and-buyer-first-experience-2026-11-19)

## Build, check and preview

From the repository root, with Python 3.11+ and Node 22+:

```bash
python3 tools/publish.py             # full retained generator chain + every release check
python3 tools/publish.py --check     # checks only; fails on drift, bad links or privacy regressions
python3 tools/preview.py --host 0.0.0.0 --port 3000
```

The preview accepts both `/` and `/Zone3/`. It serves a **development-only** analytics config
pointing to its real same-origin `/collect` endpoint. It never changes the production config.
Preview aggregates live under ignored `.preview/`, never in the campaign ledger. Do not use
a sandbox preview as a durable production analytics endpoint.

The release command lists its exact builders and checks in [`tools/publish.py`](tools/publish.py).
GitHub Actions rebuilds the tree, runs the gates and requires `git diff --exit-code` to be clean.
Optional real Chromium/axe checks, pinned dependencies and representative screenshots are in
[`sessions/1c072a7a/README.md`](sessions/1c072a7a/README.md). Core release checks need no npm install.
A structural source-link check is not independent fact verification; historical provenance
advisories remain explicitly published as [C3-F-01](flagged.html#C3-F-01).

## Current publication ownership

- **Content and dates:** [`data/publication.json`](data/publication.json). It holds the dated
  redirect/title observations, the guide set, the scoped official references, every batch of
  proposals, the decision paths and the decision-readiness questions (each with an answer-capture
  field on the suggestions page) and the design brief. Intended ASINs/URLs/dates/sources stay
  distinct from observed destinations. Prices, ratings, review totals and tested performance stay
  empty. Reader-facing counts and check dates are derived from this file by the renderer — and by
  this README's register-facts block — so a refresh of the register cannot leave a page asserting a
  stale number or date (`P27-F02`, `P27-F04`, and the residual drift recorded as `E41-F01`).
- **Reader renderer:** [`tools/build_publication.py`](tools/build_publication.py), called by the
  retained publication entry point in the canonical chain. Do not hand-edit its output.
- **One shared shell:** [`tools/publication_chrome.py`](tools/publication_chrome.py) and
  [`sessions/aebf0747/publish_pass.py`](sessions/aebf0747/publish_pass.py). The disclosure is under
  the masthead and repeated in the footer. All dashboards stay accessible through one **Behind
  the site** group and the footer directory. The previous C3/C17 shopper edition is retained at
  [`publication-prior.html`](publication-prior.html), not silently discarded.
- **Findability:** every canonical reader URL in `sitemap.xml`, the guide set, local search and the
  unified RSS feed retaining the other editorial desks (the register-facts block above carries the
  current figures). Research/duplicate editions remain reachable
  with their own canonical URL and `noindex,follow`, rather than competing as new front doors.
  One guide review every 14 days is an operating plan, not a demand or ranking claim.
- **Art and authorship:** labelled generated kitchen context and original generic format diagrams,
  not model photography or test evidence. Zone3 Editorial is a disclosed publisher byline,
  not a fabricated human expert.
- **Decision desk:** [`suggestions/index.html`](suggestions/index.html) holds the paths (what each
  one changes, needs, unblocks and still cannot claim), the individual proposals, the register of
  open questions with the answer owner and the discovery action for each, the intake shape a new
  suggestion has to take, and the design brief with per-block copy (block count above). Local Save / Clear,
  JSON export: choosing a path never implements it, activates analytics, changes an account or
  spends money.
- **Design brief:** [`DESIGN_PROMPT.md`](DESIGN_PROMPT.md) is the paste-ready version — rails R1–R12
  each quoting the official clause and its source row, the measured page inventory, the
  allowed/forbidden component table, the copy rules, and a definition of done keyed to the gates as
  they run today. It decides nothing on its own; where it needs an answer, it names the question.

## Measurement and account boundaries

Production collection is **OFF** (`data/shop/measurement.json`: blank endpoint, no deployment
verification). One guarded runtime, `assets/measure.js`, implements `page_view`, `outbound_click`,
`guide_view`, `intent_view`, `flag_view`. The retired `track.js` source is retained but not injected.
The self-hosted collector is [`tools/analytics_endpoint.py`](tools/analytics_endpoint.py).
It stores daily aggregates for 90 UTC days, not raw events or visitor identities. Origin/page/
product allowlists, body-size limits, a global write ceiling, private optional counts readout and
atomic persistence are tested. Browser requests omit credentials and Referer; GPC, DNT and
Save-Data disable them. Transport IP/browser headers are necessarily visible to the receiving host
but not logged or stored by this collector. Hosting/proxy logging requires separate review.

The supplied ID **`shopnow047c-20`** is recorded, not account-verified. The exact supplied links
remain unchanged. Validate one Special Link/product through an authorized enrolled workflow,
including destination and reporting, before scaling. Their status stays unresolved under
[FLG-003](flagged.html#FLG-003); this project does not call them invalid.

No Search Console ownership or authorized Associates report is available. The campaign ledger is
empty; local test counts are not visitors, eligible sessions, orders, commissions or conversions.
No conversion score, popularity signal or revenue forecast is manufactured. Safe build/editorial
checks are automated; account/API permissions and original test evidence are not simulated.

**Commercial hosting needs review.** [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
restrict business/commercial-transaction-oriented use; a technical Pages deploy is not policy
approval (P26-F02). Pages is static and cannot run the Python collector. Review host suitability
before commercial scaling and use an authorized durable HTTPS collector with reviewed logging
before enabling production measurement. See [privacy](privacy.html), [the scoped verification
record](sessions/1c072a7a/verification-2026-11-19.md), and [the repository review](sessions/1c072a7a/repo-review.md).

---

The material below is retained **historical architecture and dated observations**, not a claim
that the old parallel front doors, counts or deferred features still describe the current release.
Use the current sections above and the executive brief where they differ.

## Historical platform notes — before the 2026-11-19 consolidation

Full-stack affiliate marketing intelligence for Amazon Associates: product intake and
verification, niche / pricing / review analysis, grounded SEO content generation,
campaign tracking, and compliance enforcement — with a build-time gate that refuses to
publish any value that cannot be traced to an official source.

**Live site:** https://kanlerxz87-cyber.github.io/Zone3/ · **this build's dashboard:** `/dashboard/`

> The repository root belongs to an earlier session's flat site. This build writes only inside its
> own page directories (`dashboard/`, `products/`, `commission/`, …) and never overwrites a file
> another build owns, so both halves are served side by side and cross-link to each other.

> **Integration note.** This branch was merged into `main` alongside four earlier sessions' work rather
> than over it: their flat pages (`products.html`, `pricing.html`, …), `scripts/`, `data/*.json` and
> `assets/app.js` are intact, this session's datasets live under `data/z3/`, its landing page replaced the
> root one, and their previous landing page is preserved at `landing-prior.html`. See FLG-026.

---

### Historical status at a glance (not current release counts)

| | |
| --- | --- |
| Products submitted | 5 (three on 2026-11-13; two more added by the owner's brief on 2026-11-17, session `cbb03ec7`) |
| Submitted tokens that are ASINs | **0 of 5** (they are short-link tokens) |
| Observed redirect destination listings | **5 of 5** |
| Product-attribute cells blank in the audit sheet | **45** (9 unavailable fields × 5 observed listings) |
| Official sources cited | 22 in `data/z3/`; 83 in the flat-site register (S60–S69 added 2026-11-16; S70–S75, S83–S88 added 2026-11-17; S90 = Google Search Central) |
| Open items published for review | 140 (flat-site register, `data/flags.json`; restored union after PR #158 dropped 24 — `5B-F-*`, `929-F-*`, `F-2F-*`, `G82-F-*`, `G84-F-01` back in, plus `CBB-F-01`…`CBB-F-04` and `Z1-F-01`…`Z1-F-04` added 2026-11-17) · 29 (audit build) |
| Compliance rules enforced in the build | 25 prohibitions + 5 mandatory text blocks; `scripts/build_read.py` additionally refuses to emit an uncited table row, a price pattern, a star-rating pattern or a stored Amazon image, and `read/**` is listed in `scripts/check_site.py`'s `PAGES` so the shared gate covers it too |
| Reader-facing marketing layers | **two, in parallel** — `/read/` (The Crisp Report, 11 pages, sessions `145b8df7`/`d18303ca`) and `/site/` (Air Fryer Field Notes, 18 pages, sessions `59d84c55` + `cba81fa5`). The repository root now opens on a front-door band that leads to both, and the overlap is recorded as `Z14-F-04` and `CBA-F-03` for the owner to resolve |

The five submitted links (`link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`,
`link.amazon/B00hJ57DV`, `link.amazon/B0c8moW59`, `link.amazon/B0f3GKalj`) carry **9-character
short-link tokens**, not ASINs. Amazon defines an ASIN as 10 characters, and
`https://www.amazon.com/dp/<token>` returns Amazon's *Page Not Found* page for all five tokens.
Following each short link was observed to land on a live listing: CHEFMAN 6 Qt dual basket
(B0CDY277D3), Emeril Lagasse 26QT (B09B7SB46R), Chefman 8 Qt TurboFry (B08DKYBTPH), ThermoMaven
1 Sec Professional Digital Meat Thermometer (B0DHZTCNR5, observed 2026-11-17) and CHEF iQ Sense
Smart Wireless Meat Thermometer (B0DZFD6R9Z, observed 2026-11-17). These observed destinations are
documented; whether they match the requester's intent is not established by an official source.
The Selected Tracking ID `shopnow047c-20` from the same brief is recorded in `config/platform.json`
with status **unverified** and is embedded in no link (CBB-F-02).

> **Correction, session `588693c9`, 2026-11-14.** This paragraph previously ended
> "…through Amazon's `plpRedirect=mhFallback` route, which confirms the identifiers select
> nothing." That was wrong. A direct fetch of a *known-valid* ASIN
> (`/dp/B0CDY277D3`, `/dp/B09B7SB46R`, `/dp/B08DKYBTPH`) also ends on a URL carrying
> `plpRedirect=mhFallback` while serving the correct product, so the parameter is **not**
> evidence of a failed lookup. The conclusion still stands on different grounds: a 9-character
> code cannot be an ASIN
> ([Creators API, ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter)),
> and `dp/<code>` 404s for all three. What remains genuinely unconfirmed is whether the three
> listings the short links open are the products that were intended. Record:
> `sessions/588693c9/verification-2026-11-14.json` (observation 588-V08).

The pipeline records the observed destination listings separately from the 9-character short-link tokens, and does not infer user intent from the redirects. Dynamic price, review, and performance values remain blank unless they can be supplied through the approved data path. Full audit trail: [`docs/verification-log.md`](docs/verification-log.md).

---

## Pages

| Category | Path | What it holds |
| --- | --- | --- |
| Dashboard | `/dashboard/` | KPIs, findings, navigation |
| Executive summary | `/executive-summary/` | The whole story in one read |
| Products | `/products/` | Intake + verification register, 12-field attribute sheet, link pipeline |
| Commission | `/commission/` | Amazon's published rate tables (Standard/Onsite/Creator Ads) + Bounty schedule |
| Niches | `/niches/` | Scoring model, input availability, 10 verified category constraints |
| Pricing | `/pricing/` | Price sheet, pricing rules engine, unblock sequence |
| Reviews | `/reviews/` | Review metrics, integrity constraints, compliant sentiment design |
| Content | `/content/` | Inventory, templates, claim-grounding contract, SEO mechanics |
| Campaigns | `/campaigns/` | Performance ledger, schema provenance, optimiser boundary |
| Compliance | `/compliance/` | Mandatory text blocks, programme economics, 25 prohibitions |
| Agent terms | `/agent-terms/` | Amazon's AI-agent rules, mapped clause by clause |
| Methodology | `/methodology/` | 8-stage pipeline, verification protocol, scalability, limits |
| Requirements | `/requirements/` | All 30 brief clauses traced to status |
| Sources | `/sources/` | Every official document cited, with what was observed |
| Flagged | `/flagged/` | 29 open items with source links and resolutions |
| Repo review | `/repo-review/` | Audit of the repository as found |
| **This pass (2026-11-14)** | `/` (root dashboard) | Independent re-verification of every load-bearing claim against its official source, with a per-claim result table; corrections V-F1/V-F2 published at `/flagged.html`; repo review at `COORDINATION.md` § *Part: session b8beb448* |
| **Final integration pass (2026-11-14)** | `/content-topics.html` | The editorial topic plan the brief asks for: 12 working article titles, the verified Amazon fact each is built on, the page that already carries it, and the rule that governs what it may not state. Every row carries an official source link |
| **This pass (2026-11-15)** | `/suggestions.html` | Design and marketing proposals for making the site read like a polished marketing affiliate website, the open questions that must be answered before any decision, and suggestions for discovering the missing information. Proposals are labelled as proposals; every factual row links its official source. Nothing on this page is implemented yet — it is published for review |
| **This pass (2026-11-16)** | `/design-brief.html` | **Design brief and prompt pack.** Why the site reads as machine output (ten findings against this repo's own files), a copy-and-paste prompt for the redesign, the design system, a twelve-article editorial plan, the organic-traffic architecture, the conversion architecture and an anti-slop checklist. Every factual row links its official source. Proposals only — nothing here is implemented |
| **This pass (2026-11-16)** | `/decision-queue.html` | **Review console.** All 22 proposals in one queue with a recommendation, priority, effort, risk, the question that blocks it and a decision state; then the information this project has, the information it does not have, and the actions that would get it. This is the section to review before implementing anything |
| **This pass (2026-11-16)** | `/sessions/757efebc/` | This session's record: executive summary, the 28 claims re-verified live on 2026-11-16 against the official page each one cites, the line-by-line repository review with link-outs for manual checking, and the four irregularities raised |
| **This pass (2026-11-16)** | `/site/` | **The reader-facing marketing site.** Built by `tools/build_i2_site.py` from `data/i2/*.json`, gated by `tools/i2_gate.py` (G1–G11). Twenty pages: a home page that leads with the three products, a comparison table where every row links the listing it came from and every blank cell says why, five buying guides plus three field-notes articles, a source register, a line-by-line verification log, a "flagged for review" page, the open-questions register, the house style, the front-door audit copy, and a decision board with 24 proposals, 16 open questions, 12 discovery actions, a 6-part prompt pack and an Accept/Reject/Defer control that changes nothing until a choice is recorded. Session ded63349 (2026-11-17) added the measurement layer (rows below). |
| **This pass (2026-11-16)** | `/read/` | **The Crisp Report** — the second reader-facing implementation of the Suggestions page: `read/index.html` front page, six sourced articles (`capacity`, `features`, `cleaning`, `bestseller`, `listing-titles`, `getting-paid`), a 13-attribute three-way `compare.html`, a five-question `buying-guide.html` with an FAQ, `read/category/air-fryers.html` and `read/method.html`. Generated by `scripts/build_read.py` from `data/editorial.json`; every factual sentence footnotes the official page and its capture date, and the build gate forbids prices, star ratings, review counts, testing claims and Amazon-hosted images. Overlaps `/site/` — see `Z14-F-04` |
| **This pass (2026-11-16)** | `/suggestions.html` | The ten 2026-11-15 proposals now carry an implementation status beside their original text, plus a 10-row answers register (what official sources settle vs what only the owner can settle, and the decision each unlocks) and four ranked paths with a recommendation |


| **Final integration pass (2026-11-14)** | `/content-topics.html` | The editorial topic plan the brief asks for: 12 working article titles, the verified Amazon fact each is built on, the page that already carries it, and the rule that governs what it may not state. Every row carries an official source link |
| **Suggestions & decisions** | `/suggestions.html` | Design and marketing proposals for making the site read like a polished marketing affiliate website, the open questions that must be answered before any decision, and suggestions for discovering the missing information. Proposals are labelled as proposals; every factual row links its official source. The **Decision log** records what session 5a56c084 implemented, deferred or left blocked (2026-11-16) |
| **Research Desk (2026-11-16)** | `/articles/` | The article hub: four grounded articles (affiliate-link anatomy, what you may say about an untested product, category & commission mechanics, the 24-hour session window) plus the full 12-topic plan with status. Every claim carries an inline source link; every article carries a verified / not-verified box and its editorial constraints. Proposals SUG-02/SUG-03 implemented |
| **This pass (2026-11-16)** | `/sessions/5a56c084/` | Independent re-verification of the three submitted links, the three destinations and the load-bearing policy pages, fetched 2026-11-16 — 8/8 observations match the register; two listing-title wording drifts recorded as Info items |
| **Executive summary (document)** | [`EXECUTIVE-SUMMARY.md`](EXECUTIVE-SUMMARY.md) | The standalone executive summary: verified facts, deliberately blank fields, capability status, and the three items that unblock the build |

---

## The reader-facing site (`/site/`, added 2026-11-16)

The repository's other builds are audit surfaces: they answer "what do we know and how do we know it",
which is the right answer for a reviewer and the wrong first impression for a reader deciding what to buy.
`/site/` is the reader-facing layer, and it keeps the same evidence rule while dropping the audit tone.

| Page | What a reader gets |
| --- | --- |
| [`site/index.html`](site/index.html) | The promise, the three products as cards built only on listing facts, a seven-row comparison, and an explicit statement of what is deliberately left out |
| [`site/products.html`](site/products.html) | Full listing detail, the nine-character-token caution, and a table of every field that is blank with the rule that requires it |
| [`site/guides/index.html`](site/guides/index.html) | The guide plan and the one live guide, `dual-basket-vs-single-basket.html` |
| [`site/evidence.html`](site/evidence.html) | 14 official sources read 2026-11-16, their observed text, and a 22-row verification log with the outcome per claim |
| [`site/flagged.html`](site/flagged.html) | 8 open items, each with severity, what was found, what would resolve it and its source |
| [`site/guides/capacity-maths.html`](site/guides/capacity-maths.html) | 6QT / 8QT / 26QT: what each listing states, the ratios shown as our arithmetic, and the four checks to run before choosing (session `cba81fa5`) |
| [`site/guides/air-fryer-oven-vs-basket.html`](site/guides/air-fryer-oven-vs-basket.html) | Why the 26QT is a different machine rather than a bigger one — including how Amazon's own browse nodes file it |
| [`site/guides/what-four-in-one-means.html`](site/guides/what-four-in-one-means.html) | Counted claims ("4-in-1", "24 presets", "450°F"): what is enumerated, what is not, and the two-minute check |
| [`site/guides/dishwasher-safe-baskets.html`](site/guides/dishwasher-safe-baskets.html) | What the "dishwasher safe" claim is a claim about, listing by listing, with the unstated parts left blank |
| [`site/answers.html`](site/answers.html) | The decision register: 9 questions research has settled (each with its official page), 11 only the owner can answer (known / missing / how to close / what it blocks / the default if unanswered), and the three paths those answers choose |
| [`site/style-guide.html`](site/style-guide.html) | House style: eleven banned constructions with the rule behind each and the sentence to write instead, plus the seven requirements every reader page must meet before it publishes |
| Front door on the root page | `index.html` opens with a band (brand, the three listings, the latest guides, the disclosure) generated by `tools/build_cba81fa5_site.py`; the dashboard content stays below it, unchanged |

**Current build entry point:** `python3 tools/publish.py` (see the top of this README).
The old sequence is retained in [the integration record](sessions/1c072a7a/legacy-build-order.md)
for reproducibility, not as a competing publishing command. C3/C17 source files remain unchanged;
`tools/build_publication.py` composes their preceding shopper edition on a temporary page and
publishes it at `publication-prior.html` with `noindex,follow`. Their direct root-patching CLIs
intentionally refuse the new `p26-main` owner instead of overwriting it.


Two redundant verification gates from session ded63349 run *after* the chain as checks (they are
no-ops on a tree `publish_pass.py` has already processed): `tools/apply_sponsored.py --check`
(product links must carry `rel="sponsored"`) and `tools/add_disclosure_banner.py --check`
(every page's §5 disclosure must sit above the fold).
| [`site/decisions.html`](site/decisions.html) | 24 proposals · 16 open questions · 12 discovery actions · 6 prompts · a working Accept/Reject/Defer control with an export. D-16..D-24 (ded63349, 2026-11-17): the five-event ledger, the cadence, the feed, the sponsored rel, the endpoint blocker, Search Console, the mobile pass, the front-page pass and the intent record |
| [`site/measure.html`](site/measure.html) | **How we measure** (ded63349, 2026-11-17): the five defined events, what the ledger stores and never stores (no cookies, no identifiers, no third parties, no server yet), the publishing cadence each new guide enters, live device-side counts with CSV export, and the honest limits — conversions, an endpoint and search queries all wait on owner decisions |
| [`site/intent-record.html`](site/intent-record.html) | **Product-intent confirmation record** (ded63349, 2026-11-17): per submitted link — intended ASIN (blank on purpose, owner-only), official listing URL, confirmation date, source, and the observed redirect target kept in a separate field; machine copy at `data/ded63349/intent_record.json`. The dashboard's own intent table lives on [`products.html`](products.html) (session 82372fd1) — the two never merge intended and observed fields |

**What is different about it, concretely:**

- **The disclosure is a banner above the navigation, not a footer line.** The exact Operating Agreement §5
  sentence is unchanged; its placement now also meets the FTC's guidance that a footer-only disclosure is
  likely to be missed ([I2-S01](https://affiliate-program.amazon.com/help/operating/agreement),
  [I2-S06](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)).
- **A blank cell is a designed element, not a gap.** It renders as `Not published` with a one-sentence
  reason and a link to the open item that blocks it.
- **No figure can be published by accident.** `tools/i2_gate.py` G6 fails the build on any money amount,
  percentage, star rating or review count that is not in the published-rate allowlist.
- **Nothing on the decisions page is applied by reading it.** Choices are held in the browser, exported as
  text, and only become changes when a later session implements what was accepted.

```bash
python3 tools/build_i2_site.py     # rebuild site/ from data/i2/*.json
python3 tools/i2_gate.py           # G1–G11; exit 1 on any prohibited construct (G11 = sponsored rel, added by ded63349)
```

---

## Layout

```
dashboard/ + 15 page dirs   generated static site (committed, served by GitHub Pages)
assets/app.css, app.js     dashboard styling; sort/filter; no runtime fetching
data/z3/*.json             single source of truth for every published cell in this build
data/*.json                datasets owned by earlier sessions (kept, not overwritten)
config/platform.json       configuration; credentials committed as null on purpose
tools/build_site.py        renders the site + enforces the provenance gate (G1–G8)
tools/verify_site.py       audits every HTML file in the tree (V1–V7), inherited pages included
tools/amazon_intake.py     ASIN validation → /dp/ probe → Creators API
tools/niche_score.py       niche ranking; never imputes a missing input
tools/link_report.py       provenance coverage report
docs/                      executive summary, verification log, repo review, compliance
landing-prior.html         previous root landing page, preserved verbatim
COORDINATION.md            shared task board for parallel agent sessions
```

---

## Working with it

```bash
python3 scripts/build_site.py            # rebuild the flat site + articles/ + session records
                                         # (runs scripts/build_5a56c084.py for the Research Desk)
python3 scripts/check_site.py            # data + HTML gate      (exit 1 on violation)
python3 tools/verify_site.py             # whole-tree release gate (exit 3 on violation)
python3 tools/link_report.py             # provenance coverage report
python3 tools/link_report.py --strict    # fail if any table is under-covered
python3 scripts/build_sitemap.py         # rewrite sitemap.xml from the checked-in tree
python3 scripts/build_sitemap.py --check # exit 1 if any live page is missing from it
python3 scripts/check_all_links.py       # crawl every published page for broken links

# verify the finding yourself
for a in B04G1MEwY B02NbDxp3 B00hJ57DV; do
  echo "$a chars=${#a}"; curl -sSI "https://www.amazon.com/dp/$a" | head -1
done
curl -sSI https://www.amazon.com/dp/B0CDY277D3 | head -1   # control: 10 chars, resolves

python3 tools/amazon_intake.py --link 'https://link.amazon/B04G1MEwY' --validate-only
python3 tools/amazon_intake.py --asin B0CDY277D3 --offline   # exit 0, queued for API
```

No third-party dependencies: the standard library only.

---

## The 2026-11-16 pass (session 5a56c084): the polished-marketing layer

Session 4f83ee7b (2026-11-15) published ten design/marketing proposals
(SUG-01…10) with ten owner questions (Q1…10) and six discovery actions
(D1…6) — published for review before anything was implemented. Session
5a56c084 is the follow-up pass that recorded a decision per proposal (the
**Decision log** on `suggestions.html`) and implemented only the unblocked
subset:

- **Design system rebuilt** — an editorial "research desk" look (warm paper
  ground, evergreen primary, copper accents, serif display headings) replaces
  the generic dashboard styling, across every generated page. No external
  fonts, no images, no JavaScript required.
- **Disclosure made prominent** — the Associates statement is now a strip
  directly under the header on every page (Operating Agreement §5, "clearly
  and prominently"; FTC: hard to miss), repeated beside product pointers on
  the articles, with the Amazon content disclaimer and trademark note in the
  footer.
- **Landing page is now a front door, not a file listing** — hero with the
  actual promise, the three listings as cards (labelled source links only),
  proof stats computed from the registers, the Research Desk's articles,
  a point-in-time "In the kitchen now" module anchored to the dated Best
  Sellers benchmark, a trust section, and a Decision Center banner. The
  20-link wall of navigation is grouped into five primary links plus a
  "More pages" menu; the site map is collapsed into it.
- **Research Desk** — `articles/index.html` plus four articles written from
  official pages, each claim linked, each with a verified / not-verified box,
  a how-this-was-written note and enforced editorial constraints. The desk's
  review checklist is published on the hub (SUG-03's anti-AI-slop gate).
- **Still blocked, on purpose** — no conversion CTA (SUG-05 needs the owner's
  Associates tag, Q1), no price/rating display (2(b)/6(t) — no approved data
  path), no campaign numbers (no account data). The decision log shows
  exactly what waits on which owner input.

Full decision records: `suggestions.html` Decision log and
`data/suggestions.json` (`implementation` fields); board record:
`COORDINATION.md` Part session 5a56c084.

---

## Design rule

**Automation without fabrication.** Every stage has an explicit failure mode: when a value
cannot be obtained from an official source, the field is set to `null`, a flag is raised, and
the pipeline continues. The gate is what makes that a guarantee rather than a style guide —
`build_site.py` exits non-zero if any table row has neither a source, nor a flag, nor a
repository anchor that actually exists.

Amazon's rules deliberately bound what the agent may do: no price-alerting features, no
per-visitor sub-tag attribution, no automated clicks, no link shortening, no storing Amazon
images, and no caching of Program Content beyond 24 hours. The agent identifies itself as
`Agent/Zone3ProductResearch` in its User-Agent, as the Program Policies' Agent Terms require,
and treats a block response as a result rather than an obstacle. Details on
`/agent-terms/` and `/compliance/`.

---

## Disclosure

As an Amazon Associate I earn from qualifying purchases.

CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED ‘AS IS’
AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.

Zone3 is independent and is not affiliated with, endorsed or sponsored by Amazon. Amazon,
Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates.

*No license file is present — see the flagged item in `docs/repo-review.md` §2.2.*

---

## Multi-session integration record

Six sessions worked this repository concurrently (`26634cd5`, `66a80e53`, `45ec61ec`,
`a9cafea1`, `7f84fea4`, `3c6cba43`). Sessions `7f84fea4`, `26634cd5`, `66a80e53` and `a9cafea1`
published through PRs #1, #3, #5 and #6; this session's integration ran as the merge commit that
follows.

| Question | Answer |
| --- | --- |
| Was any other session's work deleted? | **No.** Conflicting files were kept on both sides. |
| How were add/add conflicts resolved? | Theirs wins where they own the file (`assets/app.js`, `scripts/`, `data/*.json`, their flat pages); this session's files moved to non-colliding names (`assets/dashboard.js`, `data/z3/`, `landing-prior.html`, `docs/executive-summary-prior-sessions.md`). |
| Root landing | Theirs (the flat-page dashboard), with a link added into `/dashboard/`. This session's landing is at `/dashboard/`, and `landing-prior.html` keeps the earlier root revision verbatim. |
| Do both sites still work? | Yes — 32 HTML pages all serve; their `scripts/check_site.py` and this session's `tools/verify_site.py` both pass. |
| Root `index.html` | Owned by `scripts/build_site.py`. This build writes its landing to `dashboard/index.html` instead, so neither builder can clobber the other. |
| Anything found in *their* work? | One compliance gap, fixed additively: `category/kitchen.html` was hand-authored and had no Associates disclosure (required by Operating Agreement §5). Their generated pages all had it. Recorded at `B:FLG-025` in `COORDINATION.md`. |
| Anything this session corrected about *itself*? | Yes — it had concluded per-category commission rates were unobtainable because one endpoint redirects to sign-in. The statement is public; rates are now published. Recorded at `B:FLG-013`. |
---

## Shared data layer owned by earlier sessions

Kept intact by this integration; documented so the merged tree is navigable.

| Path | Contents |
| --- | --- |
| `data/sources.json` | Source registry of the earlier build (S01–S29): every official page used, its retrieval status, what it supports. |
| `data/policy_facts.json` | Verbatim policy quotes PF-01…PF-43 (PF-14 withdrawn), each with source and section. |
| `data/products.json`, `data/flags.json` | The earlier build's product dataset and flag register. Identical numbering to `data/z3/*` means different items. |
| `research/` | Session `33226b37`'s independent line-by-line verification record and product dossiers, with the ID mapping to that data layer. |
| `scripts/build_site.py`, `scripts/check_site.py` | The earlier build and its audit. That builder owns the root `index.html`; this one never writes it, so running either one is safe for the other. |
| `docs/executive-summary-33226b37.md` | Executive summary preserved from that session. |

Two independent verification records now cover the same three links and agree on the substance: all
three identifiers are 9 characters, every `/dp/` probe returns Amazon's *Page Not Found* page, and each
short link was observed to resolve to a live listing; the destination is documented without inferring user intent. Reaching that from separately fetched evidence
is what makes it a finding rather than a shared assumption. This session additionally published the
rate tables (`/commission/`), which neither earlier record had located.

---

## Session `c4e71983` — additive contribution

`main` already carried a canonical site and data schema from sessions `26634cd5`, `66a80e53`,
`7f84fea4` and `33226b37`. This session worked in parallel from baseline `ed1a796` and, on finding
the collision, reset onto `main` and contributed additively. **Nothing on `main` was overwritten.**

| Path | Contents |
| --- | --- |
| `data/c4e71983-commercial-snapshot.json` | Prices, ratings, promotion badges and velocity signals, with exact capture timestamps decoded from Amazon's `qid` parameter |
| `data/c4e71983-competitors.json` | Official Best Sellers in Air Fryers, ranks 1–6, with exact rating counts |
| `data/c4e71983-sources.json` | Source register for this session, namespaced `C4E-Snn` |
| `research/c4e71983-verification-log.md` | Line-by-line verification record, plus a mapping to `main`'s `S01–S29` / `FLG-001–021` |
| `research/c4e71983-commercial-snapshot.md` | Commercial snapshot, capture method, and the volatility risk |
| `research/c4e71983-niche-competition.md` | Niche, competition, pricing, and the clause that constrains the AI layer |
| `docs/executive-summary-c4e71983.md` | This session's summary, kept under its own name |
| `archive/c4e71983/` | This session's complete standalone 17-page dashboard, unchanged, browsable at `archive/c4e71983/index.html` |

**Correction worth knowing:** Amazon browse node `289742` is *Coffee, Tea & Espresso Appliances*,
**not** Air Fryers. It returns a valid, confidently-titled Best Sellers page, so a wrong guess looks
right. The Air Fryers node is **`17659096011`**.

**Caution on the commercial snapshot:** those prices were captured by hand. Program Policies
§2(b) permits price display only if Amazon serves the link or the data came from Creators API or
PA API. They are evidence for FLG-004, not figures to publish.

See the session entry appended to `COORDINATION.md` for the full conflict log, flag list (`c4e71983-FLG-nn`)
and ID mapping.

---

## Parallel build: `/docs/` sub-site (session `arena-79f85104`, PR #14)

A second, self-contained static site lives in [`docs/`](docs/) — dashboard landing, executive
summary, products table, analysis, SEO content kit, compliance, flagged register and sources
log. It is served at `/docs/` alongside the root site and cross-references this board.

| Page | Purpose |
|---|---|
| [`docs/index.html`](docs/index.html) | Dashboard landing page |
| [`docs/executive-summary.html`](docs/executive-summary.html) | Executive summary |
| [`docs/products.html`](docs/products.html) | Product research table (per-row official source links) |
| [`docs/analysis.html`](docs/analysis.html) | Pricing / reviews / competition / commission analysis |
| [`docs/content.html`](docs/content.html) | SEO product articles, comparison, buying guide |
| [`docs/compliance.html`](docs/compliance.html) | Associates OA §5 disclosure + Program Policies + FTC compliance |
| [`docs/flagged.html`](docs/flagged.html) | Flagged for Review (unverified items & irregularities) |
| [`docs/sources.html`](docs/sources.html) | Line-by-line source & verification register |

**Verification policy (both builds):** every asserted value links to an official source
(amazon.com, affiliate-program.amazon.com, ftc.gov); values that cannot be confirmed from an
official source are left blank and flagged — never inferred. Data captured 2026-11-13.

> **Resolved distinction.** The submitted 9-character values are short-link tokens, not ASINs; the
> short links were separately observed to open three Amazon listings. The sites now distinguish
> the observed destination from whether it was the product the requester intended; see FLG-027
> on the Flagged for review page and the session record in [`COORDINATION.md`](COORDINATION.md).

## Coordination

Shared task board: [`COORDINATION.md`](COORDINATION.md) — claims, status, verification log,
flagged items, PR/deploy record.

## Disclosure

As an Amazon Associate we earn from qualifying purchases.
