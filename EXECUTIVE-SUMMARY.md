# Executive summary — Zone3 AI-powered Amazon affiliate platform

**Prepared:** 2026-11-14 · **Originally integrated:** session `edbd56a1` · **Independent correction pass:** session `043344f8`
**Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Verification log:** https://kanlerxz87-cyber.github.io/Zone3/verification.html
**Flagged for review:** https://kanlerxz87-cyber.github.io/Zone3/flagged.html

> The source-linked findings below include the original 2026-11-14 verification record and the
> independent correction pass in this session. Redirect targets are treated as observed destinations,
> not as proof of requester intent. Unavailable or policy-restricted values remain blank and flagged.

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

48 official sources · 51 policy facts · 51 flags · 12 root pages, a 16-page audit build and a
marketing section. All 51 facts and all three submitted links were re-read on 2026-11-14; the
row-by-row record is the [Verification log](https://kanlerxz87-cyber.github.io/Zone3/verification.html).

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
| SEO articles, comparisons, buying guides | **Structure, briefs, comparison and buying guide pages built; no unsourced product claims.** Every product claim must be accurate (PF-10), and the first-hand experience the FTC describes (PF-21) has not happened. |
| Publish and manage affiliate links | **Link pipeline built; publishing intentionally off.** No Associates tag, so nothing is a trackable Special Link (FLG-010). |
| Track clicks and conversions | **Ledger schema built, empty by design** (FLG-011). |
| Continuous optimisation | **Boundary defined; no data to optimise.** Rebuilding from verified data is one command. |
| Associates and FTC compliance | **Built and enforced at build time.** The generator refuses to emit a page without the §5 disclosure; the checker fails the build on an unsourced table row. |
| Automation and scalability | **Built.** Static generation from JSON, no runtime dependency, no secrets in the repo, deterministic rebuild (verified to a stable fixpoint). |

**Site structure:** the landing dashboard links to Products, Pricing & commission, Reviews & competition,
Content & compliance, Campaigns & tracking, Category: Air Fryers, Marketing, the Executive summary,
Verification log, Flagged for review and Sources. The 16-page `/dashboard/` build supplies the full
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

51 entries on the [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page —
3 critical, 12 high, 16 medium, 15 low, 5 informational (informational entries record a correction
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

---

## 7. How this was verified

* All three submitted short links re-fetched on 2026-11-14; all three direct `/dp/<code>` checks
  re-run. Results identical to 2026-11-13.
* All 51 policy facts in `data/policy_facts.json` re-checked against their source page.
* Commission tables (S25, S26), the Creators API pages (S04–S06), the FTC pages (S07, S24, S44), the
  enrolment pages (S28, S29) and the Amazon bestseller page (S43) re-read; the Operating Agreement
  and Program Policies were read section by section across all 4 and 11 chunks respectively.
* Build gates, all green: `scripts/check_site.py` (12 pages, 3 products, 48 sources, 51 flags),
  `tools/verify_site.py` (69 pages, 1,172 rows, 971 with an official source link, 347 flagged, the
  rest anchored to the repo), `tools/link_report.py` (no dangling refs), `scripts/build_sitemap.py`
  (63 pages covered), and both site generators rebuild to a stable fixpoint.
* **Limits:** the sandbox reaches only github.com, npm and PyPI directly, so official pages were read
  through a fetch tool rather than an automated HTTP client, and the `--online` link check was not
  run. Whether `link.amazon` redirects without an affirmative click has not been tested in a
  logged-in Associates account (FLG-003).
