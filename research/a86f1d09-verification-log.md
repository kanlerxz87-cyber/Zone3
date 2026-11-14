# First-hand verification log — 2026-11-14

## Method
Fetched each supplied short link, then fetched the resolved Amazon product page directly. The submitted nine-character tokens are link identifiers, not ASINs: direct `/dp/<token>` probes return Page Not Found, while the short links resolve to live product pages. Product values below are dated research observations, not live offers; do not render static prices under the Associates price-display rules. All source URLs below are first-party Amazon pages.

| Ref | Submitted short URL → target ASIN | Listing | Rating / ratings | Price snapshot | Category / rank | Official source |
|---|---|---|---|---|---|---|
| P-01 | [B04G1MEwY](https://link.amazon/B04G1MEwY) → B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | 4.2 / 4,859 | $79.93 new; $57.45 used; $99.99 list, observed 2026-11-14 | Air Fryers; Kitchen & Dining #4,782; Air Fryers #29 | [Amazon listing](https://www.amazon.com/dp/B0CDY277D3) |
| P-02 | [B02NbDxp3](https://link.amazon/B02NbDxp3) → B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 4.3 / 18,320 | $149.99 new; $97.49 used; $209.99 list, observed 2026-11-14 | Air Fryers; Kitchen & Dining #1,043; Air Fryers #15 | [Amazon listing](https://www.amazon.com/dp/B09B7SB46R) |
| P-03 | [B00hJ57DV](https://link.amazon/B00hJ57DV) → B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | 4.4 / 16,863 | $79.91 new; $51.94 used; $119.99 list, observed 2026-11-14 | Air Fryers; Kitchen & Dining #554; Air Fryers #10 | [Amazon listing](https://www.amazon.com/dp/B08DKYBTPH) |

## Additional verified facts

- Each listing breadcrumb: Home & Kitchen → Kitchen & Dining → Small Appliances → Fryers → Air Fryers. Sources: [P-01](https://www.amazon.com/dp/B0CDY277D3), [P-02](https://www.amazon.com/dp/B09B7SB46R), [P-03](https://www.amazon.com/dp/B08DKYBTPH).
- Commission schedules publicly show Kitchen: Standard 4.50%; Onsite Table A 1.25%; Creator Ads Table B 2.25%. These are different link/program models, not interchangeable product-specific rates. Sources: [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ), [Onsite Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA).
- Program Policies: onsite prices/availability may be displayed only under allowed Amazon-served-link or API routes; comparisons must meet specified price presentation requirements. Source: [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies).
- Review-summary signals: P-01 reliability 137 mentions (9 positive / 128 negative); heat output 83 (23 / 60). P-02 reliability 1,637 (1,142 / 495), heating 746 (239 / 507), cleaning 450 (366 / 84). P-03 reliability 876 (506 / 370), durability 454 (74 / 380), cleaning 412 (375 / 37). Source for each: its linked Amazon listing above.

## Corrections and limits

The earlier rejected-intake verdict was incorrect as applied to short links. Nine-character inputs do not pass as ASINs, but their short links resolve deterministically to the listings above; a direct `/dp/<short-token>` 404 is expected and is not evidence that the short link fails. Values are product-page observations on 2026-11-14, not API/license data. Do not display static prices or claim conversion rates, trend histories, competitor counts, or revenue: these were not verified. Tracking tag, clicks, conversions, API credentials, and actual program link model remain unverified. Historical contradictory statements remain in archived records for provenance.
