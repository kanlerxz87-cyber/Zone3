# Repo review — session `21acd3c0`, 2026-11-14 (line-by-line tree audit)

**Reviewed at:** `main` @ `e8e3e9d` (PR #56 merge) plus this session's claim commit.
**Method:** every directory and file class enumerated; canonical registers read field-by-field
(`data/products.json`, `data/sources.json`, `data/flags.json`); all four local gates re-run;
cross-checks between registers, generated pages and the live web recorded in
[`21acd3c0-verification-log.md`](21acd3c0-verification-log.md). Links are given for manual review.

---

## 1. What the repository is

A static GitHub Pages site (source `main` `/`, `.nojekyll`) for an Amazon-Associates affiliate
marketing platform: product research records for the three submitted links, pricing/reviews/
competition analysis (with everything unverified kept blank and flagged), an SEO marketing
section (product spotlights, comparison, buying guide), link/campaign tracking ledgers (empty by
design until a tag exists), compliance documentation, and an audit trail of ~20 agent sessions in
`COORDINATION.md` (~2,750 lines).

## 2. Inventory by directory (all files accounted for; 258 files at review time)

| Path | Purpose | Review result |
|---|---|---|
| `index.html` + root pages (`products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `executive-summary.html`, `flagged.html`, `sources.html`, `verification.html`, `dashboard.html`, `marketing.html`, `disclosure.html`, `air-fryers.html`, `landing-prior.html`, `analysis.html`, `flagged-for-review.html`, `404.html`) | The 12-page canonical site + legacy redirect stubs (`analysis.html`, `disclosure.html`, `flagged-for-review.html`, `air-fryers.html`, `categories/home-kitchen-air-fryers.html` redirect to current pages) | OK — all pass V1–V7 in `tools/verify_site.py` |
| `<section>/index.html` (products, pricing, reviews, content, campaigns, executive-summary, flagged, sources, dashboard, marketing, niches, methodology, requirements, repo-review, compliance, commission, agent-terms, category) | Directory-style aliases of the sections (used by the sitemap's `/section/` URLs) | OK |
| `marketing/` | SEO content: `index`, `briefs`, `buying-guide`, `comparison`, 3 product spotlight pages | OK — grep-verified to contain no price/rating values (see verification log §B) |
| `data/` | Canonical registers: `products.json` (3 rows), `sources.json` (48 sources), `flags.json` (49 flags), `policy_facts.json`, plus `z3/` sub-register and snapshot JSONs from sessions c4e71983/51fcb80d | OK — schema holds; every non-null fact carries a source ID (checked by `scripts/check_site.py`); P1–P3 fact fields all `null` by rule |
| `scripts/` (`build_site.py`, `check_site.py`, `check_all_links.py`, `build_marketing.py`, `build_sitemap.py`, `update_data_2026_11_14.py`) | Generator + gates | OK — gates re-run green this session |
| `tools/` (`verify_site.py`, `link_report.py`, `build_site.py`, `amazon_intake.py`, `niche_score.py`) | Secondary verifier + intake/scoring pipeline (automation scaffold for the research→content→tracking loop) | OK — `verify_site.py` and `link_report.py --strict` exit 0 |
| `research/`, `docs/` | Per-session verification records, repo reviews, markdown executive summaries | OK — additive, session-namespaced |
| `sessions/` (3c886b62, 03bbd050, 588693c9, f1b7da46) | Other sessions' scoped workspaces (own pages, data, docs) | OK — non-overlapping scopes; not merged into root registers |
| `archive/` (26634cd5, 66a80e53, c4e71983) | Preserved earlier sessions' whole sites with `ARCHIVE_NOTE.md` (no-clobber policy) | OK |
| `config/platform.json`, `assets/` (css/js), `robots.txt`, `sitemap.xml`, `.nojekyll`, `.gitignore` | Config, styles, SEO plumbing | OK — robots.txt points at the sitemap; .gitignore covers build scratch and secrets |
| `COORDINATION.md`, `README.md`, `EXECUTIVE-SUMMARY.md` | Shared task board, repo map, executive summary | OK in content; see irregularity 21-F-01 re board readability |

## 3. Gates re-run by this session (all green)

| Gate | Result |
|---|---|
| `python3 tools/verify_site.py` | VERIFY PASS · 69 pages · 1169 rows · 967 sourced · 346 flagged · 82 anchored · V1–V7 pass |
| `python3 tools/link_report.py --strict` | exit 0 |
| `python3 scripts/check_all_links.py` | 115 HTML pages · 104 external URLs · 0 errors |
| `python3 scripts/check_site.py` | OK · 12 pages · 3 products · 48 sources · 49 flags |

## 4. Line-by-line data findings

- `data/products.json` — 3 products (P1–P3). Each row: submitted URL + 9-char code recorded;
  `asin: null`; all fact fields `null`; 5 flags and 7 sources each; PR #26's observed readings
  quarantined under `observed_2026_11_14` (FLG-038). **No inferred values found.**
- `data/sources.json` — 48 sources (S01–S55 with gaps). Hosts are official (amazon.com,
  affiliate-program.amazon.com, sell.amazon.com, sellercentral.amazon.com, ftc.gov) plus the
  repo's own github.com/api.github.com records and one explicitly-marked third-party page (S17,
  not used as a fact). **No third-party content used as a fact.**
- `data/flags.json` — 49 flags (FLG-001…038, V-*, E-*). All non-blocking; all published on
  [flagged.html](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) with source links.
- `data/policy_facts.json` — quoted policy text with section references (see verification log §C
  for what this session did and did not re-fetch).

## 5. Irregularities flagged for review (non-blocking)

| ID | Severity | Finding | Where to look |
|---|---|---|---|
| 21-F-01 | Info | `COORDINATION.md` duplicates several Parts verbatim (e.g. "PART C — a53a7e52" appears twice; "Part E — 252122ff" and the "G Session registry" block each appear twice) — merge artifacts from earlier add/add resolutions. Board state is hard to read as one view (corroborates H-F-02). Not edited: the no-clobber rule protects other sessions' records | https://github.com/kanlerxz87-cyber/Zone3/blob/main/COORDINATION.md |
| 21-F-02 | Info | `sitemap.xml` lists both the root URL (`''`) and `index.html` — the same page twice | https://kanlerxz87-cyber.github.io/Zone3/sitemap.xml |
| 21-F-03 | Info | Redirect stub `categories/home-kitchen-air-fryers.html` exists but is not in the sitemap (harmless for SEO; arguably correct) | https://github.com/kanlerxz87-cyber/Zone3/blob/main/categories/home-kitchen-air-fryers.html |
| 21-F-04 | Info | Session workspaces (`sessions/3c886b62/*`, `sessions/03bbd050/`) are included in the public sitemap — other sessions' sub-sites are publicly discoverable. Owner may want them indexed or excluded | https://kanlerxz87-cyber.github.io/Zone3/sitemap.xml |
| 21-F-05 | Low | Live page widgets showed a price ($69.97) for `dp/B0CDY277D3` that differs from the register's same-day snapshot ($79.93). Confirms prices are volatile; the site correctly publishes none as facts (FLG-004/022/038) | https://www.amazon.com/dp/B0CDY277D3 |

Nothing in this review blocks publishing. No file outside this session's scope was changed.
