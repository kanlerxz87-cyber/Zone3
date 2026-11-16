# Repository review — session `cba81fa5` (2026-11-16)

Line-by-line read of the combined tree at the rebase base (`add6525`, merge of PR #99) and again at
`d3a8498` after three rebases during the session. Every count below was measured in the working
tree with the commands in §4, not estimated. Nothing here edits another session's file: the
dispositions named below are either this session's own files or change requests on the board.

## 1. What the repository now is

Two things in one tree, published from one root:

| Layer | What it holds | Built by | Pages |
|---|---|---|---|
| Operations dashboard (root flat pages, `/dashboard/`, `/products/`-style audit directories, `/docs/`, `/sessions/**`) | data tables, source register, flag registers, verification logs, per-session records | `scripts/build_site.py` from `data/*.json`; `tools/build_site.py` from `data/z3/*.json` | measured 152 HTML pages outside `archive/`, plus 46 inside it |
| Reader layer | `/read/` ("The Crisp Report", 11 pages, images, JSON-LD) and `/site/` ("Air Fryer Field Notes": landing, products, evidence, decisions, flagged, front-door note, 1 guide + 4 added by this session, open-questions register, house style) | `scripts/build_read.py`; `tools/build_i2_site.py`; `tools/build_cba81fa5_site.py` (this session's post-build regions) | 18 pages under `site/`, 11 under `read/` |

Root `index.html` opens on a generated front-door band (this session) with the dashboard tables
below it; 101 URLs are in `sitemap.xml`; five root files are meta-refresh redirect stubs
(`analysis.html`, `disclosure.html`, `flagged-for-review.html`, `marketing.html`,
`categories/home-kitchen-air-fryers.html`).

## 2. Structural findings (measured)

| # | Observation | Evidence in the tree | Read |
|---|---|---|---|
| R1 | The root page's nav carries 22 links, including three "Verification (session …)" entries, "Reference (/docs/)", "Full audit (16 pages)" and two marketing entries | `index.html`, generated from the `NAV` list in `scripts/build_site.py` | The nav is a provenance index, not a reader nav. It is the single clearest reason the root read as internal tooling rather than a site. Partly addressed: the front-door band now leads, and the reader navs are three to five items |
| R2 | Parallel registers for the same facts: `data/products.json` (3 products) vs `data/z3/products.json` (4 records); `data/flags.json` vs `data/z3/flags.json`; `data/sources.json` (52 records, IDs S01…S59 with gaps) vs `data/z3/sources.json` vs `data/i2/sources.json` (14) vs `data/cba81fa5/sources.json` (15) | counted with `json.load` on each file | Namespaced registers are the coordination mechanism, and they work — but a reader cannot tell which is canonical. The board has carried this as FLG-004-style duplication since 2026-11-14; it is still open. `scripts/renumber_sources.json` on `main` (added during this session) is the first attempt to renumber the shared register, which is why this session did **not** add rows to `data/sources.json` |
| R3 | `data/sources.json` IDs are not contiguous (S33–S39, S33.. absent; S40–S59 present) | same count | Harmless for the gates (they resolve by ID) and worth one line in the sources page so a reviewer does not read a gap as a deleted fact |
| R4 | Two root directories for the same idea: `category/` (two real pages, 14.5 KB and 8 KB) and `categories/` (one 292-byte redirect stub) | `ls`, byte sizes | Consolidation candidate, not a defect. Left alone |
| R5 | The release gate's ownership set was broken, so V1/V2/V3/V4 could never fail | `tools/verify_site.py` `generated_set()` read `data/z3/build-manifest.json` `files` values, which held digests (`'agent-terms': '94cb0fee17a9'`) | Reported as **CBA-F-02** with the reproduction; corroborates 71-F-01. **Fixed upstream during this session** by commit `f48ec8b` (PR #112): the manifest now records explicit `paths` and the gate consumes them, with `scripts/test_manifest_regression.py` as the regression test. Re-verified by this session on the rebased tree |
| R6 | `COORDINATION.md` is 5,472 lines / 565 KB, with 88 lines containing "in progress" | `wc`, grep count | The board is now the largest file in the repository. Closed Parts should be archived (AB-F-03 asked for this on 2026-11-16; still open) |
| R7 | Two reader brands covering the same three products, published the same day, with overlapping topics | `read/index.html`, `site/index.html`, `site/guides/index.html`, `site/articles/index.html` | Reported as **CBA-F-03** with a middle-path implementation; the decision is the owner's (Q-12) |

## 3. Content and compliance review of the reader layer

Checked against the rules in `data/policy_facts.json` (55 facts, verbatim quotes from
[Program Policies](https://affiliate-program.amazon.com/help/operating/policies) and the
[Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)) and the FTC
pages:

- **Disclosure.** Every reader page carries "As an Amazon Associate I earn from qualifying
  purchases." in a top banner and again in the footer beside the links. Consistent with
  PF-01/PF-02 and with the FTC's placement language ("place it so it's hard to miss",
  "with the endorsement message itself"), re-read 2026-11-16 (CBA-S12).
- **Prices and ratings.** No page publishes a product price, star rating or review count. The
  fetched listing and category pages do display them, including for neighbouring listings; none
  of those values reached a file in this session. Bounty amounts that do appear
  (`site/products.html`) are Amazon's own published bounty rates, not product prices — allowed,
  but on a product-facing page it reads ambiguously: **CBA-F-04**.
- **Links.** No link shortener, no `amzn.to`, no `http://`; `link.amazon` appears only as the
  evidence of what each submitted link resolves to, never as a shopping link. Every outbound link
  is https to `amazon.com`, `affiliate-program.amazon.com`, `ftc.gov` or `github.com` (165 distinct
  external URLs, 0 broken, `scripts/check_all_links.py`).
- **Experience claims.** None. Pages state the absence instead ("nobody cooked in these
  machines"), which is also the answer to the "don't read like AI slop" instruction: the copy is
  specific because it is quoted, and its gaps are named rather than filled.
- **Unscored comparison.** "Best" is used only in titles of the form "which fits what", never as
  a ranking of the three. The one rank that appears anywhere (position #6 on Amazon's Best Sellers
  in Air Fryers) is presented as a dated snapshot of a page, with the page linked (CBA-S06).
- **No stored Amazon assets.** No `<img>` on a reader page points at an Amazon host (gate V6).
  `/read/` ships its own generated illustrations under `assets/img/` — those are this repository's
  own files, and they should be labelled as illustrations, not product photography, so a reader
  does not mistake them for the listing's images. Suggested as a follow-up for the owner of
  `read/`, not changed here.

## 4. How to reproduce every number above

```
python3 - <<'PY'                      # page and register counts
import json,pathlib
root=pathlib.Path('.')
h=[p for p in root.rglob('*.html') if 'archive' not in p.parts and '.git' not in p.parts]
print(len(h), len([p for p in root.rglob('*.html') if 'archive' in p.parts]))
for f in ['data/products.json','data/z3/products.json','data/sources.json','data/i2/sources.json']:
    d=json.loads(pathlib.Path(f).read_text()); print(f, len(d.get('products',d.get('sources',[]))))
PY
python3 scripts/check_site.py                 # OK: 24 pages, 3 products, 62 sources, 97 flags
python3 tools/verify_site.py                  # VERIFY PASS: 106 pages, 1,701 rows, 1,462 sourced
python3 scripts/check_all_links.py            # 152 html pages, 165 external URLs, 0 errors
python3 tools/cba81fa5_lint.py                 # PASS: 18 pages, 0 new, 22 inherited
python3 tools/build_cba81fa5_site.py --check    # idempotent
python3 tools/link_report.py --strict           # exit 0
python3 scripts/build_sitemap.py --check        # exit 0
```

## 5. What this session changed, and what it deliberately did not

Changed: five new reader pages and one new guide set under `site/` (four guides, open-questions
register, house style, flagged-for-review section, nav entries), the front-door band on the root
page plus its scoped stylesheet, the post-build integrator that makes both durable and idempotent,
the lint and its reviewed baseline, two namespaced data registers, and this review with its
verification log.

Did not change: `data/*.json` shared registers, `tools/build_site.py`, `tools/verify_site.py`,
`scripts/build_site.py`, anything under `read/`, `docs/`, `sessions/**` or `archive/**`. Where
those files need an edit, the request is recorded on the board (CBA-F-02, CBA-F-04, CBA-F-05).
