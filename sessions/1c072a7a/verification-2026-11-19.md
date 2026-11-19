# Verification scope — 2026-11-19 · session 1c072a7a

This is a **bounded current verification**, not a claim to have re-verified every inherited claim in this approximately 200-page repository. Baseline gates were run before changes (`baseline-checks.json`). Historical records retain their own dates and limitations. A passing HTML/source-link gate is not independent verification of the linked claim.

## Current product observations (one fetch per supplied link)

| Submitted link | Observed ASIN | Official observed listing | Scope checked |
|---|---|---|---|
| https://link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Redirect, page title, Air Fryers breadcrumb |
| https://link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Redirect, page title, Air Fryers breadcrumb |
| https://link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Redirect, page title, Air Fryers breadcrumb |
| https://link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Redirect, page title, Thermometers & Timers / Meat breadcrumb |
| https://link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Redirect, page title, Thermometers & Timers / Meat breadcrumb |

All five official listing titles matched the inherited titles in substance. TurboFry’s trademark glyph is non-substantive. Transient query parameters are omitted from the normalized observed listing URL. A title’s speed/accuracy/certification/capacity wording is a **listing claim**, not independent performance or certification verification. No review, price, availability or image is republished from these fetches. Intended ASINs and all intent-confirmation fields remain empty. No self-purchase, conversion test or fabricated impression is performed.

## Official pages actually read

See the dated, scoped `sources` rows in [`data/publication.json`](../../data/publication.json). Amazon Agreement chunks 0–1 and Program Policies chunks 0, 3, 4, 5 were read with the page-fetch tool. Full FTC Disclosures 101, Google review guidance, GitHub Pages overview and limits, and FoodSafety.gov temperature chart were read. Google sponsored-link, Search Console and canonicalization guidance were read at chunk 0. No claim of reading untouched page chunks is made.

## Material findings

- **Two analytics stacks:** inherited `track.js` and `measure.js` implement different five-event sets. Standardize runtime injection on the documented default `measure.js` schema, remove legacy `track.js` script tags, and prevent double initialization. Historical alternate source stays in the repo, not in the active runtime.
- **No durable collector host:** production measurement must stay off. A same-origin, real collector is available in the development preview; its test counts are not campaign evidence. Pages cannot execute the Python POST collector.
- **No account authority:** no authorized Associates report, Creators/PA API credential, Search Console property or intended-ASIN confirmation was supplied. Those cannot be truthfully completed by autonomous coding.
- **Host suitability:** [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) restrict business/commercial-transaction-oriented hosting. A deploy is technical success, not GitHub approval. Review the affiliate business use and move to suitable hosting before commercial scaling.
- **Index dilution:** root, `/site/`, `/read/` and multiple audit pages compete as front doors. Keep historical content reachable; make the publication + catalogue + six guides the indexable reader surface. Legacy dashboards are `noindex,follow`, not removed or falsely canonicalized to unrelated pages.
- **Authorship/art:** identify the actual publisher (Zone3 Editorial), AI assistance and no hands-on tests. Generic art is explicitly labelled; no generated depiction is passed off as a listed product.

## Implementation and integration verification

- Rebased onto main `0ee4153` after completed C3/C17/3301 publication work. Their renderers, CSS, art, source/flag rows and review records are retained. The current renderer composes the preceding shopper edition on a scratch page at `publication-prior.html`; it cannot overwrite the canonical root. Older research pages explicitly point to current operational status and historical verification limits.
- `python3 tools/publish.py`: 16 retained generation steps plus 25 release checks. Full output is recorded in `release-checks.json`; inherited provenance/style advisories remain disclosed, not called fresh factual verification.
- The strict current-publication gate checks 16 reader/review pages, 51 official-source table rows, 14 canonical sitemap URLs and 24 feed entries. The shared shell covers 118 current HTML pages, including the preserved previous edition; historical docs/session snapshots remain historical.
- Ten isolated HTTP/config tests, 20 collector self-tests, the preserved Node harness and 18 extended Node regressions pass. These exercise accepted/rejected schema and origins, known targets, credential/referrer omission, duplicate initialization, retention, atomic reload, concurrency, private readout and activation evidence. Production config remains disabled and the campaign ledger is unchanged/empty.
- Real Chromium: 14 interaction/privacy checks; 32 automated WCAG 2.0/2.1 A/AA page/viewport scans on all 16 current reader/review pages at 1440/390px, plus 320/768px root checks. No reported automated violations or ordinary request/page errors. All five event types were accepted locally; primary and middle outbound clicks were tested with Amazon navigation prevented. GPC, DNT, Save-Data and the disabled production file made no analytics request. Search, focus/menu handling, review save/reload/export/clear, clipboard, storage denial and no-JS fallbacks were exercised.
- Browser findings fixed during the pass: search inputs consumed the first native Escape; the logo's explicit accessible name omitted part of the visible tagline; tiny format captions and question numbers had insufficient contrast. The repeat suite passes. Chrome serverless single-process/context teardown and launch-flag defects were fixed in the test harness, not by weakening collector Origin validation.
- Visual inspection: homepage desktop/mobile, product cards, suggestions mobile and thermometer guide mobile screenshots. Context image and diagrams are clearly labelled, not claimed testing evidence. No manual screen-reader, Safari/Firefox or real-user performance certification is claimed.
- Immutable-row union check after rebase: all 149 upstream flags and all 83 upstream source rows match exactly; this pass adds five flags/four sources (154/87). Product, product-intent and campaign registers match upstream byte for byte. Counts are repository observations, not verified by external policy pages.

Final PR, merge SHA and Pages deployment/live-fetch results are recorded only after execution in the session's publish section of `COORDINATION.md`. Local test counts and synthetic review choices are never imported as performance evidence.
