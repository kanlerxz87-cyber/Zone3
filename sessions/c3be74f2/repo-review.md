# C3 scoped repository review — 2026-11-19

## Scope and method

This review was deliberately divided into two honest levels:

1. **Line-by-line review of C3-owned output:** `index.html`, `assets/zone3-publication.css`, the original local illustration asset and `sessions/c3be74f2/build_front_page.py` were inspected after generation. The root page has one `h1`, an above-the-fold exact disclosure string, marker-bounded output, source links beside each observed listing card, no placeholder text, and `rel="sponsored"` on every root outbound Amazon product link.
2. **Whole-tree machine review of inherited output:** the repository's existing release gates were run. They validate data references, link targets, disclosure/sponsored coverage, sitemap/feed consistency and prohibited constructs, but they do not upgrade historical advisory findings to passing source evidence.

No claim in this record says that every historical page was manually re-read by C3. The gate results and the explicit exception below are the evidence of what this pass did and did not establish.

## Findings

| ID | Finding | Evidence | Disposition |
|---|---|---|---|
| C3-R-01 | Root page led with a repeated product card grid before a reader could choose a question; product and audit pathways competed above the fold. | Pre-change `index.html`; C3 build script / generated marker. | Remediated: question-first hero, four decision paths, separated listing desk and review handoff. |
| C3-R-02 | The two observed thermometer listings could be visually mistaken for more air-fryer content. | [Intent record](../../intent-record/index.html), rows 4–5. | Remediated in C3 root UI: distinct “Separate category decision” shelf; no thermometer recommendation or guide claim added. |
| C3-R-03 | A root product card did not link visibly to both its direct official listing source and the separate confirmation record. | Pre-change root cards and existing intent register. | Remediated: each new card has “Listing source” and “Read the confirmation record”; the submitted link remains separate. |
| C3-F-01 | The whole-tree verifier exits successfully while keeping historical per-row provenance gaps as advisories. | `tools/verify_site.py` baseline result; [published flag](../../flagged.html#C3-F-01). | Published for review. It does not block this narrow front-page refresh, but it prevents a claim that every historical table row is official-source-linked. |

## Evidence boundary review

- The root uses the existing observation record dated **2026-11-17**, not a fabricated current fetch date.
- No intended ASIN, intended listing URL, intent confirmation date or source was filled.
- The root does not state a price, availability, rating, review count, sales rank, performance result, trend, conversion, product superiority, personal use, or revenue forecast.
- The original local hero illustration is abstract and contains no product, brand, Amazon asset, text or claim. The release gate specifically checks that no Amazon CDN image is stored or used.
- The active buyer-facing cards retain the submitted links as supplied. This pass makes no statement that those links are valid or invalid Special Links. The existing test requirement remains open.

## Manual-review routes

- [Root page](../../index.html)
- [Product-intent confirmation record](../../intent-record/index.html)
- [Sources register](../../sources/index.html)
- [Suggestions / decision review](../../suggestions.html)
- [Decision queue](../../decision-queue.html)
- [Flagged for review](../../flagged.html)

## Source policy pages

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies)
- [Amazon Creators API GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items)
- [FTC: Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [Google: Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
