# Executive summary — Zone3 Amazon affiliate platform

**Prepared:** 2026-11-14 · **Site:** https://kanlerxz87-cyber.github.io/Zone3/ · **Branch:** `arena/b8beb448-zone3`
**Verification pass:** independent re-check of every load-bearing claim against the official source that backs it.
Record: `COORDINATION.md` § *Part: session b8beb448*, table A1–A15.

---

## 1. The bottom line in four sentences

1. **None of the three submitted links can be confirmed as a product listing.** The codes in them
   (`B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV`) are 9 characters; Amazon defines an ASIN as a
   **10-character** identifier ([Creators API, GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter),
   [Sell on Amazon](https://sell.amazon.com/blog/what-is-an-asin)), and `https://www.amazon.com/dp/<code>`
   returns Amazon's *Page Not Found* for all three — re-tested 2026-11-14, reproduced exactly.
2. **Each short link does open a real Amazon listing — but three different, unrelated ones**:
   `B0CDY277D3` (CHEFMAN 6 Qt dual-basket air fryer), `B09B7SB46R` (Emeril Lagasse 26QT French-door
   air fryer oven), `B08DKYBTPH` (Chefman TurboFry 8 Qt). That mapping was identical on 2026-11-13 and
   2026-11-14, so it is deterministic, not random. It is still **not** evidence that these are the products
   you meant to submit: three arbitrary codes returning three different coherent products is what a
   generic fallback looks like. Without the original submission context this cannot be settled, so the
   product names, prices, ratings and commission figures are **left blank**, not guessed.
3. **The platform is built and published; the data pipeline is deliberately idle.** The site, the generator,
   the checker, the source register, the content and compliance framework and the campaign ledger all
   exist and pass their checks. What is missing is the *input*: a valid ASIN, an Associates tag, and API
   eligibility. Those are three specific items at the end of this document.
4. **Two things the earlier version of this site said were wrong, and are now corrected** rather than
   quietly dropped — the commission rate card is *not* sign-in-only, and the policy case against
   `link.amazon` is narrower than it was stated. Both corrections are published on the
   [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page as V-F1 and V-F2.

---

## 2. What is verified (and where)

| Fact | Status | Official source re-read 2026-11-14 |
|---|---|---|
| ASIN is a 10-character alphanumeric identifier | Verified, quoted verbatim | [Creators API GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) |
| All three submitted codes are 9 characters; all three `/dp/` pages 404 | Verified, reproduced | [/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) · [/dp/B02NbDxp3](https://www.amazon.com/dp/B02NbDxp3) · [/dp/B00hJ57DV](https://www.amazon.com/dp/B00hJ57DV) |
| Short links resolve to three different real listings | Observed, deterministic across two days | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) · [B02NbDxp3](https://link.amazon/B02NbDxp3) · [B00hJ57DV](https://link.amazon/B00hJ57DV) |
| Required disclosure wording, and it must be clear and prominent | Verified, quoted verbatim | [Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement) (header: Updated October 15, 2025) |
| Prices and star ratings may be shown **only** if Amazon serves them or they come via Creators API/PA API | Verified, quoted verbatim | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) — Participation Requirements 2(b) and 6(t) |
| Purchases through a "Redirecting Link" are disqualified | Verified, quoted verbatim | same, Commission Income Statement §2(e) |
| No price tracking or price-alerting functionality on the site | Verified, quoted verbatim | same, 6(y) |
| No artificial clicks, impressions or sessions | Verified, quoted verbatim | same, 6(s) |
| Program Content may not be used to train or improve ML/LLM models; API data may not be aggregated or analysed without **prior written approval** | Verified, quoted verbatim | same, IP License §1 and §2(e) |
| AI agents must identify themselves as `Agent/[name]` and may not solve CAPTCHAs or mimic humans | Verified, quoted verbatim | same, Agent Terms §4 |
| PA-API 5 is deprecated; calls return HTTP 403 `AccessDeniedException` | Verified | [PA-API 5 deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) |
| Creators API prerequisite: ≥10 qualifying sales in the past 30 days | Verified, quoted verbatim | [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| Standard commission Table 1 (Luxury Beauty 10.00 %, Physical Books/Kitchen/Automotive 4.50 %, Home 3.00 %, All Other Categories 4.00 %, …) | Verified, full table, **no sign-in required** | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| Onsite commission Table A | Verified | [Onsite Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) |
| FTC Endorsement Guides were revised in 2023; disclosure must be hard to miss and placed with the endorsement | Verified | [FTC topic hub](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews) · [Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| Associates approval needs ≥3 qualifying sales in the first 180 days; account dormant after 180 days without a sale | Verified | Associates help topics (S27–S29 in `data/sources.json`) |
| Payment ≈60 days after month end; US minimums: deposit $10, gift card $10–$2,000, cheque $100 with a $15 fee | Verified | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), Payment Minimum Chart |

`data/sources.json` holds **31** sources; each row on the site links the official page it came from.

---

## 3. What is deliberately blank, and why that is the correct answer

The brief says: *if a value can't be confirmed from an official source, leave it blank and flag it as
unverified, and never infer or fill in values.* Three consequences follow, and all three are policy
requirements, not preferences:

| Blank field | Why it cannot be filled |
|---|---|
| Product name, brand, model, capacity, price, rating, review count, best-seller rank (3 products × 12 fields) | The identifiers do not resolve, so no product record exists to read. Substituting the redirect target would be an inference — exactly what the brief forbids. |
| Star ratings and review text | 6(t): those may be displayed **only** when obtained through Creators API or PA API. Copying them off a rendered page would breach the policy even if the number were read correctly. |
| Live prices and availability | 2(b): same rule. Amazon must serve the price in the link, or it must come from the API. |
| Per-product commission rate and commission income | Table 1 gives the *category* rate, but the listing's category is unverified (FLG-021) and the account-specific rate card route is sign-in gated. |
| Clicks, orders, conversion rate, revenue | Amazon is the system of record and reports only inside a logged-in account. No campaign is live and no tag has been supplied. |
| "Trending" and "high-converting" scores | No official Amazon endpoint for affiliates exposes trend or conversion data. Any number would be invented. |

---

## 4. What the platform does today

| Capability the brief asked for | State |
|---|---|
| Product research and intake with an automated gate | **Built.** Intake refuses any item whose identifier is not a 10-character ASIN or whose `/dp/` page does not serve a product. All three submitted items are refused, with the evidence recorded. |
| Trending / high-converting product identification | **Blocked** on official data; no legitimate source exists for the scores, and the API that might approximate demand needs 10 qualifying sales first. |
| Price, review and competition analysis | **Blocked.** Rules that constrain this are recorded and enforced; the data is withheld for the policy reasons in §3. |
| Commission potential modelling | **Partly built.** Verified public rate tables plus the working rules (24-hour session, 89-day cart, 180-day ship/pay, disqualified-purchase list) are published; the per-product rate input is missing. |
| SEO-optimised articles, comparisons, buying guides | **Templates and a claim-grounding contract are built; the prose is not written**, because every product claim must be sourced and the FTC expects first-hand experience that has not happened. Writing it from a redirect title would be fabricated review content. |
| Publish and manage affiliate links | **Link pipeline built, publishing intentionally off.** No Associates tag has been supplied, so no link on the site is a trackable Special Link. |
| Track clicks and conversions | **Ledger schema built, empty by design** — no tag, no campaign, no reports. |
| Continuous optimisation | **Optimiser boundary defined; no data to optimise.** Rebuilding the site from verified data is a single command. |
| Compliance with Associates policy and FTC disclosure | **Built and enforced at build time.** The generator refuses to emit a page without the §5 disclosure; 25 prohibitions are encoded; the checker fails the build on an unsourced table row. |
| Automation and scalability | **Built.** Static generation from JSON, no runtime dependency, no secrets in the repo, deterministic rebuild. |

---

## 5. Three items that unblock everything

1. **A valid ASIN for each product** — the 10-character identifier from the address bar of the real product
   page, or the product page URL itself. Everything in the "blank" column of §3 depends on this.
2. **Your Associates tag** (the `xxxxx-20` parameter, *not* a password or API secret), plus confirmation that
   the account is active. Without it no link on the site can earn.
3. **Enrolment status and API access.** The Creators API needs ≥10 qualifying sales in 30 days; until then,
   price and rating display is impossible under 2(b)/6(t) regardless of how it is scraped or stored.

Until item 1 arrives, the honest answer to "which product is this and is it worth promoting" is *unknown*,
and the site says so instead of filling the gap.

---

## 6. Irregularities published for your review

Full detail, each with its source link, on the live **Flagged for review** page: 26 entries —
2 critical, 5 high, 10 medium, 7 low, and 2 informational. The ones worth your attention first:

| ID | Sev | What it means for you |
|---|---|---|
| FLG-001 | Critical | The three codes are not ASINs and their product pages do not exist. Anything built on them would be fiction. |
| FLG-003 | Critical | `link.amazon` is Amazon-served but undocumented in the policies; a shortener that obscures the destination, or a link that redirects without an affirmative click, is exactly what 6(w)/6(v)/CIS 2(e) prohibit. Publish canonical `/dp/` URLs instead. |
| FLG-010 | High | No Associates tag in any supplied link → nothing is trackable yet. |
| FLG-015 | High | Operating Agreement Schedule 1 lists the **United States / amazon.com only**, so a non-US operator's eligibility for the US programme is not established by the text read (the Oslo location is recorded on the Flagged page from an earlier session's observation, not from an official document). |
| FLG-016 | High | Automated *analysis* of Amazon product data needs Amazon's prior written approval. This constrains the "AI-powered analysis" part of the brief directly — it is a permission problem, not a technical one. |
| V-F1 | Info | **Correction:** the commission tables are public. The earlier "rates are unavailable" statement was wrong. |
| V-F2 | Info | **Correction:** no policy names `link.amazon`; FLG-003's claim was narrowed to the clauses that actually apply. |
| V-F3 / V-F4 / V-F5 | Low | `/docs/` is live but unreachable by browsing; `sitemap.xml` covers only one of the four page sets. Owner decision, not a defect. |

---

## 7. How to check this yourself

```bash
python3 scripts/build_site.py     # regenerate the flat site from data/*.json
python3 scripts/check_site.py     # 9 pages, 3 products, 31 sources, 25 flags — must print OK
python3 tools/build_site.py       # regenerate the 16-page audit build from data/z3/*.json
python3 tools/verify_site.py      # 57 pages, 899 table rows — must print VERIFY PASS
for a in B04G1MEwY B02NbDxp3 B00hJ57DV; do printf "%s = %s chars\n" "$a" "${#a}"; done
# expect: 9 chars each, and a 404 from each of these:
#   https://www.amazon.com/dp/B04G1MEwY   https://www.amazon.com/dp/B02NbDxp3   https://www.amazon.com/dp/B00hJ57DV
```

Any figure in this document that you cannot reproduce from those sources should be treated as an error and
reported — that is the standard the site is held to.
