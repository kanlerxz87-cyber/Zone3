# Session `757efebc` — independent live verification log (2026-11-16)

Branch `arena/757efebc-zone3`, based on `main` @ `933e2f3`.

**Method.** Every row below was produced by a fetch performed *by this session, today*, of the
official page named in the Source column. Nothing is taken from a search result, a blog, an
aggregator, or from another session's record. Where this session did **not** re-read a clause,
the row says so and is marked accordingly — it is never silently carried over.

The three submitted tokens are written as plain text and are **not hyperlinked**: this repo's own
release gate (`tools/verify_site.py`, check V6) treats `link.amazon` as a prohibited link
shortener in emitted output, and the Program Policies bar link-shortening that obscures an Amazon
destination (§6(w), verified below).

---

## Part 1 — Product links (re-verified 2026-11-16)

| # | Claim | Observed today | Source |
|---|---|---|---|
| V01 | `link.amazon/B04G1MEwY` opens a live listing | Final URL `https://www.amazon.com/dp/B0CDY277D3`; served title "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black". Breadcrumb: Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | [S14](https://www.amazon.com/dp/B0CDY277D3) |
| V02 | `link.amazon/B02NbDxp3` opens a live listing | Final URL `https://www.amazon.com/dp/B09B7SB46R`; served title "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included". Same breadcrumb | [S15](https://www.amazon.com/dp/B09B7SB46R) |
| V03 | `link.amazon/B00hJ57DV` opens a live listing | Final URL `https://www.amazon.com/dp/B08DKYBTPH`; served title "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel". Same breadcrumb | [S16](https://www.amazon.com/dp/B08DKYBTPH) |
| V04 | All three listings sit in the **Air Fryers** browse node | The breadcrumb on each of the three pages ends at "Air Fryers", browse node `17659096011`, inside Small Appliances › Fryers. This is the *browse* path, not a commission category | [S14](https://www.amazon.com/dp/B0CDY277D3) · [S43](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) |

**Not claimed.** The Best Sellers page at node `17659096011` was **not** fetched by this session.
Its contents (ranking positions, which products hold them) are therefore unverified and are
deliberately left blank everywhere in this session's output. No trend, rank, price, rating or
review-count figure appears anywhere in this session's pages.

## Part 2 — Associates programme rules (re-read verbatim 2026-11-16)

| # | Clause | Wording read today | Source |
|---|---|---|---|
| V05 | Operating Agreement §5 | "You must clearly and prominently state the following … on your Site or any other location where Amazon may authorize your display or other use of Program Content: 'As an Amazon Associate I earn from qualifying purchases.'" — followed by "You will not misrepresent or embellish our relationship with you (including by expressing or implying that we support, sponsor, or endorse you)" | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |
| V06 | Participation Requirements §2(a) | "Special Links must use the Associates ID we have assigned to you." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V07 | Participation Requirements §2(b) — tag | "you must include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V08 | Participation Requirements §2(b) — **original content** | "When linking to pages with Product lists you must have additional original content on your Site that is relevant to the Special Link. Product lists include search results, events (e.g. Prime Day), or a department homepage (e.g. grocery)." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V09 | Participation Requirements §2(b) — claims | "You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product, an Amazon Site, or any of our policies, promotions, or prices." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V10 | Participation Requirements §2(b) — prices | "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V11 | Participation Requirements §2(b) — promotions | "You must remove from your Site any links and related references to limited time promotions as soon as that promotion on the relevant Amazon Site ends." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V12 | Commission Income Statement §2(g) | Purchases are disqualified where "not correctly tracked or reported because the links from your site to the relevant Amazon Site are not properly formatted" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V13 | Commission Income Statement §2(e) | A "Redirecting Link" (sending users indirectly to an Amazon Site via an intermediate site with no affirmative click) disqualifies the purchase | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V14 | Commission Income Statement §2(c)–(d) | Prohibited Paid Search Placement: no bidding on "amazon"/"kindle" or any Amazon Mark. Links *generated or displayed on a search engine* disqualify | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V15 | Participation Requirements §6(f) — **paid search is allowed to your own site** | "You may purchase paid search advertisements and submit links to Search Engines to appear in response to a general Internet search query or keyword (i.e., in natural, free, organic, or unpaid search results), so long as you comply with the Agreement and those paid or unpaid search results send users to your site and not directly, or indirectly via a Redirecting Link, to an Amazon Site." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V16 | Participation Requirements §6(t) | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V17 | Participation Requirements §6(w) | "You will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V18 | Participation Requirements §6(y) | "Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality." | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V19 | Participation Requirements §6(z) | "You will not display on your Site … any Program Content to advertise or promote any products that are offered on any site that is not an Amazon Site" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| V20 | Participation Requirements §1(g) | No Amazon trademark "in any domain name, subdomain name, in any 'tag' or Associates ID, or in any username, group name, or other identifier on any social networking site" | [S02](https://affiliate-program.amazon.com/help/operating/policies) |

## Part 3 — Commission rates (re-read 2026-11-16)

| # | Claim | Observed today | Source |
|---|---|---|---|
| V21 | Standard Commission Income Statement, Table 1, is public | Row "Physical Books, Kitchen, Automotive — 4.50%"; row "All Other Categories — 4.00%"; bounty rows $12.00 / $2.00 / $5.00 / $0.25 read as printed | [S25](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |

**Not claimed.** Table 1 lists *product categories*. Nothing on that page states which category a
given ASIN is settled in, and no per-product rate was read. The browse path observed in V04 is not
a commission category. A per-product commission rate is therefore left blank and flagged.

## Part 4 — Identifier rule (re-read 2026-11-16)

| # | Claim | Observed today | Source |
|---|---|---|---|
| V22 | Creators API `GetItems` identifies items by ASIN | `itemIdType` — "Type of item identifier used to look up an item", default value `ASIN`, usage `{"itemIdType":"ASIN"}`; `itemIds` examples `"B0199980K4"`, `"B000HZD168"` (10 characters each) | [S31](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) |
| V23 | A Creators API call requires a partner tag | `partnerTag` — "Unique Id for a partner" — is listed **Required: Yes**; usage `{"partnerTag":"xyz-20"}` | [S06](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) |

## Part 5 — What this session did **not** re-read

These are carried in the repo's own register from earlier sessions. This session did not re-fetch
them and marks them so, rather than implying they were confirmed today:

* PA-API 5 deprecation status ([S05](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation)).
* Creators API prerequisite "at least 10 qualifying sales within the past 30 days" ([S04](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)).
* Account dormancy — 180 days to refer a sale ([S28](https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG)).
* FTC disclosure guidance ([S07](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers), [S24](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews), [S44](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)).

## Part 6 — Repository-state observations (read from this checkout, 2026-11-16)

| # | Observation | Where |
|---|---|---|
| V24 | The top-level nav contains two entries named after agent sessions: "Verification (3ead7ac8)" and "Verification (25513d33)" | [`scripts/build_site.py`, `NAV`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/scripts/build_site.py) |
| V25 | The landing page's headline statistics are "3 Product links submitted / 0 of 3 … 0 of 3 Prices verified / 3 Critical flags open / 78 Total flags open" | [`index.html`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/index.html) |
| V26 | Nav labels are internal document names ("Pricing & commission", "Content & compliance", "Campaigns & tracking"), not reader destinations | [`scripts/build_site.py`, `NAV`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/scripts/build_site.py) |
| V27 | Two independent site generations are merged into one nav (root flat pages and the 16-page `/dashboard/` audit build) | [`README.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/README.md) |
| V28 | The default accent colour is `#1f5eff` (a default UI blue) and body type is `system-ui` | [`assets/style.css`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/assets/style.css) |

## Irregularities raised by this session

| ID | Item | Severity | Disposition |
|---|---|---|---|
| 757-F-01 | Amazon listing titles drift. The three titles read today match the ASINs and destinations recorded by earlier sessions; wording differences of this kind are normal Amazon listing edits, not a destination change | Info | Recorded. No flag raised against the site's data |
| 757-F-02 | PR [#71](https://github.com/kanlerxz87-cyber/Zone3/pull/71) (`arena/71dc8fea-zone3`) is still **open** but its head branch no longer exists on the remote, and GitHub reports `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`. Last updated 2026-11-14T19:07:15Z | Medium | Logged on the board and published on Flagged for review. Not actioned: it is another session's PR |
| 757-F-03 | The three submitted tokens are 9 characters. Amazon's Creators API documents ASINs as 10 characters (V22) and this session did not resolve the tokens as ASINs. Whether the three listings the short links open are the products the requester *intended* is not established by any official source | High | Carried forward from earlier sessions, re-confirmed today. Published for review; no intent is inferred |
| 757-F-04 | No Associates tag exists in the repository. Under §2(a), §2(b) and §2(g) (V06, V07, V12) every monetisable link needs one; without it no published link can accrue commission | High | Blocks the conversion workstream. Published for review |
