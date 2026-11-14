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
| Products that passed intake verification | **0 of 3** |
| Data cells left blank because no official source exists | **36** |
| Official sources cited | 19 |
| Open items published for review | 28 |
| Compliance rules enforced in the build | 25 prohibitions + 5 mandatory text blocks |

The three submitted links (`link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`,
`link.amazon/B00hJ57DV`) carry **9-character** identifiers. An Amazon ASIN is 10
characters, and `https://www.amazon.com/dp/<id>` returns Amazon's *Page Not Found* page for
all three. Following each link landed on a **different** unrelated product through Amazon's
`plpRedirect=mhFallback` route, which confirms the identifiers select nothing.

Rather than invent a product, the pipeline rejects them at intake and publishes the evidence.
Full audit trail: [`docs/verification-log.md`](docs/verification-log.md).

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
| Flagged | `/flagged/` | 28 open items with source links and resolutions |
| Repo review | `/repo-review/` | Audit of the repository as found |
| **This pass (2026-11-14)** | `/` (root dashboard) | Independent re-verification of every load-bearing claim against its official source, with a per-claim result table; corrections V-F1/V-F2 published at `/flagged.html`; repo review at `COORDINATION.md` § *Part: session b8beb448* |
| **Executive summary (document)** | [`EXECUTIVE-SUMMARY.md`](EXECUTIVE-SUMMARY.md) | The standalone executive summary: verified facts, deliberately blank fields, capability status, and the three items that unblock the build |

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
python3 tools/build_site.py            # rebuild + run the provenance gate (exit 2 on violation)
python3 tools/verify_site.py           # audit the emitted HTML    (exit 3 on violation)
python3 tools/link_report.py           # provenance coverage report
python3 tools/link_report.py --strict  # fail if any table is under-covered

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
short link falls back to a different unrelated product. Reaching that from separately fetched evidence
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

> **Cross-session discrepancy (needs review).** This sub-site's controls found that the three
> supplied 9-character codes are *registered* short links that resolve stably to three real
> Amazon listings (all air fryers), while the root build's intake rejected them as non-ASINs
> ("0 of 3"). Both positions and the control evidence are published for review in
> [`COORDINATION.md`](COORDINATION.md) (session `arena-79f85104` section) and
> [`docs/flagged.html`](docs/flagged.html). Neither blocks publication.

## Coordination

Shared task board: [`COORDINATION.md`](COORDINATION.md) — claims, status, verification log,
flagged items, PR/deploy record.

## Disclosure

As an Amazon Associate we earn from qualifying purchases.
