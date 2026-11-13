# Zone3

Zone3 is an Amazon affiliate research dashboard. It shows every product link from the brief, the official sources behind each value, the verification status of each field, and the items that still need review.

**Live site:** https://kanlerxz87-cyber.github.io/Zone3/

## What is in this repo

| Path | What it is |
|---|---|
| `index.html`, `executive-summary.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `flagged.html`, `sources.html` | Generated site pages (GitHub Pages serves `main` at `/`). |
| `assets/style.css`, `.nojekyll` | Site styling; disables Jekyll processing. |
| `data/sources.json` | Source registry: every official page used, its retrieval status, and what it supports (S01–S29). |
| `data/policy_facts.json` | Verbatim policy quotes (PF-01 to PF-43, PF-14 withdrawn), each with its source and section. |
| `data/products.json` | One record per product link. A `null` value means *unverified* and is shown blank. |
| `data/flags.json` | Irregularities and unverified items (FLG-001 to FLG-021) with evidence and actions. |
| `scripts/build_site.py` | Regenerates every page from `data/*.json` (standard library only). |
| `scripts/check_site.py` | Verifies the data and the generated pages (see below). |
| `research/` | Independent verification record of session 33226b37-zone3 (line-by-line log and product dossiers, with the ID mapping to the canonical data layer). |
| `docs/executive-summary.md` | Markdown executive summary (the rendered version is `executive-summary.html`). |
| `COORDINATION.md` | Shared task board for parallel sessions. |
| `analysis.html`, `categories/home-kitchen-air-fryers.html`, `disclosure.html` | Redirect stubs for URLs from the earlier PR #1 and PR #3 sites. |
| `archive/26634cd5/`, `archive/66a80e53/` | Files from earlier sessions (PR #1 and PR #3), kept unchanged for reference. Not used by the site. |

## Rebuild and check

```bash
python3 scripts/build_site.py   # regenerate the HTML pages from data/*.json
python3 scripts/check_site.py   # must print "All checks passed."
```

`check_site.py` fails if a product or a non-null value has no official source, if a table row's Source column has no link to an official site, if a link is broken, or if the Associates disclosure is missing from a page. Add `--online` to also request each official source URL from the machine running the check.

## Rules this project follows

- Only values confirmed from an official source are shown. Anything else is left blank and marked *Unverified*. Values are never inferred.
- Product data comes from official sources only. Price and review data may be shown only through a Special Link or the Creators API (Program Policies, Participation Requirements §2(b) and §6(t)).
- Creators API data may not be used for AI analysis, aggregation or model training without Amazon's written approval (Creators API IP License §1, §2(c)(e); Participation Requirements §5). No such analysis is built.
- The Associates disclosure (`As an Amazon Associate I earn from qualifying purchases.`) appears on every page (Operating Agreement §5).

## Status

As of 2026-11-13 the three submitted identifiers are not valid product pages, so no product fields are verified yet. The earlier site from PR #1 is merged in; see `COORDINATION.md` for the integration and the ID mapping. See `flagged.html` (the live Flagged for review page) for the blockers and the owner actions.
