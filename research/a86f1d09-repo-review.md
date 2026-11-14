# Repository review — a86f1d09-zone3

Reviewed the tracked repository inventory (223 files) and traced both active site pipelines and datasets, generated output, policy/source records, coordination history, and retained archives. This is a repository-level line-by-line review, not an assertion that every historical archive is current.

## Active architecture

| Area | Files | Finding / review note | Official/source link |
|---|---|---|---|
| Root site generator | `scripts/build_site.py` | Flat HTML generation reads `data/*.json`; copy and templates must not overstate short-link failure. | [Amazon product links](https://link.amazon/B04G1MEwY) |
| Root site checks | `scripts/check_site.py` | Validates source IDs, official source hosts, row citations, links, disclosure, and placeholders. | [Repository checker](https://github.com/kanlerxz87-cyber/Zone3/blob/main/scripts/check_site.py) |
| Dashboard generator | `tools/build_site.py` | Reads `data/z3/*.json`; generates dashboard routes and includes a data integrity gate. | [Repository generator](https://github.com/kanlerxz87-cyber/Zone3/blob/main/tools/build_site.py) |
| Dashboard verifier | `tools/verify_site.py` | Checks generated pages/table citations and internal links; rerun after changes. | [Repository verifier](https://github.com/kanlerxz87-cyber/Zone3/blob/main/tools/verify_site.py) |
| Product datasets | `data/products.json`, `data/z3/products.json` | Previously conflated nine-character short-link IDs with ASINs and classified valid resolving links as rejected. Corrected finding: short IDs resolve to separate ten-character ASIN product pages. | [P-01 target](https://www.amazon.com/dp/B0CDY277D3), [P-02 target](https://www.amazon.com/dp/B09B7SB46R), [P-03 target](https://www.amazon.com/dp/B08DKYBTPH) |
| Policy and sources | `data/policy_facts.json`, `data/sources.json`, `data/z3/sources.json` | Public commission tables and price-display restrictions require consistent representation; source entries should point directly to primary sources. | [Standard rates](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ), [Onsite/Creator Ads rates](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA), [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| Generated pages | root HTML plus `dashboard/`, `products/`, `pricing/`, `reviews/`, `flagged/`, and other routes | Generated output is not canonical; rebuild from data/generator and validate links. | [Live site](https://kanlerxz87-cyber.github.io/Zone3/) |
| Historical material | `archive/`, `sessions/3c886b62/`, `docs/` | Preserve for provenance; some records contain superseded findings and must not be presented as current without qualification. | [Current verification log](a86f1d09-verification-log.md) |

## Irregularities / manual review

- Two site generations and preserved prior site snapshots duplicate facts; the dashboard is the newer route, but root pages remain in the repository and require synchronized correction.
- Historical records contain now-disproved “0 of 3 / rejected” findings. They are retained as history; current pages must explicitly supersede them.
- Static HTML generated previously included point-in-time prices. Amazon policy limits onsite price/availability display; raw observations belong in dated research, not static offers.
- Product targeting/link tagging and click/conversion instrumentation cannot be represented as operational without an Associates tag and actual measurement data.
- The brief requests trend and conversion analysis, but three products and public product-page signals do not establish conversion performance or profitable niches; leave those values blank/unverified.

## Review method and scope

Inspected tracked-file inventory and active Python generators/checkers, JSON schema and generated-page references for the relevant claims. Product/commission/policy statements in this review link to official Amazon or repository sources. This review does not claim every line of retained archived artifacts is a current factual statement; those files are explicitly historical and preserved.
