# Session `1dddf8c0` — verification and remediation record (2026-11-16)

Branch: `arena/1dddf8c0-zone3` · base: `add6525` (merge of PR #99, session `1f1b8bd2`).
Role: final integration takeover — independent official-source re-verification, repo
review, and remediation of the open compliance exposure (AB-F-01, 71-F-04).

## 1dd-T1 — Independent line-by-line re-verification from official sources

Every claim below was fetched live by this session on 2026-11-16. Page URL is the source.

| # | Claim | Result |
|---|---|---|
| 1dd-V01 | `link.amazon/B04G1MEwY` redirects to `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven | **Confirmed** — live fetch today; title and Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers breadcrumb observed |
| 1dd-V02 | `link.amazon/B02NbDxp3` redirects to `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French Door air fryer toaster oven | **Confirmed** — live fetch today; same breadcrumb |
| 1dd-V03 | `link.amazon/B00hJ57DV` redirects to `amazon.com/dp/B08DKYBTPH` — Chefman 8 Qt TurboFry 4-in-1 | **Confirmed** — live fetch today; same breadcrumb |
| 1dd-V04 | `amazon.com/dp/<each 9-char token>` returns Amazon "Page Not Found" | **Confirmed ×3** — `/dp/B04G1MEwY`, `/dp/B02NbDxp3`, `/dp/B00hJ57DV` all served the Page Not Found page |
| 1dd-V05 | Operating Agreement: "Updated: October 15, 2025"; §5 disclosure "As an Amazon Associate I earn from qualifying purchases."; §6 material-breach clause for §5 violations | **Confirmed verbatim** — [OA](https://affiliate-program.amazon.com/help/operating/agreement) |
| 1dd-V06 | Program Policies: "Updated: April 14, 2026"; CIS §1 session window (24 h / 89-day cart / 180-day fulfilment); §2(e) Redirecting Link; §5 commission-limitations; §6 payment ~60 days, US minimums $10 / $10–$2,000 / $100 + $15 check fee | **Confirmed verbatim** — [Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| 1dd-V07 | PR 2(b): prices/availability only if Amazon serves the link or via Creators/PA API | **Confirmed verbatim** — [Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| 1dd-V08 | PR 6(s) artificial clicks; 6(t) reviews/star ratings only via Creators/PA API; 6(v) cloaking/Redirecting Links; 6(w) link-shortener clarity; 6(y) no price tracking/alerting | **Confirmed verbatim** — [Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| 1dd-V09 | PR 5: Special Links/Program Content may not be used to develop machine-learning models without Amazon's express prior written approval; IP License 1 excludes data mining/robots | **Confirmed verbatim** — [Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| 1dd-V10 | Standard Commission Table 1: Luxury Beauty 10.00%; Physical Books/Kitchen/Automotive 4.50%; All Other Categories 4.00%; bounties $12/$2/$5/$0.25 | **Confirmed row-for-row** — [CIS Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) (category rates only; never assigned to a product) |
| 1dd-V11 | Creators API: 4 operations (SearchItems, GetItems, GetVariations, GetBrowseNodes); prerequisite "at least 10 qualifying sales within the past 30 days" | **Confirmed verbatim** — [Creators API intro](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| 1dd-V12 | ASIN = "10-Character alphanumeric unique identifier assigned by Amazon" (ItemIdType, default ASIN; 10-char examples) | **Confirmed verbatim** — [GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter) |
| 1dd-V13 | FTC Disclosures 101 (November 2019): material-connection disclosure, clear and hard-to-miss placement | **Confirmed** — [FTC](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) |
| 1dd-V14 | FTC Consumer Reviews and Testimonials Rule Q&A: rule "went into effect on October 21, 2024"; §465.2/465.4/465.6/465.7/465.8; influencer-relationship disclosures remain under the FTC Act / Endorsement Guides | **Confirmed verbatim** — [FTC Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers) (register S59) |

**Not re-verified, and why:** observed price / rating / review-count / demand values as
product facts (barred by 2(b)/6(t) without API access — deliberate refusal, not a gap);
per-product commission rates (Amazon publishes by category only); live clicks / conversions
(no Associates account configured); whether the three redirect destinations are the
submitter's intended products (needs owner input, FLG-002/027).

## 1dd-T2 — Repository review, line by line

| Check | Result |
|---|---|
| `python3 scripts/check_site.py` | **OK** — 13 pages, 3 products, 52 sources, 86 flags |
| `python3 tools/verify_site.py` | **VERIFY PASS** — 75 pages, 1,377 rows, 1,165 with official source, 315 with flag, 55 repo-anchored; V1–V7 all pass |
| `python3 tools/link_report.py --strict` | **exit 0** |
| `python3 scripts/check_all_links.py` | **121 HTML pages, 106 distinct external URLs, 0 errors** |
| `python3 scripts/build_sitemap.py --check` | **exit 0** — 70 pages covered |
| Generator idempotency (`scripts/build_site.py`, `tools/build_site.py`, `sessions/3c886b62/tools/build.py`) | **re-run clean** after remediation |
| Git hygiene (`git diff --check`, conflict markers, secrets) | **0 / 0** |
| Brief-deliverable reachability | suggestions, decision center, executive summary, content topics, marketing hub, flagged, products, pricing, reviews, campaigns, sources, air-fryers all present and linked from the landing page |

## 1dd-T3 — Compliance remediation (public restricted-value exposure)

**Basis.** Amazon Associates Program Policies Participation Requirements 2(b) (prices and
availability only if Amazon serves the link or the data comes via Creators/PA API) and 6(t)
(customer reviews and star ratings only via Creators/PA API), re-read verbatim today
([Policies](https://affiliate-program.amazon.com/help/operating/policies)). This closes
AB-F-01 and 71-F-04, whose requested remediation was to remove the restricted values from
public output rather than rely on warnings.

**What was done (86 files):**

- `sessions/3c886b62/data/products.json` — 22 restricted field values (prices, list prices,
  unit prices, badges, lowest other offers, ratings, rating counts, demand signals) withheld
  at the data layer, with the official source links and flag references preserved.
- `sessions/3c886b62/tools/build.py` — renderers patched to be withheld-safe, so
  regeneration cannot restore the values (`money()`, `discount_depth()`, comparison,
  analysis, category and product-page renderers).
- Archive pages and records under `docs/`, `sessions/03bbd050/`, `sessions/3c886b62/`,
  `research/` and the frozen `archive/c4e71983/` copy — every observed price, list price,
  unit price, star rating, review count, demand figure, promotion badge and value derived
  from them replaced with an explicit "Withheld" marker. Row labels, source links and flag
  references kept on every row; narrative rewritten to stay true without the figures.
- Root data files `data/c4e71983-commercial-snapshot.json`, `data/c4e71983-competitors.json`,
  `data/z3-51fcb80d-snapshot.json` and the flag registers `data/flags.json`,
  `sessions/3c886b62/data/flags.json` — values withheld.
- Regeneration: `sessions/3c886b62/tools/build.py`, `scripts/build_site.py`,
  `tools/build_site.py` re-run; `sessions/3c886b62/.nojekyll` regenerated.
- Tooling kept for audit: `sessions/1dddf8c0/remediate_restricted_values.py` and
  `sessions/1dddf8c0/remediate_restricted_values_phase2.py`.

**Residual exposure (deliberate, flagged):** `COORDINATION.md` — the shared governance
ledger — retains historical observed values inside prior sessions' records. It is an
append-only coordination record rather than a site content page; redacting it would rewrite
other sessions' merged work. Raised as `1dd-F-01` for an owner decision.

**Post-remediation gates:** all green (table in 1dd-T2), re-run immediately before the PR.

## 1dd irregularities

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| 1dd-F-01 | Medium | `COORDINATION.md` retains historical observed price/rating/review figures inside prior sessions' verification records. It is the append-only coordination ledger, not a site content page; this session did not rewrite other sessions' merged records. | **Open, for review** — owner decision: accept the ledger as a historical audit record, or redact the figures across all Parts. Published on the Flagged for review page. |
