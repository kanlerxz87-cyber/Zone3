# Session `41e84402` — verification record, 2026-11-19

Branch `arena/41e84402-zone3`. Base at claim: `6eb8c18` (`main`, PR #178). Merged base after three rebases and one merge of `origin/main` `1623c1c` — PRs #181, #183, #185–#191, #193, #194, #195 and #196 landed inside this session's window (sessions `07fb37ba`, `cbbd4d8f`, `8aa259bb`, `d3493182`, `b3e82b38`, `222cfe13`, `cdb0a5ac`, `aebf0747`, `4d7fe998`).
Every number below was produced by a command in this repository, on this checkout, on 2026-11-19. Nothing here is a traffic, demand, conversion, ranking, price, rating or revenue figure, and no Amazon endpoint was navigated to.

## 1. Commands, and what each one proves

| # | Command | Result on the merged tree |
|---|---|---|
| 1 | `python3 tools/publish.py` | **41 commands checked; 0 failed** (16 builders + 25 checks), on the merged union tree of 122 published pages. Run three times: the second and third changed **0** tracked files. `python3 tools/publish.py --check` on the same tree: 25 checks, 0 failed. |
| 2 | `python3 sessions/8aa259bb/measure_brief_rows.py` (another session's read-only measure, re-used, not edited) | 122 published pages; **0** pages missing a `<title>`; **0** missing a meta description; disclosure sentence on **122/122**; og:image and JSON-LD on **31**; `rel="sponsored"` absent from **1,227** `amazon.*` anchors (3,026 total) on the merged tree, all of which are policy/agreement citations on `affiliate-program.amazon.com` — 1,222 of 3,016 on the tree this pass measured first |
| 3 | `python3 sessions/41e84402/measure_drift.py` (this pass; JSON in `measurement-2026-11-19-drift.json`) | **`drift_found: false`** on the merged tree — no live reader page, README line or register field states a count its register does not hold (registers read: 10 guides, 28 proposals, 38 questions, 18 canonical URLs, 28 feed entries, 15 search rows). All **18** indexable reader URLs carry og:image + JSON-LD + disclosure + canonical. **0** of the reader pages' `amazon.com` links are unsponsored. Chooser present on 4 shop surfaces. No dimension-like field in any of the four product registers. |
| 4 | `python3 tools/preview.py --host 127.0.0.1 --port 3000` + `node sessions/41e84402/browser_measure.cjs` (JSON in `measurement-2026-11-19.json`, screenshots in `screenshots/`) | Compare page at 320/390/768 px: sticky product column holds its left edge (`left_before == left_after_scroll == 16px` at 320/390) while the region is scrolled 160 px sideways; the region needs no sideways scroll at 768 px (the table fits, which is recorded, not smoothed over). Chooser with its 3 steps renders above `#comparison` at all three widths. Interactive targets under 24 px: **0 of 26** (before this pass: category pills 31 px, in-cell link 11 px, guide-card link 18 px). 14 of 26 remain under 44 px and all are inline text links. |
| 5 | `node sessions/1c072a7a/browser_check.cjs` (the published harness, unmodified) | **14/14 checks pass; 40 WCAG 2.0/2.1 A/AA page/viewport scans over 20 pages, 0 violations** (`browser-harness-report-2026-11-19.json` is that run's report, copied here for provenance). |
| 6 | `python3 tools/build_brief_status.py --check`, `python3 tools/build_publication.py --check`, `python3 scripts/build_sitemap.py --check`, `python3 tools/build_feed.py --check` | all pass — sitemap **18** URLs, feed **28** entries, search index **15** rows, 23 register rows. |

## 2. The five links, and what is still not known

The five submitted short links are recorded in `data/publication.json → products` exactly as earlier sessions observed them, and this pass did **not** re-open them (three separate 2026-11-19 records already did: `sessions/b580d790/`, `sessions/6b68afc8/`, `sessions/d3493182/`). Intended ASIN, official listing URL, confirmation date and confirmation source stay **blank** for all five; the observed redirect ASINs stay in their own fields. The two fields are not merged. `FLG-003` — whether the supplied links comply — remains **unresolved**, and this record does not call them invalid.

| Product | Submitted (as supplied) | Observed destination, per the register | Intended ASIN confirmed? |
|---|---|---|---|
| SHOP-01 Chefman 6-quart dual-basket | `https://link.amazon/B04G1MEwY` | `B0CDY277D3` | no — blank |
| SHOP-02 Emeril Lagasse 26QT French-door | `https://link.amazon/B02NbDxp3` | `B09B7SB46R` | no — blank |
| SHOP-03 Chefman TurboFry 8 Qt | `https://link.amazon/B00hJ57DV` | `B08DKYBTPH` | no — blank |
| SHOP-04 ThermoMaven digital thermometer | `https://link.amazon/B0c8moW59` | `B0DHZTCNR5` | no — blank |
| SHOP-05 CHEF iQ Sense wireless | `https://link.amazon/B0f3GKalj` | `B0DZFD6R9Z` | no — blank |

Official references used for the rules this pass had to satisfy — the same URLs the site cites:
[Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) ·
[Program Policies / Participation Requirements](https://affiliate-program.amazon.com/help/operating/policies) ·
[FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) ·
[Google: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) ·
[Google: snippet / unique descriptions](https://developers.google.com/search/docs/appearance/snippet) ·
[Google: crawlable links and anchor text](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) ·
[Google: page experience](https://developers.google.com/search/docs/appearance/page-experience) ·
[Google: helpful, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) ·
[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 3. Irregularities found and published, not absorbed

1. **`E41-F01` — counts typed into live copy.** `tools/build_publication.py` said “the current six guides” twice on the suggestions page and `data/publication.json → P26-S3` told the reviewer to choose “which of the six guides”, while the register held eight; `README.md`’s headline said six four lines above its own line saying eight. All three are now derived or count-neutral, and the publication gate fails on a count phrase that disagrees with its register. Tested by hand-stale-ing the README block: `FAIL README register-facts row 'Question-led guides': README says 8, register says 9`.
2. **`E41-F02` / `E41-B03` — a same-day measurement read a shared footer link as article-level linking.** Brief row S-24 was recorded as “all four articles and all eight guides link to the comparison page (`products/index.html`)”. On a guide page that string occurs only in the site-wide footer directory, labelled “Research product register”, pointing at the research intake register — not the buyer comparison table at `shop/products/index.html`. The article bodies held no such link. This pass measured the bodies separately and shipped the link on all nine guides; the earlier row’s text was left intact above the amendment.
3. **`E41-F03` / `E41-B02` — the per-centimetre analysis cannot be written from what this repository holds.** `data/publication.json`, `data/shop/products.json`, `data/z3/products.json` and `data/products.json` contain no footprint or interior dimension for any product (measured by field-name scan, `s23_dimension_check`). So `S-23` stays “Not found here”, the analysis was **not** written, and the capture decision is on the desk as `E41-P1` / `E41-Q1`.
4. **`E41-F04` / `E41-B04` — “sticky comparison bar” shipped as a sticky product column.** Named as what it is, with the alternative (a floating bar) put to the owner as `E41-Q2`.
5. **`E41-B01` — 121 of the 164 rows in `data/flags.json` carry no `status`**, which is why the review page cannot be split into open / resolved / historical (`S-11`). No status was asserted onto a historical row; a new gate requirement stops the backlog growing (a row with `raised` must carry a `status`).
6. **`E41-F05` — four sessions moved `main` inside this session’s window.** #181 shipped the executive-brief count fix this pass had partially claimed, and #185 shipped a full re-measure of the brief register that overlapped `E41-T6`. Both were kept; this session re-scoped to amending and verifying instead of duplicating, and rebased rather than reverting.


## 4. Deliberately not claimed by this pass

No price, star rating, review count, sales, conversion, commission or revenue figure. No trending, popularity or demand statement — the only `trend*` sentence on any reader page is the disclaimer on `about.html` (measured). No product photography added; no Amazon Program Content stored. No generated “test”. No campaign-ledger row (still 0 by design, and the executive brief’s `0` is read from that file). No Search Console, no analytics deployment, no account change, no hosting change. The new guide makes no measurement claim: it quotes listing titles and lists what is unknown.

## 5. Reader-facing changes this pass, each traceable

| Change | Where it is enforced | What a reviewer can check by hand |
|---|---|---|
| Three-question chooser above the comparison table | `tools/build_publication.py → catalogue()`; asserted in `browser_measure.cjs` | [shop/products/](https://kanlerxz87-cyber.github.io/Zone3/shop/products/index.html) — the chooser section precedes `#comparison` |
| Sticky product column + scroll note | `assets/publication.css` E41 appendix | same page, on a phone or at 320 px: scroll the table sideways, the product names stay |
| Every guide links the comparison table in its own body | `tools/build_publication.py → guide_page()` | any [guide](https://kanlerxz87-cyber.github.io/Zone3/guides/), “Explore the shortlist / Compare all five listings in one table” |
| New guide: thermometer listing numbers | `data/publication.json → guides`; sitemap, feed and search index are register-driven | [guides/thermometer-numbers-on-the-label.html](https://kanlerxz87-cyber.github.io/Zone3/guides/thermometer-numbers-on-the-label.html) |
| Counts derived; README block generated and gated | `tools/build_publication.py → readme_facts()`, `tools/check_publication.py` | `python3 tools/publish.py` then hand-stale the README row and re-run the gate |
| Tap targets ≥24 px on the compare page | `assets/publication.css` E41 appendix rules | `node sessions/41e84402/browser_measure.cjs` |

## 6. Second-round count drift, found by this session's own gate on the merged tree

Union with `cdb0a5ac` (PRs #194/#195, a tenth guide `guides/where-does-the-probe-go.html`, its own re-measure of
every brief row, and the same count-derivation applied to `review_round_html`) and with `aebf0747`/`4d7fe998`
(#196, audit refresh and executive-summary reconciliation) — resolved as a **merge**, not a replay, because four
commits had landed while this session was mid-flight: `data/publication.json` re-formed from main's register with
this pass's guide, `E41-P1/P2`, `E41-Q1/Q2` and the count-neutral clause fixes appended; `data/shop/brief-status.json`
kept **main's** row texts as the base (their re-measure covers 20 rows to my 13) and my `Re-measured … (session
41e84402…)` sentences were appended field-by-field where absent, with the page-count claims re-measured to 122;
`tools/build_publication.py` took **main's** derived counts inside `review_round_html` over my literals;
`tools/build_brief_status.py` kept **my** derived `_meta` machinery, so the hardcoded eyebrow main had typed
("sessions 8aa259bb and cdb0a5ac, merged") became a `_meta.rechecks` entry for `cdb0a5ac` instead, and the page
now names four measurement passes without a string in the template. `S-24`'s flag column kept main's `M38-F-12`
(a single-value field; my `E41-B03` reference lives in the row text) — replacing it, as an earlier attempt of mine
did, would have silently dropped their cross-reference.

The union with `b3e82b38` (PRs #189–#191) and `222cfe13` (PR #193) moved the registers to **9 guides / 28 proposals /
38 questions / 15 sources / 13 design blocks / 6 paths**, which re-opened the same `E41-F01` class in three places:

| Where | What had gone stale | What this pass did |
|---|---|---|
| `README.md` headline (re-typed by #193) | “five … eight practical question-led guides” and an ownership bullet listing “eight guides, … twenty-six proposals … thirty-six decision-readiness questions” against registers of 9 / 28 / 38 | kept this session's count-neutral prose and the generated `z3:register-facts` block instead of re-typing new numbers |
| `data/publication.json → questions[B38-Q4].known` | “eight guides exist” | rewritten to read the count from the register rather than quote it |
| `data/publication.json → proposals[B38-P1].discoveries[0]` | “the current eight guides” | now says “the published guides” |
| `data/publication.json → review_b9008684` | “the six guides” | **left alone** — a dated review round records what was true on its date |

**The gate was closed where it had a hole.** `tools/check_publication.py` required the numeral to sit *immediately*
before the register label, and only inspected README's pre-block prose; both #187 and #193 wrote counts that slip
past those rules (“eight practical\nquestion-led guides”, counts inside the ownership bullets). The pattern now
allows a short closed list of qualifiers across a line break, and the README scan covers the whole file except the
generated block and headings that mark a dated section (record / history / log / session / update / archive). Proof
it bites: planting “The site ships ten practical / question-led guides today.” in the ownership section produced
`FAIL README.md current-state prose: states 10 question-led guides; the register holds 9` → `PUBLICATION FAIL`,
and removing it returned a PASS; the widened scan also flagged this session's own README sentence quoting the old
headline, which was rewritten count-neutral rather than exempted.

**Board hygiene, recorded not edited:** `main`'s `COORDINATION.md` carries three stray `>>>>>>> <sha> (B38-T1: …)`
lines committed inside session `b3e82b38`'s Part (they were in `main` before this session's merge). They are another
session's text, so they were left as found and flagged here; the file remains append-only for this Part.
