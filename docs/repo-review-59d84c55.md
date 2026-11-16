# Repository review — session `59d84c55`, 2026-11-16

Line-by-line audit of `kanlerxz87-cyber/Zone3` as found at base commit `933e2f3`, plus what this
session changed. Every finding below is either a count this session ran itself or a file path you can
open. Nothing here is inferred.

**Scope note.** This is a review *of the repository*, not a review of Amazon's programme. The
programme facts are re-verified separately in `site/evidence.html` and recorded as data in
`data/i2/verification.json`.

---

## 1. What the tree contains at `933e2f3`

| Measure | Value | How it was counted |
|---|---|---|
| Tracked files | 302 | `git ls-files \| wc -l` |
| HTML pages in the tree | 82 (128 including `archive/`) | `rglob('*.html')`, excluding `archive/` |
| Distinct site generations served from the root | **4** | see §2 |
| Internal links checked | 2,723 | full-tree relative-link crawl, 0 broken |
| External URLs checked | 115 | `scripts/check_all_links.py`, 0 errors |
| Largest tracked file | `COORDINATION.md`, 528 KB | `git ls-files -z \| xargs -0 du -h` |
| Repository size on disk | 1.9 MB (`.git`) | `du -sh .git` |

---

## 2. Four site generations are published side by side

This is the single biggest structural irregularity in the repository, and it is the direct cause of the
"looks like an internal tool" impression.

| Generation | Path | Built by | Data source | Pages |
|---|---|---|---|---|
| Flat page set | `/` (`index.html`, `products.html`, …) | `scripts/build_site.py` | `data/*.json` | 13 root pages |
| Audit build | `/dashboard/` and 15 sibling dirs | `tools/build_site.py` | `data/z3/*.json` | 16 |
| `/docs/` reference set | `/docs/` | hand-authored / earlier build | own data | 8 |
| Session archives | `/sessions/`, `/archive/` | each session | each session | 19 + 8 |

**Why it happened.** Each session was told not to overwrite another's output, so each wrote into a new
namespace. The strategy kept every session's work — verified: nothing is missing — but it means a crawler
and a reader both see several pages making similar claims with different dates.

**Finding R-01 (structural, medium).** Four generations with no single canonical entry point. The root
`index.html` is an audit dashboard, and the newly added `/site/` is the reader-facing layer. Proposed fix:
`D-01` and `D-08` on `/site/decisions.html`. Not applied, because it changes other sessions' pages.

---

## 3. Compliance irregularities found by inspection

| ID | What was found | Evidence | Disposition |
|---|---|---|---|
| I2-F-01 | The exact §5 disclosure is present on every page but placed in the **footer only**. That meets the Operating Agreement's "on your Site" wording; it is weaker than the FTC's placement guidance, which warns a disclosure appearing only at the end of a page is "likely to be missed". | [Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement), [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | The new `/site/` places it in a non-dismissable banner above the navigation. Older pages flagged, not edited. |
| I2-F-02 | No publishable price, star rating or review count exists for the three products. `data/products.json` keeps 2026-11-14 manual captures under `observed_2026_11_14`; they are not rendered as facts. **This session's independent fetch did not attribute a price or rating to any of the three featured ASINs** — the numbers on those pages belong to related-item carousels for other ASINs. | Program Policies [2(b) and 6(t)](https://affiliate-program.amazon.com/help/operating/policies) | Cells stay blank with an explanation. Blocked on `Q4`. |
| I2-F-03 | None of the three submitted short links resolves to a URL carrying an Associates tag, and no tag exists anywhere in the repository. | The observed final URLs are recorded in `site/evidence.html` (I2-S07…S09); none has a `tag=` parameter | Every buy action on `/site/` is disabled and labelled. Blocked on `Q1`. |
| I2-F-04 | The nine-character tokens are not ASINs; `/dp/B04G1MEwY` returns *Page Not Found* when re-fetched today. The destinations are documented; **requester intent is not established by any official source**. | I2-S13; [Creators API GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) | Identity labelled unconfirmed on every product card. Blocked on `Q2`. |
| I2-F-05 | No per-product commission rate. The public table is organised by product **category**; no official page maps an ASIN to a row. | [Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | Kitchen 4.50% published as a category reference only. |
| I2-F-06 | No official trend, demand or conversion endpoint exists. The Creators API exposes exactly four operations. | [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) | No trend or conversion claim is published anywhere. Not fixable by this build. |
| I2-F-07 | Superseded pages still render numeric price and rating strings: 5 under `/docs/`, 13 under `/sessions/3c886b62/`. **19 `/sessions/` URLs are in `sitemap.xml`**, which advertises superseded pages as current. | counted in this session; `sitemap.xml` | Proposed `D-08`. Not applied — those pages are the audit record. |

---

## 4. Data-layer review — what is trustworthy and what is not

### 4.1 `data/i2/` (new in this session)

| File | Rows | Cross-check |
|---|---|---|
| `sources.json` | 14 sources | Each was fetched today; the "observed" text is a paraphrase written at read time, and each URL opens the page |
| `verification.json` | 22 claims | 18 confirmed, 1 confirmed with corrected wording, 1 not re-checked, 2 unverified |
| `catalog.json` | 3 products × 13 fields | 9 of 13 fields are `null` by design for every product |
| `decisions.json` | 12 proposals, 12 questions, 9 discovery actions, 6 prompts | Every factual statement carries an `I2-Snn` link |

### 4.2 Older data layers — left intact, with the caveats that matter

| File | Assessment |
|---|---|
| `data/products.json` | The `observed_2026_11_14` blocks contain usable research evidence *and* unpublishable price/rating figures. Correctly **not rendered**. Keep, but never serve as facts. |
| `data/z3/products.json` | Same pattern: attributes sourced from listing titles, dynamic values `null`. Sound. |
| `data/topics.json` | 12 working titles, each tied to a verified fact and a "must not state" rule. This is the strongest content artifact in the repository and the basis for the guide format. |
| `data/suggestions.json` | 10 proposals + 10 questions + 6 discovery actions from session `4f83ee7b`. Sound; the new `/site/decisions.html` is a reader-ready presentation of the same approach, extended with accept/reject/defer. |
| `data/flags.json`, `data/z3/flags.json` | Two registers with **the same numbering for different items**. A reader who sees "FLG-013" on two pages sees two different findings. Documented by earlier sessions; still a real trap. |
| `data/sources.json` | 51 entries, `S01`…`S58` with gaps (S33–S39 absent). Gaps are harmless but look like lost data. |

---

## 5. Code review of the generators and gates

| Script | Lines | Verdict |
|---|---|---|
| `scripts/build_site.py` | 2,900+ | Writes the flat pages. **Edits this session:** one NAV entry, one dashboard tile, one sitemap group, one hero CTA. Output regenerated, not hand-edited. |
| `tools/build_site.py` | 1,574 | Writes the 16-page audit build. Untouched. Its provenance gate (G1–G8) passes. |
| `tools/verify_site.py` | 340 | Audits the whole tree. **Edit this session:** widened the flag-ID pattern to accept `I2-F-nn` and `class="blank"`, so the new pages' deliberate blanks are recognised as provenance rather than reported as defects. One line, additive. |
| `tools/build_i2_site.py` | ~1,100 | **New.** Builds `/site/`. |
| `tools/i2_gate.py` | ~290 | **New.** G1–G10 gate. 13 injected violations were each caught (see `COORDINATION.md` §I2). |
| `scripts/check_site.py` | 380 | Passes; does not know about `/site/`, so `/site/` is gated by `i2_gate.py` instead. Not modified — adding it would require editing a file other sessions own. |
| `scripts/build_sitemap.py` | 150 | Walks the tree, so it picked up `/site/` automatically. |

### 5.1 Bug found in an existing gate

`tools/i2_gate.py`'s own image rule initially matched only `amazon.com` and would have let every real
product image through, because Amazon serves imagery from `m.media-amazon.com`,
`images-na.ssl-images-amazon.com` and similar hosts. Caught by a negative test before publishing; the
host list now covers the CDNs. **This is worth carrying into `tools/verify_site.py`**, whose `V6`
rule has the same narrow host pattern — logged as a recommendation, not applied, because that file is
owned by another session.

### 5.2 Repository hygiene

| Item | Status |
|---|---|
| Licence file | **missing.** `README.md` already flags it. Someone has to choose a licence before the code can be reused. |
| `COORDINATION.md` | 528 KB, with **four section headers duplicated**. History of repeated merge resolutions, not corruption, but it makes the board hard to claim against. Proposed de-duplication in I2-F-09. |
| `.github/workflows/` | **absent.** Every gate runs only when a human remembers to run it. A CI workflow running `i2_gate.py`, `verify_site.py` and `check_site.py` on push would make the gates real. Not added, because enabling Actions is a repository-level decision. |
| `.nojekyll` | present — required for the `_`-prefixed paths and for keeping Jekyll from reprocessing generated HTML. |
| `robots.txt` | allows everything, points at `sitemap.xml`. Given §I2-F-07, the sitemap advertises pages that should not be indexed. |
| Open PR #71 | `mergeable=CONFLICTING`, open since 2026-11-14. Not part of this build. |

---

## 6. What this session changed, exhaustively

**New files**

```
site/                              8 pages + assets/site.css + assets/site.js + site-index.json
data/i2/sources.json               14 sources read 2026-11-16
data/i2/verification.json          22-claim verification log
data/i2/catalog.json               3 products, 9 of 13 fields null by design
data/i2/decisions.json             12 proposals, 12 questions, 9 actions, 6 prompts
tools/build_i2_site.py             generator
tools/i2_gate.py                   G1–G10 release gate
docs/repo-review-59d84c55.md        this document
```

**Modified files**

| File | Change | Why it was unavoidable |
|---|---|---|
| `scripts/build_site.py` | +1 NAV entry, +1 dashboard tile, +1 sitemap group, hero CTA retargeted | Without these, `/site/` would be unreachable from the published site — the exact defect earlier sessions flagged as V-F3 |
| `tools/verify_site.py` | flag-ID regex widened by `I2-F-\d+\|class="blank"` | The new pages would otherwise report 15 false advisories |
| `README.md`, `EXECUTIVE-SUMMARY.md` | new sections describing this pass | The brief asks for an executive summary |
| `COORDINATION.md` | one appended Part (this session) | The shared board protocol requires it |
| Regenerated pages | `index.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `flagged.html`, `sources.html`, `air-fryers.html`, `content-topics.html`, `decision-center.html`, `executive-summary.html`, `marketing/briefs.html`, `verification.html` | Produced by re-running the existing generator after the NAV change, so the committed output is what the generator produces |

**Nothing was deleted, renamed or moved.** No other session's data, page or script was overwritten.

---

## 7. Ranked recommendations for the next session

| # | Recommendation | Effort | Why now |
|---|---|---|---|
| 1 | Answer `Q1` (tag), `Q3` (marketplace), `Q2` (intent) | owner | Nothing commercial can start until these exist, and all three are a few minutes of account reading |
| 2 | Accept or reject `D-01`/`D-08` and make `/site/` the canonical root | low | Turns four generations into one front door without deleting any evidence |
| 3 | Remove the 19 archive URLs from `sitemap.xml`, add a visible "superseded" label | low | Stops advertising pages that carry price figures this site's own rule prohibits |
| 4 | Fix the `V6` host pattern in `tools/verify_site.py` to match the CDN fix in `i2_gate.py` | trivial | The narrower pattern is a real hole in a published gate |
| 5 | Add `.github/workflows/validate.yml` running the three gates | low | Gates that only run when remembered are not gates |
| 6 | Choose a licence | decision | Already flagged in the README; blocks reuse |
| 7 | De-duplicate `COORDINATION.md` | low | 528 KB with four duplicated headers is a claiming hazard |
| 8 | Name an editor (`Q5`) and publish the second guide | medium | The only path to content that does not read as generated |

---

## 8. How to reproduce every number in this document

```bash
git ls-files | wc -l                                   # 302 tracked files
find . -name '*.html' -not -path './archive/*' | wc -l # 82 pages
du -sh .git                                            # 1.9M

python3 tools/i2_gate.py          # new site: G1–G10
python3 tools/verify_site.py      # whole tree: V1–V7
python3 tools/build_site.py       # flat pages: provenance gate
python3 scripts/check_site.py     # data + page checks
python3 scripts/build_sitemap.py --check
python3 scripts/check_all_links.py
python3 tools/link_report.py --strict
```

All eight pass on commit `07c5031` + this session's follow-ups. The negative-test harness that proves
`i2_gate.py` fails on each violation is recorded in `COORDINATION.md` §I2-T3.
