# Repo review — session `0b2ffabd` (2026-11-17)

**Base:** `d192053` (main at claim, merge of PR #141 / session `82372fd1`).
**Merged tree this record was finalised on:** `2868a3a` — main moved twice while this pass was open (PR #151
session `ded63349`, PR #152 sessions `59b2194c`/`73029680`, plus `2f181cd9`'s merged five-link intake), so the
review was **re-run against the merged tree** before publication. §1a keeps the base snapshot, because that is
what the register's "at this session's base" wording measures; §1b is the tree this pass actually committed.
Every count in §3, §4 and in the published `data/suggestions.json` rows is the §1b number.
**Branch:** `arena/0b2ffabd-zone3`. **Claim commit:** pushed before any other work, per the protocol in this
repository's `COORDINATION.md`. The rebase onto `2868a3a` touched one file textually (`COORDINATION.md`, both
sides kept in full) and renumbered this session's source ids (flag `G0B2-F-10`).
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

## 1b. Gate snapshot on the merged tree, after this pass's edits (all green, chain re-run twice for idempotency)

| Gate | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 36 pages, 5 products, 86 sources, 135 flags |
| `python3 tools/verify_site.py` | VERIFY PASS — 144 pages, 2,332 table rows, 1,993 with an official source, 396 with a flag, 116 with a repo anchor; 490 inherited-page advisories: **0 on any row this pass added to `suggestions.html`**, 14 of them belonging to another session's tables on that page (`G0B2-F-11`) and 3 on this session's own rows on `flagged.html`, which is a property of that table's columns rather than of the data (`G0B2-F-09`) |
| `python3 tools/link_report.py --strict` | exit 0; the same "cannot be obtained" notes (price/rating, trend rank, conversion rate, competition density, clicks/orders/revenue) |
| `python3 tools/i2_gate.py` | PASS — 20 pages, 186 rows, 170 sourced, 16 explicit blanks, 0 flagged |
| `python3 tools/cba81fa5_lint.py` | PASS — 20 pages, 0 new findings, 22 inherited |
| `python3 tools/build_cba81fa5_site.py --check` | current ("WOULD REWRITE nothing") |
| `python3 tools/build_feed.py --check` | current — 9 entries (union of both guide registers) |
| `python3 sessions/aebf0747/publish_pass.py --check` | 106 pages, 0 changed, no missing footer targets |
| `python3 tools/measure_pass.py --check` | 106 pages, 0 would change |
| `python3 tools/apply_sponsored.py --check` / `python3 tools/add_disclosure_banner.py --check` | both PASS |
| `python3 tools/analytics_endpoint.py --self-test` | SELF-TEST PASS — allow-list, field filter, aggregate-only store |
| `python3 tools/build_shop.py --check` | OK — 11 pages |
| `python3 tools/build_measurement.py` / `tools/build_brief_status.py --check` | current — brief status 23 rows, 13 sourced claims, 0 prices, 0 ratings, 0 ranks |
| `python3 scripts/build_sitemap.py --check` | 101 pages covered, 0 extra entries |
| `python3 scripts/check_all_links.py` | 190 pages, 241 distinct external URLs, 0 errors |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 144 pages, 0 with repr-shaped text |
| `python3 sessions/aebf0747/audit.py` | 106 pages, 1,558 Amazon links, 1,558 sponsored, 0 missing; `link_check.py` 0 broken internal links |

Two notes on method, because they changed the outcome. (1) The chain has to be run **twice** on this tree: the
layer generators (`scripts/build_read.py`, `scripts/build_marketing.py`, `scripts/build_5a56c084.py`,
`tools/build_i2_site.py`) rewrite pages that `publish_pass.py`, `measure_pass.py` and
`build_cba81fa5_site.py` post-process, so one pass leaves the injected `z3:css` / `z3:rss` / `z3:strip` /
`z3:measure` blocks missing from ~30 pages; the second pass converges and the tree is then stable. (2) One
generated page legitimately changes from my register edit alone: `read/method.html` prints the source count in
its method copy, and 75 → 86 is that number moving.

## 2. Live-site spot check

Fetched `https://kanlerxz87-cyber.github.io/Zone3/suggestions.html` (cache of the deployed `d192053`): the page
serves the 2026-11-17 review — the four "shipped since the last review" rows, DP-A/DP-B/DP-C, the re-status
table — so the deploy matches the tree, and this session's additions to the same register will render on merge.

## 3. Measured inventory of the reader-facing surfaces (grep/`find` counts, not estimates)

Measured on the merged tree (the base numbers are in parentheses, where they differ).

| Surface | HTML pages | With `rel="canonical"` | With `og:image` + JSON-LD |
|---|---|---|---|
| `site/` (Air Fryer Field Notes) | 20 (18) | 20 (18) | 0 |
| `read/` (The Crisp Report) | 11 | 11 | 11 |
| `shop/` (Zone3 Kitchen) | 11 | 11 | 0 |
| `marketing/` (Research Desk briefs) | 7 | 1 | 0 |
| `guides/` (root question guides) | 5 | 5 | 0 |
| `articles/` (Research Desk articles) | 5 | 5 | 0 |
| root `*.html` (register + dashboards) | 25 | 22 | 0 |
| **Total HTML outside `docs/` and `archive/`** | **136** (134) | **102** | **11** (all `read/`, none else) |

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
| `sitemap.xml` `<lastmod>` | 0 occurrences in 101 `<loc>` entries (97 at this session's base) | "Google uses the `<lastmod>` value if it's consistently and verifiably … accurate" — so an absent value costs nothing, an inaccurate one is worse than none |
| `sitemap.xml` `<priority>` / `<changefreq>` | 0 occurrences | "Google ignores `<priority>` and `<changefreq>` values" — omitting them is correct, not a gap |
| Sitemap location | `/Zone3/sitemap.xml`, declared in `robots.txt` | "unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory … a sitemap posted at the site root can affect all files on the site" — for a GitHub Pages **project** site the effective root is `https://kanlerxz87-cyber.github.io/Zone3/`, which is what the file covers |
| Pages listed that no one should index | `404.html` is in the sitemap | "Include the URLs in your sitemap that you want to see in Google's search results." |
| Page titles / descriptions | 50 root + `site/` + `guides/` pages checked: 0 missing `<title>`, 0 missing `name="description"`, 0 descriptions under 60 characters; four pages sharing the title "Moved" (the meta-refresh redirect stubs, counted as one duplicate group) | "Identical or similar descriptions on every page of a site aren't helpful … create descriptions that accurately describe the specific page" |
| `rel="sponsored"` on Amazon links | enforced by `sessions/aebf0747/publish_pass.py` (audit on the merged tree: 1,558 product links, all sponsored, 0 missing) and by `tools/build_cba81fa5_site.py`; `tools/i2_gate.py` G11 and `tools/apply_sponsored.py --check` re-test the same rule from the other side | "Mark links that are advertisements or paid placements … with the `sponsored` value" |
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
   This session re-fetched both links itself on 2026-11-17, and on the merged tree two other sessions had done
   the same that day (`2f181cd9`'s S70–S73 plus the new P4/P5 product rows, `73029680`'s S83–S88), so the claim is
   backed three ways and `data/products.json` now carries both as rows P4 and P5 with
   `confirmed_as_submitted_product: false`. What remains is `G82-F-03`'s owner half: whether those two listings are
   the products that were *intended*, which no fetched page can answer.
3. **G0B2-F-04 (fixed, re-measured after the rebase).** Four rows on `suggestions.html` (Q11, Q12, D8, D10) rendered "no source" and were
   reported by `verify_site` V4 as rows with neither an official link, a flag, nor a repo anchor. They now carry
   real sources (S80/S92/S70/S71 where the row states a fact — ids as re-pointed in `G0B2-F-10`; a repo anchor
   where the row states an owner choice).
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

## 5b. What the merge changed in this review's own conclusions

| Claim as written at the base | Status on the merged tree |
|---|---|
| "six reader surfaces, `site/` 18" | Still six; `site/` is 20. The register row now carries 20 (`G0B2-F-02`). |
| "no capture for the two thermometer links in the canonical registers" | Closed by other sessions the same day; the residual is owner intent only (`G0B2-F-03` rewritten). |
| "the five defined events are not defined anywhere in this repository" | **Overtaken.** `tools/build_measurement.py` now publishes five *proposed* events with a working aggregate-only collector and a counter that ships off, pending hosting and the owner's confirmation of the names (flag `M38-F-04`, which lives in the shop layer's own register at `data/shop/flags.json`, not in `data/flags.json`). SUG-13's status therefore moved from "build this" to "adopt what exists, then host it", and its blocker now says so; the six clauses behind `G0B2-F-05` are unaffected. |
| "no one has cited Google Search Central anywhere" | Still true of the pre-merge tree, and still true in the sense that this pass is the first to cite it as an official host (`check_site.py` `OFFICIAL_HOSTS`, `G0B2-F-09`). |
| source ids S70–S81 owned by this session | Renumbered: S90–S93 are the four genuinely new rows, the other eight re-point at existing rows (`G0B2-F-10`). |
| suggestions.html had 19 V4 advisories | The rows this pass touched: 0. The page overall: 14 hard advisories in another session's tables (`G0B2-F-11`) and 43 V4-review notes, the by-design grade for repo-sourced rows. Three of this pass's own rows are reported on `flagged.html` and stay reported: that table renders no repo-anchor column and `verify_site` does not credit a Google host, so the honest options are widening that checker (not this session's file) or citing an Amazon/FTC page for a sitemap-count claim (a false citation). Recorded in `G0B2-F-09`. |

## 6. What this review did **not** do

- No reader-layer page was restyled, moved or archived; the six surfaces stay as their owners built them.
- No price, rating, review count, sales or ranking value was added anywhere, even where the fetched listing
  pages displayed them (Program Policies 2(b) / 6(t)); they were deliberately not transcribed.
- No claim about search volume, trend or popularity is made in this file or in the register additions.
- `data/products.json`, `data/decision-queue.json`, `data/design-brief.json`, every other session's
  `sessions/**` files and every other session's register rows are untouched by this Part: `data/products.json`
  changed only in the sense that its owner (`2f181cd9`) had already grown it to five rows before this pass
  rebased. `index.html` and `feed.xml` are byte-identical to the merged tree. `scripts/check_site.py` gained the
  one recorded line in `G0B2-F-09`; `scripts/build_site.py` changed only inside `build_suggestions()`.
