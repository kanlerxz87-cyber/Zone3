# Verification log — session `21acd3c0`, 2026-11-14 (line-by-line re-verification)

**Branch:** `arena/21acd3c0-zone3` · **Base:** `main` @ `e8e3e9d` (PR #56 merge)
**Repo:** https://github.com/kanlerxz87-cyber/Zone3 · **Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Rule applied:** every value is either confirmed against the official page cited, or left blank and
flagged. Nothing is inferred. "Confirmed" below means *this session* fetched the source on
2026-11-14 and read the quoted result itself.

Environment note (honesty requirement): this session's shell has no general internet egress
(only github.com / npm / pypi). Live fetches were made with the session's page-fetch tool, which
does reach the open web. Every "confirmed live" row below was fetched by that tool in this session.

---

## A. Live checks performed by this session (2026-11-14)

| # | Claim checked | Source URL (official) | Observed by this session | Matches register? |
|---|---|---|---|---|
| A1 | Submitted link 1 resolves to `amazon.com/dp/B0CDY277D3`, listing titled "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows … Digital Double Air Fryer - Black : Home & Kitchen" | https://link.amazon/B04G1MEwY | Fetched; final URL `https://www.amazon.com/dp/B0CDY277D3?lv=shuf&…`; page title as quoted; breadcrumb Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers | Yes — S11/S14 and the `redirect_observed` block of P1 |
| A2 | Submitted link 2 resolves to `amazon.com/dp/B09B7SB46R`, listing titled "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … : Home & Kitchen" | https://link.amazon/B02NbDxp3 | Fetched; final URL `https://www.amazon.com/dp/B09B7SB46R?lv=shuf&…`; page title as quoted; same breadcrumb chain | Yes — S12/S15, P2 |
| A3 | Submitted link 3 resolves to `amazon.com/dp/B08DKYBTPH`, listing titled "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option … Stainless Steel : Home & Kitchen" | https://link.amazon/B00hJ57DV | Fetched; final URL `https://www.amazon.com/dp/B08DKYBTPH?lv=shuf&…`; page title as quoted; same breadcrumb chain | Yes — S13/S16/S23/S32, P3 |
| A4 | `amazon.com/dp/B04G1MEwY` (the submitted code used as a product ID) returns Amazon's "Page Not Found" page | https://www.amazon.com/dp/B04G1MEwY | Fetched; page title literally `Page Not Found`; body is Amazon's standard error page ("Sorry! We couldn't find that page") | Yes — S08; supports FLG-001/FLG-035 |
| A5 | An ASIN is a **10-character** identifier (so the three 9-character submitted codes cannot be ASINs) | https://sell.amazon.com/blog/what-is-an-asin | Fetched; Amazon Selling Partner Blog, article dated Jun 4 2025: *"'ASIN' stands for 'Amazon Standard Identification Number.' It's a unique 10-character alphanumeric code assigned to every product listed in the Amazon store."* The article also states the ASIN "appears after `/dp/`" in product URLs | Yes — S45; arithmetic: `B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV` are each 9 characters (also re-counted locally) |

Determinism note: A1–A3 reproduce the same destinations that sessions 7f84fea4 (2026-11-13),
b90c5685 (2026-11-14) and 4575cf95 (2026-11-14) recorded (register S52–S55). This is now the
fourth independent observation round with identical results.

## B. Local integrity checks (this session, at `e8e3e9d` + claim commit)

| Check | Command | Result |
|---|---|---|
| Site verifier | `python3 tools/verify_site.py` | **VERIFY PASS** — 69 pages · 1169 table rows · 967 with official source · 346 with flag · 82 with repo anchor. Every row satisfies V4 provenance (official source OR flag OR repo anchor that exists). Checks V1 disclosure, V2 disclaimer, V3 single-h1, V4 row provenance, V5 no broken links, V6 no prohibited constructs, V7 no placeholders all pass |
| Strict link report | `python3 tools/link_report.py --strict` | exit 0 (documented blanks remain blank: trend rank, conversion rate, competition density, clicks/orders/revenue have no official affiliate-side source and stay unfilled) |
| External + internal links | `python3 scripts/check_all_links.py` | 115 HTML pages, 104 distinct external URLs, **0 errors** |
| Register checker | `python3 scripts/check_site.py` | OK — 12 pages, 3 products, 48 sources, 49 flags |
| No-inference audit of the product register | `python3` field scan of `data/products.json` | P1, P2, P3: `product_name`, `brand`, `price`, `rating`, `review_count`, `commission_rate` are all `null` (unverified-by-rule). Each product row carries 5 flags and 7 source IDs. PR #26's filled readings are preserved only under `observed_2026_11_14` and are not rendered as facts (FLG-038) |
| Marketing-copy leak test | `grep` for `79.93`, `99.99`, `4.2 out`, `4.8K` in `marketing/*.html` | **no matches** — the marketing section publishes no price or rating values |
| Sitemap coverage | normalized comparison of `sitemap.xml` vs page files | 69 sitemap URLs vs 52 root-level page files (plus session/doc subsites). Exact match except the two quirks logged as 21-F-02/21-F-03 below |

## C. Claims NOT re-verified by this session (published on evidence recorded earlier; links for manual review)

These remain "confirmed by prior recorded evidence" only. Per the rule, this log does not upgrade
them to "verified by 21acd3c0". They are not blanked either, because the register's own sessions
(Parts A–H) fetched and quoted them with section references; the quotes live in
`data/policy_facts.json` and the row-by-row record is the site's
[Verification log](https://kanlerxz87-cyber.github.io/Zone3/verification.html).

| Item | Register IDs | Manual-review source links |
|---|---|---|
| Operating Agreement §5 disclosure wording and material-breach clause | S01, S49, PF-01… | https://affiliate-program.amazon.com/help/operating/agreement |
| Program Policies: Participation Requirements 2(b), 6(t), 6(v), 6(w), 6(s), 6(y); CIS §1 (89/180 days), 2(e), §6 payments | S02, S30, S50, PF-02… | https://affiliate-program.amazon.com/help/operating/policies |
| Commission Schedule 1 / Standard Table 1 (Kitchen 4.50 %) and Onsite Table A (Kitchen 1.25 %) — shown only as category reference; no rate is attached to any product row (FLG-005/FLG-021) | S25, S26 | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ · https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA |
| Creators API `GetItems` ItemIdType "10-Character alphanumeric unique identifier" quote and PA-API 5 deprecation | S04–S06, S31 | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter · https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation |
| FTC Endorsement Guides (2023 revision) and disclosure-101 guidance | S07, S24, S44 | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking · https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| Enrolment gate (≥3 qualifying sales in first 180 days; personal orders excluded) and 180-day dormancy rule | S28, S29, PF-40/41 | https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM · https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG |
| Prices, ratings, review counts (volatile page observations) | S40–S48, `observed_2026_11_14` blocks | https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH — kept as dated snapshots only (FLG-004/FLG-022/FLG-038) |

## D. Corroboration notes (observations, not facts)

- During fetch A1 the live page's "Customers who viewed" widget showed a card linking to
  `dp/B0CDY277D3` at **$69.97**, while the register's snapshot for P1 records **$79.93** (deal) /
  list $99.99 earlier on 2026-11-14. Two different figures within one day, from the same page
  surface. This corroborates the register's policy (FLG-004/022/038): price and rating values are
  volatile and are never published as product facts. Neither figure is used anywhere on the site.
- Widget cards on all three pages show *other* products' ratings and prices (e.g. Ninja FO101
  $199.95, Cosori B0C33CHG99 $99.99). They were ignored, exactly as H-F-01 records.

## E. Result

- 5 of 5 live checks performed by this session match the register exactly. No contradiction found
  between `data/*.json`, the generated pages, the marketing section, and the live web.
- 0 unprovenanced table rows (1169/1169 pass V4). 0 broken links. 0 leaked unverified values in
  marketing copy. All product fact fields blank-by-rule.
- Unresolved (non-blocking, published on [flagged.html](https://kanlerxz87-cyber.github.io/Zone3/flagged.html)):
  the identity question behind FLG-002/FLG-035 (whether the owner *intended* the destination
  products), the missing Associates tag (FLG-010), and the API-eligibility gate for automation
  (FLG-012/FLG-019). None of these can be closed from public sources; they need the owner.
