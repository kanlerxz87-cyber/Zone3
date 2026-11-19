# C3 release verification — 2026-11-19

## Data and source boundary

The C3 front page reads `sessions/aebf0747/intent-record.json` and labels its product observations **2026-11-17**. C3 did not change this date or claim that a dated observation is a product-intent confirmation. The root cards link to the corresponding direct Amazon listing and to the existing intent record; every table row introduced by C3 includes an official-context link.

Fresh external product/policy retrieval is not claimed by this pass. The published manual-review URLs are:

| Purpose | Official link |
|---|---|
| Associates disclosure / agreement | https://affiliate-program.amazon.com/help/operating/agreement |
| Participation Requirements / link rules | https://affiliate-program.amazon.com/help/operating/policies |
| ASIN identifier context | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items |
| Disclosure placement context | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| Sponsored-link context | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |

## Root-page assertions

The local C3 assertion script passed after generation:

- Exactly one `<h1>` is present.
- `As an Amazon Associate I earn from qualifying purchases.` appears near the opening masthead region.
- Every root `link.amazon` or `amazon.com/dp/` anchor has `rel="sponsored"`.
- No `TODO`, `FIXME` or lorem placeholder is present.
- `sessions/c3be74f2/build_front_page.py --check` reports current output (idempotent).
- `scripts/mark_sponsored.py --check` reports all product links marked.
- `git diff --check` is clean.

## Baseline gate snapshot (before C3 release build)

| Command | Result |
|---|---|
| `python3 scripts/check_site.py` | PASS — 42 shared pages, 5 products, 83 sources, 148 flags at baseline. |
| `python3 tools/verify_site.py` | PASS — 152 pages, 2,517 table rows; 532 inherited advisories. Provenance: Amazon/FTC 1,938; flag/blank 90; repo-only 269; uncited 220. |
| `python3 tools/link_report.py --strict` | PASS — all registered dashboard-row coverage. |
| `python3 tools/i2_gate.py` | PASS — 20 reader pages, 186 rows, 0 flagged. |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings; 22 inherited advisories. |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 152 pages, 0 repr-shaped output. |
| `python3 tools/build_feed.py --check` | PASS — 22 feed entries. |
| `python3 scripts/build_sitemap.py --check` | PASS — 106 pages, 0 extra entries. |
| `python3 scripts/mark_sponsored.py --check` | PASS — every outbound product link marked. |
| `python3 tools/apply_sponsored.py --check` | PASS — product links marked. |
| `python3 tools/add_disclosure_banner.py --check` | PASS — disclosure above fold. |
| `python3 tools/build_shop.py --check` | PASS — 11 shop pages. |
| `python3 tools/build_measurement.py --check` | PASS — current. |
| `python3 tools/build_brief_status.py --check` | PASS — 23 rows. |

## Newly published finding

**C3-F-01 — High: source provenance / release gate.** The pass added this item to the shared flag register and regenerated the Flagged for Review outputs. The current verifier treats inherited table provenance problems as non-blocking, so the site cannot truthfully say that every historical table row has an official source link. The flag links the exact report, explains the distinction, and gives a remediation path. The finding is repository-state evidence, not an unsupported external claim.

## Final release requirements

After the flag regeneration, run the established generator chain, then run the C3 root patcher **after** `sessions/aebf0747/publish_pass.py`; its marker-bounded operation preserves the disclosure, footer, stylesheet, RSS and measurement markers. Run `scripts/mark_sponsored.py` after the C3 patch and finish with all checks listed above.

## Final local release run

The complete documented generator chain was run twice after C3-F-01 was added. The tracked-diff hashes after run one and run two were identical:

```
03d9ddba47af8d6658f69d93ab2d196960867be3d51881450f5ebbd109009143
```

A first final-gate attempt found the inherited masthead route `index.html#products` no longer had an anchor after the new listing-desk layout. C3 corrected the generated root section to retain `id="products"` and kept `id="listing-desk"` for the hero call-to-action. The release was then re-run; it does not ship a broken anchor.

| Final command | Result |
|---|---|
| `python3 scripts/check_site.py` | PASS — 42 pages · 5 products · 83 sources · **149 flags**. |
| `python3 scripts/check_all_links.py` | PASS — 198 HTML pages · 264 distinct external URLs · **0 errors**. |
| `python3 tools/verify_site.py` | PASS — 152 pages · 2,522 table rows · 2,140 with official source · 419 with explicit flag · 117 repo anchors. The 533 inherited advisories remain published as C3-F-01 rather than hidden. |
| `python3 tools/link_report.py --strict` | PASS. |
| `python3 tools/i2_gate.py` | PASS — 20 pages · 186 rows · 0 flagged. |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings · 22 inherited advisories. |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 152 pages · 0 repr-shaped output. |
| Feed, sitemap, publication, disclosure and sponsored-link checks | PASS / current. |
| `tools/analytics_endpoint.py --self-test` + `sessions/38650305/test_measure.js` | PASS — collector filtering/aggregation and disabled-by-default client behavior. |

Pages deployment and live retrieval are recorded in `COORDINATION.md` after the PR is merged.
