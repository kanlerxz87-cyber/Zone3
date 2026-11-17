# Repository review — session `2f181cd9` (2026-11-17)

Reviewed against the base commit `fedc9f66`. Claims about the repository are observations
of files in the tree; claims about Amazon or the FTC are quoted and sourced.

## What the repository is

A generated static site plus its source registers: `data/*.json` holds the sources,
products, policy facts, flags and decisions; `scripts/build_site.py` renders the flat
pages; five further generators render the other page families. At the base commit the
published set is 115 HTML pages, 78 of them in `sitemap.xml`.

The habit of the project is unusually disciplined and it holds: no price, star rating or
review count is displayed anywhere; a cell with no official source is left blank and
flagged; every table row carries a source link; the gates pass.

## Line-by-line findings

| # | Observation | Evidence | Severity | Raised as |
|---|---|---|---|---|
| 1 | Only three of the five links in this session's brief are in the product register. The two added on 2026-11-17 open meat thermometers, not air fryers. | `data/products.json` at base (3 products); destinations read 2026-11-17 | High | F-2F-01 (fixed in this session by adding P4/P5), SUG-2F-01 |
| 2 | Every outbound link can be clicked without earning: no Associates tag has been supplied. | `data/products.json` → `associates_tag: null` for every product | High | F-2F-03 |
| 3 | Outbound product links are marked `rel="sponsored"` on 6 links and not on the rest; the same class of link is marked two different ways depending on which generator built the page. | Repository-wide scan, 2026-11-17: 6 sponsored against 2,377 `rel="noopener noreferrer"` | Medium | F-2F-05, SUG-2F-07 |
| 4 | Four visual languages are published on one domain. | `assets/style.css`, `assets/front-door.css`, `assets/read.css`, `site/assets/` | Medium | F-2F-07, SUG-2F-03 |
| 5 | The reader's path runs through an operations dashboard: status callout, source and flag counts, a 78-page site map, on the front page. | `index.html` at base | Medium | F-2F-06, SUG-2F-02 |
| 6 | Product pages carry no photography at all. | `marketing/product-*.html`, front-door cards | Low | F-2F-08, SUG-2F-04 |
| 7 | Copy that says "three" is hard-coded across several generators, so adding links leaves the site internally inconsistent. | `grep -rn "three" scripts/build_site.py` — 20 matches | Low | F-2F-09 (partly fixed here: the flat pages now read five) |
| 8 | Boilerplate is repeated at scale: the same "built by" footer sentence on 23 pages, the same status sentence on 18. | Sentence-frequency scan of all 115 pages, 2026-11-17 | Low | Recorded in the design diagnosis |
| 9 | The published page set includes per-session archives, a superseded `/docs/` build and two marketing builds of the same content. | 115 pages published, 78 in the sitemap | Low | SUG-2F-10 |
| 10 | Per-session registers are namespaced and append-only, and the coordination board records hand-offs. This is the project's strongest habit and it should not be lost in a redesign. | `COORDINATION.md`, `data/sources.json` `id_reservation` | — | Kept as is |

## What this session changed in shared files, and why it was safe

* `data/sources.json` — S70–S82 appended; the `id_reservation` note extended so the next
  session appends from S83. No existing ID renumbered.
* `data/flags.json` — F-2F-01…F-2F-10 appended, unioned by ID. Nothing removed.
* `data/products.json` — P4 and P5 appended with the same null-valued fields as P1–P3,
  and a `content_status` block that says no brief, comparison or buying guide exists for
  them, so the Content page does not claim content that was never written.
* `scripts/build_site.py` — 19 targeted string replacements (each asserted against a
  single occurrence) plus one new navigation group and one new site-map group.
  `scripts/_patch_2f181cd9.py` is kept so the edits can be re-read or re-applied.
* `scripts/check_site.py` — this session's six pages added to `PAGES` and `TABLE_PAGES`
  so the shared gates cover them.

## What this session did not change

The injected front-door band on `index.html` (`tools/build_cba81fa5_site.py`), the
`/read/` pages (`scripts/build_read.py`), the `/site/` pages (`tools/build_i2_site.py`
and `tools/build_cba81fa5_site.py`) and `/marketing/` still say "three". Editing those
means running four generators whose data this session did not touch, and a partial
update would leave the site mixing "three" and "five". Logged as F-2F-09 with the exact
surfaces listed, to be done in one pass after the scope decision.
