# Session 66964850 — independent verification round, 2026-11-17

All observations below were made by this session on 2026-11-17 (UTC) by fetching the
official page named in the source column directly. No value is copied from another
session's record without a fresh read; where a register quote was compared, the
comparison is stated. Prices, star ratings and review counts were visible in some
listing fetches and are **deliberately not recorded here** (Program Policies
Participation Requirements 2(b)/6(t), read verbatim today — see V14/V15).

Fetch method: platform page fetch (follows redirects; final URL and served `<title>`
captured). Sandbox direct egress to amazon.com/ftc.gov is blocked, so no `curl`
claims are made.

## A. The five submitted short links (owner brief 2026-11-17)

| ID | Submitted link | Observed final URL (2026-11-17) | Served page title (leading text) | Register comparison | Result |
|---|---|---|---|---|---|
| Z1-V01 | `https://link.amazon/B04G1MEwY` | `https://www.amazon.com/dp/B0CDY277D3?…plpRedirect=mhFallback` | Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen | `data/shop/products.json` SHOP-01 (`B0CDY277D3`, same title); `data/sources.json` S67 | **Confirmed** |
| Z1-V02 | `https://link.amazon/B02NbDxp3` | `https://www.amazon.com/dp/B09B7SB46R?…plpRedirect=mhFallback` | Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen | SHOP-02 (same ASIN + title); S68 | **Confirmed** |
| Z1-V03 | `https://link.amazon/B00hJ57DV` | `https://www.amazon.com/dp/B08DKYBTPH?…plpRedirect=mhFallback` | Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen | SHOP-03 (same ASIN; register title omits the ® mark — punctuation-only drift, not a different listing); S69 | **Confirmed** |
| Z1-V04 | `https://link.amazon/B0c8moW59` | `https://www.amazon.com/dp/B0DHZTCNR5?…plpRedirect=mhFallback` | Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill BBQ Camping, Black : Home & Kitchen | SHOP-04 (same ASIN + title) | **Confirmed** |
| Z1-V05 | `https://link.amazon/B0f3GKalj` | `https://www.amazon.com/dp/B0DZFD6R9Z?…plpRedirect=mhFallback` | Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 : Home & Kitchen | SHOP-05 (same ASIN + title) | **Confirmed** |

## B. Direct `/dp/<token>` checks (the nine-character claim)

| ID | URL fetched | Served title | Register claim | Result |
|---|---|---|---|---|
| Z1-V06 | `https://www.amazon.com/dp/B04G1MEwY` | Page Not Found | S8 / FLG-001: token is not a working ASIN | **Confirmed** |
| Z1-V07 | `https://www.amazon.com/dp/B02NbDxp3` | Page Not Found | S9 / FLG-001 | **Confirmed** |
| Z1-V08 | `https://www.amazon.com/dp/B00hJ57DV` | Page Not Found | S10 / FLG-001 | **Confirmed** |
| Z1-V09 | `https://www.amazon.com/dp/B0c8moW59` | Page Not Found | new this round: extends the same observation to brief link 4 | **Confirmed** |
| Z1-V10 | `https://www.amazon.com/dp/B0f3GKalj` | Page Not Found | new this round: extends the same observation to brief link 5 | **Confirmed** |

Note: a Page-Not-Found on `/dp/<token>` says only that the nine-character code is not
a working ASIN under that path; it says nothing about whether the supplied short link
itself works (Z1-V01…V05 show they do), and it is not a claim that the supplied links
are invalid — see FLG-003.

## C. Load-bearing official documents

| ID | Claim checked (register id) | Official page (fetched 2026-11-17) | Observed | Result |
|---|---|---|---|---|
| Z1-V11 | ASIN is a 10-character identifier (S31 / PF-… ItemIdType) | Creators API → GetItems → ItemIdType Parameter | "ASIN \| Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." | **Confirmed verbatim** |
| Z1-V12 | Required disclosure sentence (PF-01, OA §5) | Operating Agreement (page header: "Updated: October 15, 2025") → §5 Identifying Yourself as an Associate | "…you must clearly and prominently state …: \"As an Amazon Associate I earn from qualifying purchases.\"" | **Confirmed verbatim** |
| Z1-V13 | Associates tag must be a URL parameter (PF-03, Participation Requirements 2(b)) | Program Policies (page header: "Updated: April 14, 2026") → §2(b) | "…you must include your Associates ID or \"tag\" (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site." | **Confirmed verbatim** |
| Z1-V14 | Prices may be shown only via Amazon-served link or Creators/PA API (PF-04 / PF-44 / PF-54, 2(b)) | same page → §2(b) | "…your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…" | **Confirmed verbatim** |
| Z1-V15 | Customer reviews / star ratings restricted (PF-05 / PF-45, 6(t)) | same page → Participation Requirements §6(t) | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API…" | **Confirmed verbatim** |
| Z1-V16 | Link must not be obscured / unclear (6(v), 6(w)) | same page → §6(v), §6(w) | "(v) You will not cloak, hide, spoof, or otherwise obscure the URL of your Site containing Special Links…"; "(w) You will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site." | **Confirmed verbatim** |
| Z1-V17 | 24-hour session window (PF-12 family, Commission Income Statement §1) | Program Policies → Commission Income Statement §1(b) | Session ends on the first of: 24 hours elapse from the click; order placed; click through another Associate's Special Link; (cart purchases count if completed no later than 89 days; ship/pay within 180 days) | **Confirmed** |
| Z1-V18 | Kitchen category fixed rate 4.50% (S25, Standard Commission Table 1) | Associates Program Standard Commission Income Statement → Table 1 | Row "Physical Books, Kitchen, Automotive \| 4.50%" | **Confirmed** (category reference only; the listings' own category is still unverified — FLG-021 stands) |
| Z1-V19 | FTC disclosure placement guidance (S07/S51) | ftc.gov → Disclosures 101 for Social Media Influencers (page dated November 2019) | "Place it so it's **hard to miss**… The disclosure should be placed with the endorsement message itself… Don't mix your disclosure into a group of hashtags or links." | **Confirmed** |
| Z1-V20 | `rel="sponsored"` marks paid links (SH-S04 / S-05) | developers.google.com → Qualify your outbound links to Google (page: Last updated 2025-12-10 UTC) | "Mark links that are advertisements or paid placements (commonly called _paid links_) with the `sponsored` value." | **Confirmed** |

## D. Drift and reconciliation notes

- **No quote drift.** Every register quote checked above still matches the official
  page byte-for-byte in substance on 2026-11-17. This agrees with existing flag
  F2-F-02 (Program Policies re-issued April 14, 2026 / OA October 15, 2025; quotes
  still match) — independently re-confirmed here.
- **G82-F-03, observed half closed by evidence.** The two links the previous session
  could not find a register row for (`B0c8moW59`, `B0f3GKalj`) were resolved live
  today (Z1-V04, Z1-V05) and match `data/shop/products.json` SHOP-04/SHOP-05 exactly.
  The intent half (what the owner intended each link to point at) stays open — a
  redirect is not evidence of intent.
- **Cross-repo note (brief irregularity).** The owner brief's S-14/S-15/S-17… rows
  cite `Zone4` decision pages (D-04…D-27). `github.com/kanlerxz87-cyber/Zone4` exists
  and contains `DESIGN_PROMPT.md` (GitHub API, 2026-11-17), so those statuses describe
  the sibling Zone4 repository, not this one. Session 38650305's flag that S-14/S-15
  "cite files this repo does not contain" is therefore a cross-repo reference, not a
  phantom file.
- **Not re-read this round** (prior verbatim reads stand, none contradicted): the full
  11-chunk Program Policies beyond the sections listed, the FTC Endorsement Guides
  16 CFR Part 465 text, the Onsite Table A (S26), and the PA-API deprecation notice
  (S05).

## E. Environment limitation (recorded, not a site defect)

Direct HTTPS egress from the sandbox shell to `amazon.com`, `ftc.gov`,
`affiliate-program.amazon.com` and `developers.google.com` returns no connection
(`curl` exit 000); all fetches above were made through the platform's page-fetch
tool, which resolves those hosts. Any future session re-running this round should
use the same tool or record its own method.
