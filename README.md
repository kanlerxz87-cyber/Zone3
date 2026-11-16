# Zone3 — AI Amazon Affiliate Marketing Platform

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

## Status at a glance

| | |
| --- | --- |
| Products submitted | 3 |
| Submitted tokens that are ASINs | **0 of 3** (they are short-link tokens) |
| Observed redirect destination listings | **3 of 3** |
| Product-attribute cells blank in the audit sheet | **27** (9 unavailable fields × 3 observed listings) |
| Official sources cited | 22 in `data/z3/`; 62 in the flat-site register (S60–S69 added 2026-11-16) |
| Open items published for review | 97 (flat-site register: `Z14-F-01`…`Z14-F-04` added 2026-11-16, plus `A0-F-*`/`F1-F-*` from PR #110) · 29 (audit build) |
| Compliance rules enforced in the build | 25 prohibitions + 5 mandatory text blocks; `scripts/build_read.py` additionally refuses to emit an uncited table row, a price pattern, a star-rating pattern or a stored Amazon image, and `read/**` is listed in `scripts/check_site.py`'s `PAGES` so the shared gate covers it too |
| Reader-facing marketing layers | **two, in parallel** — `/read/` (The Crisp Report, 11 pages, session `145b8df7`) and `/site/` (Air Fryer Field Notes, 8 pages, session `59d84c55`). Overlap recorded as `Z14-F-04`; the owner picks one as canonical |

The three submitted links (`link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`,
`link.amazon/B00hJ57DV`) carry **9-character short-link tokens**, not ASINs. Amazon defines an
ASIN as 10 characters, and `https://www.amazon.com/dp/<token>` returns Amazon's *Page Not Found* page
for all three tokens. Following each short link was observed to land on a live listing: CHEFMAN
6 Qt dual basket (B0CDY277D3), Emeril Lagasse 26QT (B09B7SB46R), and Chefman 8 Qt TurboFry
(B08DKYBTPH). These observed destinations are documented; whether they match the requester's intent
is not established by an official source.

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
| **This pass (2026-11-16)** | `/site/` | **The reader-facing marketing site.** Built by `tools/build_i2_site.py` from `data/i2/*.json`, gated by `tools/i2_gate.py` (G1–G10). Eight pages: a home page that leads with the three products, a comparison table where every row links the listing it came from and every blank cell says why, a buying guide, a source register with 14 pages read on 2026-11-16, a 22-row line-by-line verification log, a "flagged for review" page with 8 open items, and a decision board with 12 proposals, 12 open questions, 9 discovery actions, a 6-part prompt pack and an Accept/Reject/Defer control that changes nothing until a choice is recorded. |
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
| [`site/decisions.html`](site/decisions.html) | 12 proposals · 12 open questions · 9 discovery actions · 6 prompts · a working Accept/Reject/Defer control with an export |

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
python3 tools/i2_gate.py           # G1–G10; exit 1 on any prohibited construct
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
