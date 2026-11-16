# Session a0ffcab0 — repo review, live re-check, restricted-value scan (2026-11-16)

Branch `arena/a0ffcab0-zone3`, base `add6525`, `main` at `609dc76` when the work was checked.
Task IDs `A0-Tn` and irregularity IDs `A0-F-nn` are namespaced; see the A0 Part in `COORDINATION.md`.

> Rule followed for this record: no Amazon price, star rating, review count or sales badge is
> quoted here. Where a restricted value exists, the file and line are named instead. Program
> Policies 2(b) and 6(t) apply to this document too.

## 1. Gates on `main` (run before any change, then again after)

| Gate | Command | Before this session's edits | After this session's edits |
|---|---|---|---|
| Site check | `python3 scripts/check_site.py` | OK · 13 pages · 3 products · 52 sources · 86 flags | OK · 13 pages · 3 products · 52 sources · **92 flags** |
| Row provenance | `python3 tools/verify_site.py` | VERIFY PASS · 83 pages · 1,482 rows · 1,258 official · 439 flag · 89 repo anchor | VERIFY PASS · 83 pages · 1,488 rows · 1,264 official · 440 flag · 89 repo anchor |
| Link report | `python3 tools/link_report.py --strict` | exit 0 | exit 0 |
| External + internal links | `python3 scripts/check_all_links.py` | 129 HTML pages · 116 external URLs · 0 errors | same |
| Sitemap | `python3 scripts/build_sitemap.py --check` | covers every live page; 0 extra | same (see §5, sitemap) |
| Reader site | `python3 tools/i2_gate.py` | PASS · 8 pages · 105 rows · 89 sourced · 16 blanks | same |
| Generator idempotence | `build_site.py`, `build_marketing.py`, `build_i2_site.py` | **not idempotent**: six `marketing/*.html` pages were one nav line behind (A0-F-04) | idempotent after regeneration |

Gate exit codes were read from each command directly, not through a pipe.

## 2. Repo review, line by line (read-only except where stated)

| # | Area | Found | Verdict |
|---|---|---|---|
| R1 | Board | `COORDINATION.md` 5,464 lines before this session; 93 "in progress" strings, many from closed sessions | A0-F-06 (Info) |
| R2 | Branch state | Local branch was at `add6525`; `main` had moved to `b38d96a` (PR #101) and then `609dc76` (PR #103). Fast-forwarded before any work | fine |
| R3 | Conflict | Append-append conflict in `COORDINATION.md` on rebase. Resolved by a merge, keeping main's text verbatim and appending this Part. No conflict markers were committed or pushed | fine |
| R4 | Live product links | Read 2026-11-16, see §3 | confirmed |
| R5 | Restricted values on public output | Scan in §4 | **A0-F-01, A0-F-02 (High)** |
| R6 | Provenance gate | `verify_site` passes flagged and repo-anchored rows | **A0-F-03 (Medium)** |
| R7 | Generator drift | `marketing/*.html` one nav line behind `scripts/build_site.py` (new `/site/` entry) | **A0-F-04 (Low, fixed)** |
| R8 | Sitemap | `scripts/build_sitemap.py` (without `--check`) would drop five "Moved" redirect stubs that main's committed sitemap lists. Not applied; main's canonical sitemap kept (decision 98-T6) | Info, no flag |
| R9 | Secrets / conflict markers | Not re-scanned in this pass beyond the merge check in R3 | open for next integration |

## 3. Live re-check of official sources (fetched 2026-11-16, this session)

Every row was read from the page itself. No aggregator and no earlier capture was used.

| ID | Claim | Official page read | Result |
|---|---|---|---|
| A0-V01 | `link.amazon/B04G1MEwY` opens the listing for ASIN B0CDY277D3 | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) → [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | **Confirmed.** Title "CHEFMAN 6 Quart Dual Basket Air Fryer Oven…"; breadcrumb ends Air Fryers |
| A0-V02 | `link.amazon/B02NbDxp3` opens ASIN B09B7SB46R | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) | **Confirmed.** Title "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven…" |
| A0-V03 | `link.amazon/B00hJ57DV` opens ASIN B08DKYBTPH | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) | **Confirmed.** Title "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1…" |
| A0-V04 | The 9-character code is not an ASIN: `amazon.com/dp/B04G1MEwY` gives Amazon's page-not-found page | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) | **Confirmed.** Title "Page Not Found" |
| A0-V05 | ASIN = 10-character alphanumeric identifier | [Creators API GetItems, ItemIdType](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) | **Confirmed verbatim** |
| A0-V06 | Operating Agreement: "Updated: October 15, 2025"; §5 disclosure sentence "As an Amazon Associate I earn from qualifying purchases."; §6 — any §5 violation is a material breach | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | **Confirmed verbatim** |
| A0-V07 | Program Policies: "Updated: April 14, 2026"; 2(b) tag as URL parameter; no per-visitor sub-tags; prices and availability only if Amazon serves the link or via Creators/PA API | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | **Confirmed verbatim** |
| A0-V08 | Program Policies 6(s) no artificial clicks; 6(t) no reviews or star ratings except via Creators/PA API; 6(w) shorteners must not make the Amazon destination unclear; 6(y) no price tracking or alerting | same | **Confirmed verbatim** |
| A0-V09 | Standard Commission Table 1 rows: Luxury Beauty 10.00%; Physical Books, Kitchen, Automotive 4.50%; All Other Categories 4.00% | [Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | **Confirmed as printed.** Category rates only; not attached to any product |
| A0-V10 | Bounty rows: Prime Free Trial, Prime Paid Membership, Prime for Young Adults (trial and paid), Prime Access and Prime Sign Up at Checkout $12.00 each; Prime Video free trial $2.00; Prime Video First Stream $5.00; Prime Video Stream $0.25 | same | **Confirmed as printed** |
| A0-V11 | FTC Disclosures 101 (dated November 2019): disclose "financial, employment, personal, or family relationship"; "Place it so it's hard to miss"; disclosures "likely to be missed" on profile pages or after MORE; "You can't talk about your experience with a product you haven't tried." | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | **Confirmed verbatim** |

Not re-checked in this pass: policy sections not listed above, including the Operating Agreement §7 disclaimer. Those were verified in earlier records (see `research/1f1b8bd2-verification-log.md`). No price, rating or review count was read for use on the site.

## 4. Restricted-value scan (A0-T4)

Pattern set (case-sensitive, over every tracked text file): star-rating glyphs, "bought/month", "K reviews", "N out of 5", currency values in the observed-price format, and "Observed price/rating" labels. A match means the file contains a value that Program Policies 2(b) or 6(t) restrict. It does not by itself show that the value is a display.

| Location | Files | Status | Owner | Action this session |
|---|---|---|---|---|
| `docs/` (on sitemap; linked from root) | 5 HTML + 1 Markdown carry values; 2 further Markdown files belong to other sessions | open | shared output | **Flagged, not edited** (A0-F-01). Owner decision |
| `sessions/` | 19 files | open | other sessions | Change request (A0-F-02). 20 sessions URLs are on the sitemap |
| `archive/` | 16 files | open | other sessions | Change request (A0-F-02) |
| `research/` | 4 files | open | other sessions | Change request (A0-F-02) |
| root `data/` snapshots | 3 JSON files (`c4e71983-*`, `z3-51fcb80d-snapshot.json`) | open | other sessions | Change request (A0-F-02) |
| `flagged.html`, `data/flags.json`, `COORDINATION.md`, `docs/flagged.html` | quote the pattern in flag or board prose | allowed (flag and board prose) | — | none |
| `tools/i2_gate.py`, `scripts/update_data_2026_11_14.py` | pattern lists in code | allowed (code, not display) | — | none |
| `site/`, root product pages, `marketing/` product pages | none that display a restricted value | pass | — | none |

Root `sources.html` and the `site/` reader site were checked and show no restricted values. Session `ab3ed329` (PR #98) had already cleaned the root sources page and the public data files.

## 5. Changes made in this session

| File | Change | Why |
|---|---|---|
| `data/flags.json` | six entries appended: A0-F-01 (High), A0-F-02 (High), A0-F-03 (Medium), A0-F-04 (Low, fixed), A0-F-05 (Info), A0-F-06 (Info) | publish irregularities on the Flagged page |
| `flagged.html` | regenerated by `scripts/build_site.py` | shows the six new entries |
| `index.html`, `executive-summary.html` | regenerated by `scripts/build_site.py` | flag count 86 → 92 in generated text |
| `marketing/index.html`, `buying-guide.html`, `comparison.html`, `product-1-…`, `product-2-…`, `product-3-…` | regenerated by `scripts/build_marketing.py`; each gained one nav link (`../site/index.html`) | A0-F-04 |
| `EXECUTIVE-SUMMARY.md` | flag count 86 → 92 and severity counts (3 critical, 16 high, 24 medium, 29 low, 20 info); update block for this session | keep the summary consistent with the register |
| `research/a0ffcab0-record.md` | this record | |
| `COORDINATION.md` | claim, addendum, A0 Part | protocol |

Not changed: any file in `docs/`, `sessions/`, `archive/`, `research/`, `data/` (other than `flags.json`), `sitemap.xml` (main's canonical version kept), `site/**`, `tools/**`, `scripts/**`.

## 6. Change requests (logged for owners; not edited here)

- **To the owner (A0-F-01):** choose between redacting the `/docs/` values or removing `/docs/` from the public sitemap and branch. The redaction changes the derived analysis, so it needs a decision first.
- **To the owner (A0-F-02):** the same two options for `sessions/`, `archive/`, `research/` and root data snapshots. Any of these can be removed from the published branch by a single owner decision.
- **To `tools/verify_site.py` (A0-F-03):** split row types as described in the flag; fail V4 on any factual row without an official link.
- **To `scripts/build_sitemap.py`:** either remove the five "Moved" redirect stubs from its generator output or from the canonical sitemap, so that the two generators agree.

## 7. Sources used in this record

- Amazon Associates Program Operating Agreement — https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies — https://affiliate-program.amazon.com/help/operating/policies
- Standard Commission Income Statement, Table 1 — https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ
- Creators API GetItems, ItemIdType parameter — https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items
- FTC Disclosures 101 for Social Media Influencers — https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Short links — https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV
- Product pages reached by the short links — https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH
- Page-not-found check — https://www.amazon.com/dp/B04G1MEwY
- Live pages checked for the restricted-value issue — https://kanlerxz87-cyber.github.io/Zone3/docs/sources.html

## 8. Not done, and why

- The `/docs/` redaction (A0-F-01) and the archive decisions (A0-F-02) were not made here. Both change what the public site shows and require the owner's choice (see §6).
- No price, rating, review, or sales figure was added anywhere. None is verifiable through an eligible route (Program Policies 2(b), 6(t)).
- No live click, conversion or revenue data exists; none was invented.
