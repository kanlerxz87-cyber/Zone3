# COORDINATION.md — Shared Task Board

**Repo:** `kanlerxz87-cyber/Zone3` · **Pages site:** https://kanlerxz87-cyber.github.io/Zone3/
**Purpose:** Amazon affiliate marketing platform — product research, content generation, compliance, campaign tracking.

This file is the single shared coordination surface. Sessions claim rows here, work only inside
their claimed file scope, and record sources + verification + irregularities when done.

---

## Session Registry

| Session ID | Branch | Role | Status | Last heartbeat (UTC) |
| --- | --- | --- | --- | --- |
| `3c6cba43` | `arena/3c6cba43-zone3` | Build + Final integration + publish | active | 2026-11-13 22:45 |

> Claim-expiry rule: a claim older than 60 minutes with **no commits** may be taken over by another
> session; the takeover must be recorded in the Handoff Log below.

---

## Task Board

| # | Task | Status | Owner | File scope |
| --- | --- | --- | --- | --- |
| 1 | Link/ASIN verification of the 3 submitted product links | **in progress** | `3c6cba43` | `data/products.json`, `docs/verification-log.md` |
| 2 | Repo review (baseline audit of checkout) | unclaimed | — | `docs/repo-review.md` |
| 3 | Amazon Associates policy + compliance research (official sources) | unclaimed | — | `data/policies.json`, `docs/compliance.md` |
| 4 | Site scaffold (landing page + nav + shared CSS/JS dashboard) | unclaimed | — | `index.html`, `assets/*` |
| 5 | Category subpages + data tables (Products, Niche, Pricing, Reviews, Content, Campaigns) | unclaimed | — | `products/*`, `pricing/*`, `reviews/*`, `niches/*`, `content/*`, `campaigns/*` |
| 6 | Executive summary | unclaimed | — | `executive-summary.html`, `docs/executive-summary.md` |
| 7 | Flagged-for-Review page | unclaimed | — | `flagged/index.html`, `data/flags.json` |
| 8 | Methodology / automation architecture docs | unclaimed | — | `methodology/index.html`, `data/requirements.json` |
| 9 | Final integration: re-verify every table row, link-check build, push | unclaimed | — | whole tree |
| 10 | PR → `main`, merge, confirm GitHub Pages deploy | unclaimed | — | n/a (git + gh) |

---

## Handoff Log

| Time (UTC) | From | To | Task | Reason |
| --- | --- | --- | --- | --- |
| — | — | — | — | No handoffs. This board was created empty by the repo owner; no other session had claimed work at branch creation. |

---

## Change Requests (cross-scope edits)

| Requested by | Target file | Owner of target | Request | Resolution |
| --- | --- | --- | --- | --- |
| — | — | — | None pending. `3c6cba43` owns every scope in this run, so no cross-scope edits were needed. | — |

---

## Irregularities Flagged for Review

All items below are published on the site at **`/flagged/`** ("Flagged for Review").
They do **not** block the merge.

| Flag ID | Severity | Item | Detail | Verified against |
| --- | --- | --- | --- | --- |
| `FLG-001` | Critical | Product link 1 `https://link.amazon/B04G1MEwY` | `link.amazon` is not an Amazon Associates short-link domain; the only Amazon-owned affiliate short domains are `amzn.to` and regional equivalents. | https://affiliate-program.amazon.com/ |
| `FLG-002` | Critical | Product link 2 `https://link.amazon/B02NbDxp3` | Same domain irregularity as FLG-001. | https://affiliate-program.amazon.com/ |
| `FLG-003` | Critical | Product link 3 `https://link.amazon/B00hJ57DV` | Same domain irregularity as FLG-001. | https://affiliate-program.amazon.com/ |
| `FLG-004` | Critical | ASIN `B04G1MEwY` is 9 characters | Amazon ASINs are 10-character identifiers. 9 chars cannot be a valid ASIN. `https://www.amazon.com/dp/B04G1MEwY` → "Page Not Found" (HTTP 404 error page). | https://www.amazon.com/dp/B04G1MEwY |
| `FLG-005` | Critical | ASIN `B02NbDxp3` is 9 characters | As FLG-004. `https://www.amazon.com/dp/B02NbDxp3` → "Page Not Found". | https://www.amazon.com/dp/B02NbDxp3 |
| `FLG-006` | Critical | ASIN `B00hJ57DV` is 9 characters | As FLG-004. `https://www.amazon.com/dp/B00hJ57DV` → "Page Not Found". | https://www.amazon.com/dp/B00hJ57DV |
| `FLG-007` | High | `link.amazon/B04G1MEwY` redirect landed on an unrelated product | Followed by the fetch tool; it resolved to `https://www.amazon.com/dp/B0CDY277D3` (a CHEFMAN dual-basket air fryer) carrying `plpRedirect=mhFallback` — Amazon's *fallback* route for an unresolvable link, not the submitted product. **This is not product data and was not used.** | https://www.amazon.com/dp/B0CDY277D3 |
| `FLG-008` | High | Product names, prices, ratings, review counts, categories, availability, commission rates for all 3 SKUs | **Not obtainable.** No official source exists for these fields because the identifiers do not resolve. Every one of these cells is left blank on the site and marked *Unverified*. Refused to infer. | — |
| `FLG-009` | High | Amazon Associates Program API terms vs. scraping | Product, price, rating and review data may only be obtained through the Product Advertising API (PA-API 5.0) by a registered associate. Scraping `amazon.com` to populate these tables would breach the Operating Agreement; it was therefore not done. | https://webservices.amazon.com/paapi5/documentation/ |
| `FLG-010` | Medium | Repo baseline was empty | At branch creation `main` contained a single commit `ed1a796` with one file, `README.md` (7 bytes, contents `# Zone3`). There was no prior code, no `COORDINATION.md`, no data, and no site to review. | `git log` of this repo |
| `FLG-011` | Medium | No Amazon Associates Account ID / tag supplied | Affiliate tracking cannot be wired or tested without the associate's own `tag` (`?tag=` / `&linkCode=`) and an approved PA-API credential set. Left blank, never fabricated. | https://affiliate-program.amazon.com/help/node/topic/GRXPHTNBHVPA7WA5 |
| `FLG-012` | Medium | Click/conversion analytics | The brief asks the platform to "track clicks and conversions". Real figures require the associate's own report export; there is no public official source. The Campaigns page therefore ships as an **instrumented but empty** ledger — no invented traffic numbers. | https://affiliate-program.amazon.com/help/node/topic/GRP5WFLZQHB8KZ8A |

---

## Sources Used (official / primary only)

| Source ID | URL | Used for | Retrieved |
| --- | --- | --- | --- |
| `SRC-01` | https://www.amazon.com/dp/B04G1MEwY | Non-resolution check | 2026-11-13 |
| `SRC-02` | https://www.amazon.com/dp/B02NbDxp3 | Non-resolution check | 2026-11-13 |
| `SRC-03` | https://www.amazon.com/dp/B00hJ57DV | Non-resolution check | 2026-11-13 |
| `SRC-04` | https://www.amazon.com/dp/B0CDY277D3 | Control: a 10-char ASIN that does resolve (proves the check works) | 2026-11-13 |
| `SRC-05` | https://affiliate-program.amazon.com/ | Associates programme entry point, disclosure line | 2026-11-13 |
| `SRC-06` | https://webservices.amazon.com/paapi5/documentation/ | PA-API 5.0 — the only sanctioned data source | 2026-11-13 |
| `SRC-07` | https://sellercentral.amazon.com/help/hub/reference/external/G200481490 | ASIN definition / 10-character identifier | 2026-11-13 |
| `SRC-08` | https://affiliate-program.amazon.com/help/node/topic/GRXPHTNBHVPA7WA5 | Associates Operating Agreement | 2026-11-13 |
| `SRC-09` | https://affiliate-program.amazon.com/help/node/topic/GFGYTPQ3LZTURHX7 | Qualifying-purchases / disclosure guidance | 2026-11-13 |
| `SRC-10` | https://www.amazon.com/b?node=18190131011 | "Make Money with Us" — Become an Affiliate entry | 2026-11-13 |

> Where a `SRC-*` row could not be retrieved from its official host during this run, the dependent
> field is left blank on the site and carries an *Unverified* flag rather than an assumed value.

---

## Verification Notes (how to reproduce)

1. `git log --oneline` → confirm only `ed1a796 Initial commit` existed before this work.
2. `curl -I https://www.amazon.com/dp/B04G1MEwY` → `404` / "Page Not Found" (also true for the other two).
3. `python3 -c "print(len('B04G1MEwY'))"` → `9`; ASINs are 10 characters (`SRC-07`).
4. Open any site table: every row's last column is a live link to the official source that backs it,
   or the row reads *Unverified* with a link to `/flagged/`.
