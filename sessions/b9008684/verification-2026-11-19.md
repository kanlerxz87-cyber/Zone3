# Verification scope — 2026-11-19 · session `b9008684`

Suggestions review round (B9-T2). Independent dated verification of the pages this round's
suggestions and decision rows rest on. Method: one page-fetch per official URL, fetched live on
2026-11-19 by this session. No claim in the review round rests on a page that is not in this record
or already registered in `data/publication.json` with a dated scope. Historical claims keep their
original dates and are not re-verified here.

## Official pages re-read (2026-11-19, session b9008684)

| # | Page | What was read | Result | Registered as |
|---|---|---|---|---|
| V1 | https://affiliate-program.amazon.com/help/operating/agreement (chunk 1 of 4) | §4 no representation of traffic/commission amounts ("We do not make any representation, warranty, or covenant regarding the amount of traffic or commission income you can expect"); §5 disclosure sentence verbatim; §6 any violation of §5 "deemed a material breach" | confirmed | `amazon-agreement` |
| V2 | https://affiliate-program.amazon.com/help/operating/policies (chunk 3 of 11) | Participation Requirements 2(b): tag in URL, no dynamic per-user sub-tags, Special Links must link to Products with relevant original content, remove expired promotions, no inaccurate/overbroad/deceptive claims, prices/availability only when Amazon serves the link or via Creators API/PA API | confirmed verbatim | `amazon-policies` |
| V3 | https://affiliate-program.amazon.com/help/operating/policies (chunk 5 of 11) | 6(f) paid search must send users to your site, not directly/indirectly to an Amazon Site; 6(s) no artificial clicks; 6(t) reviews/star ratings only via Creators API or PA API; 6(v) no cloaking; 6(w) no link shortening that obscures the Amazon destination; 6(y) no price tracking/alerting | confirmed verbatim | `amazon-policies` |
| V4 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | material connection must be disclosed; placement "hard to miss"; "You can't talk about your experience with a product you haven't tried"; can't make up claims that would require proof | confirmed; page dated November 2019 | `ftc` |
| V5 | https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | safe minimum internal temperature chart (poultry 165°F/74°C; 145°F + 3-minute rest for whole cuts; leftovers 165°F); "Date Last Reviewed: November 21, 2024" | confirmed | `food-safety` |
| V6 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` marks advertisements/paid placements; multiple rel values allowed | confirmed; page last updated 2025-12-10 UTC | `google-links` |
| V7 | https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews | reviews need expertise, evidence of experience, quantitative measures, pros/cons from original research; "best" recommendations need first-hand supporting evidence; affiliate-page note links to the thin-affiliate spam policy | confirmed; last updated 2025-12-10 UTC | `google-reviews` |
| V8 | https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data (new source) | structured data enables rich results; "Don't create blank or empty pages just to hold structured data, and don't add structured data about information that is not visible to the user" | confirmed; added to `data/publication.json` as `google-structured-data` | `google-structured-data` |
| V9 | https://developers.google.com/search/docs/appearance/page-experience (new source) | page-experience self-assessment: Core Web Vitals, secure serving, mobile display, no excessive ads, no intrusive interstitials, distinguishable main content | confirmed; added to `data/publication.json` as `google-page-experience` | `google-page-experience` |
| V10 | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | "GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site…"; 1 GB site limit; 100 GB/month soft bandwidth; 10 builds/hour soft limit | confirmed | `github-limits` |

## The five supplied product links re-fetched (2026-11-19, session b9008684)

One live fetch per supplied `link.amazon` short link. Same observations as the same-day record by
session `cd746460` (`sessions/cd746460/verification-2026-11-19.md`) — two independent same-day
readings that agree.

| Submitted link | Observed destination | Page title observed (live) | Breadcrumb (live) | Registered match |
|---|---|---|---|---|
| https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | ASIN + title: match |
| https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included | …› Fryers › Air Fryers | ASIN + title: match |
| https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option… \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel | …› Fryers › Air Fryers | ASIN: match; title: match in substance (live title carries the non-substantive ® glyph) |
| https://link.amazon/B0c8moW59 | https://www.amazon.com/dp/B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified… | …› Kitchen Utensils & Gadgets › Thermometers & Timers › Meat | ASIN + title: match |
| https://link.amazon/B0f3GKalj | https://www.amazon.com/dp/B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range… \| Gen3 | …› Thermometers & Timers › Meat | ASIN + title: match |

Deliberately not recorded (unchanged policy): prices, star ratings, review counts, "bought in past
month" badges and availability seen in the fetched text — Participation Requirements 2(b)/6(t) permit
those on a site only via Amazon-served links or the authorized APIs, which are not established here.
Intended-ASIN fields stay empty; observed redirect targets stay in separate fields (never merged).
No Associates attribution test was performed; FLG-003 remains unresolved and is not claimed either
way. No clicks to Amazon were generated by this session other than the five observation fetches.

## Result

No drift between the register and the live observations. No new irregularities found; no flag rows
added by this session (the flag register stays at 154 entries). Everything this round publishes on
the review surface is either (a) a dated observation in this record, (b) an editorial suggestion
explicitly labelled as a hypothesis or judgement, or (c) a repository fact checked against the tree.
