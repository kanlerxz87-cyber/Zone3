# c3dbcc40 — verification record (2026-11-14)

Scope: tasks C3-T1 and C3-T2 on `COORDINATION.md`. Base `f618a53` (main, PR #72). Sources are official Amazon pages fetched live this session. No third-party page is used as evidence.

## 1. Gate re-run on the base tree (C3-T1)

| Gate | Command | Result |
|---|---|---|
| Site check | `python3 scripts/check_site.py` | exit 0 · 12 pages · 3 products · 51 sources · 66 flags |
| Build + provenance gate | `python3 tools/build_site.py` | exit 0 |
| HTML audit | `python3 tools/verify_site.py` | VERIFY PASS · 70 pages · 1223 table rows · 1022 with official source · 388 with flag · 0 advisories |
| Provenance coverage | `python3 tools/link_report.py --strict` | exit 0 |
| Link check | `python3 scripts/check_all_links.py` | 116 pages · 105 distinct external URLs · 0 errors |

The build regenerated `sitemap.xml`. The regenerated file lists five pages that the committed file lacks: `analysis.html`, `disclosure.html`, and three others. That change was reverted here because `sitemap.xml` is a shared output reserved for the integration session. See irregularity C3-F-01.

## 2. Live re-fetch of the three submitted links (C3-T2)

| Submitted link | Final URL after redirect (ASIN) | Live page title (as fetched) | Matches repo record? |
|---|---|---|---|
| https://link.amazon/B04G1MEwY | https://www.amazon.com/dp/B0CDY277D3 | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows …" | Yes — B0CDY277D3 appears in `data/z3/products.json`, `pricing.json`, `reviews.json` |
| https://link.amazon/B02NbDxp3 | https://www.amazon.com/dp/B09B7SB46R | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven …" | Yes — B09B7SB46R recorded in the repo's Emeril row |
| https://link.amazon/B00hJ57DV | https://www.amazon.com/dp/B08DKYBTPH | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 …" | Yes — B08DKYBTPH recorded in the repo's Chefman 8 Qt row |

Control check: `https://www.amazon.com/dp/B04G1MEwY` (the raw 9-character token used as an ASIN) returns Amazon's "Page Not Found" page. The repo's claim that the tokens are not ASINs is therefore consistent with the live site.

What this does not establish: that these three listings are the products the requester intended. Only the redirect destination is verified. Whether the short-link owner meant these listings is not confirmed by any official source. That item stays flagged, as the repo already records.

Official sources used (fetched 2026-11-14):
- https://link.amazon/B04G1MEwY → https://www.amazon.com/dp/B0CDY277D3
- https://link.amazon/B02NbDxp3 → https://www.amazon.com/dp/B09B7SB46R
- https://link.amazon/B00hJ57DV → https://www.amazon.com/dp/B08DKYBTPH
- https://www.amazon.com/dp/B04G1MEwY (control; Page Not Found)

## 3. Irregularities (non-blocking; for manual review)

- **C3-F-01 — sitemap drift.** The committed `sitemap.xml` omits five pages that the build emits (`analysis.html`, `disclosure.html`, and three more). Shared output. Owner: integration session. Action: regenerate `sitemap.xml` during integration. Not edited by this session.
- **C3-F-02 — intent not established.** Same as the repo's existing flag for the short links. The redirect destinations are verified; the link owners' intent is not. No change in status.
