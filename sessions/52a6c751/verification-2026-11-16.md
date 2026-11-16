# Session 52a6c751 — post-integration verification record (2026-11-16)

Scope: read-only verification of load-bearing claims against official pages, plus a read-only check of the
public tree for values that Amazon's policies restrict. No shared output was edited by this session.

Repository state checked: `main` at `90046e6` (gates) and re-checked at `a5d64fd` (live Pages build still running at the time of writing).

## 1. Gates (run on `main` at `90046e6`)

| Gate | Command | Result |
|---|---|---|
| Site checker | `python3 scripts/check_site.py` | OK — 24 pages, 3 products, 62 sources, 97 flags |
| Verifier | `python3 tools/verify_site.py` | PASS — 100 pages, 1,649 table rows, 1,410 with an official source, 450 with a flag, 99 with a repo anchor; checks V1–V7 |
| Link report | `python3 tools/link_report.py --strict` | exit 0 |
| Sitemap | `python3 scripts/build_sitemap.py --check` | exit 0 — 95 pages checked, 0 extra entries |

Note: the verifier counts a row as "with an official source" by checking for a link. It does not check whether
the linked page supports the cell. A row can pass V4 and still carry a restricted value (see F-01 and F-02).

## 2. Live official-source re-fetch (all fetched 2026-11-16 by this session)

| ID | Claim | Official source fetched | Result |
|---|---|---|---|
| 52A-V01 | `link.amazon/B04G1MEwY` opens listing `B0CDY277D3` (CHEFMAN 6 Qt Dual Basket) | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) → [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | **Confirmed** — page title "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven…". Observed destination only; intended match not established (FLG-001). |
| 52A-V02 | `link.amazon/B02NbDxp3` opens `B09B7SB46R` (Emeril Lagasse 26QT) | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) → [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | **Confirmed** — title "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven…". Observed destination only. |
| 52A-V03 | `link.amazon/B00hJ57DV` opens `B08DKYBTPH` (Chefman 8 Qt TurboFry) | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) → [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | **Confirmed** — title "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1…". Observed destination only. |
| 52A-V04 | Operating Agreement header date | [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | **Confirmed** — "Updated: October 15, 2025". §5 sentence not re-fetched by this session (see §4). |
| 52A-V05 | Program Policies header date | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | **Observed** — "Updated: April 14, 2026". The repo's cited date is checked in §3. |
| 52A-V06 | Policy 2(b): prices and availability only if Amazon serves the link, or via Creators/PA API; remove expired limited-time promotions | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (chunk 3) | **Confirmed verbatim** — "Your Site may only show prices and availability if: (a) we serve the link … or (b) you obtain Product pricing and availability data via Creators API or PA API…"; "You must remove from your Site any links and related references to limited time promotions as soon as that promotion … ends." |
| 52A-V07 | Policy 6(t): reviews and star ratings only via Creators/PA API | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (chunk 5) | **Confirmed verbatim** — "You will not display or otherwise use any of our customer reviews or star ratings … unless you have obtained a link … through Creators API or PA API…" |
| 52A-V08 | Standard Commission Table 1: Kitchen 4.50%; All Other Categories 4.00%; Bounty Prime Free Trial / Paid $12.00; Prime Video Free Trial $2.00; First Stream $5.00; Stream $0.25 | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) (chunk 0) | **Confirmed as printed** |
| 52A-V09 | ASIN is a 10-character identifier | [Creators API GetItems — ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) (chunk 1) | **Confirmed** — "ASIN — 10-Character alphanumeric unique identifier assigned by Amazon." |
| 52A-V10 | FTC: disclose where it is "hard to miss"; disclosures in an ABOUT ME page, at the end of posts, or behind MORE are likely to be missed; "You can't talk about your experience with a product you haven't tried." | [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | **Confirmed** — dated "November 2019" on the page |

## 3. Public-tree sweep for restricted values (read-only)

Method: grep over every tracked `.html` / `.md` / `.json` file outside `archive/`, for the nine listing prices
observed in §2 and for rating patterns (`x.x out of 5`, `x.x (n ratings)`). Amazon's published program rates and
bounty amounts are not restricted under 2(b) or 6(t) and are excluded from the findings.

| # | File | Line | What is shown | Rule | Status on `main` |
|---|---|---|---|---|---|
| F-01 | `docs/index.html` | 65–67, 86, 95, 104, 124 | Live page shows "Avg. rating 4.3 / 5", "39.9K reviews combined", "Price range (observed) $79.91–$149.99", "List prices $99.99–$209.99", "8K+ bought in past month", and per-product star ratings 4.2★ / 4.3★ / 4.4★ | 2(b) prices; 6(t) ratings and reviews | **Restricted values displayed publicly** (confirmed live after PR #119, see §6) |
| F-02 | `docs/content.html` | ~58 | "Observed price: $79.93 (list $99.99, 'Limited time deal' at capture)" | 2(b); remove expired promotions | **Restricted value and promotion mention displayed publicly** |
| F-03 | `docs/sources.html` | 95, 112, 129 | "Price $79.93 · list $99.99 · 4.2★ · 4.8K reviews · 1K+ bought/month · deal badge · other offer $57.45" (and the same pattern for the other two listings) | 2(b) / 6(t) | **Restricted values displayed publicly** — prices, star ratings, review counts, purchase counts and competitor offers |
| F-04 | `sessions/3c886b62/index.html` (and the other `sessions/3c886b62/*.html` and `docs/*.md` files that match the sweep) | notice at lines 26–34 | Prices, star ratings and review counts remain on the page under a notice that it "is not a compliant product display" | 2(b) / 6(t) | **Restricted values displayed publicly** — same as 71-F-04 |
| F-05 | `site/evidence.html` | ~72 | Star ratings and review counts of OTHER ASINs quoted in the verification note (e.g. "4.41,393", "4.43,727") | 6(t) | **Ratings displayed publicly** (quoted for other products; still a display of star ratings) |

`docs/` and `sessions/` are in the public sitemap. The restricted values above are therefore publicly reachable on GitHub Pages.

## 4. Not verified by this session (stated, not asserted)

- The Operating Agreement §5 disclosure sentence was not re-fetched this session. Earlier sessions recorded it verbatim (98-V01, I2-V01).
- The 180-day / three-sale window and Creators API eligibility text were not re-fetched.
- No live Amazon account, tag, or Creators/PA API access exists in this repo, so no price or rating can be lawfully displayed from this build.

## 5. Irregularities (published as flags for owner review; none edit a shared output)

See the board Part for the change requests. Severity: F-01…F-04 **High** (Policy 2(b)/6(t) display; affects Associate account standing under OA §2); F-05 **Medium**.

## 6. Post-merge live check (2026-11-16, after PR #119)

| Check | Result |
|---|---|
| PR #119 (session `52a6c751` record) | MERGED 2026-11-16T19:03:40Z, merge commit `ced0713` |
| GitHub Pages build for `ced0713` | `built` at 19:04:05Z |
| Live `/flagged.html` (fetched 2026-11-16) | Renders: "97 entries: 3 critical, 17 high, 26 medium, 29 low, 22 info". **None of 52A-F-01…05 is listed.** The brief requires irregularities to be published on the Flagged for Review page. |
| Live `/docs/index.html` (fetched 2026-11-16) | Renders the observed price range, the list-price range, the average star rating, the combined review count, "bought in past month", and per-product star ratings. Confirms F-01 on the public site. |

Requests raised: CR-52A-4 (publish 52A-F-01…05 on the Flagged for Review page) and CR-52A-1 (remove the restricted values).
