# Independent verification log — session `252122ff` (2026-11-14)

**Scope (COORDINATION.md Part E, task E-T3).** Every value below was fetched live by this
session from the official page named in its row, between **10:05 and 10:17 UTC on 2026-11-14**.
Nothing in this log is inferred, filled in, or copied from another session's record: each
"confirmed" row means this session's own fetch of the official URL reproduced the stated value.
Rows that were not re-fetched are listed separately in §5 as **carried**, with their links, and
are not claimed as verified by this session. Method: direct HTTP fetch of the official URL
(redirect chain followed to its final URL; final URL and page title recorded from the response).

---

## 1. The three submitted links — redirect identity (all confirmed)

| # | Submitted link (as given) | Final URL observed 2026-11-14 | Page title observed | Matches prior records? |
|---|---|---|---|---|
| 1 | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) | `amazon.com/dp/B0CDY277D3` (with `lv=shuf&…&plpRedirect=mhFallback` params) | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | yes — same target and title as S11/S14 and session `9fef7647`'s PR #26 row |
| 2 | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) | `amazon.com/dp/B09B7SB46R` (same param family) | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen" | yes — same as S12/S15 and PR #26 |
| 3 | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) | `amazon.com/dp/B08DKYBTPH` (with `&th=1`, same param family) | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen" | yes — same as S13/S23 and PR #26 |

Category breadcrumb read on all three destination pages: **Home & Kitchen › Kitchen & Dining ›
Small Appliances › Fryers › Air Fryers** (node 17659096011).

This is the fifth independent observation round across sessions and the mapping is stable
(rounds: `7f84fea4`, `33226b37`, `c4e71983`, `f1b7da46`/`9fef7647`, now `252122ff`).
**Caution carried forward (FLG-002, FLG-022):** the mapping is *observed*, not documented —
Amazon short links can be re-pointed. Re-check before publishing any product row.

## 2. The raw 9-character codes are not ASINs (all confirmed "Page Not Found")

| Raw code | URL fetched | Result observed 2026-11-14 |
|---|---|---|
| `B04G1MEwY` | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) | "Page Not Found" |
| `B02NbDxp3` | [amazon.com/dp/B02NbDxp3](https://www.amazon.com/dp/B02NbDxp3) | "Page Not Found" |
| `B00hJ57DV` | [amazon.com/dp/B00hJ57DV](https://www.amazon.com/dp/B00hJ57DV) | "Page Not Found" |

Each code is 9 characters; the Creators API defines an ASIN as a **"10-Character alphanumeric
unique identifier assigned by Amazon"** (re-verified this session, §4, PF-18) and the three
redirect targets all use 10-character IDs. FLG-001 stands.

## 3. Dated offer snapshots (search results pages, read 2026-11-14)

Source pages are Amazon's own search results for each ASIN (same pages as register entries
S40–S42). Values are **dated observations, volatile**, shown here only for research. Displaying
prices/ratings on a live Associates site is restricted (PF-04, PF-05 — see §4); the site's
marketing copy states none.

| Listing | Page | Observed 2026-11-14 (~10:10 UTC) | PR #26 / S40–S42 claim (observed ~09:45–10:00 UTC) | Match |
|---|---|---|---|---|
| B0CDY277D3 (Chefman 6 Qt dual basket) | [amazon.com/s?k=B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) | $79.93 · List $99.99 · 4.2★ · (4.8K) | $79.93 (list $99.99) · 4.2★ · ~4.8K | **identical** |
| B09B7SB46R (Emeril Lagasse 26QT) | [amazon.com/s?k=B09B7SB46R](https://www.amazon.com/s?k=B09B7SB46R) | $149.99 · List $209.99 · 4.3★ · (18.3K) | $149.99 (list $209.99) · 4.3★ · ~18.3K | **identical** |
| B08DKYBTPH (Chefman 8 Qt TurboFry) | [amazon.com/s?k=B08DKYBTPH](https://www.amazon.com/s?k=B08DKYBTPH) | $79.91 · List $119.99 · 4.4★ · (16.8K) | $79.91 (list $119.99) · 4.4★ · ~16.8K | **identical** |

Also observed (not previously recorded): product 1's result showed "1K+ bought in past month",
product 2 "4K+ bought in past month" (badge "Early Black Friday Deal"), product 3 "3K+ bought in
past month" with a "Best Seller in Deep Fryers" badge. Demand badges are volatile and are **not**
added to any data file by this session (no need; not claimed anywhere).

## 4. Policy facts re-verified verbatim against live official pages (this session)

Each quote below was matched **word for word** in this session's fetch of the linked page.

| Fact | Source (official link) | Section | Re-verified text |
|---|---|---|---|
| PF-01 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | §5 | "You must clearly and prominently state the following, or any substantially similar statement previously allowed under this Agreement, on your Site … : 'As an Amazon Associate I earn from qualifying purchases.'" |
| PF-02 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | §6 | "any violation of Section 5 and as specified in the Program Policies will be deemed a material breach of this Agreement." |
| PF-35 | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Schedule 1 | "United States \| Amazon.com Services LLC \| amazon.com" |
| PF-04 / PF-44 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Participation Requirements §2(b) | "Product prices and availability may vary from time to time. … your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API …" |
| PF-05 | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Participation Requirements §6(t) | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API …" |
| (same page) | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | §6(s)(v)(w)(y)(z) | artificial-clicks ban, cloaking ban, shortener ban ("makes it unclear that you are linking to an Amazon Site"), price-tracking ban, non-Amazon-products ban — all present verbatim |
| (same page) | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | CIS §2(b), §2(e) | "any Product order where a cancellation, return, or refund has been initiated" disqualified; "Redirecting Link" definition verbatim |
| PF-18 / S31 | [Creators API GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) | ItemIdType Parameter | "ASIN \| Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." |
| PF-38 | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | Table 1 | "Physical Books, Kitchen, Automotive \| 4.50%" (full 11-row table read; 0.00%–10.00%; All Other Categories 4.00%) |
| PF-39 | [Onsite Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) | opening + Table A | "We will pay you commission income ('Onsite Commission Income') for Qualifying Purchases, which in the case of Onsite Commission Income is limited to Direct Qualifying Purchases." · Table A row "Digital Music, Physical Music, Handmade, Digital Videos, Health & Personal Care, Sports, Kitchen, Automotive \| 1.25%" |
| PF-40 | [Application Review Process](https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM) | body | "we require at least three within the first 180 days … personal orders do not qualify … a good rule of thumb is at least 10 posts" |
| PF-41 | [Account Dormancy](https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG) | body | "Once you've applied, you have 180 days to refer a sale through one of your Associates links." · "Your application can be withdrawn if there were not enough qualifying sales for 180 days after your application was submitted." |
| PF-19 | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | When to Disclose | "Disclose when you have any financial, employment, personal, or family relationship with a brand." |
| PF-20 | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | How to Disclose | "Place it so it's hard to miss." |
| PF-21 | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | What Else to Know | "You can't talk about your experience with a product you haven't tried." (page dated November 2019 — basis of FLG-017) |
| PF-50 | [FTC Endorsement Guides FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | "What About Affiliate or Network Marketing?" | "You should disclose your relationship to the retailer clearly and conspicuously on your site … The closer the disclosure is to your recommendation, the better." |
| PF-51 | [FTC Endorsement Guides FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) | same section | "Consumers might not understand that 'affiliate link' means that the person placing the link is getting paid for purchases made through the link. Similarly, a 'buy now' button would not be adequate." |

**Result: 0 contradictions found.** Every quote matched the live page.

## 5. Not re-fetched this session — carried from prior records (NOT claimed as verified here)

These entries remain as earlier sessions recorded them (chiefly `dff4acde` D-T4, 2026-11-14, and
`ecbfe91b`). Links are given for manual review:

- PF-16 — [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) (10 qualifying sales / 30 days).
- PF-17 — [PA-API 5 deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation).
- PF-36 — [Program Policies](https://affiliate-program.amazon.com/help/operating/policies), Influencer Program §3(c) ("#Ad"/"#Sponsored").
- PF-42, PF-43 — payment timing/minimums ([Program Policies](https://affiliate-program.amazon.com/help/operating/policies) CIS §6; [Associates home](https://affiliate-program.amazon.com/)).
- PF-45–PF-49 — as cited on the site's compliance pages (register entries in `data/policy_facts.json`, sources S02/S40–S45).
- S03 — [Commission Schedule](https://affiliate-program.amazon.com/help/operating/schedule) (login-gated; status "not-accessible" carried).
- S43 — [Best Sellers: Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) (dated rank capture).
- S45 — [Sell on Amazon: What is an ASIN](https://sell.amazon.com/blog/what-is-an-asin).
- S17 (third-party, excluded as evidence), S18 (not accessible), S20–S22 (repo/Pages metadata).

## 6. Marketing-content fact review (brief item: "build marketing for the products")

Marketing content for the three products is being built by session `9fef7647` (PR #26:
`marketing.html` — 3 SEO product briefs, a comparison, a buying guide; facts-only, no prices or
ratings stated, no first-hand claims, per-row source links). Per the coordination rules this
session did **not** duplicate that work. This session instead verified the factual basis of its
claims from the official listings:

| Marketing claim (PR #26) | This session's check | Verdict |
|---|---|---|
| P1: two independent 3-qt baskets, Sync Finish, easy-view windows, Hi-Fry, auto shutoff | product 1 listing title (fetched, §1) lists all five | confirmed as "as listed" |
| P2: 26-qt French-door air fryer toaster oven, 24 cooking functions, dual-speed fan, rotisserie | product 2 listing title (fetched, §1) lists all four | confirmed as "as listed" |
| P3: 8-qt XL nonstick dishwasher-safe basket, TurboFry 4-in-1, 450°F Hi-Fry, bake/dehydrate/frozen | product 3 listing title (fetched, §1) lists all of these | confirmed as "as listed" |
| Comparison: form factors, capacities, category path | titles + breadcrumb (fetched, §1) | confirmed |
| Buying guide statements ("only product 1 lists two independent baskets", etc.) | compared across the three fetched titles | confirmed |

Note (E-F-02): the brief's marketing requirement is met on `main` once PR #26 merges. A
claim-level re-read of the rendered page should be repeated after its in-flight source-ID remap
(see §7) so citations match the merged register.

## 7. Irregularities raised by this session (namespaced `E-F…`, non-blocking)

| ID | Severity | Finding | Evidence / action |
|---|---|---|---|
| E-F-01 | Info | Whole-tree link sweep (104 HTML pages, 2 435 relative refs) finds **15 broken relative links, all inside `archive/c4e71983/content/`** (pre-archive paths such as `data/products.json`, `categories/air-fryers.html`). Unreachable from navigation; archive is a preserved snapshot. Known as D-F-02; session `a53a7e52` (PR #31, open) claims an "archive link repair". No nav-reachable page is broken. | this session's sweep, 2026-11-14 |
| E-F-02 | Medium | **Source-ID collision incoming:** PR #26's latest commit (`d9aafec`, 10:12Z) remaps its sources to **S45–S53**, but `main` already uses **S45** for "Sell on Amazon: Understanding ASIN numbers" (added by session `ecbfe91b`, PR #32). PR #26's branch is based on `cfec2b3` (PRs #18–#25) and does not contain PRs #27–#32's register additions (S45, PF-44–PF-51). A straight merge will collide. **Request to the PR #26 owner (logged in COORDINATION.md Part E):** merge registers additively and remap to S46+ before landing. | this session's git inspection + `data/sources.json` on `main` |
| E-F-03 | Info | Root-page ID citations checked programmatically: every `Sxx`/`FLG-xxx`/`PF-xx` cited on the 10 root pages exists in the merged registers; the S30/S31 mis-citation described in FLG-027 is **no longer present** (all S30/S31 anchors now carry their register titles). "PF-14" hits on root pages are prose in FLG-014's withdrawal note, not fact citations. | this session's cross-ref script, 2026-11-14 |
| E-F-04 | Info | Data-layer cross-references clean: no dangling source or flag IDs in `data/*.json`; all three product rows keep unverifiable cells **blank + flagged** (FLG-001/002/004), per the brief. | this session's cross-ref script, 2026-11-14 |

## 8. What this session did not do (scope honesty)

- Did not edit any data file, page, or script (no rule violation was found that is not already
  flagged and owned; E-F-02 is a request to another session, logged, not silently rewritten).
- Did not merge or push to PR #26's or PR #31's branches — both sessions were active within
  minutes of this review (commits at 10:09Z and 10:12Z).
- Did not claim any price, rating, commission rate, or identity as a standing fact; every
  volatile value above is a dated observation.

---

## 9. Addendum (2026-11-14, after `main` moved to `ee7d1d1`)

- **E-F-02 resolved upstream:** session `b90c5685` (JH, PRs #37/#38) integrated the open PR #26
  branch into `main` with a full ID renumbering (`5cba3ca` — "renumber colliding S/FLG IDs, keep
  blank product cells, keep both marketing sections, fix two gate defects"). `main` now carries
  S44–S55 and FLG-031…038 additions; the S45 collision this log warned about was handled exactly
  as requested (registers merged additively). The source-ID request to `9fef7647` is therefore
  **moot for `main`** — it applies only if PR #26 itself were merged raw, which would now collide
  again and must not be done without the same renumbering.
- **JH-F-02 resolved by this session's §3:** JH reported the dollar prices/list prices/star
  ratings/review counts in PR #26's data as "not reproducible" from their control fetches of the
  `/dp/` product pages (where the star block does not render in text-mode fetches). This session
  fetched the **search-results pages PR #26 actually cited** (`amazon.com/s?k=<ASIN>`, register
  S40–S42) and reproduced every value identically ($79.93/List $99.99/4.2★/4.8K; $149.99/List
  $209.99/4.3★/18.3K; $79.91/List $119.99/4.4★/16.8K — §3). The values are genuine dated
  observations of Amazon's own pages; the discrepancy was a fetch-method artifact, not bad data.
- **Brief requirement "build marketing for the products" is now met on `main`:** `marketing/`
  (index, briefs with 3 product briefs + comparison + buying guide, per-product pages) is live in
  the navigation, facts-only with per-row source links. Verified as factually accurate against
  the fetched listing titles (§6).
- Whole-tree link sweep re-run on the integrated tree (113 pages, 2 690 relative refs): the only
  broken links remain the 15 inert `archive/c4e71983/content/` references (E-F-01; PR #31 repair
  still open). All navigation-reachable pages clean.
