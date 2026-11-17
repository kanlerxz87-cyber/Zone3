# Repo review — session `0b2ffabd` (2026-11-17)

**Base:** `d192053` (main at claim, merge of PR #141 / session `82372fd1`).
**Branch:** `arena/0b2ffabd-zone3`. **Claim commit:** pushed before any other work, per the protocol in this
repository's `COORDINATION.md`.
**Task:** G0B2-T1. This review is read-only: it measures the tree and the live site, and records what the
suggestions layer now overstates, understates or has never covered. Nothing in the reader layers was edited.

## 1. Gate snapshot on the claimed base (all run before any edit)

| Gate | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 30 pages, 3 products, 62 sources, 113 flags |
| `python3 tools/verify_site.py` | VERIFY PASS — 134 pages, 2,068 table rows, 1,769 with an official source, 369 with a flag, 66 with a repo anchor |
| `python3 tools/link_report.py --strict` | 0 errors; the four "cannot be obtained" notes (price/rating, trend rank, conversion rate, competition density) still stand |
| `python3 tools/i2_gate.py` | PASS — 18 pages, 164 rows, 148 sourced, 16 explicit blanks, 0 flagged |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings, 22 inherited |
| `python3 tools/build_cba81fa5_site.py --check` | current |
| `python3 tools/build_feed.py --check` | current — 9 entries (union of both guide registers) |
| `python3 sessions/aebf0747/publish_pass.py --check` | 102 pages, 0 changed, no missing footer targets |
| `python3 tools/build_shop.py --check` | OK — 11 pages |
| `python3 scripts/build_sitemap.py --check` | 97 pages covered, 0 extra entries |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 134 pages, 0 pages with repr-shaped text |

`gh pr list --state open` at claim time returned nothing, so no other session was mid-flight against this base.
Pages API: `status=built`, `https_enforced=true`.

## 2. Live-site spot check

Fetched `https://kanlerxz87-cyber.github.io/Zone3/suggestions.html` (cache of the deployed `d192053`): the page
serves the 2026-11-17 review — the four "shipped since the last review" rows, DP-A/DP-B/DP-C, the re-status
table — so the deploy matches the tree, and this session's additions to the same register will render on merge.

## 3. Measured inventory of the reader-facing surfaces (grep/`find` counts, not estimates)

| Surface | HTML pages | With `rel="canonical"` | With `og:image` + JSON-LD |
|---|---|---|---|
| `site/` (Air Fryer Field Notes) | 18 | 18 | 0 |
| `read/` (The Crisp Report) | 11 | 11 | 11 |
| `shop/` (Zone3 Kitchen) | 11 | 11 | 0 |
| `marketing/` (Research Desk briefs) | 7 | 1 | 0 |
| `guides/` (root question guides) | 5 | 5 | 0 |
| `articles/` (Research Desk articles) | 5 | 5 | 0 |
| root `*.html` (register + dashboards) | 25 | 22 | 0 |
| **Total HTML outside `archive/`** | **134** | | **11** |

**Finding (G0B2-F-02).** `data/suggestions.json` Q12 and design path DP-C both describe the duplication problem
as "three parallel reader layers (`site/`, `read/`, `marketing/`)". As of this base there are **six** reader-facing
surfaces plus the register at the root, and the root page itself is now a publication front page (session
`aebf0747`, PR #136) with its own `guides/` set. The owner decision Q12 asks is therefore not "which of three"
but "which of six", and the consolidation cost of DP-C is understated in its current wording. Corrected by the
dated review added in this pass (`data/suggestions.json → review_2026_11_17b`), which carries the table above.

## 4. Findability coverage, measured against Google's own published guidance

Re-read 2026-11-17 (see `verification.md` for the quotes and which chunk of each page was read):

| Check | Measured here | What the official page says |
|---|---|---|
| `sitemap.xml` `<lastmod>` | 0 occurrences in 97 `<loc>` entries | "Google uses the `<lastmod>` value if it's consistently and verifiably … accurate" — so an absent value costs nothing, an inaccurate one is worse than none |
| `sitemap.xml` `<priority>` / `<changefreq>` | 0 occurrences | "Google ignores `<priority>` and `<changefreq>` values" — omitting them is correct, not a gap |
| Sitemap location | `/Zone3/sitemap.xml`, declared in `robots.txt` | "unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory … a sitemap posted at the site root can affect all files on the site" — for a GitHub Pages **project** site the effective root is `https://kanlerxz87-cyber.github.io/Zone3/`, which is what the file covers |
| Pages listed that no one should index | `404.html` is in the sitemap | "Include the URLs in your sitemap that you want to see in Google's search results." |
| Page titles / descriptions | 48 root + `site/` + `guides/` pages checked: 0 missing `<title>`, 0 missing `name="description"`, 0 descriptions under 60 characters; one duplicate title ("Moved", on the meta-refresh stubs) | "Identical or similar descriptions on every page of a site aren't helpful … create descriptions that accurately describe the specific page" |
| `rel="sponsored"` on Amazon links | enforced by `sessions/aebf0747/publish_pass.py` (audit: 1,422 product links, all sponsored) and by `tools/build_cba81fa5_site.py` | "Mark links that are advertisements or paid placements … with the `sponsored` value" |
| FAQ rich results | no `FAQPage` markup anywhere (11 JSON-LD blocks are `Article`/`BreadcrumbList`-shaped, all in `read/`) | The former doc URL `…/structured-data/faqpage` now redirects to the Search Central updates page anchored at the June 2026 entry "Removing documentation for the FAQ rich result feature" — so "add FAQ schema" is not a ranking play, and the question-shaped guides stand on reader value, not on a rich result |

**Finding (G0B2-F-06).** Three mechanical findability items are open, each one generator edit, and each one
touches a file two generators already fight over (`sitemap.xml`) or a second publisher (`read/` owns the only
`og:image`/JSON-LD set). They are therefore **published as decisions** (suggestions SUG-11/SUG-12 in the register),
not applied silently in a marketing pass.

## 5. Evidence-state findings

1. **G0B2-F-01 (needs owner).** The selected tracking ID supplied in the 2026-11-17 owner brief is printed on
   five published files (`publication-pass.html`, `intent-record/index.html`, `shop/decisions/index.html`,
   `shop/findings/index.html`, `shop/flagged/index.html`), while Q1's own recorded rule is that the value is kept
   in `COORDINATION.md` only. Both cannot be the convention. This session did not edit another session's pages;
   it records the conflict with the two ways to close it (redact the value from the public pages, or amend the
   Q1 rule and record where the value is allowed to appear).
2. **G0B2-F-03 (needs owner).** The observed destinations for two of the five submitted links
   (`link.amazon/B0c8moW59`, `link.amazon/B0f3GKalj`) are published on the front page and in the intent record,
   but **no** row in the canonical registers carried a capture for them: `grep` over `data/*.json` for
   `B0DHZTCNR5` and `B0DZFD6R9Z` hit only `data/shop/*.json` and `sessions/aebf0747/intent-record.json`.
   This session re-fetched both links itself on 2026-11-17 and records the captures as S77/S78, so the front
   page's claim is now backed in the canonical register as well as in the shop layer. `data/products.json`
   still has no product row for either link (that is `G82-F-03`'s owner half, unchanged).
3. **G0B2-F-04 (fixed).** Four rows on `suggestions.html` (Q11, Q12, D8, D10) rendered "no source" and were
   reported by `verify_site` V4 as rows with neither an official link, a flag, nor a repo anchor. They now carry
   real sources (S71/S75/S77/S78 where the row states a fact, a repo anchor where the row states an owner choice).
4. **G0B2-F-05 (fixed).** Six clauses this project's design decisions actually rest on were quoted nowhere in
   `data/policy_facts.json`: the sub-tag / end-user-association ban, the no-bookmark rule, "All Special Links must
   be accessed directly from your Site", the limited-time-promotion removal duty, the product-list originality
   requirement, and the comparison-price display condition. All six were read verbatim on 2026-11-17 and appended
   as PF-57…PF-62, so the rails in `DESIGN_PROMPT.md` cite a repo record rather than a recollection.
5. **Not a finding, recorded so it is not re-litigated.** The three `assets/img/*.jpg` illustrations are the
   `read/` layer's own artwork and each `<figure>` states "Illustration: our own. Amazon product imagery is
   Program Content and may not be copied onto this site." No product photography is stored anywhere in the
   published tree (`verify_site` V6 enforces the Amazon-CDN image pattern). The owner's open question remains the
   one already on the register — S-18 "real product photography … never generated or copied" is still
   *needs a decision*, and this session added no image asset of any kind.

## 6. What this review did **not** do

- No reader-layer page was restyled, moved or archived; the six surfaces stay as their owners built them.
- No price, rating, review count, sales or ranking value was added anywhere, even where the fetched listing
  pages displayed them (Program Policies 2(b) / 6(t)); they were deliberately not transcribed.
- No claim about search volume, trend or popularity is made in this file or in the register additions.
- `index.html`, `feed.xml`, `data/products.json`, `data/decision-queue.json`, every gate script and every other
  session's `sessions/**` files are untouched by this Part.
