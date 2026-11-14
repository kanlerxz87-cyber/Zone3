# Findings — irregularities flagged for review (session `03bbd050`, 2026-11-14)

Every item below was found by reading the tree at `58d2744` and re-fetching the cited source the same day.
Severity is about *consequence for the affiliate account*, not about how hard it is to fix. **None of these block
the merge**; they are published here and on the site for manual review, each with the link that proves it.

Files owned by other sessions are **not** edited by this session — where a fix belongs in someone else's scope it
is written as a change request (`03-CR-n`), per the coordination rules in `COORDINATION.md`.

---

## 03-F-02 · High → **RESOLVED on main by PR #31** · A live sub-site published price cells with no Associates disclosure

`sessions/3c886b62/` is served at `https://kanlerxz87-cyber.github.io/Zone3/sessions/3c886b62/` (16 pages). **10 of
those pages render a `$` amount in a table cell** for the three listings (`analysis.html`, `comparison.html`,
`commission.html`, `category-home-kitchen.html`, `index.html`, `products.html`, `verification.html` and the three
`product-*.html` articles). **15 of the 16 pages contain no disclosure sentence at all** — only `compliance.html`
carries the words "qualifying purchases", and there only as advice the price pages do not follow:

> … disclosure wording, *As an Amazon Associate I earn from qualifying purchases*, must go into that banner and
> into the body of any pag…

The page-level banner on those same pages says instead: *"Disclosure & status. This site is being prepared for the
Amazon Associates program."* — which is not a disclosure of a material connection. The sub-site therefore documents
the rule in one page and breaks it on the ten pages that show prices.

*Why it matters:* omission of the required disclosure is treated by Amazon as a **material breach** (Operating
Agreement §5, and §2's "cease payment … without notice" remedy), and the FTC separately requires the material
connection to be "hard to miss" and placed "with the endorsement message itself" — not on a separate compliance page.
*Reproduce:* `for f in sessions/3c886b62/*.html; do printf "%s %s\n" "$f" "$(grep -c 'As an Amazon Associate I earn' $f)"; done`
(→ `1` for `compliance.html` only) and
`grep -lE '>[[:space:]]*\$[0-9]+\.[0-9]{2}[[:space:]]*<' sessions/3c886b62/*.html` (→ the 10 files listed above).
*Sources:* [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) ·
[FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
*Owner:* session `3c886b62` scope (`sessions/3c886b62/**`), merged via PR #15/#16 → change request 03-CR-6.

## 03-F-03 · High → **RESOLVED on main by PR #31** · The `/docs/` sub-site repeated the pattern with a pronoun variant

`docs/` (8 pages, `…/Zone3/docs/`) carries **"As an Amazon Associate *we* earn from qualifying purchases."** —
plural, on every page. The prescribed sentence is singular and first-person ("I"), and the root build renders it
exactly. Six of the eight pages render a price cell for one of the three listings (`analysis.html`, `content.html`,
`executive-summary.html`, `flagged.html`, `index.html`, `products.html`); five of those six have no exact sentence
(`executive-summary.html` is the exception). This is the same issue `dff4acde` raised as `D-F-01`;
still open on `main` as of `58d2744`. *Owner:* `79f85104` scope → change request 03-CR-7.

## 03-F-04 · Medium · Where a price may come from is narrower than "we saw it on Amazon"

The repo's own policy register (`data/policy_facts.json`, source S02 = the Program Policies page) says a Site
**may only show prices and availability if (a) Amazon serves the link in which that data is displayed, or
(b) the data is obtained via the Creators API / PA API** under the licence. A value captured from a product page and
committed into `data/products.json` is neither route. Two further facts close the loop:

| Fact | Effect on this project |
|---|---|
| Creators API prerequisite: "Have at least 10 qualifying sales within the past 30 days" ([docs](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)) | route (b) is not available to a new/low-volume account |
| PA-API 5 "has been deprecated and is being replaced by the Creators API" ([deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation)) | the legacy route is closed |
| PF-27 date/time stamp requirement; PF-10 "no inaccurate … or misleading claims about … prices" | a static number goes stale the moment Amazon changes it |

`data/products.json` on `main` keeps `price: null` — **correct under this rule**. PR #26 proposed filling those fields
with observed values ($79.93 / $149.99 / $79.91 — all three re-confirmed by me today, see `verification.md` §A);
that proposal is what 03-CR-1 responds to. Keep the observation in a dated research log, out of rendered tables.

## 03-F-05 · Medium · Tokenised redirect URLs are cited as sources but cannot be re-opened

`data/products.json → redirect_observed.final_url` pins `…&btn_ref=srctok-<hex>…`. Across four fetches of the same
three short links I recorded three different tokens, and the third fetch of link 3 also gained `&th=1`. So
`S11/S12/S13`'s status notes cite a URL string that no longer reproduces. *Fix:* cite
`https://www.amazon.com/dp/<resolved-ASIN>` as the source and keep the tokenised URL in the capture log only.
*Sources:* [link 1](https://link.amazon/B04G1MEwY) · [link 2](https://link.amazon/B02NbDxp3) ·
[link 3](https://link.amazon/B00hJ57DV)

## 03-F-06 · Medium · Category ⇒ commission rate stays an inference gap (and the site is right to leave it blank)

Live breadcrumb for listing 1: **Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers
(node 17659096011)** ([the listing](https://www.amazon.com/dp/B0CDY277D3)). Table 1 offers
"Physical Books, **Kitchen**, Automotive — **4.50 %**" and "Toys, Furniture, **Home**, … — **3.00 %**"
([source](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ)). Nothing official maps a browse
node to a rate-card category, so choosing 4.50 % over 3.00 % would be a guess with a 1.5-point revenue consequence.
The account's own rate card — the only authoritative mapping — sits behind sign-in
([/help/operating/schedule](https://affiliate-program.amazon.com/help/operating/schedule), recorded as sign-in
gated). **No action for the site; action for the owner: read the rate card in-account.**

## 03-F-07 · Medium · A hop link is the wrong *monetisation* link, independent of the disclosure question

The site's own register (S30) captures Amazon's definition: *"any Product purchased by a customer who is referred to
an Amazon Site by a link that sends users indirectly to an Amazon Site via an intermediate site, without requiring
the customer to click on a link or take some other affirmative action on that intermediate site (a "Redirecting
Link")"* ([Program Policies](https://affiliate-program.amazon.com/help/operating/policies)). `tools/verify_site.py`
already lists `link.amazon` among shortener domains (V6), with an explicit carve-out for
`https://link.amazon/` so the submitted links can be displayed. Read together: **displaying the owner's submitted
hop link is fine; publishing it as the affiliate link is not a monetisation strategy.** Correct construction is a
Special Link built from the account's own tag, which no page here does yet because no tag is configured
(`associates_tag: null`, `campaigns` ledger empty by design). *Owner decision needed before any link goes live.*

## 03-F-08 · Low · Two source IDs per URL inflate the evidence count

`data/sources.json` on `main` contains `S02` and `S30` → the same Program Policies URL, and `S16` and `S32` → the
same `dp/B08DKYBTPH` URL. Citing two rows of one document as two sources overstates corroboration, and
`tools/link_report.py` counts each once. PR #26 adds four more of the same (`S30–S33`, `S36–S37` vs `S11–S14`,
`S01`, `S02`). *Fix:* reuse the id, or record a `same_page_as` field. → 03-CR-3.

## 03-F-09 · Low · `tools/link_report.py` still prints an out-of-date line

It reports "per-category commission — rate card is behind Associates sign-in", but Table 1 is public (03-F-06).
Part C already filed this as a change request to the file's owner; it is still open. My run reproduced it at
`58d2744`.

## 03-F-10 · Low · Two registers use colliding ID names on one site

The root register uses `S01…S45`; the sub-site `sessions/3c886b62/data/sources.json` uses `S1…S12` for a
**different** set of URLs. A reader who sees "S2" on `/sessions/3c886b62/analysis.html` and follows the site-wide
convention lands on the wrong document. My whole-tree audit flags `S1…S9` as dangling references for exactly this
reason. → 03-CR-8 (prefix per-register ids, e.g. `3c6-S2`).

## 03-F-11 · Low · SEO/sitemap coverage is partial; `404.html` has no `<h1>`

`sitemap.xml` lists 16 URLs; 13 nav-reachable pages (root flat pages, `marketing/`, `docs/`, `/dashboard/`) are not
listed — matches `D-F-05`/`V-F4`, still open. `404.html` uses an `<h2>` as its only heading. Neither affects data
integrity.

## 03-F-12 · Info · Checked and cleared (recorded so the audit shows its negatives)

| Probe | Result |
|---|---|
| Conflict markers in any tracked file | 0 |
| Secret patterns (AWS key, private key, `ghp_`, Slack token) | 0 hits |
| Broken internal links outside `archive/` | 0 of 110 pages |
| Placeholder markers | 3 hits, all benign: 2 inside `archive/c4e71983/**` (preserved snapshot), 1 in `repo-review/index.html` where "placeholder" is the word being discussed |
| `dashboard.html` `$0.00` KPI | labelled "illustrative commission (price unverified)" — an explicit zero, not an invented price |
| `marketing/` (7 pages, PR #34) | 0 broken links, disclosure on every page, no prices, no ratings — policy-clean as built |
| `data/sources.json` `S17` = `linktw.in` | correctly labelled `"publisher": "LinkTwin (commercial competitor; NOT an Amazon source)"`, `"status": "third-party"`, `"used_for": "Flag only (FLG-003). Not used as a fact."` — the exclusion works |
| `products.json` null fields | 36 blank cells, each carrying a flag reference — 0 blank fields without a flag |
| Rows without any source | 0 |

---

## Change requests (this session will not edit files owned by other sessions)

| ID | To | Request |
|---|---|---|
| 03-CR-1 | `data/products.json` / root generator owner | Keep `price` / `rating` / `review_count` out of **rendered tables**. Either leave them `null` (as `main` does today) or populate from a live Creators API response with the PF-27 date/time stamp adjacent. Basis: 03-F-04. |
| 03-CR-2 | `scripts/build_site.py` owner | Add a build-time rule: any cell containing `$` or a star rating must cite a Creators-API/Amazon-served source *and* carry `observed <date>`; otherwise fail the build. `tools/verify_site.py` V4 proves links but not the *route* the price came from — that is the gap 03-F-04 exploits. |
| 03-CR-3 | `data/sources.json` owner | Deduplicate by URL (`S02`/`S30`, `S16`/`S32`, and the four new ones in PR #26): reuse the existing id or add `same_page_as`. |
| 03-CR-4 | `index.html` owner | The landing page states "The nine-character tokens are short-link IDs, not ASINs" with no citation beside it; add the [Amazon ASIN definition](https://sell.amazon.com/blog/what-is-an-asin) (10-character) to that sentence, as `products.html` does. |
| 03-CR-5 | integration session | One nav slot for `sessions/03bbd050/index.html` ("Independent audit"), next to the existing "Full audit" link, so this re-verification is reachable from the landing page. |
| 03-CR-6 | `sessions/3c886b62/**` owner | Add the exact sentence *"As an Amazon Associate I earn from qualifying purchases."* to the banner of all 16 pages (they currently carry a "being prepared for the program" note), or remove the price cells from the 11 that show them. Basis: 03-F-02. |
| 03-CR-7 | `docs/**` owner (`79f85104`) | Change "**we** earn" to "**I** earn" to match the Operating Agreement wording, or state on the page why the plural is used for this entity. Basis: 03-F-03, `D-F-01`. |
| 03-CR-8 | `sessions/3c886b62/**` owner | Namespace that register's ids (`S1` → `3c6-S1`) so they cannot be confused with root `S01…`. Basis: 03-F-10. |
| 03-CR-9 | `tools/link_report.py` owner | Drop the stale "rate card is behind Associates sign-in" line for per-category commission; Table 1 is public and cited. Basis: 03-F-09, Part C gap 5. |


---

## Status at merge time — re-run on the merged tree (`161dfff` + this session's files)

The tree moved under this audit: sessions `a53a7e52` (PR #31) and `252122ff` (PR #39) merged while I was writing.
Everything above was therefore re-checked; the numbers here — not the ones raised at 10:2x UTC — are the current truth.

| Flag | Status now | Re-check I ran |
|---|---|---|
| 03-F-02 | **Resolved** | `grep -c 'As an Amazon Associate I earn from qualifying purchases' sessions/3c886b62/*.html` → ≥1 on every page (was 0 on 15 of 16). Program-content pages missing the sentence: **0 of 21**. Fixed by commit `97bde69` — "T-INT4: disclosure fixes + row-level provenance on inherited pages; archive link repair". |
| 03-F-03 | **Resolved** | `docs/index.html` and `docs/products.html` now read "**I** earn from qualifying purchases." — the plural variant is gone. |
| 03-F-11 (archive links) | **Resolved** | broken internal links, tree-wide: **0** (was 15 across 5 archive pages). |
| 03-F-11 (sitemap, `<h1>`) | **Partly** | sitemap now lists 35 URLs (was 16); still unlisted: `dashboard/index.html`, `marketing/index.html`, `marketing/briefs.html`. 33 pages still have zero or multiple `<h1>` (17 archive, 13 sub-site, 3 root stubs incl. `404.html`). |
| 03-F-08 | **Worsened** | duplicate URLs under different ids: **10 groups** (was 2) — `S01`/`S49`, `S02`/`S30`/`S50`, `S07`/`S51`, `S11`/`S52`/`S55`, `S12`/`S53`, `S13`/`S54`, `S16`/`S32`, `S40`/`S46`, `S41`/`S47`, `S42`/`S48`. |
| 03-F-04 | **Live, mitigated, still open** | `data/products.json` keeps `price`/`rating`/`review_count` = `null` ✓, but `category/air-fryers.html` renders `USD 79.93 (observed 2026-11-14; list USD 99.99)`-style columns and `sources.html` quotes prices in status notes, cited to `S46–S48` = `https://www.amazon.com/s?k=<ASIN>` search pages. Dated, labelled, disclosed — still not the licensed route. |

### 03-F-13 · Medium · The register has holes exactly where the category page cites into it

`data/sources.json` holds 48 ids and **skips `S33`–`S39`**, yet `category/air-fryers.html` renders `S33`, `S34`, … as
citation labels. The inline `href` still works, so no reader hits a dead link — but the register cannot answer "what
does this row rest on?", which is the whole purpose of the id. Reproduce:

```
python3 -c "import json;i=[int(s['id'][1:]) for s in json.load(open('data/sources.json'))['sources']];\
print([n for n in range(1,max(i)+1) if n not in i])"   # -> [33, 34, 35, 36, 37, 38, 39]
```

Fix: fill the gaps or renumber, and make `tools/link_report.py` fail on a cited-but-unregistered id (it currently
reports "dangling source refs=none" because it only walks `data/products.json`).

### 03-F-14 · Medium · Two pages of one build disagree about the same product

For the identical three listings, `products.html` renders the price and rating cells **blank** ("unverified") while
`category/air-fryers.html` renders dated values from the side block `observed_2026_11_14`, and `flagged/index.html`
describes the sub-site's figures as "displays prices ($79.93, $149.99, $79.91)". A visitor cannot tell which page is
the site's position; against the brief's rule ("if a value can't be confirmed from an official source, leave it blank
and flag it"), one of the two is wrong by construction. This is a single generator-level decision, not a per-page edit
→ folded into 03-CR-1 and 03-CR-2.

### 03-F-14 addendum · the landing page's own sentence is now contradicted by a page of the same build

Live at https://kanlerxz87-cyber.github.io/Zone3/ (read 2026-11-14 after the deploy of `6fbd7bb`), the landing
headline asserts:

> Static price offers and unverified analytics are not published.

and the KPI strip says **0 of 3 — Prices verified**. Both are true of `data/products.json` (`price: null`) and of
`products.html` / `pricing.html` / `reviews.html`. They are **not** true of `category/air-fryers.html`, which renders a
"Price (observed 2026-11-14)" and a "Rating (observed)" column for all three listings, nor of `sources.html`, whose
status notes quote `USD 79.93 (deal; List: USD 99.99)` and friends.

Requested of the page owner (03-CR-1/03-CR-4 family), pick one and make the generator enforce it:

- **(a)** keep the rule — move the observed figures out of rendered columns into the dated research record, or render
  them only where the sentence also says they are not offers and cites the display clause (PF-04) next to them; or
- **(b)** accept dated observations — then soften the landing sentence to something the tree can support, e.g.
  "no price is presented as current; dated observations are labelled as observations", and update the KPI label from
  "Prices verified" to "Prices published as current".

Either way the fix is one generator rule applied to every page, not a per-page edit — the failure mode this session
keeps finding on this repo is *correct wording in one place, contradicting data in another*, which is what
03-CR-2 proposes to make un-buildable.
