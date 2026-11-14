# Verification log — session `3d359c23` (2026-11-14)

**Scope.** Every load-bearing claim the flat site publishes, re-read live by this session against the
official page it cites. Nothing here was taken from a search result, a blog, an aggregator or an
earlier session's record. Where a claim could **not** be re-read in this session it is listed as
*carried* with its link and is not upgraded to "verified by 3d359c23".

**Base commit:** `f618a53` (merge of PR #72) · **Branch:** `arena/3d359c23-zone3`
**Register IDs** are the canonical ones in `data/sources.json` and `data/flags.json`.

---

## 1. The three submitted links (read live, 2026-11-14)

| # | Submitted link | Result of the fetch | Register IDs |
|---|---|---|---|
| V01 | `https://link.amazon/B04G1MEwY` | Resolves to `https://www.amazon.com/dp/B0CDY277D3?…`. Page title: *"Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen"*. Breadcrumb: Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers. | S11, S14, S52 |
| V02 | `https://link.amazon/B02NbDxp3` | Resolves to `https://www.amazon.com/dp/B09B7SB46R?…`. Page title: *"Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen"*. Same breadcrumb. | S12, S15, S53 |
| V03 | `https://link.amazon/B00hJ57DV` | Resolves to `https://www.amazon.com/dp/B08DKYBTPH?…`. Page title: *"Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen"*. Same breadcrumb. | S13, S16, S23, S32, S54 |
| V04 | `https://www.amazon.com/dp/B04G1MEwY` | Amazon's **"Page Not Found"** page (title element `Page Not Found`, the "Dogs of Amazon" error page). | S08 |

**Conclusion.** The redirect mapping is unchanged from every earlier observation, and the three
submitted tokens are still 9 characters. `plpRedirect=mhFallback` appears on the resolved URL of a
valid product page, so it is not evidence of a failed lookup (FLG-026). Identity still rests on
observation only (FLG-002, FLG-027, FLG-035).

### V05 — an observation worth recording (3D-F-02)

On the `dp/B0CDY277D3` page the *Customers who viewed this item also viewed* carousel renders a
**4.4-star / 392-review / $69.97** entry whose own link points at `dp/B0B7C327LK` — a different
ASIN — while the link it renders under is the destination ASIN `dp/B0CDY277D3`. The same pattern
appeared on the other two destination pages. Any capture that reads price or rating text from a
product page without binding it to the page's own ASIN will attribute another product's numbers to
this one. FLG-029 already records the trap; this is an independent second observation of it.

---

## 2. Identifier rule

| # | Claim | Official page re-read | Result |
|---|---|---|---|
| V06 | An ASIN is a 10-character alphanumeric identifier | [Creators API — `GetItems`, ItemIdType parameter](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) (chunk 1) | **Confirmed verbatim**: "Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." |
| V07 | The three submitted codes are not ASINs | counted from the submitted strings | **Confirmed**: `B04G1MEwY` = 9, `B02NbDxp3` = 9, `B00hJ57DV` = 9. |

---

## 3. Operating Agreement and Program Policies (read live, 2026-11-14)

| # | Claim | Official page re-read | Result |
|---|---|---|---|
| V08 | Agreement header date | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (chunk 0) | **Confirmed**: "**Updated:** October 15, 2025". |
| V09 | §5 disclosure wording | same, chunk 1 | **Confirmed verbatim**: "You must clearly and prominently state the following, or any substantially similar statement previously allowed under this Agreement, on your Site or any other location where Amazon may authorize your display or other use of Program Content: “As an Amazon Associate I earn from qualifying purchases.”" |
| V10 | A §5 breach is a material breach | same, chunk 1 | **Confirmed verbatim**: "any violation of Section 5 and as specified in the Program Policies will be deemed a material breach of this Agreement." |
| V11 | Compliance failure can stop all commission | same, chunk 0 (§2) | **Confirmed**: Amazon reserves the right to "permanently … cease payment of (and you agree you will not be eligible to receive) any and all commission income". |
| V12 | 2(b) — tag in every link, no dynamic sub-tags, price display rule | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (chunk 3) | **Confirmed verbatim**: "you must include your Associates ID or “tag” (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link"; "you may not dynamically assign sub-tags to users as they arrive"; "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API". |
| V13 | 6(s), 6(t), 6(v), 6(w), 6(y), 6(z) | same, chunk 5 | **Confirmed verbatim**, one line each: 6(s) "You will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site"; 6(t) "You will not display or otherwise use any of our customer reviews or star ratings … unless you have obtained a link to that customer review or star rating through Creators API or PA API"; 6(v) no cloaking "including by use of Redirecting Links"; 6(w) "You will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site"; 6(y) "your Site must not have price tracking and/or price alerting functionality"; 6(z) no Program Content used to promote products offered on any site that is not an Amazon Site. |
| V14 | 6(a) — no altering Program Content | same, chunk 4 | **Confirmed**: "You will not add to, delete from, or otherwise alter any Program Content in any way". |
| V15 | IP License 2(e) — no analysis of API data without written approval | same, chunk 7 | **Confirmed verbatim**: "You will not, without our express prior written approval, access or use Creators API, PA API or Data Feeds for the purpose of aggregating, analyzing, extracting, or repurposing any Product Advertising Content … or in the direct training or fine-tuning of a machine learning and/or foundational model." |
| V16 | IP License §1 — no ML model from Program Content | same, chunks 6–7 | **Confirmed**: "no use of data mining, robots, or similar data gathering and extraction tools"; "will not allow any third party to … develop or improve large language or multimodal models, machine learning models or related technology." |
| V17 | IP License 2(h)–(k) — caching, date stamp, 40 KB, disclaimer | same, chunk 8 | **Confirmed verbatim**, including the 24-hour cache rule, the adjacent date/time stamp plus the "Product prices and availability are accurate as of the date/time indicated…" disclaimer, the 40 KB limit, and the "COMES FROM AMAZON" text disclaimer. |
| V18 | Agent Terms §4(c) | same, chunk 8 | **Confirmed verbatim**: "“Agent/\[agent name\]” (e.g., Agent/AmazonAgent)"; no mimicking of human keystrokes or navigation; no completing or circumventing CAPTCHAs. |
| V19 | CIS 2(e) — Redirecting Link disqualifies the purchase | same, chunk 1 | **Confirmed verbatim**: "any Product purchased by a customer who is referred to an Amazon Site by a link that sends users indirectly to an Amazon Site via an intermediate site, without requiring the customer to click on a link or take some other affirmative action on that intermediate site (a “Redirecting Link”)". |
| V20 | CIS 2(b) — cancellation, return or refund disqualifies | same, chunk 1 | **Confirmed verbatim**: "any Product order where a cancellation, return, or refund has been initiated". |
| V21 | CIS §6 — payment timing and minimums | same, chunk 2 | **Confirmed verbatim**: "approximately 60 days following the end of each calendar month"; Payment Minimum Chart — deposit 10 USD, gift card 10 USD / 2000 USD, check 100 USD, check processing fee 15 USD. |
| V22 | Influencer Program 3(c) — `#Ad` / `#Sponsored` | same, chunk 9 | **Confirmed verbatim**: "by using the text “#Ad” or “#Sponsored”". |
| V23 | PR §5 — no ML model from Special Links or Program Content | same, chunk 4 | **Confirmed**: "You will not, without or express prior written approval, use, or allow any third party to use, any Special Links or Program Content to develop machine learning models or related technology." |

---

## 4. Commission and API (read live, 2026-11-14)

| # | Claim | Official page re-read | Result |
|---|---|---|---|
| V24 | Standard Commission Table 1 | [Associates Program Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | **Confirmed row for row**: Luxury Beauty / Luxury Stores Beauty / Amazon Explore 10.00 %; Digital Music, Physical Music, Handmade, Digital Videos 5.00 %; **Physical Books, Kitchen, Automotive 4.50 %**; … Toys, Furniture, Home, Home Improvement … 3.00 %; … **All Other Categories 4.00 %**. Read without a sign-in. |
| V25 | Creators API operations and prerequisites | [Welcome to Creators API](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) | **Confirmed**: four operations — SearchItems, GetItems, GetVariations, GetBrowseNodes; prerequisite 2 is "Have at least 10 qualifying sales within the past 30 days to access the PA API through the Creators API". |

---

## 5. FTC (read live, 2026-11-14)

| # | Claim | Official page re-read | Result |
|---|---|---|---|
| V26 | Disclosure triggers and placement | [Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | **Confirmed verbatim**: "Disclose when you have any **financial, employment, personal, or family relationship** with a brand"; "Place it so it’s **hard to miss**"; "You can’t talk about your experience with a product you haven’t tried." Page dated **November 2019**. |

---

## 6. Carried, not re-read by this session

These are unchanged from earlier sessions' records and are **not** re-verified here. They are listed
so the record is complete and so nobody reads the list above as covering more than it does.

| Register ID | Claim | Page |
|---|---|---|
| S26 | Onsite Table A — Kitchen 1.25 % | [Onsite Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) |
| S28 | 180 days to refer a sale; dormancy | [Account Dormancy](https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG) |
| S29 | "at least three within the first 180 days"; personal orders excluded | [Application review process](https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM) |
| S43 | Air Fryers Best Sellers, browse node 17659096011 | [Best Sellers — Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/) |
| S44 | Endorsement Guides revised 2023; affiliate FAQ | [FTC's Endorsement Guides: What People Are Asking](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) |
| S05 | PA-API 5 deprecation and 403 `AccessDeniedException` | [PA-API 5 deprecation notice](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) |

---

## 7. Deliberately not attempted

| Item | Why |
|---|---|
| Prices, star ratings, review counts, demand badges as **product facts** | Participation Requirements 2(b) and 6(t) bar displaying them without an Amazon-served link or API data, and this build has neither. Reading them off a rendered page is not a verification. |
| The `--online` link check of `scripts/check_site.py` | The sandbox can reach only `github.com`, `registry.npmjs.org` and `pypi.org`. Every official page was read through the platform's fetch tool instead; the URLs are the same ones in the register. |
| Whether a `link.amazon` short link redirects without an affirmative click | Requires a logged-in Associates account (FLG-003). Not testable here; not claimed. |

**No third-party page was used as evidence anywhere in this session.**
