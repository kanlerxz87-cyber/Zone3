# Verification scope — 2026-11-19 · session `cd746460`

Final-integration, bounded current verification. The branch base is `825f513` (`main`, PR #172 merge). This pass re-verifies the five supplied product links line by line against the live Amazon destination pages and re-checks the combined publication register; historical claims retain their own dates and are not re-verified here.

## Product links re-verified (one fresh fetch per supplied link, 2026-11-19)

| Submitted link | Observed redirect destination | Observed ASIN | Listing title observed (live) | Registered match |
|---|---|---|---|---|
| https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | ASIN + title: match |
| https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included | ASIN + title: match |
| https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel | ASIN: match; title: match in substance — recorded title omits the non-substantive ® trademark glyph |
| https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill BBQ Camping, Black | ASIN + title: match |
| https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 | ASIN + title: match |

- Redirect targets, ASINs and listing titles in `data/publication.json` and `data/shop/products.json` agree with the fresh 2026-11-19 observations. No drift found.
- Scope checked: redirect destination, final URL, listing page title, category breadcrumb (Air Fryers for SHOP-01..03; Thermometers & Timers / Meat for SHOP-04..05). Title wording is a listing claim, not independent verification of performance, accuracy, certification or capacity.
- Prices, ratings, review counts and availability seen on the destination pages are deliberately **not** recorded: the register keeps `price`, `rating`, `review_count` and `tested_performance` empty by design.
- Intended ASINs and all intent-confirmation fields remain empty for all five products; observed redirect targets are kept in separate fields and were not merged into them.
- No self-purchase, conversion test or fabricated impression was performed. No claim is made that the supplied short links' Associates attribution is valid — that remains unresolved (FLG-003).

## Register re-check

- `data/publication.json`: 5 products, 6 guides, 10 official sources, 9 decision questions, 6 proposals, 14 indexable pages — schema and values consistent with the builders and gates.
- `data/shop/products.json`: product-intent confirmation record intact; intended_* fields blank for all five; observed fields match `data/publication.json`.
