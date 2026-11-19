# Verification record — session d3493182 (2026-11-19)

**Scope:** the five submitted short links (line by line: submitted code, observed ASIN, listing title, breadcrumb) plus a re-read of the official policy sources that govern the site's disclosure, links and editorial rules. Every value below was read live on 2026-11-19. Prices, ratings and review counts visible on the live listing pages were **not** transcribed and are **not** published anywhere on the site (register rule: `price`, `rating`, `review_count`, `tested_performance` stay empty).

## 1. Submitted links — observed destinations (unchanged from the register)

| # | Submitted link | Observed ASIN | Observed listing title (live, 2026-11-19) | Breadcrumb (live) | Register match |
| --- | --- | --- | --- | --- | --- |
| 1 | https://link.amazon/B04G1MEwY | `B0CDY277D3` | Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | ASIN + title + breadcrumb match |
| 2 | https://link.amazon/B02NbDxp3 | `B09B7SB46R` | Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | ASIN + title + breadcrumb match |
| 3 | https://link.amazon/B00hJ57DV | `B08DKYBTPH` | Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | ASIN + title + breadcrumb match |
| 4 | https://link.amazon/B0c8moW59 | `B0DHZTCNR5` | Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black : Home & Kitchen | Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat | ASIN + breadcrumb match; **title variant flagged** (see §3) |
| 5 | https://link.amazon/B0f3GKalj | `B0DZFD6R9Z` | Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3: Home & Kitchen | Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat | ASIN + title + breadcrumb match |

**Method:** each `link.amazon/<code>` URL was opened live; the final `amazon.com/dp/<ASIN>` URL, page `<title>` and breadcrumb were read from the fetched page. The 9-character short-link codes are not ASINs (an ASIN is a 10-character identifier); the observed ASINs above are the redirect destinations, kept in the register's **observed** fields only. The **intended** fields (`intended_asin`, `official_listing_url`, `intent_confirmed_on`, `intent_confirmation_source`) remain blank — no observed value was copied into them.

**What this does not prove:** that the short links attribute to the selected Associates account (`shopnow047c-20`, user-supplied), or that they are enrolled-workflow Special Links. That check needs the account owner (FLG-003, P26-Q2). The site does not describe the supplied links as invalid or as attribution-verified.

## 2. Official sources re-read (2026-11-19)

| Source | URL | What was confirmed |
| --- | --- | --- |
| Amazon Associates Operating Agreement (Updated October 15, 2025) | https://affiliate-program.amazon.com/help/operating/agreement | §1: links must properly use the provided tagged formats ("Special Links"); Program Content includes data, images and text. §4: Amazon makes no representation about traffic or commission income. §5: "You must clearly and prominently state … 'As an Amazon Associate I earn from qualifying purchases.'" §6: a §5 violation is a material breach. |
| Amazon Associates Program Policies (Updated April 14, 2026) | https://affiliate-program.amazon.com/help/operating/policies | Participation Requirements 2(a): Special Links enable tracking and must use the assigned Associates ID. 2(b): tag parameter required; no bookmarking inducement; no sub-tag associated with a specific end user; original content required on listing pages; no inaccurate/overbroad/misleading claims; prices/availability only via an Amazon-served link or a licensed API. Commission Income Statement: 24-hour session; cart orders within 89 days. |
| FTC: Disclosures 101 for Social Media Influencers (November 2019) | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | Place the disclosure with the endorsement so it is hard to miss; simple, clear language ("advertisement", "ad", "sponsored"); you cannot talk about your experience with a product you have not tried. |
| Google: Creating helpful, reliable, people-first content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | Self-assessment (original information, insight beyond the obvious, descriptive titles without exaggeration); people-first vs search-engine-first; "Are you writing about things simply because they seem trending?" is a warning sign. |
| Google: Qualify your outbound links (last updated 2025-12-10) | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` marks advertisements or paid placements; marked links are generally not followed. |

## 3. Irregularities flagged for review (non-blocking)

1. **SHOP-04 title variant.** The register's `listing_title` for `B0DHZTCNR5` reads "…Highly Waterproof for Grill BBQ Camping, Black", while the live title read on 2026-11-19 reads "…IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black". The ASIN and breadcrumb are unchanged. The register title was **not** edited in this session (additive-only scope); the owner may refresh it in a later pass. No site copy depends on the differing words.
2. **Intent fields blank (all five).** Intended ASIN, official listing URL, confirmation date and source are unconfirmed. This is the standing P26-Q1 gap, not a new finding.
3. **Attribution unverified (FLG-003).** No enrolled-workflow Special Link validation or tracking-report check exists. Unresolved; see P26-Q2.
4. **Live listing pages display prices and ratings.** The site publishes neither, per the register rule. No value was transcribed into this repository.

## 4. Checks run

- `python3 tools/publish.py --check` before any edit: **25/25 PASS** (baseline).
- Full `python3 tools/publish.py` after the batch-3 register append: see the COORDINATION.md publish record for this session.
