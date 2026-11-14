# Verification record — session `03bbd050`, 2026-11-14

**Method.** Every row below is a fetch performed by this session on 2026-11-14 (~10:10–10:35 UTC) using the
agent's page fetcher. A search-engine snippet was never accepted as evidence; where the fetcher failed, the
item is recorded as *not verified by this session* rather than carried forward as verified. No value in this
file was inferred, extrapolated, or filled in.

**Scope of the claim.** These checks cover the three submitted links, the commission/policy sources that the
site's conclusions rest on, and the GitHub Pages state. They do **not** re-verify the whole policy corpus.

---

## A. The three submitted links

| # | Submitted | Length | `amazon.com/dp/<code>` | Resolves to | Page title as served | Buy box observed 2026-11-14 | Source |
|---|---|---|---|---|---|---|---|
| 1 | `link.amazon/B04G1MEwY` | 9 chars | Page Not Found | `dp/B0CDY277D3` (token `btn_ref=srctok-1f979f303a4b5691`) | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | **$79.93** ("Buy New", "$39.97 per count"), In Stock, Ships from / Sold by Amazon.com | [link](https://link.amazon/B04G1MEwY) · [dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) · [dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) |
| 2 | `link.amazon/B02NbDxp3` | 9 chars | not re-fetched (see §D) | `dp/B09B7SB46R` (token `btn_ref=srctok-0cd8be3c7e2e0de3`) | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen" | **$149.99**, In Stock, FREE delivery Thu Nov 19, Ships from / Sold by Amazon.com | [link](https://link.amazon/B02NbDxp3) |
| 3 | `link.amazon/B00hJ57DV` | 9 chars | not re-fetched (see §D) | `dp/B08DKYBTPH` (token `btn_ref=srctok-7c59360cbbbd59b7`, `&th=1`) | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen" | **$79.91**, In Stock, Ships from / Sold by Amazon.com | [link](https://link.amazon/B00hJ57DV) |

Cross-checks and what they do **not** prove:

1. All three codes are 9 characters. Amazon's own definition: "ASIN stands for Amazon Standard Identification
   Number. It's a unique **10-character** alphanumeric code assigned to every product listed in the Amazon
   store" — <https://sell.amazon.com/blog/what-is-an-asin>. So none of the three codes **is** an ASIN.
2. `https://www.amazon.com/dp/B04G1MEwY` returned Amazon's Page Not Found page (logo, "Sorry! We couldn't
   find that page.", dogs-of-Amazon image), i.e. no listing exists under the submitted identifier.
3. The redirect **is** stable in its *target* (same three ASINs every fetch since 2026-11-13) but **not** in
   its URL: the `btn_ref=srctok-…` value differed on every fetch (three distinct tokens observed across four
   fetches), and fetch 3 additionally gained `&th=1`. A citation that pins a tokenised URL cannot be
   re-opened and matched — cite `https://www.amazon.com/dp/<resolved-ASIN>` instead.
4. Resolving a short link to a listing does **not** establish that this listing is the product the owner meant
   to submit. Nothing official states the owner's intent, so `confirmed_as_submitted_product` stays `false`
   and `asin` / `product_name` / `brand` / `commission_rate` stay blank on the product rows. That is the
   brief's rule: unconfirmed ⇒ blank + flagged, never inferred.
5. Category is read from the live breadcrumb on `dp/B0CDY277D3`: **Home & Kitchen › Kitchen & Dining › Small
   Appliances › Fryers › Air Fryers (node 17659096011)**. A browse node is not a rate-card category, so it
   does not license a commission number (see B).

## B. Commission and disclosure rules

| # | Claim the site makes | What I read 2026-11-14 | Source |
|---|---|---|---|
| B1 | Table 1 rates are public, no sign-in | Table rendered without login; "Luxury Beauty, Luxury Stores Beauty, Amazon Explore — 10.00 %"; "**Physical Books, Kitchen, Automotive — 4.50 %**"; "Toys, Furniture, Home, Home Improvement, Lawn & Garden, … — 3.00 %"; "All Other Categories — 4.00 %"; "Gift Cards; Wireless Service Plans; Alcoholic Beverages; … — 0.00 %" | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| B2 | Kitchen 4.50 % is a *category reference*, not a per-product rate | Table 1 lists categories, never ASINs; nothing maps node 17659096011 to "Kitchen" vs "Home". The two candidate rows differ by 1.5 points, so picking one is a guess. | same as B1 |
| B3 | Disclosure sentence is fixed by the Operating Agreement | Page header "**Updated:** October 15, 2025". §1: links "must properly use the special **tagged** link formats we provide … ("Special Links")". §2: on violation Amazon "reserve[s] the right to permanently … cease payment of … any and all commission income … without notice". (§5's exact sentence: not re-read today — fetcher failure; see §D.) | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) |
| B4 | FTC requires the disclosure to be unavoidable | "Disclose when you have any financial, employment, personal, or family relationship with a brand"; "Place it so it's **hard to miss**"; "Disclosures are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE"; "Don't mix your disclosure into a group of hashtags or links"; "You can't talk about your experience with a product you haven't tried". Brochure dated **November 2019**. | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| B5 | A price in a table cell is licence-gated | Repo's own cited clause (from `data/policy_facts.json` PF-04/PF-44, source S02): a Site "may only show prices and availability if (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…". PF-27 adds a date/time stamp when content is refreshed less often than hourly; PF-34 forbids price tracking/alerting. | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |

## C. Repository state

| # | Check | Result |
|---|---|---|
| C1 | Pages / tracked files | 110 HTML pages, 243 tracked files at `58d2744` |
| C2 | `python3 scripts/build_site.py` → `git status` | rebuild idempotent (no diff) ⇒ earlier generator-drift finding stays fixed |
| C3 | `python3 scripts/check_site.py` | `OK: 10 pages, 3 products, 38 sources, 39 flags. All checks passed.` |
| C4 | `python3 tools/verify_site.py` | VERIFY PASS (see page for counts) |
| C5 | `python3 tools/link_report.py --strict` | PASS; residual: prints "rate card is behind Associates sign-in" for per-category commission, but Table 1 is public (B1) |
| C6 | `python3 sessions/3c886b62/tools/check_links.py` | OK |
| C7 | Conflict markers in tracked files | 0 |
| C8 | Secrets pattern scan (AWS key, private key, `ghp_`, Slack token) | 0 hits |
| C9 | Broken internal links outside `archive/` | 0 of 110 pages |
| C10 | Broken internal links inside `archive/` | 15 links in 5 pages (preserved snapshots; D-F-02 still open) |
| C11 | `marketing/` (added by session `588693c9`, PR #34) | 7 pages, 0 broken links, disclosure on every page, **no** hard-coded prices — clean |
| C12 | Pages that render a `$` table cell *and* name one of the three listings | 17; see `findings.md` 03-F-09 |

## D. Not verified by this session (fetcher upstream errors, 2026-11-14 10:2x–10:35 UTC)

Recorded as open rather than borrowed. Each was read by another session on 2026-11-14 and is linked so the
owner can re-check manually:

| Item | Official URL | Last read by |
|---|---|---|
| OA §5 exact disclosure sentence | <https://affiliate-program.amazon.com/help/operating/agreement> | `dff4acde`, `588693c9` |
| Program Policies body (PF-04 / PF-27 / PF-34 / 6(t) / 6(w) / 6(y) / 6(z)) | <https://affiliate-program.amazon.com/help/operating/policies> | `9fef7647` (S30 note), `dff4acde` |
| Commission Schedule (per-account rate card) = sign-in gated | <https://affiliate-program.amazon.com/help/operating/schedule> | `dff4acde` |
| Creators API prerequisites; PA-API 5 deprecation; GetItems ASIN definition | <https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction>, <https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation>, <https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items> | `dff4acde` |
| `dp/B02NbDxp3`, `dp/B00hJ57DV` direct lookups (404 class) | <https://www.amazon.com/dp/B02NbDxp3>, <https://www.amazon.com/dp/B00hJ57DV> | `f1b7da46`, `dff4acde` |
| Rating / review-count values for all three listings | <https://www.amazon.com/dp/B0CDY277D3> etc. | `3c886b62`, `9fef7647` |
