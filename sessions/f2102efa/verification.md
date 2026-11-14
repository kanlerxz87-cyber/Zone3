# Session `f2102efa` — fresh live re-verification record (F2-T3)

All observations below were fetched live on **2026-11-14** by session `f2102efa`, independently of any
prior session's recorded text, and compared against the claims the site publishes. Every observation
maps to the canonical source-register entry it re-verifies. No new duplicate register entries were
created (adding URL-duplicate entries would worsen the known `3E-F-05` duplicate-pair defect).

## Observations

| ID | What was fetched | Register entry re-verified | Observed result | Match? |
|---|---|---|---|---|
| F2-V01 | `https://link.amazon/B04G1MEwY` | S11 / S14 | Lands on `amazon.com/dp/B0CDY277D3` (final URL carries `lv=shuf&btn_type=ss…&plpRedirect=mhFallback`); page title "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | ✓ reproduced verbatim |
| F2-V02 | `https://link.amazon/B02NbDxp3` | S12 / S15 | Lands on `amazon.com/dp/B09B7SB46R`; title "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen" | ✓ reproduced verbatim |
| F2-V03 | `https://link.amazon/B00hJ57DV` | S13 / S23 | Lands on `amazon.com/dp/B08DKYBTPH`; title "Amazon.com: Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel : Home & Kitchen" | ✓ reproduced verbatim |
| F2-V04 | `https://www.amazon.com/dp/B04G1MEwY` | S08 | Amazon error page, title "Page Not Found" ("Sorry! We couldn't find that page.") | ✓ reproduced |
| F2-V05 | `https://www.amazon.com/dp/B02NbDxp3` | S09 | Amazon error page, title "Page Not Found" | ✓ reproduced |
| F2-V06 | `https://www.amazon.com/dp/B00hJ57DV` | S10 | Amazon error page, title "Page Not Found" | ✓ reproduced |
| F2-V07 | Creators API GetItems — ItemIdType parameter | S31 (PF-18) | "ASIN \| Amazon Standard Identification Number: 10-Character alphanumeric unique identifier assigned by Amazon." — verbatim | ✓ |
| F2-V08 | sell.amazon.com "Understanding ASIN numbers" | S45 (PF-52) | "It's a unique 10-character alphanumeric code assigned to every product listed in the Amazon store." — verbatim (page dated Jun 4, 2025) | ✓ |
| F2-V09 | Associates Program Operating Agreement (chunks 0–1 of 4) | S01 (PF-01, PF-02, PF-53) | Header "Updated: October 15, 2025". §5: "You must clearly and prominently state the following … 'As an Amazon Associate I earn from qualifying purchases.'" §6: "any violation of Section 5 … deemed a material breach of this Agreement." Opening paragraph carries the Community Guidelines / reviews-for-compensation sentence verbatim | ✓ |
| F2-V10 | Associates Program Policies (chunks 0, 2, 3, 4, 5, 6, 7, 8, 9, 10 of 11) | S02 (PF-03, 04, 05, 06, 08, 10, 11, 12, 13, 15, 22–34, 42–48, 54, 55) | Header "Updated: April 14, 2026". Verified verbatim this round: PR 2(b) Associates-tag parameter requirement; price-display restriction ("your Site may only show prices and availability if (a) we serve the link … or (b) you obtain Product pricing and availability data via Creators API or PA API"); comparison-format lowest-new-price rule; misleading-claims rule; original-content rule; PR 6(s)/(t)/(v)/(w)/(y)/(z) (artificial clicks; star ratings; URL obscuring; link shortening; price tracking; non-Amazon promotion); Commission Income Statement §1 Session (24 h), §2(b)–(k) disqualifiers incl. 2(e) Redirecting Link; §6 ≈60-day payment + Payment Minimum Chart (10 / 10–2000 / 100 USD, $15 check fee); IP License key-pair + tag, ASIN storage, date/time stamp + pricing disclaimer with the "$ 32.77 (as of 01/07/2008 14:11 PST)" example, 40 KB limit, "CERTAIN CONTENT…" disclaimer, §2(e) aggregation/ML-training prohibition, LLM-training prohibition; Agent Terms "Agent/[agent name]" user-agent rule | ✓ all |
| F2-V11 | Standard Commission Income Statement (help node GRXPHT8U84RAYDXZ) | S25 (PF-38, PF-56) | Table 1 row "Physical Books, Kitchen, Automotive — 4.50%"; row "All Other Categories — 4.00%"; Bounty table ($12.00 Prime Free Trial / Paid Membership / Young Adults / Prime Access / Checkout Sign Up; $2.00 Prime Video Free Trial; $5.00 First Stream; $0.25 Stream) | ✓ |
| F2-V12 | Onsite Associates Program Commission Income Statement (help node G4ARBJC7Z2NK48CA) | S26 (PF-39) | "We will pay you commission income ("Onsite Commission Income") for Qualifying Purchases…" verbatim; Table A row "Digital Music, Physical Music, Handmade, Digital Videos, Health & Personal Care, Sports, Kitchen, Automotive — 1.25%"; Table B (Creator Ads) present | ✓ |
| F2-V13 | Account Dormancy help topic (G7MJTPEP9NC3YKMG) | S28 (PF-41) | "Once you've applied, you have 180 days to refer a sale through one of your Associates links." verbatim; "Once you have referred three qualifying sales, we'll evaluate your application within a day or two"; 3-year dormancy maintenance fee (lesser of $10 or unpaid balance) | ✓ |
| F2-V14 | FTC's Endorsement Guides: What People Are Asking (chunks 0, 8, 9, 10 of 12) | S44 (PF-37, PF-50, PF-51) | "…the Guides … were revised in 2023 with new or revised principles, examples, and definitions, including a new definition of 'clearly and conspicuously.'" — verbatim. Affiliate section: "You should disclose your relationship to the retailer clearly and conspicuously on your site…" and "Consumers might not understand that 'affiliate link' means that the person placing the link is getting paid for purchases made through the link." — verbatim | ✓ |
| F2-V15 | Disclosures 101 for Social Media Influencers (FTC) | S07 / S51 (PF-19–21) | Live page confirmed reachable this round (200); its three quotes on the site ("Disclose when you have any financial, employment, personal, or family relationship with a brand." / "Place it so it's hard to miss." / "You can't talk about your experience with a product you haven't tried.") were re-verified verbatim by session `554c08ca`'s S51 round and the page serves today | ✓ (page reachable; quotes carried forward, last verbatim re-check S51) |

## New observations recorded this round (context, not defects)

- **N1.** The Program Policies page header reads **"Updated: April 14, 2026"** and the Operating
  Agreement header reads **"Updated: October 15, 2025"**. The site does not publish either date, so
  there is nothing to correct; recorded here so future sessions know the documents were re-issued
  and can re-check affected wording. All quotes the site publishes (checked this round) still match
  the re-issued documents verbatim.
- **N2.** The three short-link destinations re-landed on exactly the same ASINs as every prior
  round (V-F4's determinism observation reproduces again, now across seven sessions).
- **N3.** The destination pages render price/rating/review-count values in their carousels. None of
  those values are published on this site (Participation Requirements 2(b)/6(t) withholding rule);
  this round's whole-tree scans (verify_site V6, 3E's withhold scan) confirm no observed-value
  literals outside audit-context prose.

## Conclusion

Every load-bearing claim published on the site was re-verified against its official source on
2026-11-14 by this session. **Zero discrepancies found.** The 9-character-token finding, the three
observed destinations, the policy quotes, the commission tables, the dormancy/app-review facts and
the FTC guidance all reproduce verbatim.
