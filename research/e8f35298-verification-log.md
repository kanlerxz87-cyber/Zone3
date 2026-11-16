# Session e8f35298 — Fresh live re-verification log (2026-11-16)

**Session ID:** `e8f35298` · **Branch:** `arena/e8f35298-zone3` (fixed; no other branch may be created or pushed)
**Base at claim time:** `add6525725882cba9572e47aa58da0bded807e8a` (= `origin/main`)
**Claimed:** 2026-11-16 · **Status:** verification complete; PR/merge/Pages record pending (E8F-T4)

## Method

Official sources only. Each claim below was re-fetched live today (2026-11-16) by this session; the page URL is the source. Nothing is inferred; a value that could not be confirmed from an official page is left blank and flagged. No third-party blog, aggregator or search result was used as evidence — search was used only to locate the official documents.

## Verification performed (all fetched 2026-11-16)

| # | Claim | Result | Official source |
|---|---|---|---|
| V1 | Operating Agreement header date | **Confirmed** — "Updated: October 15, 2025" | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) |
| V2 | Operating Agreement §5 disclosure wording | **Confirmed verbatim** — "You must clearly and prominently state the following... 'As an Amazon Associate I earn from qualifying purchases.'" and a Section 5 violation is a material breach (§6(a)) | [Operating Agreement §5–6](https://affiliate-program.amazon.com/help/operating/agreement) |
| V3 | Schedule 1: Amazon entity/site by location | **Confirmed** — one row: United States / Amazon.com Services LLC / amazon.com (US-only) | [Operating Agreement, Schedule 1](https://affiliate-program.amazon.com/help/operating/agreement) |
| V4 | Program Policies §2(b): Special Links must carry the Associates tag | **Confirmed verbatim** — "You must include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site." | [Program Policies §2(b)](https://affiliate-program.amazon.com/help/operating/policies) |
| V5 | Program Policies §2(b): price/availability display rule | **Confirmed verbatim** — a site may show prices/availability only if Amazon serves the link or the data comes via Creators API or PA API | [Program Policies §2(b)](https://affiliate-program.amazon.com/help/operating/policies) |
| V6 | Program Policies §6(t): reviews and star ratings via API only | **Confirmed verbatim** — customer reviews/star ratings may be displayed only if obtained through Creators API or PA API | [Program Policies §6(t)](https://affiliate-program.amazon.com/help/operating/policies) |
| V7 | Standard Commission Income Statement, Table 1 (public, no sign-in) | **Confirmed** — "Physical Books, Kitchen, Automotive | 4.50%"; "All Other Categories | 4.00%"; Luxury Beauty 10.00% | [Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| V8 | Short link `link.amazon/B04G1MEwY` resolves to a live Amazon listing | **Confirmed** → `amazon.com/dp/B0CDY277D3` (CHEFMAN 6 Quart Dual Basket Air Fryer Oven); breadcrumb Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers (node 17659096011). Stable across days and sessions (matches S11/S52/S55). Observed destination only — not confirmed as the submitter's intended product (FLG-002). | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) · [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) |
| V9 | Direct `amazon.com/dp/<9-character token>` → Page Not Found | **Confirmed ×3** for B04G1MEwY, B02NbDxp3, B00hJ57DV; positive control passes (real ASINs serve pages) | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) |
| V10 | FTC Disclosures 101: disclosure obligations | **Confirmed** — disclose any financial/personal/family/material relationship; placement "hard to miss", simple and clear language; "You can't talk about your experience with a product you haven't tried." Page dated November 2019. | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |

## Not re-verified, and why (deliberate, not a gap)

- **Price, star rating, review count as product facts:** barred by Program Policies §2(b) and §6(t) unless Amazon serves the link or the data comes via Creators API/PA API. No account credentials or API access exist in this repo (config/platform.json has null tag/account/keys), so these cells stay blank and flagged (FLG-022).
- **Per-product commission rate:** Table 1 is public but the listings' own category membership is not officially confirmed, so no per-product rate is stated (FLG-021; PF-38).
- **Whether the three redirect destinations are the products the owner intended:** needs owner input (FLG-002/FLG-027/FLG-035). Observed destinations only.
- **AI-automation features (auto product research, auto content generation, click/conversion tracking, campaign optimization):** not built. The repository is a static, verified research/dashboard prototype (see FLG-007 and 71-F-05). No hosted backend, model-provider client or enabled credentials were found.
- **Live clicks/conversions/revenue:** no Associates account is configured; Amazon is the system of record, in-account only (FLG-010, FLG-012).

## Gates on the final tree (re-run 2026-11-16, all green)

| Gate | Result |
|---|---|
| `python3 scripts/build_site.py` | exit 0; idempotent (zero working-tree diff on re-run) |
| `python3 scripts/check_site.py` | **OK: 13 pages, 3 products, 52 sources, 86 flags** |
| `python3 tools/verify_site.py` | **VERIFY PASS · 75 pages · 1,377 table rows · 1,169 with official source · 414 with flag · 89 with repo anchor · 0 advisories** |
| `python3 tools/link_report.py --strict` | **exit 0** (no dangling source/flag references) |
| `python3 scripts/build_sitemap.py --check` | **exit 0 — 70 pages** |
| `python3 scripts/check_all_links.py` | **121 HTML pages, 106 distinct external URLs, 0 errors** |
| Conflict-marker / secrets sweep | **0 / 0** |

## Conclusion

Every load-bearing claim on the site was re-confirmed against its official page today. No new irregularities were found. All previously registered flags remain published, non-blocking, on the Flagged for review page (`flagged.html`) with official source links. No value was inferred or filled; unverifiable cells remain blank.

## Sources used (all official, fetched live 2026-11-16)

1. https://affiliate-program.amazon.com/help/operating/agreement — Amazon Associates Program Operating Agreement (§5 disclosure, §6 breach, Schedule 1 US-only)
2. https://affiliate-program.amazon.com/help/operating/policies — Amazon Associates Program Policies (§2(b) tag/price rules, §6(t) reviews via API, §6(w), §6(y), CIS §2(e))
3. https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ — Standard Commission Income Statement Table 1 (public)
4. https://link.amazon/B04G1MEwY — submitted short link (→ dp/B0CDY277D3)
5. https://www.amazon.com/dp/B04G1MEwY — direct-ID control (Page Not Found)
6. https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers — FTC Disclosures 101 (November 2019)

No third-party page was used as evidence.
