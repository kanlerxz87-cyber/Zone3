# AI-Powered Amazon Affiliate Platform — Design Suggestions

This document feeds into the design prompt for a polished marketing affiliate website. It outlines the architecture for an AI-powered Amazon affiliate marketing platform that automates product research, identifies trending and high-converting products, analyzes pricing/reviews/competition/commission potential, generates SEO-optimized content, publishes and manages affiliate links, tracks clicks and conversions, and continuously optimizes campaigns — all while prioritizing automation, scalability, data-driven decisions, and compliance with Amazon Associates policies and disclosure requirements.

**Status:** Proposal for the design brief. Not implemented. Nothing here asserts a fact the site does not have.

---

## 1. Goals (ordered by buyer value, not by revenue)

| # | Goal | How it serves the buyer |
|---|------|------------------------|
| 1 | Every page answers a real buyer question first | Readers land with a question about a kitchen appliance; the page answers four things: what the listing says, what it does not say, what to check at home, where the sponsored link goes. |
| 2 | Every claim is source-linked and dated | No invented test results, no fake reviewers, no unverified prices or ratings. |
| 3 | Automation only behind a gate | Drafts can be queued; nothing publishes without dated evidence, disclosure check, sponsored-rel check, and intent confirmation. |
| 4 | Compliance is structural, not fine print | `rel="sponsored"` on every Amazon link, disclosure strip above the fold, no price/rating unless Amazon-served, no per-visitor sub-tagging, no urgency/countdown. |

---

## 2. Platform architecture — six layers

### Layer 1 — Intake & product-intent confirmation (manual gate)

**What it does:** Receives a submitted Amazon link (e.g. `link.amazon/B04G1MEwY`), records the intended ASIN, intended official listing URL, confirmation date, and confirmation source in a strictly separate field from the observed redirect destination. Never merges the two.

**Why manual:** Only the account owner can confirm intent. An observed redirect is not evidence of intent (FLG-002).

**Compliance:** ASINs are 10 characters (Creators API GetItems, S06). Nine-character submitted codes cannot be ASINs (FLG-001). Redirect targets are recorded as observations only.

**Output:** `data/shop/intent-record.json` — one row per submitted link, intended fields blank until owner confirmation.

### Layer 2 — Product research & data collection (automated, gated)

**What it does:** For each intent-confirmed product:
- Reads the official listing page for title, brand, format, features, exterior dimensions, capacity-as-listed
- Captures the read date and source URL
- Records price/rating/review count as blank (not available without Creators API or Amazon-served link — PF-04, PF-05, FLG-022)

**Why gated:** Participation Requirements 2(b) and 6(t) restrict price/rating display. Scraping is prohibited (FLG-009). The Creators API requires ≥10 qualifying sales in 30 days (FLG-020) — cold-start cannot be automated.

**Output:** `data/products.json` — verified fields only; blank cells stay blank and flagged.

### Layer 3 — Niche & competition identification (automated, hypothesis-level)

**What it does:**
- Maps each product to its Amazon browse node (e.g. Air Fryers node 17659096011)
- Records category breadcrumbs from official listings
- Identifies competitor ASINs visible on Amazon Best Sellers pages (dated observation only — no quality claim)
- Notes commission-rate category references (Kitchen 4.50% standard, Table 1 — public, S25; Onsite 1.25%, Table A — S26)

**Why hypothesis-level:** "Trending," "high-converting," and competition density have no official Amazon source for affiliates (FLG-016). These are editorial hypotheses until measured first-party data exists.

**Output:** `data/niches.json` — category nodes, competitor ASINs (dated), commission category references.

### Layer 4 — Content generation (automated drafts, human gate)

**What it does:** From verified product data and official sources:
- Generates question-shaped buying guides (titles are working titles, not trend claims)
- Generates comparison tables with blank unverified cells
- Generates product cards with listing wording, format illustrations, sponsored CTAs
- Applies house style and banned-phrase lint (B38-P1, already shipped)

**Why human gate:** A confident draft is not evidence. Automation cannot authorise an API, confirm product intent, or validate attribution (P26-S5).

**Output:** Guide HTML, comparison tables, product cards — all gated by `tools/check_publication.py`.

### Layer 5 — Link management & attribution (manual validation)

**What it does:**
- Generates one Associates Special Link per product in the enrolled workflow
- Validates destination and tracking report before scaling
- Applies `rel="sponsored"` and `tag=` parameter to every product link
- Keeps intended ASIN/URL separate from observed redirect (never merged)

**Why manual:** Only the Associates account can produce Special Links and tracking reports (FLG-003, FLG-010). `link.amazon` short links may be Redirecting Links (§2(e)) — unresolved until tested in-account.

**Output:** Tagged product URLs on every card/CTA; intent record with validation date.

### Layer 6 — Measurement & optimization (automated collection, first-party only)

**What it does:**
- Five first-party events: `page_view`, `outbound_click`, `guide_view`, `intent_view`, `flag_view`
- Aggregate by UTC day; no cookies, no visitor profiles, no fingerprints
- Honours Global Privacy Control, Do Not Track, Save-Data
- Production collection OFF until a durable host exists (GitHub Pages limits restrict business use — FLG-013-adjacent)
- Search Console verification for query/page reports before topic selection from data

**Why off by default:** A click is not an order; an order is not a trend. No conversion scores or revenue forecasts are presented (P26-Q5).

**Output:** `data/shop/measurement.json` — blank endpoint, no deployment verification (production off).

---

## 3. Compliance rails (non-negotiable, enforced by build gate)

| Rail | Rule | Source | Build enforcement |
|------|------|--------|-------------------|
| R1 | Disclosure above the fold, undismissable | OA §5 (S01) | Disclosure strip on every page; lint fails if missing |
| R2 | No price/rating/review count unless Amazon-served | Policies 2(b) (S02) | `price: null` everywhere; lint fails on `$` or `★` cells |
| R3 | No urgency, countdown, scarcity | Policies 2(b) (S02) | No banner slot for deals; seasonal strip states calendar facts only |
| R4 | No bookmarking inducement | Policies 2(b) (S02) | CTAs are inline actions only |
| R5 | No per-visitor sub-tagging | Policies 2(b) (S02) | Aggregate-only analytics; no identifier fields |
| R6 | Original content on product-list pages | Policies 2(b) (S02) | Category pages carry editorial above cards |
| R7 | No experience we don't have | FTC Disclosures 101 (S07) | No "we tested" ribbons; byline = Zone3 Editorial (org) |
| R8 | "Best" claims need original evidence | Google review guidance (S94) | No winner column; blank cells labelled |
| R9 | Images are ours or labelled | OA §1, Program Content (S01) | AI editorial still life + generic diagrams only; lint enforces |
| R10 | `rel="sponsored"` on Amazon links | Google outbound links (S90) | Lint fails build if any Amazon anchor lacks `rel="sponsored"` |
| R11 | No invented market data | OA §4 (S01) | No fabricated counters, badges, or popularity chips |
| R12 | No Amazon marks in domain/tag | Policies 1(f)/(g) (S02) | Brand decision must avoid Amazon-adjacent names |

---

## 4. Publishing cadence (operating plan, not forecast)

| Cadence | Action | Owner |
|---------|--------|-------|
| Every 14 days | Review one guide; re-verify its sources | Editorial |
| Per new guide | Question-shaped title, sourced fact spine, disclosure, sponsored rels, feed/sitemap entry | Build (gated) |
| Per new product | Intent confirmation + one Special Link validation | Account owner (manual) |
| After launch | Search Console query reports guide topic selection | Measurable only |

---

## 5. Definition of done (per build)

The documented chain runs twice and the second run changes nothing; every gate passes; every table row carries a dated official source or an honest blank; no page loses its disclosure or sponsored rel; the deployed page is fetched and read back. Re-measure counts — pages, guides, sources, flags — and put both readings in the register. "Polished" is a number that moved, not a sentence in a changelog.

---

## 6. What this platform does NOT do (boundary, by design)

- Does not scrape Amazon pages (prohibited, FLG-009)
- Does not publish prices, ratings, or review counts without an authorized route (FLG-022)
- Does not claim "trending," "high-converting," or "best seller" without first-party data (FLG-016)
- Does not assign per-visitor sub-tags or build visitor profiles (Policies 2(b))
- Does not run paid search that lands on Amazon (Policies, standing rule)
- Does not simulate hands-on testing or invent reviewers (FTC S07)
- Does not treat a redirect target as product identity (FLG-002)
- Does not merge intended identifiers with observed destinations (FLG-002, 0C4-F-02)

---

## 7. Feeds into the design prompt

Append these lines to `DESIGN_PROMPT.md` when approved:

> **AI platform rails:** Automation is queued-drafts-only; the release gate says no. Product-intent confirmation and Special Link validation are manual, account-owner steps. Price/rating cells stay blank until an authorized route exists. Every Amazon link carries `rel="sponsored"` and the tag parameter. Disclosure strip is non-dismissible above the fold. No urgency, countdown, or scarcity UI. No per-visitor tracking. Topic choice moves to measured Search Console queries only after verification; until then, titles are editorial hypotheses. Images are labelled AI editorial still life or original generic diagrams — never product photographs presented as evidence.

---

**Sources:** Amazon Associates Program Operating Agreement (S01), Program Policies (S02), Creators API docs (S04–S06), FTC Disclosures 101 (S07), Google outbound-link guidance (S90), Google review guidance (S94), GitHub Pages limits (S91). All fetched 2026-11-19 unless noted; see `data/sources.json`.
