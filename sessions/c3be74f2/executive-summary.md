# Zone3 publication refresh — executive summary

**Pass date:** 2026-11-19  
**Live-site target:** `https://kanlerxz87-cyber.github.io/Zone3/`  
**Scope:** buyer-facing root-page refresh, release-gate audit, and a transparent handoff of decisions that still need evidence or owner confirmation.

## Bottom line

The root page is now a buyer-led publication front page rather than a register-first dashboard. It starts with four question-shaped paths, groups the five observed listings without pretending that observations are intent confirmations, keeps the two thermometer listings outside the air-fryer guide shelf, and routes a reader to the existing guides, product-intent record, source register, decision queue and flags.

The page adds no price, availability, rating, review-count, sales, trend, conversion, commission, or testing claim. It uses an original abstract editorial illustration rather than a product image. Every newly added outbound Amazon product link is marked `rel="sponsored"`; the disclosure remains directly under the masthead and is repeated in the footer.

## What a buyer can do now

| Start here | Reader outcome | Evidence / next page |
|---|---|---|
| **Basket or oven-style?** | Compare form language, compartments and accessory wording. | [Guide](../../guides/basket-or-oven-style.html) |
| **What does capacity mean?** | Check whether a capacity term is total, per compartment, or not established. | [Guide](../../guides/capacity-checklist.html) |
| **What has to fit and clean up?** | Turn listing care wording and your own counter measurement into a checklist. | [Guide](../../guides/cleanup-and-counter-space.html) |
| **What do function counts mean?** | Ask what a count represents before treating it as a benefit. | [Guide](../../guides/multi-function-questions.html) |
| **Which product did a link mean?** | See intended fields held blank separately from observed redirects. | [Intent record](../../intent-record/index.html) |

## Verified current record, with its boundary

- The five submitted codes are not represented as owner-confirmed ASINs. The product-intent record holds intended ASIN, intended official URL, confirmation date and source as blank until the owner confirms them.
- The front page identifies five **observed** listing destinations from the existing, dated 2026-11-17 record: three air-fryer listings and two meat-thermometer listings. Each card links to the observed Amazon listing and separately to the submitted link / confirmation record.
- The two thermometer listings are visibly held outside the air-fryer guide shelf. This is a category decision still waiting for review, not a product comparison claim.
- The submitted link format and the owner-supplied tag are not declared compliant or invalid by this pass. The required enrolled-Associates destination-and-report test remains open.

This pass did **not** claim a fresh external re-read on 2026-11-19. The product observations displayed retain their 2026-11-17 date and their direct Amazon links so a reviewer can re-check them manually. No observation date was silently updated.

## Decision order

1. **Confirm product intent.** Supply an intended ASIN and official listing URL for every submitted link; retain redirect observations separately. See the [intent record](../../intent-record/index.html).
2. **Choose editorial scope.** Keep an air-fryer-only guide cluster or create a separate thermometer cluster; do not blend them merely because a listing says it can be used near an air fryer. See the [decision queue](../../decision-queue.html).
3. **Validate one Special Link per product.** In the enrolled Associates workflow, confirm landing destination and tracking-report attribution before scaling. The supplied short links remain unresolved rather than labelled invalid. See [Amazon Program Policies](https://affiliate-program.amazon.com/help/operating/policies).
4. **Pick one measurement stack and deploy only after the event contract, endpoint host and privacy treatment are accepted.** The current endpoint is intentionally off; the campaign ledger remains empty. See [measurement](../../measurement.html).
5. **Resolve source-provenance debt.** C3-F-01 records that the whole-tree verifier still treats historical uncited rows as advisory. See [Flagged for review](../../flagged.html#C3-F-01).

## Manual-review sources

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) — disclosure wording and placement basis.
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) — link and Program Content requirements.
- [Amazon Creators API GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) — ASIN identifier context.
- [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) and [FTC endorsement guidance](https://www.ftc.gov/business-guidance/resources/advertising-marketing/endorsements-influencers-reviews) — disclosure / no-invented-experience context.
- [Google Search Central: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) — `rel="sponsored"` context.

## Release outcome

The root page replacement is marker-bounded and regenerated by `sessions/c3be74f2/build_front_page.py`. It is designed to run after the existing generators and after the site-wide publication pass. The local release checks, final generated-output list, and the provenance caveat are recorded in [verification.md](verification.md).
