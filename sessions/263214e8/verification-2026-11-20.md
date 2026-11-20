# Verification record — session 263214e8 — 2026-11-20

Method: each official page below was fetched live in this session (2026-11-20) and read
in full or in the chunks noted. Bash outbound network in this sandbox reaches only GitHub,
npm and PyPI, so Amazon/Google/FTC fetches were done through the page-fetch tool, not curl.
Nothing below was copied from a prior session's record without re-reading it here.
Prices, ratings and review counts visible on Amazon listing pages were observed during the
fetch but deliberately NOT recorded or published (Program Policies 2(b)/6(t)).

## 1. Official sources re-read 2026-11-20

| Ref | URL | What was read | Result vs register |
|---|---|---|---|
| S01 Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Header "Updated: October 15, 2025". §1 Special Links must use tagged formats. §5 exact sentence: "As an Amazon Associate I earn from qualifying purchases." §6 violation of §5 is a material breach. §4: no representation about traffic or commission income. | Matches register. Disclosure sentence verbatim. |
| S02 Policies | https://affiliate-program.amazon.com/help/operating/policies | Header "Updated: April 14, 2026". Commission Income Statement §1: 24-hour session; §2(e) Redirecting Link disqualified; §2(g) improperly formatted links disqualified. Participation Requirements 2(a) Special Links must use assigned Associates ID. 2(b): tag XXXXX-## as URL parameter; sub-tags never per end user; prices/availability only if Amazon serves link or via Creators/PA API; no misleading claims. 6(t) reviews/star ratings only via Creators/PA API. 6(v)/(w) no cloaking or unclear shortening. 6(y) no price tracking/alerting. IP License: ASINs may be stored indefinitely; price timestamp + disclaimer rules; Agent Terms §4 (identify as Agent, no CAPTCHA solving, no mimicry). | Matches register. Note: Policies header date is now April 14, 2026 (register cited older reads). No clause change affecting this site's gates. |
| Schedule (Appendix) | https://affiliate-program.amazon.com/help/operating/schedule | Redirects to Amazon sign-in. | NOT verified this session (login-gated). The register's Kitchen 4.50% category reference (VB-3) is left at its prior date and NOT re-claimed. Recorded as unverified this pass. |
| S07 FTC | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | "Place it so it's hard to miss"; with the endorsement message itself; likely missed if only on ABOUT ME/profile or behind MORE; simple clear language; "You can't talk about your experience with a product you haven't tried." Dated November 2019. | Matches register. Supports strip-under-masthead placement. |
| Google outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | rel="sponsored" for advertisements/paid placements; multiple values space/comma separated. Last updated 2025-12-10 UTC. | Matches register. Site uses rel="sponsored noopener". |
| Google helpful content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | People-first content; self-assess questions (original information, substantial description, descriptive title without exaggeration). | Matches register. Basis for question-led guides and anti-slop rules. |
| Google reviews | https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews | Demonstrate knowledge; evidence of own experience; quantitative measurements; pros/cons from original research; first-hand evidence for "best" claims. Last updated 2025-12-10 UTC. | Matches register. This site makes no first-hand claim, so no "best" ranking is published. |
| Search Console | https://developers.google.com/search/docs/monitor-debug/search-console-start | Verify ownership; submit sitemap; Search performance report shows impressions/clicks by query/page/country. | Matches register. No property verified; no query data exists. |
| FoodSafety.gov | https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | Beef/veal/lamb steaks roasts chops 145°F rest 3 min; ground meat 160°F; poultry 165°F; ham raw 145°F rest 3 min; pork 145°F rest 3 min; seafood 145°F. Last reviewed November 21, 2024. | Matches register. Basis for new guide G13. |
| FSIS thermometers | https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers | "Color is Not a Reliable Indicator"; thermometer is only reliable way; thickest part away from bone/fat/gristle; check manufacturer instructions for insertion depth; ice-water calibration 32°F. | Matches register. Basis for new guides G12/G13. |
| GitHub Pages limits | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | "GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions..." Soft bandwidth 100 GB/month. | Matches register (P26-F02). Pages is a technical deploy, not commercial approval. |

## 2. Submitted links re-followed 2026-11-20 (observed only, never intent)

| Submitted link | Observed destination ASIN | Observed title (as served) | Breadcrumb | vs register |
|---|---|---|---|---|
| https://link.amazon/B04G1MEwY | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven ... - Black | Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers | Unchanged |
| https://link.amazon/B02NbDxp3 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven ... | Same air-fryer breadcrumb | Unchanged |
| https://link.amazon/B00hJ57DV | B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry 4-in-1 with 450°F Hi-Fry Option ... | Same air-fryer breadcrumb | Unchanged |
| https://link.amazon/B0c8moW59 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer ... Black | Home & Kitchen > Kitchen & Dining > Kitchen Utensils & Gadgets > Thermometers & Timers > Meat | ASIN unchanged. Title wording variant: served title reads "...IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black" vs register "...for Grill BBQ Camping, Black". Recorded as Info drift (263-F01); register title NOT overwritten. |
| https://link.amazon/B0f3GKalj | B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes ... Gen3 | Same thermometer breadcrumb | Unchanged |

All five submitted tokens are 9 characters (not 10-character ASINs). Intended ASIN / official
listing URL / confirmation date / source remain blank for all five (FLG-S02, P26-Q1).
Supplied short links are NOT called invalid; compliance status unresolved (FLG-003).
No Associates tag was observed on any destination URL.

## 3. Site gates verified locally (no network)

- `python3 tools/publish.py --check` at baseline: 31/31 PASS.
- Disclosure sentence present under masthead and in footer on every page (gate-enforced).
- Every outbound Amazon product link carries rel="sponsored" + tag=shopnow047c-20 (gate-enforced).
- Campaign ledger empty; production measurement OFF (gate-enforced).

## 4. Irregularities raised this session

| ID | Severity | Item | Disposition |
|---|---|---|---|
| 263-F01 | Info | SHOP-04 listing title wording drift (see §2). | Recorded here; register title left unchanged; no reader claim depends on the drifted words. |
| 263-F02 | Medium | Commission Appendix (Kitchen rate) is login-gated; rate not re-verified this pass. | Left at prior register date; not re-claimed. Flagged for owner with account access. |
| 263-F03 | Medium | GitHub Pages commercial-use limit (see §1). | Already flagged (P26-F02); carried forward. Pages deploy is not commercial approval. |
