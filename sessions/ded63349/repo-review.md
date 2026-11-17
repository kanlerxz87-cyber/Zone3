# Session ded63349 — repository review record (2026-11-17)

Scope: the reader-facing layer (`site/`, `tools/build_i2_site.py`, `tools/build_cba81fa5_site.py`,
`tools/i2_gate.py`), the flat pages the brief's priorities touch, and the new machinery this session
added. Line-by-line where this session made changes; structural review elsewhere. The independent
verification of official-source facts is in `verification-2026-11-17.md` (D6-V01..V18).

## 1. State found on arrival (`fedc9f6`, PR #134 merged)

- Working tree clean; `check_site` OK (30 pages / 3 products / 62 sources / 108 flags) on the
  untouched tree — reproduced before any edit.
- No `rel="sponsored"` anywhere in published pages; no RSS/Atom feed; no defined event set; no
  product-intent record page; disclosure in footers only on 11 published pages (published as
  proposal D-07 by session 59d84c55, awaiting exactly the instruction this brief gives).
- The board (COORDINATION.md) showed no active claims; last session (f65d393b) closed via PR #133/#134.

## 2. Implemented this session (and where the truth lives)

| Brief priority | Implementation | Enforced by |
|---|---|---|
| Click/conversion measurement first | `site/assets/site.js` ledger, five defined events, `site/measure.html` | i2_gate G6/G7 (no figures, no tracking controls); cba_lint (no invented claims) |
| Privacy-preserving counter | localStorage `z3-events-v1`, no cookies/identifiers/referrer, 500-row cap | code review — the gate cannot prove a negative; the measure page states it |
| Self-hosted analytics endpoint | **cannot exist on GitHub Pages** — recorded as blocked D-20 with options | `site/decisions.html` D-20; Q14 |
| Publishing cadence | fortnightly guide, monthly review, quarterly re-read — `site/measure.html` | D-17; feed + sitemap automation |
| Each new guide in sitemap + feed | `tools/build_feed.py` derives entries from the pages themselves | `build_feed --check` fails a stale feed |
| Disclosure above the fold, every page | `tools/add_disclosure_banner.py` (+ the reader layer already had it) | `add_disclosure_banner --check` |
| Every outbound product link `rel="sponsored"` | emitted by both site generators; `tools/apply_sponsored.py` covers all other pages | `apply_sponsored --check` + i2_gate **G11** |
| Product-intent confirmation record | `site/intent-record.html` + `data/ded63349/intent_record.json` | i2_gate G5 (every row sourced or blank-with-reason); G7 (short links quoted as text, not clickable) |
| Publication front page + footer dashboard group | front-door band additions in `tools/build_cba81fa5_site.py` (links generated from `scripts/build_site.py`'s own nav lists) | `build_cba81fa5_site --check`; check_site crawl |
| Mobile-first pass | fluid type scale, 44px tap targets, sticky quick-compare bar on guides | CSS-only; lint + gates re-run |
| Decision console | D-16..D-24, Q14..Q16, DA-10..DA-12 appended to `data/i2/decisions.json` | renders on `site/decisions.html`; counts in README updated |

## 3. Irregularities found and fixed during this session (all self-caught before push)

| ID | Sev | Finding | Fix |
|---|---|---|---|
| D6-F-01 | Medium (self) | First draft of the product-link pattern required two path segments before `/dp/`, so direct `amazon.com/dp/<ASIN>` evidence links were never marked sponsored. Caught by a targeted test matrix (8 cases) before push. | Pattern rewritten to `amazon.<tld>(?:/segment)?/dp/<10-char ASIN>`; test matrix rerun, 8/8 |
| D6-F-02 | Medium (self) | `tools/build_feed.py` never detected its own injected links because the gate regex did not escape the `+` in `atom+xml` — every run injected a duplicate discovery link. Caught when `--check` reported pages with links present as out of date. | Regex escaped to `atom\+xml`; injection now collapses any existing links to one canonical link |
| D6-F-03 | Medium (self) | An edit to `build_guides` dropped the `page()` write for `guides/dual-basket-vs-single-basket.html`, leaving the committed file stale while gates kept passing on the old bytes. Caught by grepping the emitted page for the sticky bar. | Page call restored; the regenerated page is content-identical plus the feed link, sponsored rel, updated nav and the sticky bar |
| D6-F-04 | Low (self) | The sticky quick-compare bar built its links with `rel()`, which reads the depth of the *previous* `page()` call — producing `products.html` instead of `../products.html` and two broken internal links. | Fixed prefixes for the known depth-1 guide location; `check_all_links` 0 errors after |
| D6-F-05 | Low (self) | `tools/build_cba81fa5_site.py --check` compared unmarked expected text against the sponsored-marked file, reporting permanent staleness. | Comparison and write both operate on marked text (`--check` now passes twice in a row) |

No inherited irregularity was found in the pre-existing generated pages; the 108-flag register and the
62-source register were left untouched (this session adds no flags and no new official-source captures —
its own observations live in the session record only).

## 4. Gates on the final tree

All exit 0 after the last change (see EXECUTIVE-SUMMARY.md § Session ded63349 pass for numbers):
`tools/i2_gate.py` (with the new G11) · `tools/cba81fa5_lint.py` (0 new findings; 22 inherited advisory
unchanged from the reviewed baseline) · `scripts/check_site.py` · `tools/verify_site.py` ·
`tools/link_report.py --strict` · `scripts/check_all_links.py` · `tools/apply_sponsored.py --check` ·
`tools/add_disclosure_banner.py --check` · `tools/build_feed.py --check` ·
`tools/build_cba81fa5_site.py --check` · `scripts/build_sitemap.py --check`.
The full generator chain was run twice; the tree hash is identical across runs (idempotency proof).

## 5. Honest limits of what was built

- The ledger measures this device's visitor only until an endpoint exists; nothing on the site
  presents device-side counts as site-wide numbers.
- Conversions, search queries and reported orders remain unmeasurable until the owner answers
  Q14/Q15 and the account questions Q1/Q4; every related cell stays blank with a reason.
- The five events and the cadence are this project's own definitions (labelled editorial on the
  measurement page), not claims about any external standard, traffic level or search demand.
