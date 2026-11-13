# Executive Summary — Zone3 Amazon Affiliate Marketing Platform

**Prepared by:** `session-33226b37-zone3` · **Date:** 2026-11-13 · **Repo:** https://github.com/kanlerxz87-cyber/Zone3
**Live site (after merge):** https://kanlerxz87-cyber.github.io/Zone3/

> **Final-integration update (2026-11-13).** Three independent agent sessions worked this repo in
> parallel: `26634cd5` (PR #1), `66a80e53` (PR #3), and `7f84fea4` (PRs #5/#6, final site and data
> schema). The canonical site is the one on `main`: `index.html`, `executive-summary.html`,
> `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`,
> `flagged.html`, `sources.html`, generated from `data/*.json` (sources S01–S29, policy facts
> PF-01–43, flags FLG-001–021). This markdown file and `research/verification-log.md` /
> `research/products.md` are the independent verification record of session `33226b37-zone3`
> (PR #7); its unique additions to the canonical data layer are the control-ASIN test (S27),
> the enrollment/dormancy rules (PF-40, PF-41; S28, S29) and the payment-timing facts
> (PF-42, PF-43). Earlier sections below were written mid-session and describe the pre-merge
> state; where they conflict with `data/*.json`, the data layer wins.

---

## 1. Objective

Build an AI-powered Amazon affiliate marketing platform that automates product research, identifies
trending and high-converting products, analyzes pricing, reviews, competition and commission
potential, generates SEO-optimized content (articles, comparisons, buying guides), manages affiliate
links, tracks clicks and conversions, and continuously optimizes campaigns — with automation,
scalability, data-driven decisions, and full compliance with Amazon Associates policies and
disclosure requirements.

This repository delivers the **foundation of that platform**: a verified data layer, a compliance
framework sourced line-by-line from official Amazon and FTC documents, content and campaign
methodology templates, and a live GitHub Pages dashboard.

## 2. Products in scope — verification outcome

The tasking supplied three product links (`link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`,
`link.amazon/B00hJ57DV`). **None of the three could be verified from an official source**, so — per
the project's own rules — no product data was inferred or filled in. Specifically:

- Each supplied code is **9 characters**; Amazon officially defines ASINs as **10-character**
  alphanumeric codes (source: https://sell.amazon.com/blog/fba-new-selection-program).
- All three codes return Amazon's official **"Sorry! We couldn't find that page"** error at
  `amazon.com/dp/<code>` (checked 2026-11-13; method validated with a control lookup of Amazon's own
  documented example ASIN `B00005N5PF`).
- Web searches for each code produced **zero catalog matches**.
- The `link.amazon` URLs did not resolve to product pages for the supplied codes; the checked URL
  fell back to an unrelated listing with Amazon fallback parameters.

**Decision:** all product-specific fields (title, brand, category, price, rating, commission) are
left blank and published on the site's **Flagged for Review** page with source links. Generating
product-specific marketing content for unidentifiable products would violate the verified Amazon
rule against "inaccurate, overbroad, deceptive or otherwise misleading claims about any Product"
(https://affiliate-program.amazon.com/help/operating/policies, Participation Requirements §2(b)).

## 3. What was built

| Deliverable | Description |
|---|---|
| **Coordination protocol** | `COORDINATION.md` shared task board with session registry, claims, verification log, merge log |
| **Verification layer** | `research/verification-log.md`, `research/products.md`, `data/products.json` — every row linked to an official source; unverified values blank |
| **Executive summary** | This document (also rendered on the site) |
| **Live dashboard site** | Landing page + subpages (products, analysis, content plan, compliance, tracking, sources, flagged items) — clean tables, every row with a source link |
| **Compliance framework** | 14+ verified program rules with exact official citations (session windows, payment terms, disclosure, price-display, AI/ML restriction, FTC requirements) |
| **Content system** | SEO article / comparison / buying-guide templates that are compliant-by-design (original commentary, no hard-coded prices, required disclosure) |
| **Tracking & optimization plan** | Click/conversion tracking architecture and campaign-optimization loop using Associates-native reports |

## 4. Key verified program facts (all from official sources)

| Topic | Verified fact | Source |
|---|---|---|
| ASIN format | 10-character alphanumeric code | https://sell.amazon.com/blog/fba-new-selection-program |
| Attribution window | 24-hour session; 89-day cart completion; (new Apr 2026) 180-day ship/pay window | https://affiliate-program.amazon.com/help/operating/policies |
| Payout | ~60 days after month end; US minimums $10 deposit / $100 check | https://affiliate-program.amazon.com/help/operating/policies |
| Disclosure | Must state "As an Amazon Associate I earn from qualifying purchases" | https://affiliate-program.amazon.com/help/operating/agreement (§5) |
| Enrollment gate | ≥3 qualifying sales in first 180 days; personal orders don't count; ~10 posts of original content | https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM |
| Price display | Only via Amazon-served links or PA API — never hard-coded | https://affiliate-program.amazon.com/help/operating/policies (PR §2(b)) |
| AI/ML restriction | Program Content/Special Links must not train ML models without Amazon's written approval | https://affiliate-program.amazon.com/help/operating/policies (PR §5) |
| FTC disclosure | Material connection must be disclosed "clearly and conspicuously" (16 CFR 255, revised 2023) | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking |

## 5. Platform architecture (as designed on the site)

1. **Research engine** — ASIN validation → catalog verification → niche scoring (demand, competition,
   commission potential, content feasibility). All outputs require official-source verification
   before entering the data layer.
2. **Content engine** — template-driven generation (single-product review, comparison matrix,
   buying guide) with mandatory original commentary/analysis, disclosure block, and PA-API-only
   price rendering.
3. **Link management** — Special Links with Associates tag parameters; sub-tags for placement-level
   attribution (permitted by PR §2(b)); no cloaking/redirecting links (a verified disqualification
   trigger).
4. **Tracking & optimization loop** — Associates-native reports for clicks/units/conversion, weekly
   optimization cycle, content refresh triggers (e.g., promotion-expiry rule, PR §2(b)).
5. **Compliance gate** — every published page passes an automated checklist mapped to the verified
   rules; the disclosure statement appears on every page.

## 6. Risks, gaps, and flagged items (nothing blocks launch of the framework)

| # | Flag | Detail |
|---|---|---|
| 1 | Products unverifiable | All three supplied codes fail format check and catalog lookup — see §2 |
| 2 | `link.amazon` domain | Not a documented Amazon link format; ownership unverified |
| 3 | Commission rates | Public rate card is account-gated (`/help/operating/schedule` → sign-in); rates left blank |
| 4 | Prices | Hard-coded prices are prohibited by policy; the site displays none |
| 5 | AI/ML usage | Any model training on Program Content requires Amazon's prior written approval |

## 7. Recommended next steps

1. Supply corrected, complete 10-character ASINs (or full `amazon.com/dp/…` URLs). Each will then be
   verified against the live catalog and the data layer/site tables populated — with every value
   linked to its official source.
2. Register an Associates account (free) to unlock the official rate card and PA API access.
3. Populate the content templates only from verified product data; keep the disclosure statement on
   every page.
4. Stand up the tracking plan using Associates-native reports before adding any third-party analytics
   (keeps the privacy/cookie obligations described in Participation Requirements §3(e) manageable).
