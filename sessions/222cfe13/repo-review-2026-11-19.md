# Brief-alignment repo review — 2026-11-19 · session `222cfe13`

## Executive summary

The repository already contains the requested reader-facing publication and review desk; the live site did not need a duplicate rebuild. The canonical homepage is a shop/editorial front page, the two product categories and guide cluster are navigable, the review desk offers selectable paths, and the compliance/measurement dashboards remain reachable behind **Behind the site** and in the footer.

This pass made two narrow documentation fixes: corrected README guide/prompt counts from the live registers, and marked the older analytics schema/client/collector as historical so it cannot be mistaken for the single active runtime. No product claim, link destination, tracking configuration, account setting, search property, image, generated page, or sales/traffic number was changed.

**What still prevents the commercial parts from being called live:** the supplied product links have not been validated in the enrolled Associates workflow; the selected tag `shopnow047c-20` is not account-verified; production analytics is OFF because there is no authorized durable endpoint; Search Console is not verified; and the campaign ledger has no first-party report rows. GitHub Pages is already deployed, but a successful static deployment does not resolve these external account and hosting gates.

## Baseline and what was checked

- Branch at claim: `arena/222cfe13-zone3`, based on `6eb8c18e`.
- During the required `git pull --rebase origin main`, `main` advanced to `2a854c1` (PRs #181 and #184). There was one append/append conflict at the end of `COORDINATION.md`. I kept the upstream `07fb37ba` completion record in full, then retained this session's claim. No prior board text was discarded; the rebase result was pushed to this branch.
- Current local release command: `python3 tools/publish.py` — **41 builders/checks passed, 0 failed**. The command includes the publication/provenance gate, sitemap/feed checks, disclosure/sponsored checks, link checks, and both active and legacy analytics self-tests.
- Additional checks: `python3 tools/link_report.py --strict`; `python3 scripts/check_all_links.py` (**207 HTML files, 292 distinct external URLs, 0 errors**); `python3 tools/verify_site.py` (**161 pages, 2,606 table rows**); `git diff --check`.
- Current public Pages deployment observed through the GitHub API before this session's changes: `built` at `2a854c1`; its `Publication checks` and `pages build and deployment` runs both succeeded. The current public URL is [Zone3 Kitchen](https://kanlerxz87-cyber.github.io/Zone3/).
- These are structural/repository checks, not proof that every historical sentence is factually correct. The repository's broad verifier still reports **218 uncited rows** and the strict link report emits **570 non-blocking inherited provenance advisories** across older/research surfaces. The current publication has its own stricter provenance gate; the historical advisories remain visible and are not silently treated as verified.

## Current brief-to-repository map

| Request | Current implementation / result | Remaining limit |
|---|---|---|
| Shop-first publication homepage | [`index.html`](../../index.html) is the reader-facing front page; it leads with editorial/shortlist content rather than audit tables. | No new homepage redesign was needed in this pass. |
| Product categories and buyer questions | Five submitted products are organized across air fryers and meat thermometers; the current register has **8 question-led guides**. The page topics are editorial hypotheses, not claims of popularity or demand. | No Search Console query report or measured search demand is available. |
| Findability | The sitemap contains **16 indexable URLs** and the shipped RSS feed contains **26 entries**. New registered guides flow through the builders. | No Search Console ownership token or indexing/traffic evidence. Sitemap publication is not proof of indexing. |
| Suggestions and decisions | [`suggestions/index.html`](https://kanlerxz87-cyber.github.io/Zone3/suggestions/) contains **5 paths**, **15 proposals**, **24 decision-readiness questions**, discovery actions, answer ownership and a dated review round. Choices are review-only and saved locally; they do not implement changes. [`DESIGN_PROMPT.md`](../../DESIGN_PROMPT.md) is the paste-ready design brief with R1–R12 guardrails. | This pass did not duplicate or rewrite the existing decision desk. The owner/account-only questions remain open. |
| Executive summary | [`executive-brief.html`](../../executive-brief.html) is the current short executive surface. The standalone `EXECUTIVE-SUMMARY.md` is a dated history. | The current live summary now derives its counts from registers after PR #181/#184. |
| Disclosure and sponsored links | The current shared shell places the Associates sentence beneath the masthead and repeats it in the footer; the release gates check disclosure and sponsored-link markup. | A published disclosure does not prove account enrollment or link attribution. |
| Product intent record | [`intent-record/index.html`](../../intent-record/index.html) keeps intended ASIN, official listing URL, confirmation date/source separate from observed redirect targets. Intended fields remain blank. | A redirect observation is not proof of the intended product. |
| Five supplied product links | The 2026-11-19 verification records list these observed destinations: `B04G1MEwY` → [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3); `B02NbDxp3` → [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R); `B00hJ57DV` → [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH); `B0c8moW59` → [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5); `B0f3GKalj` → [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z). These are dated observations of what the short links opened, not confirmations of intent. | `FLG-003` remains unresolved. The site does not call the supplied links invalid or validated. The drafted tagged links in `data/special-links.json` are pending the enrolled-account test and are not a substitute for that test. |
| Selected Tracking ID | `shopnow047c-20` is recorded as user-supplied. | Assignment to an enrolled Associates account and report attribution remain unverified; no Associates login/report was available. |
| Click/conversion measurement | Current canonical events are `page_view`, `outbound_click`, `guide_view`, `intent_view`, `flag_view`. The client and aggregate collector exist. [`measurement/index.html`](https://kanlerxz87-cyber.github.io/Zone3/measurement/) reports status **OFF**. | The production endpoint is blank/unhosted. GitHub Pages is static and cannot host the Python collector. Browser clicks are not orders; conversions/orders belong in the empty campaign ledger only when obtained from authorized Associates reports. |
| Product imagery | The reader site uses a labelled generic AI-generated editorial kitchen still life, not a product photograph; original generic format diagrams are separate. No Amazon product photograph is stored. | The supplied S-18 preference for real, non-generated/non-copied product photography remains a decision/rights gate. No product photo was added: the brief provided no owner-supplied or licensed asset, and none was invented or copied. |
| Automated product research | The repository contains gated research/build machinery and source registers. | No authorized data feed, account-side API approval, first-party reports, or measured trend/conversion data is available. The site therefore makes no “trending”, “high-converting”, price, review-count, commission forecast, or revenue claim. |

## Measurement-stack clarification

The tree retained two different five-event designs after earlier parallel work:

- The current canonical runtime is `data/shop/measurement.json` → `assets/measure-config.js` + `assets/measure.js` → `tools/analytics_endpoint.py`.
- The older `data/analytics.json` → `assets/track.js` → `tools/analytics_collector.py` uses different event names and routes.

Current page templates inject only the canonical runtime. This pass marked the old files as **legacy/not injected** and retained their contracts for provenance and legacy tests. Production remains OFF. I did **not** remove either stack or enable either endpoint.

**Coordination request, not edited here:** `data/flags.json` still contains open flag `0C4-F-08` saying the owner must choose one stack. The current measurement config already selects one runtime, so the flag's wording/status should be reconciled by the final integrator. PR #160 includes `data/flags.json` in its scope; this session did not change that shared register. The separately open production-host blocker (`0C4-F-05`) remains valid.

## Best next path, based only on evidence already in the repository

1. **Use the existing shop/publication and review desk as the live baseline.** Keep the question-led topics and 14-day review cadence labelled as an operating plan, not an SEO forecast.
2. **Resolve the link-intent gate before scaling affiliate CTAs.** In the enrolled Associates workflow, confirm the intended ASIN for each product; create/test one Special Link per product; verify destination, assigned tag and report attribution; then record dated evidence in the intent register. Do not infer intent from redirects.
3. **Choose an owner-controlled analytics host before enabling collection.** Review HTTPS, origin allowlist, retention and upstream request logging. Deploy the canonical collector, test with non-production data, then enable it only with dated deployment evidence. Keep orders/conversions sourced from authorized Associates reports; never equate a browser click with a sale.
4. **Set up Search Console after site ownership verification.** Submit the already-published sitemap, then choose future guide topics from observed queries—not guessed popularity.
5. **Resolve imagery and authorship decisions before adding product claims.** Use only owner-owned/licensed images or an Amazon-authorized serving path; keep hands-on review and “best” claims behind actual testing and sign-off.

The live review interface is [Suggestions & decisions](https://kanlerxz87-cyber.github.io/Zone3/suggestions/); the public irregularity register is [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html).

## Official references for manual review

The following sources were already re-opened and dated by the cited earlier verification records; this session did **not** independently fetch those external pages again. Their URLs are included so the reader can inspect them directly.

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) — disclosure and Special Link terms; `sessions/6b68afc8/verification-2026-11-19.md`.
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) — tagging, Special Links, product-list content, pricing/reviews and link requirements; same verification record.
- [Amazon Creators API — GetItems / ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) — ASIN identifier reference; also linked in the product-intent record.
- [FTC: Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) — disclosure placement and experience claims.
- [Google Search Central: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) — `rel="sponsored"`.
- [Google Search Central: creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) — editorial basis, not a ranking guarantee.
- [Google Search Central: write high quality reviews](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews) — original evidence for reviews and recommendations.
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) — commercial-hosting boundary; dated in `sessions/b9008684/verification-2026-11-19.md`.
- Product-link observations: [`sessions/b9008684/verification-2026-11-19.md`](../b9008684/verification-2026-11-19.md) and [`sessions/6b68afc8/verification-2026-11-19.md`](../6b68afc8/verification-2026-11-19.md).

## Irregularities and scope limits

- No new Amazon/FTC/Google pages were fetched in this session; the product/policy review above relies on dated 2026-11-19 records already in this repository and their official links.
- The 218 uncited rows and 570 inherited advisories are repository-wide historical limitations, not a claim that the current eight-guide publication fails its own stricter source gate.
- `FLG-003`, account assignment, destination intent, special-link report tests, Search Console, production analytics hosting, product-image rights, named human review and performance evidence remain open or blocked as described above.
- No other open PR branch was merged or cherry-picked by this session. During rebase, the already-merged changes on `main` from PRs #181/#184 were preserved.
