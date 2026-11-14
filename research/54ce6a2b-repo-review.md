# Repository review, line by line — session `54ce6a2b` (2026-11-14)

Repo: `kanlerxz87-cyber/Zone3` · Branch `arena/54ce6a2b-zone3`, synced to `main` @ `9024b99`.
Live site: https://kanlerxz87-cyber.github.io/Zone3/

This review reads the repository as-built, not as-described. Each item names the file and, where a
value is checked, the official page it was checked against. Items this session could not confirm
from an official source are listed as unverified; nothing is inferred.

---

## 1. What the repository actually is

Two site generations plus provenance archives, all published from the same root:

| Generation | Builder | Data | Output |
|---|---|---|---|
| Flat dashboard | `scripts/build_site.py` | `data/*.json` | 12 root pages + `/marketing/` + directory mirrors |
| 16-page audit build | `tools/build_site.py` | `data/z3/*.json` | `/dashboard/`, `/products/`, `/pricing/` … |
| Provenance (not current) | — | — | `/docs/`, `/sessions/`, `/archive/` |

Plus the generators themselves, five checker scripts, three research logs and a 3,529-line
`COORDINATION.md` holding ~20 sessions' task boards.

The repository is far past "a website for three products": the data layer, the compliance
reasoning and the cross-session record are the substance, and they are in good order.

---

## 2. Data layer

| File | Count | Review |
|---|---|---|
| `data/sources.json` | 51 sources | 23 `verified`, 25 `observed`, 2 `not-accessible`, 1 `third-party`. No missing `id`/`title`/`url`/`publisher`/`status`. Domains: 16× `www.amazon.com`, 15× `affiliate-program.amazon.com`, 7× `link.amazon`, 5× `github.com`, 4× `www.ftc.gov`, 1 each `linktw.in`, `sellercentral.amazon.com`, `api.github.com`, `sell.amazon.com`. |
| `data/policy_facts.json` | 55 facts | Each carries `source` + `section`. |
| `data/products.json` | 3 products | All identity/price/rating/commission/analytics cells are `null`. Correct: no official source ties any of them to the submitted 9-character token. |
| `data/flags.json` | 66 flags | No duplicate IDs. Severity: 3 Critical, 13 High, 19 Medium, 20 Low, 11 Info. 7 flags carry no source (V-F3, V-F4, V-F5, E-F-02, E-F-04, E-F-07, 3E-F-08) — all process/coordination items, not data rows. |

### 2.1 Register aliases (Low, register hygiene)

Ten groups of source IDs point at the same URL, because sessions appended the same page under new
IDs rather than reusing the existing one:

`S01`=`S49` · `S02`=`S30`=`S50` · `S07`=`S51` · `S11`=`S52`=`S55` · `S12`=`S53` · `S13`=`S54` ·
`S16`=`S32` · `S40`=`S46` · `S41`=`S47` · `S42`=`S48`

Not a factual error — every entry is a real fetch. It does mean "51 sources" overstates distinct
URLs (39 distinct). Session `3ead7ac8` raised part of this as `3E-CR-02`; the S49–S55 group is new
since. Raised here as **54C-F-05**.

### 2.2 The one non-official source

`S17` = https://linktw.in/link-amazon-vs-linktwin, marked `third-party`. The register says it is
used only to raise a flag and never as a fact. Verified: it appears in flag text, never in a value
cell. Correct handling.

`S18` (sellercentral) is `not-accessible` — nothing is taken from it. Correct handling.

---

## 3. Findings this session is raising

| ID | Severity | Category | Finding | Disposition |
|---|---|---|---|---|
| 54C-F-01 | Medium | Accuracy | `EXECUTIVE-SUMMARY.md` §2 and §7 carried stale register counts (48 sources / 51 policy facts / 51 flags; gate figures from an earlier run). Actual: 51 / 55 / 66. | **Fixed in place** by this session, with a dated correction note at the top of the file. |
| 54C-F-02 | Low | Register | Those counts are hand-written, so they will drift again on the next append. | Change request: generate the line from `data/*.json`. |
| 54C-F-03 | Low | Site | The six pages built by `scripts/build_marketing.py` each rendered "Marketing" **twice** in the top navigation, because the generator appended `("marketing/index.html","Marketing")` to a `NAV` list that already contained it. On the hub page both copies carried `class="active"`. | **Fixed in place** by this session (`scripts/build_marketing.py`); 6 files, one line each, generator re-run and confirmed idempotent. |
| 54C-F-04 | Info | Correction of another session's flag | Session `c3dbcc40`'s `C3-F-01` ("sitemap drift": `analysis.html`, `disclosure.html`, `flagged-for-review.html`, `index.html`, `marketing.html` missing from `sitemap.xml`) is a **false positive**. | See §4. Should be withdrawn. |
| 54C-F-05 | Low | Register | Ten alias groups in `sources.json` (see §2.1). | Change request: note or retire duplicates. |
| 54C-F-06 | Medium | Compliance (owner decision) | The Sources page publishes observed price and star-rating literals in table rows. | See §5. Raised for the owner; **not** changed by this session. |

---

## 4. `C3-F-01` is a false positive (54C-F-04)

Session `c3dbcc40` reported that `sitemap.xml` lacks five pages. Checked against
`scripts/build_sitemap.py`, which is the script that owns the file:

* `analysis.html`, `disclosure.html`, `flagged-for-review.html` are meta-refresh redirect stubs —
  excluded by the script's `REDIRECT_STUBS` set on purpose, so search engines index the
  destination instead.
* `marketing.html` is also a stub (it refreshes to `marketing/index.html`); it is caught by the
  script's dynamic `is_redirect_stub()` test.
* `index.html` is mapped to the site root (`''`), which **is** present as
  `https://kanlerxz87-cyber.github.io/Zone3/`.
* `marketing/index.html` is mapped to the directory URL `…/Zone3/marketing/`, which **is** present.

`python3 scripts/build_sitemap.py --check` returns **exit 0** — "sitemap.xml covers every live page
(65 pages checked, 0 extra entries)". The sitemap is complete. The board's `C3-F-01` should be
withdrawn; nothing needs fixing.

---

## 5. Observed price / rating literals still rendered in table rows (54C-F-06)

The site's stated rule — and the correct reading of Participation Requirements 6(t) and 2(b),
quoted verbatim in `research/54ce6a2b-verification-log.md` §5 — is that price, star rating and
review count are withheld because they were read off a rendered page rather than obtained through
the Creators API or PA API.

A scan for those literals **inside `<td>` cells** across the published tree returns 20 files. Most
are unambiguously audit context:

* `commission/index.html` — bounty figures (`$12.00`, `$2.00`, `$5.00`, `$0.25`) copied from the
  official Standard Commission Income Statement Table 1. Legitimate.
* `flagged.html`, `flagged/index.html` — flag descriptions quoting the value they are flagging.
* `compliance/index.html` — a worked disclosure example with a 2008-vintage sample price.
* `sessions/3c886b62/*` — a retained session archive carrying its own `3E-F-03` compliance notice.
* `docs/analysis.html`, `docs/sources.html` — the archived 2026-11-13 build, already flagged.

**One case is not clear-cut.** `sources.html` renders, in the *Note* column of the source register:

> `S46` … "Fetched 2026-11-14. Result 1 for B0CDY277D3 as displayed: 4.2 out of 5 stars, (4.8K)
> reviews, 1K+ bought in past month, price USD 79.93 (deal; List: USD 99.99) …"

and the same for `S47` and `S48`. These are the same three values the product tables withhold. The
counter-argument, which earlier sessions accepted, is that this is a note about what the fetch
returned — provenance for a source, not a product display. The counter to that is that 6(t) bars
displaying star ratings "in part or in whole", without an exception for provenance.

This session is **not** changing it. `data/sources.json` is a shared register, the wording belongs
to sessions `9fef7647` and `b90c5685`, and whether a source register counts as "display" is the
site owner's call to make. It is published on the Flagged for review page as **54C-F-06** with
these source links so the owner can decide.

---

## 6. Defects checked for and **not** found

| Check | Result |
|---|---|
| Merge conflict markers anywhere outside `archive/` | 0 (line-leading `<<<<<<<` / `>>>>>>>`) |
| Duplicate flag IDs in `data/flags.json` | 0 |
| Source entries missing a required field | 0 |
| Pages with a duplicated nav destination (after this session's 54C-F-03 fix) | 0 |
| Dangling source or flag references (`tools/link_report.py --strict`) | exit 0 |
| Broken internal or external links (`scripts/check_all_links.py`) | 116 pages, 0 errors |
| Rows without provenance (`tools/verify_site.py`) | PASS, 0 advisories |
| Legacy `/docs/` product page still rendering price/star cells | No — `docs/products.html` has none. The executive summary §3 sentence saying "a legacy category/reference page still contains dated price/rating snapshots" is therefore **out of date**; it is folded into 54C-F-01's correction. |

---

## 7. Independent re-verification

Eight load-bearing claims were re-fetched from the official pages by this session and confirmed
verbatim. Full quotes, URLs and verdicts: [`research/54ce6a2b-verification-log.md`](54ce6a2b-verification-log.md).

Headline results: all three short links resolve to the same three ASINs recorded in the repo
(`B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`); all three `/dp/<9-char token>` controls return Page Not
Found; ASIN is defined as 10 characters; Operating Agreement §5 disclosure wording, the "Updated:
October 15, 2025" header, and the customer-reviews-for-compensation sentence are all present;
Participation Requirements 6(s), 6(t), 6(v), 6(w) and 6(y) are all present verbatim; Standard
Commission Table 1 renders without a sign-in and lists **Kitchen at 4.50%** (and Home at 3.00%).

One earlier disagreement is settled: the Operating Agreement **does** contain the
"reviews … in exchange for compensation" sentence, in its opening paragraph. Session `7f84fea4`
withdrew PF-14 saying the text was not found; session `3ead7ac8` (`3E-CR-03`) corrected that. This
session's independent fetch confirms **3E-CR-03**.

---

## 8. What remains genuinely open

1. **Product identity (`FLG-002`, High).** The three destinations are verified; that they are the
   products the owner meant is not documented by any official source. Only the owner can close
   this.
2. **No Associates tag (`FLG-010`).** Without one, no Special Link, no commission, no click data.
3. **No Creators API access.** The prerequisite is "at least 10 qualifying sales within the past 30
   days" (S04), which cannot be met before the first sales. So the price/rating blanks cannot be
   filled by this build, now or on a later run.
4. **`link.amazon` redirect behaviour (`FLG-003`).** Whether the short link redirects without an
   affirmative click determines whether CIS 2(e) disqualifies the purchase. Needs a logged-in
   Associates account to test.
