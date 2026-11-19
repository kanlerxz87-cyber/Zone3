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
