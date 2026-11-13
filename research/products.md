# Research — Product Dossiers

Session: `session-33226b37-zone3` · Checked: 2026-11-13

> **Integration note (2026-11-13).** The canonical, merged product records live in
> `data/products.json` (schema of session 7f84fea4, PRs #5/#6). This file is the independent
> dossier from session `33226b37-zone3`; its per-product conclusions match the canonical records.
> See `research/verification-log.md` for the ID mapping to the canonical scheme.

Per-product records for the three codes supplied in the tasking. Fields that could not be
confirmed from an official source are intentionally left blank (`null` in JSON) — **not guessed**.

---

## Product 1 — code `B04G1MEwY`

| Field | Value | Status | Source |
|---|---|---|---|
| Code as provided | `B04G1MEwY` | as-provided | Tasking |
| ASIN-valid format (10 chars) | 9 characters | **FAIL** | Rule: https://sell.amazon.com/blog/fba-new-selection-program |
| Amazon catalog page | `https://www.amazon.com/dp/B04G1MEwY` → "Sorry! We couldn't find that page." | **NOT FOUND** | https://www.amazon.com/dp/B04G1MEwY |
| Product title | — (blank) | unverified | — |
| Brand | — (blank) | unverified | — |
| Category | — (blank) | unverified | — |
| Price | — (blank) | unverified | — |
| Rating / review count | — (blank) | unverified | — |
| Commission rate | — (blank) | unverified (rate card account-gated) | https://affiliate-program.amazon.com/help/operating/schedule |
| Web search corroboration | 0 catalog matches for the code | not found | (searches performed 2026-11-13) |

## Product 2 — code `B02NbDxp3`

| Field | Value | Status | Source |
|---|---|---|---|
| Code as provided | `B02NbDxp3` | as-provided | Tasking |
| ASIN-valid format (10 chars) | 9 characters | **FAIL** | Rule: https://sell.amazon.com/blog/fba-new-selection-program |
| Amazon catalog page | `https://www.amazon.com/dp/B02NbDxp3` → "Sorry! We couldn't find that page." | **NOT FOUND** | https://www.amazon.com/dp/B02NbDxp3 |
| Product title / brand / category / price / rating / commission | — (blank) | unverified | — |
| Web search corroboration | 0 catalog matches for the code | not found | (searches performed 2026-11-13) |

## Product 3 — code `B00hJ57DV`

| Field | Value | Status | Source |
|---|---|---|---|
| Code as provided | `B00hJ57DV` | as-provided | Tasking |
| ASIN-valid format (10 chars) | 9 characters | **FAIL** | Rule: https://sell.amazon.com/blog/fba-new-selection-program |
| Amazon catalog page | `https://www.amazon.com/dp/B00hJ57DV` → "Sorry! We couldn't find that page." | **NOT FOUND** | https://www.amazon.com/dp/B00hJ57DV |
| Product title / brand / category / price / rating / commission | — (blank) | unverified | — |
| Web search corroboration | 0 catalog matches for the code | not found | (searches performed 2026-11-13) |

## Control record — `B00005N5PF` (valid ASIN, proves lookup method)

| Field | Value | Status | Source |
|---|---|---|---|
| Code | `B00005N5PF` | verified as Amazon's documented example ASIN (Monopoly) | Amazon help docs, e.g. https://www.amazon.com/gp/help/customer/display.html?nodeId=200333520 |
| Lookup result | Checkpoint interstitial (not a 404) | method validated | https://www.amazon.com/dp/B00005N5PF |

---

## Marketing content status

Because the products cannot be identified from an official source, **no product-specific marketing
content, comparisons, buying guides, or claims were generated** — generating them would require
inferring product identities, which the tasking forbids. Instead, the site ships:

- verified, fully-sourced compliance and program-mechanics content (see `research/verification-log.md` §3);
- ready-to-fill SEO article / comparison / buying-guide **templates** that comply with Amazon
  Associates rules (original content with commentary/analysis; no hard-coded prices; required
  disclosure) — to be populated only after verified ASINs are supplied;
- a research and campaign-optimization methodology that is factual (based on the verified program
  rules) with all product-specific numbers left blank.

This is itself a compliance-driven decision: Participation Requirements §2(b) forbids inaccurate or
misleading claims about any Product
(source: https://affiliate-program.amazon.com/help/operating/policies).
