# Executive summary — Zone3 AI-powered Amazon affiliate platform

**Prepared:** 2026-11-14 · **Originally integrated:** session `edbd56a1` · **Independent correction pass:** session `043344f8` · **Final integration, compliance fix and re-verification:** session `3ead7ac8` · **Editorial topic plan and content-status correction:** session `3d359c23`
**Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Verification log:** https://kanlerxz87-cyber.github.io/Zone3/verification.html
**Flagged for review:** https://kanlerxz87-cyber.github.io/Zone3/flagged.html

> The source-linked findings below include the original 2026-11-14 verification record, the
> independent correction pass and the 2026-11-14 final integration pass. Redirect targets are treated as
> observed destinations, not as proof of requester intent. Unavailable or policy-restricted values remain
> blank and flagged.

---

## 1. The bottom line

**The three submitted short links were observed to open real Amazon listings; the requester's intended product match remains unconfirmed.** Each submitted token is **9 characters**, not a 10-character ASIN, and `https://www.amazon.com/dp/<token>` returns Amazon's *Page Not Found* page for the raw token — reproduced again on 2026-11-14:

| Submitted link | Code (length) | `amazon.com/dp/<code>` | Where the short link actually lands | Source |
|---|---|---|---|---|
| https://link.amazon/B04G1MEwY | `B04G1MEwY` (9) | Page Not Found | `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Qt dual-basket air fryer | [S08](https://www.amazon.com/dp/B04G1MEwY) · [S11](https://link.amazon/B04G1MEwY) · [S14](https://www.amazon.com/dp/B0CDY277D3) |
| https://link.amazon/B02NbDxp3 | `B02NbDxp3` (9) | Page Not Found | `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French-door air fryer oven | [S09](https://www.amazon.com/dp/B02NbDxp3) · [S12](https://link.amazon/B02NbDxp3) · [S15](https://www.amazon.com/dp/B09B7SB46R) |
| https://link.amazon/B00hJ57DV | `B00hJ57DV` (9) | Page Not Found | `amazon.com/dp/B08DKYBTPH` — Chefman TurboFry 8 Qt air fryer | [S10](https://www.amazon.com/dp/B00hJ57DV) · [S13](https://link.amazon/B00hJ57DV) · [S23](https://www.amazon.com/dp/B08DKYBTPH) |

Two official Amazon sources define the identifier as 10 characters: the
[Creators API `GetItems` reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter)
("*10-Character alphanumeric unique identifier assigned by Amazon*") and Amazon's own
[selling blog](https://sell.amazon.com/blog/what-is-an-asin) ("*a unique 10-character alphanumeric
code assigned to every product listed in the Amazon store*", article dated Jun 4 2025).

**The short links have three observed destinations, but the redirect alone does not establish whether
they match the requester's intent.** Each target listing's title, ASIN and category breadcrumb are
documented with Amazon links. The dashboard does not infer that `plpRedirect=mhFallback` indicates a
failed lookup; a direct valid-ASIN control also carried that parameter. Price, review, availability,
rank, commission and performance values remain blank unless obtained through an approved, current data
path — see §3 and FLG-022/027.

**The platform itself is built, published and passing its current checks.** The unresolved operating
inputs are an Associates tag, eligible API access, and confirmation only if the observed destination
listings are not the intended products. These conditions are listed in §5.

---

## 2. What is verified, and where it is published

51 official sources · 55 policy facts · 72 flags · 13 root pages, a 16-page audit build, a `/docs/`
reference set, a marketing section and three retained session sub-sites. Every fact and all three
submitted links were re-read from the official pages on 2026-11-14; the row-by-row records are the
[Verification log](https://kanlerxz87-cyber.github.io/Zone3/verification.html),
[session 3ead7ac8's record](https://kanlerxz87-cyber.github.io/Zone3/sessions/3ead7ac8/),
which re-reads 30 load-bearing claims and links each one to the page it came from, and
[session 3d359c23's record](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-verification-log.md),
which re-reads 26 load-bearing claims a third time and records what was and was not re-read.

| Area | What the official documents say | Source |
|---|---|---|
| Required disclosure | "As an Amazon Associate I earn from qualifying purchases." — Operating Agreement §5; breach of §5 "will be deemed a material breach" | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |
| Prices and availability | may be shown only if Amazon serves the link, or the data comes via Creators API / PA API — Participation Requirements 2(b) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Star ratings and reviews | may be shown only if obtained through Creators API / PA API — 6(t) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Link shorteners | must not be used "in a manner that makes it unclear that you are linking to an Amazon Site" — 6(w) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Cloaking / redirects | no cloaking or obscuring the URL "including by use of Redirecting Links" — 6(v); purchases via a Redirecting Link are disqualified — CIS 2(e) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Price tracking | "your Site must not have price tracking and/or price alerting functionality" — 6(y) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Artificial traffic | "You will not artificially generate clicks or impressions" — 6(s) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Commission window | a Session ends at the first of: 24 hours elapse, a non-digital order, or another Special Link click; cart converts within **89 days**; shipped and paid within **180 days** — CIS §1 | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Payment | "approximately 60 days following the end of each calendar month"; US minimums: direct deposit $10, gift card $10–$2,000, cheque $100 with a $15 fee — CIS §6 | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Standard commission rates | Table 1, readable without a sign-in: Luxury Beauty 10.00 % · Physical Books / **Kitchen** / Automotive 4.50 % · Toys / Home / Pets 3.00 % · All Other Categories 4.00 % | [S25](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| Onsite commission rates | Table A: **Kitchen** 1.25 % (applies to Onsite Content used by Amazon inside the Amazon site, not to links on your site) | [S26](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) |
| Data access | Creators API — four operations (SearchItems, GetItems, GetVariations, GetBrowseNodes); prerequisite "at least 10 qualifying sales within the past 30 days" | [S04](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| PA-API 5 | "has been deprecated and is being replaced by the Creators API"; calls return HTTP 403 `AccessDeniedException` | [S05](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) |
| AI / analysis permission | Program Content may not be used to "develop or improve large language or multimodal models, machine learning models or related technology"; API data may not be "aggregat[ed], analyz[ed], extract[ed], or repurpos[ed]" without express prior written approval — IP License §1, §2(e) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Agents | must send `Agent/[agent name]` in the user-agent string and must not solve CAPTCHAs or mimic humans — Agent Terms §4(c) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Enrolment | "we require at least three within the first 180 days"; "personal orders do not qualify"; ~10 posts as a rule of thumb | [S29](https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM) |
| Dormancy | "you have 180 days to refer a sale through one of your Associates links"; the application can be withdrawn after 180 days without qualifying sales | [S28](https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG) |
| FTC disclosure | Endorsement Guides "revised in 2023"; disclose "clearly and conspicuously"; "The closer the disclosure is to your recommendation, the better"; "affiliate link" alone, or a "buy now" button, is **not** adequate | [S44](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) · [S24](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews) |
| Territory | Operating Agreement Schedule 1 lists **United States / amazon.com** only | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |

---

## 3. What is deliberately blank, and why that is the correct answer

Your instruction is: *if a value can't be confirmed from an official source, leave it blank and flag
it as unverified; never infer or fill in values.* Three of those blanks are also Amazon policy, so
filling them would breach the programme:

| Blank field | Why it cannot be filled |
|---|---|
| 9 product-attribute fields for each of 3 observed destination listings (27 cells total) | Dynamic commercial/review/availability/variation/commission/trend/competition values have no approved current source in this build. Destination title, target ASIN and category breadcrumb are separately documented; whether they match requester intent remains open. |
| Star ratings and review text | 6(t) — displayable only when obtained through Creators API or PA API. Copying them off a rendered page breaches the policy even if the number is read correctly. |
| Live prices and availability | 2(b) — same rule. Amazon must serve the price in the link, or it must come from the API. |
| Per-product commission rate and commission income | Public category tables are cited. No product-specific category-to-rate assignment or account context is published in the product row; see FLG-013. |
| Clicks, orders, conversion rate, revenue | Amazon is the system of record and reports only inside a logged-in account. No tag, no campaign. |
| "Trending" and "high-converting" scores | No official Amazon endpoint for affiliates exposes trend or conversion data. Any number would be invented. |

The current `/dashboard/` and `/marketing/` builds withhold prices, star ratings and review counts. A
legacy category/reference page still contains dated price/rating snapshots; those are not compliant live
product offers and remain flagged for removal or approved re-sourcing under FLG-028. Do not use them as
current marketing claims.

---

## 4. What the platform does today

| Capability in the brief | State |
|---|---|
| Product research and intake with an automated gate | **Built.** The 9-character submitted tokens are not ASINs, but the short links were observed to land on three live listings with target ASINs. The observed targets are recorded separately; whether they match the requester's intent remains unconfirmed. |
| Trending / high-converting product identification | **Blocked** on official data — no legitimate source for those scores. |
| Price, review and competition analysis | **Rules built and enforced; data withheld** under 2(b) / 6(t) (FLG-022). A six-position bestseller benchmark is published with rank, ASIN, title and link only. |
| Commission potential modelling | **Partly built.** The public rate tables plus the verified working rules (24 h session, 89-day cart, 180-day ship/pay, disqualified-purchase list, payment timing) are published; the per-product rate input is missing. |
| SEO articles, comparisons, buying guides | **Briefs, a comparison and a buying guide are published, and the editorial plan for the long-form articles is published too.** The plan ([Content topics](https://kanlerxz87-cyber.github.io/Zone3/content-topics.html)) lists 12 working titles, the Amazon fact each one is built on and the rule that governs what it may not state. Every product claim must be accurate (PF-10), and the first-hand experience the FTC describes (PF-21) has not happened. |
| Publish and manage affiliate links | **Link pipeline built; publishing intentionally off.** No Associates tag, so nothing is a trackable Special Link (FLG-010). |
| Track clicks and conversions | **Ledger schema built, empty by design** (FLG-011). |
| Continuous optimisation | **Boundary defined; no data to optimise.** Rebuilding from verified data is one command. |
| Associates and FTC compliance | **Built and enforced at build time.** The generator refuses to emit a page without the §5 disclosure; the checker fails the build on an unsourced table row. |
| Automation and scalability | **Built.** Static generation from JSON, no runtime dependency, no secrets in the repo, deterministic rebuild (verified to a stable fixpoint). |

**Site structure:** the landing dashboard links to Products, Pricing & commission, Reviews & competition,
Content & compliance, Content topics, Campaigns & tracking, Category: Air Fryers, Marketing, the Executive
summary, Verification log, Flagged for review and Sources. The 16-page `/dashboard/` build supplies the full
research and governance tables. Every current generated data row carries an official source, a flag or an
explicitly documented blank. The legacy snapshot exposure is flagged separately (FLG-028).

---

## 5. Three items that unblock everything

1. **Confirm the observed destinations only if they are not the intended products.** The live target
   ASINs are already recorded in the product table; no replacement input is needed if those are intended.
2. **Your Associates tag** (the `xxxxx-20` parameter — not a password or API secret), plus
   confirmation that the account is active. Without it no link on the site can earn.
3. **Enrolment status and API access.** Creators API needs ≥10 qualifying sales in 30 days; until
   then price and rating display is impossible under 2(b)/6(t), however the data is obtained.

Until item 1 arrives, the honest answer to "which product is this and is it worth promoting" is
*unknown*, and the site says so rather than filling the gap.

---

## 6. Irregularities published for your review

72 entries on the [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page —
3 critical, 13 high, 20 medium, 21 low, 15 informational (informational entries record a correction
made to this site, not a defect in a product). None of them blocks the merge; each carries its
evidence source links and the action needed.

**Read these first:**

| ID | Severity | What it means for you |
|---|---|---|
| [FLG-001](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-001) | Critical | The 9-character tokens are not ASINs, but their short links were observed to open live listings. The destination listings are documented; whether they match intent remains open. |
| [FLG-003](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-003) | Critical | `link.amazon` is Amazon-served but not documented in the policies. Whether its redirect counts as a Redirecting Link (disqualified under CIS 2(e)) has to be tested in a logged-in Associates account. Publish canonical `/dp/ASIN` URLs with your tag instead. |
| [FLG-010](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-010) | High | No Associates tag in any supplied link → nothing is trackable yet. |
| [FLG-015](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-015) | High | Schedule 1 lists the **United States / amazon.com** only. A non-US operator's eligibility for the US programme is not established by the text read. |
| [FLG-016](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-016) | High | Automated *analysis* of Amazon product data needs Amazon's prior written approval. This constrains the "AI-powered analysis" part of the brief directly — it is a permission problem, not a technical one. |
| [FLG-022](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-022) | High | Prices, ratings and review counts cannot be displayed without an approved data path, so they are blank by policy, not by omission. |
| [FLG-027](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-027) | High | Submitted tokens and observed redirect destinations are recorded separately; observed destinations do not prove requester intent. The fallback query parameter is not treated as failure evidence. |

**Corrections and fixes made in this session** (also on the Flagged page as `E-F-01`…`E-F-07`, so the
changes are auditable rather than silent):

| ID | What changed |
|---|---|
| E-F-01 | The dashboard claimed a second official source for the 10-character ASIN rule without listing it. The row now cites that page (registered as S45) and the quote is stored as PF-52. |
| E-F-02 | The root executive summary was stale — it still carried another session's branch header and repeated a claim that session had already recorded as overstated. Rewritten. |
| E-F-03 | *(not raised — already fixed on `main` before this session merged)* `tools/link_report.py` had printed "rate card is behind Associates sign-in", which V-F1 had already shown to be false. |
| E-F-04 | `/docs/` was live but had no inbound link from any dashboard (V-F3), and `sitemap.xml` covered only part of the site (V-F4). Both fixed: a nav entry was added, and `scripts/build_sitemap.py` now produces the sitemap from the checked-in tree so it covers all 63 live pages. |
| E-F-05 | The dashboard headline says product identities are "documented", which reads against FLG-002/FLG-027. **Left for your decision** — the data layer is correct, so this is editorial. |
| E-F-06 | One source note says the competition benchmark carries ratings and prices; the published benchmark shows only rank, ASIN, title and link (correctly). **Left for your decision.** |
| E-F-07 | PR #26 (another session) overlapped this session's scope, touching 23 shared root files. It was not merged, closed or edited here; it landed on `main` first and this branch was rebased onto it. |
| 3D-F-01 | The **Content & compliance** page said *"No article, comparison or buying guide has been written yet"* and its table marked all three products "Not written" — while seven marketing pages were live and nav-linked. Corrected: the table now shows what is published, and the editorial plan for the rest is published at `/content-topics.html`. |
| 3D-F-02 | Re-observed independently: the "Customers who viewed" carousel on a destination page shows a price and a star rating that belong to a **different ASIN**. The published data was never affected (no price or rating is shown anywhere); recorded so any future automated capture binds each value to the page's own ASIN. |
| 3D-F-03 | The dashboard had no tile for the new topic plan. Fixed — it is listed as a tile and in the site map. |

---

## 7. How this was verified

* All three submitted short links re-fetched on 2026-11-14; all three direct `/dp/<code>` checks
  re-run. Results identical to 2026-11-13.
* All 55 policy facts in `data/policy_facts.json` re-checked against their source page.
* Commission tables (S25, S26), the Creators API pages (S04–S06), the FTC pages (S07, S24, S44), the
  enrolment pages (S28, S29) and the Amazon bestseller page (S43) re-read; the Operating Agreement
  and Program Policies were read section by section across all 4 and 11 chunks respectively.
* Build gates, all green: `scripts/check_site.py` (13 pages, 3 products, 51 sources, 72 flags),
  `tools/verify_site.py` (71 pages, 1,269 rows, 1,068 with an official source link, 405 flagged, 82
  anchored to the repo), `tools/link_report.py` (no dangling refs), `scripts/check_all_links.py`
  (117 pages, 105 external URLs, 0 errors), `scripts/build_sitemap.py` (66 pages covered), and both
  site generators rebuild to a stable fixpoint.
* **Limits:** the sandbox reaches only github.com, npm and PyPI directly, so official pages were read
  through a fetch tool rather than an automated HTTP client, and the `--online` link check was not
  run. Whether `link.amazon` redirects without an affirmative click has not been tested in a
  logged-in Associates account (FLG-003).

---

## 8. Final integration pass — session `3ead7ac8` (2026-11-14)

**A live compliance defect was found and fixed.** Two page sets were publishing observed prices
(USD 79.93 / 149.99 / 79.91), star ratings (4.2 / 4.3 / 4.4 out of 5) and review counts
(4.8K / 18.3K / 16.8K) as product facts. Associates Program **Participation Requirements 2(b)** and
**6(t)**, re-read verbatim that day, allow those displays only where Amazon serves the link or the
data comes from Creators API / PA API — neither is true for this project, which has no Associates tag
and no API credentials.

| Page set | Action |
|---|---|
| `category/air-fryers.html` | Columns removed and replaced with a 2(b)/6(t) explanation carrying the S46–S48 and S02 links. Session `554c08ca` (PR #66) found the same file independently and raised `I-F-01`; **their fix is the one kept**, and `3E-F-01` cross-references it |
| `/docs/` (six pages) | 81 cells withheld, replaced with the `Withheld` badge plus FLG-022 / FLG-023 links |
| `sessions/3c886b62/**` and `sessions/03bbd050/` | Dated compliance notice added to 12 pages; their data cells were **not** rewritten, because those files belong to other sessions. Change request `3E-CR-01` is logged in `COORDINATION.md` |
| `category/air-fryers.html`, *Niche assessment* | Amazon's "bought in past month" badges (`1K+`, `4K+`, `3K+`) were published in prose on a page that withholds prices for exactly that reason. Withheld, and raised as `3E-F-10` |

**One stale claim was corrected.** `/docs/` and the category page said the commission rate schedule is
sign-in-only. It is not: the Standard Commission Income Statement
[Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) and the Onsite
[Table A](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) both render
publicly — Table 1 was re-read row for row (Kitchen 4.50%, All Other Categories 4.00%). Only the
per-account `/help/operating/schedule` card is gated. Rate cells stay blank because what is
unresolvable is each listing's **category** (FLG-021), not the rate card.

**Two register errors were repaired.**
[`PF-53`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/data/policy_facts.json) reinstates the
compensated-review clause whose withdrawal note ("its text was not found in any section read") was
wrong — the wording is in the Operating Agreement's opening paragraph.
[`PF-55`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/data/policy_facts.json) completes
`PF-23`, which stopped mid-sentence and omitted *"or in the direct training or fine-tuning of a
machine learning and/or foundational model"* — the clause that matters most for an AI-driven platform.

**Verification.** 13 official pages fetched and read; 30 load-bearing claims re-checked. **All
matched.** No third-party page was used as evidence. Gates on the merged tree:
`check_site` OK (12 pages / 3 products / 51 sources / 66 flags) · `verify_site` PASS (70 pages /
1,223 rows / 1,022 with an official source link / 0 advisories) · `link_report --strict` exit 0 ·
`check_all_links` 116 pages, 0 errors · all five generators idempotent.

**Merged and deployed.** [PR #70](https://github.com/kanlerxz87-cyber/Zone3/pull/70) → merge commit
`f79b85e`; follow-up [PR #72](https://github.com/kanlerxz87-cyber/Zone3/pull/72) → merge commit
`f618a53`, both merged without waiting for approval. The Pages build for `f618a53` reports
**`built`** and the corrected pages were confirmed on the live site.

**Limits carried forward.** The sandbox reaches only github.com, npm and PyPI directly, so official
pages were read through a fetch tool rather than an automated HTTP client. Program Policies chunk 10
of 11 was not read. Whether `link.amazon` redirects without an affirmative click has not been tested
in a logged-in Associates account (FLG-003).

---

## 9. Final integration pass — session `3d359c23` (2026-11-14)
**Merge note.** While this branch was open, `main` merged session `f2102efa's` three additional
flags (`F2-F-01`…`F2-F-03`), so the flag register now holds **72** entries: this session's three
(`3D-F-01`…`3D-F-03`) and `f2102efa's` three are both published, and the generated pages were
rebuilt from the merged register. `main` also carried a stray `>>>>>>>` conflict-marker line in
`COORDINATION.md` (line 3554, committed by that session and left unbalanced); this integration
removed the marker line and kept every word of the board. The resolution is scripted in
`scripts/resolve_rebase.py` so it is repeatable and auditable rather than a one-off manual edit.


**One published statement contradicted the site's own output, and it is fixed.** The *Content &
compliance* page said *"No article, comparison or buying guide has been written yet"*, and its
status table marked all three products **"Not written"** — while seven marketing pages were live
and linked from the navigation: three product briefs, a comparison, a buying guide and one page per
product. The flag register carried the same stale claim as **FLG-012**. Both are corrected in this
pass; FLG-012's earlier wording is kept in the register so the change stays auditable, and the
correction is published as **3D-F-01**.

**The brief's "catchy trendy articles and topics" is now a published plan.** The site had briefs, a
comparison and a buying guide but nothing that planned the articles themselves. The new
[Content topics](https://kanlerxz87-cyber.github.io/Zone3/content-topics.html) page carries **12
working titles**, each with:

* the verified Amazon fact it is built on (read from the listing title or from Amazon's own
  programme documents) and the official source of that fact;
* the page that already publishes those facts;
* the rule that governs what it **may not state**, with the clause — for example, no price, no
  discount and no best-seller position for a specific product (Participation Requirements 2(b) and
  6(t)), and no comparison with a non-Amazon retailer's product (6(z));
* its status: **Ready to draft** (6 topics) or **Blocked: identity unconfirmed** (6 topics, because
  FLG-002/FLG-035 are still open).

**No topic is described as trending, popular or high-converting**, because no official Amazon
endpoint publishes search volume, keyword difficulty, trend direction or conversion rate to
affiliates (FLG-033). The one official popularity surface — the category Best Sellers page — is used
in a single topic and is labelled point-in-time, because the positions move between captures
(FLG-025). A "Topics deliberately not planned" table states the four things that are *not* being
claimed and why.

**A second observation was recorded.** Re-fetching the destination page for product 1 showed the
"Customers who viewed this item also viewed" carousel rendering a 4.4-star, 392-review, $69.97
entry whose own link points at a **different** ASIN (`dp/B0B7C327LK`), while the link it renders
under is the destination ASIN (`dp/B0CDY277D3`). The published data was never affected — no price,
rating or review count appears anywhere on the site (FLG-022, FLG-029) — but any future automated
capture must bind each value to the page's own ASIN. Recorded as **3D-F-02**; the missing dashboard
tile is **3D-F-03**.

**Verification.** 13 official pages fetched and read live by this session (the three short links,
the three destination pages, one Page-Not-Found control, the Operating Agreement, the Program
Policies, Table 1, the Creators API reference and the FTC guide). Every load-bearing claim matched
the page it cites; nothing was found false and nothing was filled in. The record is
[`research/3d359c23-verification-log.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-verification-log.md);
the line-by-line repository review is
[`research/3d359c23-repo-review.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-repo-review.md).
Gates on the merged tree: `check_site` OK (13 pages / 3 products / 51 sources / 72 flags) ·
`verify_site` PASS (71 pages / 1,269 rows / 1,068 with an official source link / 0 advisories) ·
`link_report --strict` exit 0 · `check_all_links` 117 pages, 105 external URLs, 0 errors ·
`sessions/3c886b62` checker OK · sitemap covers 66 pages · all generators idempotent.

---

## 9. Independent re-verification and final integration — session `25513d33` (2026-11-14)

Session `25513d33` re-fetched and re-read every load-bearing claim from scratch, rather than
relying on an earlier session's record. **All three submitted links and all twelve policy and
disclosure statements matched.** Nothing load-bearing was found to be wrong.

| What was re-checked | Result |
|---|---|
| The three `link.amazon` short links | Re-fetched 2026-11-14. Unchanged: `B04G1MEwY`→`B0CDY277D3` (CHEFMAN 6 Qt dual basket), `B02NbDxp3`→`B09B7SB46R` (Emeril Lagasse 26QT), `B00hJ57DV`→`B08DKYBTPH` (Chefman 8 Qt TurboFry) |
| The raw 9-character codes used directly as ASINs | All three return Amazon's "Page Not Found" page. The positive control is that the same fetch returns a full product page for each destination ASIN |
| Participation Requirements 2(b), 6(t), 6(w), 6(s), 6(y) and the 2(b) tag rule | **Confirmed verbatim** against the official page (header still "Updated: April 14, 2026") |
| Commission windows (24 h session · 89-day cart · 180-day ship/pay), payment timing (~60 days), US Payment Minimum Chart | **Confirmed verbatim / row for row** |
| Standard Commission Table 1 and Onsite Table A | **Confirmed verbatim**: Kitchen 4.50% (Standard), Kitchen 1.25% (Onsite, Onsite Content only); All Other Categories 4.00% / 1.00% |
| FTC guidance on affiliate disclosures | **Confirmed verbatim**: "The closer the disclosure is to your recommendation, the better"; "'affiliate link' … would not be adequate"; Guides "revised in 2023" |

**This session independently reached the same conclusion as the site's existing rule.** Clauses 2(b)
and 6(t) permit a price or star rating on your own site only where Amazon served the link, or where
the data came through Creators API / PA API. This project has neither an Associates tag nor API
credentials, so the blank price, rating and review cells are not an omission — they are what the
policy requires.

**Two repository-integrity findings, both informational:**

* **C3-F-01 was a false positive.** An earlier session reported that `sitemap.xml` omitted five pages.
  It does not: those five are meta-refresh redirect stubs the sitemap generator excludes on purpose,
  and `index.html` is present as the site root URL. `scripts/build_sitemap.py --check` exits 0 with
  every live page covered and 0 missing. Recorded as **25-F-02**; no file change was needed.
* **A stale count, corrected in flight.** §6 of this summary said "51 entries — 3 critical, 12 high,
  16 medium, 15 low, 5 informational" and §7 said "48 sources, 51 flags" when this session read it.
  By the time this branch merged, another session had already refreshed both to the current figures
  (72 entries; 51 sources), and those are the numbers now in §6 and §7. Recorded as **25-F-03**.

**One new observation (25-F-01).** All three destination listings carry the same Amazon browse
breadcrumb — *Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers* (node
`17659096011`) — read from the pages Amazon served. The repository had recorded it for product 1 only.
No published cell changes: a browse node is a *category* fact, and a per-product commission rate still
cannot be tied to a rate without the account's own rate card.

**Full record:** [session 25513d33 verification page](https://kanlerxz87-cyber.github.io/Zone3/sessions/25513d33/)
— one row per claim, each linked to the official page it was read from.

**New page published.** `sessions/25513d33/index.html`, generated by
`sessions/25513d33/build_record.py`, which reads every source URL from `data/sources.json` at build
time so a label cannot drift from its link. It carries the §5 disclosure, is listed in the site
navigation and in `sitemap.xml`, and passes all gates with 0 advisories. A rebase-conflict resolver,
`sessions/25513d33/resolve_rebase.py`, was added alongside it: the board's own prose contains the
string `<<<<<<<`, so a substring marker test false-positives and can let a conflicted file be
published — the resolver's test is line-anchored.

## 10. Implementation pass — session `5a56c084` (2026-11-16)

**What this pass is.** The polished-marketing implementation round. Session `4f83ee7b`
(2026-11-15) published ten design/marketing proposals (SUG-01…10), ten owner questions
(Q1…10) and six discovery actions (D1…6) — deliberately without implementing anything.
Session `5a56c084` recorded a decision per proposal (now rendered as the **Decision log**
on `suggestions.html`, sourced from `data/suggestions.json`) and implemented only the
unblocked subset. Blocked proposals stayed blocked; no owner question was answered by
inference.

**Independent re-verification (2026-11-16).** All eight load-bearing observations were
re-fetched live in this session and matched the register: the three submitted short links
still open the same three listings (`B04G1MEwY`→`B0CDY277D3`, `B02NbDxp3`→`B09B7SB46R`,
`B00hJ57DV`→`B08DKYBTPH`); the three direct `/dp/<token>` checks still return Amazon's
"Page Not Found" page; the Operating Agreement (header October 15, 2025) carries the §5
disclosure wording verbatim; the Program Policies (header April 14, 2026) carry the
session definition verbatim. Two listing-title wording drifts were recorded as Info items
(precedent 4f83-F-01); no new flag was raised. Record:
`sessions/5a56c084/verification-2026-11-16.json`, rendered at `/sessions/5a56c084/`.

**What shipped.**

* **Design system** — the generic dashboard styling is replaced by an editorial
  "research desk" look across every generated page: warm paper ground, evergreen
  primary, copper accents, serif display headings; no external fonts, images or scripts.
* **Disclosure placement** — the Associates statement is a strip under the header on
  every page (§5 "clearly and prominently"; FTC "hard to miss"), repeated beside product
  pointers in the articles, with the Amazon content disclaimer and trademark note in
  every footer.
* **Landing page** — now a front door: hero, honest research-status callout, proof
  stats computed from the registers, three listing cards (labelled source links only),
  Research Desk cards, the "In the kitchen now" point-in-time module (SUG-08), a trust
  section (SUG-06), a Decision Center banner, and a collapsed site map. Navigation is
  five primary links plus a grouped "More pages" menu; every previous destination is
  still reachable and gate-checked.
* **Research Desk** — `articles/index.html` plus four grounded articles (plan topics
  T-09, T-10, T-07, plus one new evergreen grounded in the Commission Income
  Statement). Every claim carries an inline source link; every article carries a
  verified / not-verified box, a how-this-was-written note, and its enforced editorial
  constraints; the review checklist is published on the hub (SUG-03's gate).
* **Decision log** — per-proposal accept/defer/hold records with evidence links
  (SUG-01 partial, SUG-02/03/06/07/08 implemented, SUG-04/09/10 deferred, SUG-05 still
  blocked pending the owner's Associates tag).

**One defect found and fixed in flight (5a56-F-01).** The shared page template's
subdirectory link prefixer added a single `../` regardless of nesting depth; the first
page nested two levels deep rendered links that resolved one level short. Fixed
(depth-aware prefix) in the same commit, before merge; all link gates pass.

**Gates at publication.** `check_site` OK (19 pages, 3 products, 51 sources, 78 flags) ·
`verify_site` PASS (80 pages, 1,369 rows, 0 advisories) · `link_report --strict` exit 0 ·
`build_sitemap --check` exit 0 (75 pages) · `check_all_links` 126 pages, 0 errors.

**Still blank, still correct.** Prices, ratings, review counts, per-product commission
rates, clicks and conversions remain blank: no Associates tag (Q1) and no approved
Amazon data path (Q4) are connected, and 2(b)/6(t) forbid displaying those values from
anywhere else. The fastest path to a revenue-capable site remains the three unblock
items in §5 — owner tag, intended ASINs, account/API status.
