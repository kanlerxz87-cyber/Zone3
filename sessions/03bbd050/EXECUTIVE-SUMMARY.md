# Executive summary — independent verification pass (session `03bbd050`, 2026-11-14)

**Repo:** [`kanlerxz87-cyber/Zone3`](https://github.com/kanlerxz87-cyber/Zone3) ·
**Live site:** <https://kanlerxz87-cyber.github.io/Zone3/> · **Audited at:** `main@58d2744` ·
**This pass:** [`sessions/03bbd050/index.html`](https://kanlerxz87-cyber.github.io/Zone3/sessions/03bbd050/index.html)
· full record: [`verification.md`](verification.md), [`findings.md`](findings.md),
[`audit/audit-report.json`](audit/audit-report.json)

> Written by a session that ran an **independent** re-check rather than a build: no file outside
> `sessions/03bbd050/` was edited, and every other session's work was preserved. Read this as the quality-control
> report on the site, not as a replacement for
> [`EXECUTIVE-SUMMARY.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/EXECUTIVE-SUMMARY.md).

---

## 1. Bottom line in five sentences

1. The three submitted links are **9-character hop codes, not ASINs** (Amazon defines an ASIN as a
   **10-character** code — [Sell on Amazon](https://sell.amazon.com/blog/what-is-an-asin)), and
   `amazon.com/dp/B04G1MEwY` returns **Page Not Found** (re-tested 2026-11-14).
2. Each hop nonetheless opens a **real, live listing**, stably, on all four fetches since 2026-11-13:
   [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) CHEFMAN 6 Qt dual-basket,
   [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) Emeril Lagasse 26QT,
   [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) Chefman 8 Qt TurboFry — all three air fryers under
   Home & Kitchen › … › Air Fryers (node 17659096011).
3. A resolved hop is **not** proof of the owner's intent, so identity, price, rating, BSR and commission stay
   **blank and flagged** on the product rows — and that is the correct call under the brief's "never infer" rule.
4. The **data layer audits clean**: 1,073 table rows, 801 carrying an official-source link, **0 rows with no
   source**, **0 blank fields with no flag**, **0 broken links outside `archive/`**, no secrets, no conflict
   markers, and all four project gates green (`check_site`, `verify_site`, `link_report --strict`, sub-site
   checker) — and `scripts/build_site.py` now rebuilds with **zero diff**.
5. The real exposure is not the data, it is **two older published sub-sites**: 10 pages under
   `/sessions/3c886b62/` display hard-coded prices while **15 of that directory's 16 pages carry no Associates
   disclosure sentence**, and `/docs/` shows prices behind a plural **"we earn"** variant — 15 live pages in total
   pair a price with a missing or non-conforming disclosure.

## 2. What is verified, and by whom

| Layer | State | How I confirmed it today |
|---|---|---|
| Link intake (3 rows) | Verified as *hop → listing*; identity blank | re-fetched all three [links](https://link.amazon/B04G1MEwY) + all three `/dp/` checks |
| Commission rule (category only) | Table 1 public: Kitchen 4.50 %, Home 3.00 %, All Other 4.00 %, Luxury Beauty 10.00 % | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| Per-listing commission | **blank** — a browse node is not a rate-card category, and the account's own card is [behind sign-in](https://affiliate-program.amazon.com/help/operating/schedule) | confirmed both pages |
| Disclosure rule | "As an Amazon Associate I earn from qualifying purchases." (OA §5); page header still "Updated: October 15, 2025" | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) |
| FTC placement rule | "hard to miss", placed with the endorsement, not in a hashtag pile, not on a separate page | [Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| Price-display route | only Amazon-served links or Creators/PA API data; API needs 10 sales/30 days; PA-API 5 deprecated | repo's captured clause (S02) + [Creators API](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| Site build | 65 pages, 1,073 rows, all gates green, idempotent rebuild | ran all four checkers + my own [audit script](audit/audit.py) |
| Publishing | Pages legacy build from `main` `/` | [Pages API](https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages/builds/latest) |

## 3. Decisions the owner has to make (nothing here can be automated away)

| # | Decision | Why it is yours |
|---|---|---|
| 1 | **Confirm the three products.** Reply with the ten-character ASINs (or full `…/dp/<ASIN>` URLs). Every product-level field — price, rating, review count, category, commission, BSR — is one API call away once identity is certain. | No official page states what a hop code was meant to point at. |
| 2 | **Read your own rate card** in Associates Central and record the category each listing earns at. Public Table 1 gives 4.50 % (Kitchen) or 3.00 % (Home) and nothing maps the node. | It is account-specific and sign-in gated. |
| 3 | **Configure a Associates tag** and build Special Links from it. Until then no page on this site can earn, and the `link.amazon/<code>` hop must stay a display link, not a monetisation link ([Policies](https://affiliate-program.amazon.com/help/operating/policies), Redirecting Link). | Requires your account. |
| 4 | **Rule on the two sub-sites** (fix disclosure vs remove prices) — change requests 03-CR-6/7. | They belong to other sessions' scopes; I flagged rather than overwrote. |
| 5 | **Decide whether dated price snapshots stay out of rendered tables** (03-CR-1). My recommendation: yes, out — the licence route is closed and the number decays. | It is a revenue/account-risk tradeoff. |

## 4. What the platform does and does not claim

**Built and checked:** product intake with a format gate; verification register (`data/sources.json`, 38 sources,
official hosts only, one third-party URL explicitly labelled "not used as a fact"); policy-fact register
(`data/policy_facts.json`, quotes keyed to clauses); pricing/commission/review/competition tables that render
**blank where unverifiable**; a campaign ledger that is **empty by design** until real click data exists; 7 SEO
pages under `marketing/` (buying guide, comparison, three product articles) carrying disclosure with **no prices
and no ratings**; disclosure + Amazon content disclaimer on every generated page; and four CI-style checkers that
fail the build on an unsourced row or a prohibited construct.

**Not claimed:** no earnings figure, no commission rate per product, no review claims, no automated posting, no
link cloaking, no price-tracking, and no stored Program Content images — each of those is either gated by Amazon
(Participation Requirements 6(t), 6(v), 6(w), 6(y); IP-licence data-mining bar) or requires your account.

## 5. Flag register from this pass (all non-blocking, all with sources)

| ID | Sev | One-line finding |
|---|---|---|
| 03-F-02 | High | 10 live price pages in `/sessions/3c886b62/`; 15 of 16 pages there lack the §5 sentence |
| 03-F-03 | High | `/docs/` uses "we earn" instead of "I earn" and shows prices on 6 of 8 pages |
| 03-F-04 | Med | Captured prices are not a permitted display route; API route unavailable (10 sales/30 days; PA-API 5 deprecated) |
| 03-F-05 | Med | Tokenised `final_url` citations are unreproducible (3 different `srctok` values in 4 fetches) |
| 03-F-06 | Med | Category ⇒ rate stays unresolved (4.50 % vs 3.00 %); blank is correct |
| 03-F-07 | Med | Hop link ≠ monetisation link; Redirecting-Link risk; no tag configured |
| 03-F-08 | Low | 2 source URLs registered twice (`S02`/`S30`, `S16`/`S32`) |
| 03-F-09 | Low | `tools/link_report.py` still claims the rate card is sign-in-only |
| 03-F-10 | Low | Two registers collide on ID names (`S1…` vs `S01…`) |
| 03-F-11 | Low | sitemap covers 16 of 29 nav-reachable pages; `404.html` has no `<h1>` |
| 03-F-12 | Info | Clean negatives: no secrets, no markers, no unsourced rows, `marketing/` compliant |
| 03-F-01 | Info | Process: four sessions reused `E-`/`F-` ID prefixes on the shared board |

**Method note.** Nothing in this summary is inferred. Where I could not re-read a source today (the page fetcher
threw upstream errors on five official URLs), it is recorded in `verification.md` §D as *not verified by this
session* instead of being copied forward as though it were.
