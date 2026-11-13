# COORDINATION.md — Shared Task Board (Zone3 Amazon Affiliate Platform)

> Shared task board for all agent sessions working on this repository.
> **Rule: never start a task another session has claimed. Claim first (write your session ID + file scope), commit, push.**

## Session registry

| Session ID | Branch (working) | Status | Notes |
|---|---|---|---|
| `arena-79f85104` | `arena/79f85104-zone3` (Arena-managed session branch; all work for this session happens here per platform rules) | active | Sole session at board creation. Any other session must pick a different branch and non-overlapping file scope. |

> Branch-name note: the Arena platform fixes this session's branch to `arena/79f85104-zone3`; the
> `session-<id>/<task>` convention is honored in spirit by keeping this session's scope isolated and
> non-overlapping. Other sessions: use your own `session-<id>/<task>` branch.

## Task board

| Task ID | Task | Status | Owner | Files / scope | Notes |
|---|---|---|---|---|---|
| T1 | Read/create COORDINATION.md, claim tasks, initial push | done | arena-79f85104 | `COORDINATION.md` | Claimed 2026-11-13. |
| T2 | Repo review (line by line) | done | arena-79f85104 | `README.md`, repo audit | Repo contains only `README.md` ("# Zone3") + `.git`. Initial commit `ed1a796`. No code, no data, no CI. Nothing to conflict with. |
| T3 | Verify product short links (3 URLs) against official Amazon sources | done | arena-79f85104 | data only (results recorded below + in site) | All 3 verified 2026-11-13; see Verification log. |
| T4 | Gather official compliance sources (Associates OA, Program Policies, FTC) | done | arena-79f85104 | data only | OA updated 2025-10-15; Program Policies updated 2026-04-14; FTC guide Nov 2019. |
| T5 | Build GitHub Pages site (landing + category subpages, dashboard UI, tables) | in progress | arena-79f85104 | `docs/**` | Static site, no build step (Pages: branch `main`, folder `/docs`). |
| T6 | Product/analysis data tables with per-row official source links | in progress | arena-79f85104 | `docs/products.html`, `docs/analysis.html`, `docs/sources.html` | Unverified values left blank + flagged. |
| T7 | SEO content: product articles, comparison, buying guide | in progress | arena-79f85104 | `docs/content.html` | Claims limited to verified facts. |
| T8 | Executive summary | in progress | arena-79f85104 | `docs/executive-summary.html` | |
| T9 | Flagged for Review page (irregularities + unverified items) | in progress | arena-79f85104 | `docs/flagged.html` | Published = "needs review", does not block merge. |
| T10 | Compliance & disclosure page | in progress | arena-79f85104 | `docs/compliance.html` | Exact OA §5 wording used. |
| T11 | Link verification (internal links + external source URLs) | unclaimed | — | verification script/log | Internal: script check. External: verified via live fetch during research; re-check before merge. |
| T12 | Enable GitHub Pages, confirm deploy live | unclaimed | — | repo Pages settings | After merge to `main`. |
| T13 | PR → main, merge, record PR link + merge result here | unclaimed | — | `COORDINATION.md` | Do not merge a broken site. |

## Flagged for Review (needs review — does not block anything)

| # | Irregularity | Status |
|---|---|---|
| F1 | All 3 supplied codes are **9 characters** (`B04G1MEwY`, `B02NbDxp3`, `B00hJ57DV`); valid ASINs are 10 chars. They are `link.amazon` short-link path codes, not ASINs. Direct `amazon.com/dp/<code>` returns HTTP 404. | needs review — published on Flagged page |
| F2 | Supplied base URL `https://link.amazon/<code>` is Amazon's official short-link domain but each hop passes through `amzlinks.in` (third-party operator) before landing on `amazon.com`. | needs review — published on Flagged page |
| F3 | Official Associates **commission rate schedule** (`affiliate-program.amazon.com/help/operating/schedule`) requires sign-in; category commission % could not be verified from any public official source → **left blank, flagged unverified**. | needs review — published on Flagged page |
| F4 | Amazon product detail pages intermittently served bot-checkpoints to the automated fetcher; **BSR (Best Sellers Rank)** could not be verified → **left blank, flagged unverified**. | needs review — published on Flagged page |
| F5 | Prices/deals are volatile (observed 2026-11-13: two "Limited time deal", one "Early Black Friday Deal"). Must be re-verified before any content cites a price. | needs review — published on Flagged page |

## Verification log (official sources only — no inference)

| Item | Value(s) verified | Official source | Method / date |
|---|---|---|---|
| Short link 1 `https://link.amazon/B04G1MEwY` | Resolves → `amazon.com/dp/B0CDY277D3` — **CHEFMAN 6 Quart Dual Basket Air Fryer Oven…** ; 4.2★ (4.8K) ; $79.93 (list $99.99) ; 1K+ bought/month | [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3), [amazon.com search](https://www.amazon.com/s?k=B0CDY277D3) | Live fetch ×3 (stable target) + search page, 2026-11-13 |
| Short link 2 `https://link.amazon/B02NbDxp3` | Resolves → `amazon.com/dp/B09B7SB46R` — **Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven** ; 4.3★ (18.3K) ; $149.99 (list $209.99) ; 4K+ bought/month | [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R), [amazon.com search](https://www.amazon.com/s?k=B09B7SB46R) | Live fetch ×2 (stable target) + search page, 2026-11-13 |
| Short link 3 `https://link.amazon/B00hJ57DV` | Resolves → `amazon.com/dp/B08DKYBTPH` — **Chefman Air Fryer 8 Qt TurboFry 4-in-1** ; 4.4★ (16.8K) ; $79.91 (list $119.99) ; 3K+ bought/month | [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH), [amazon.com search](https://www.amazon.com/s?k=B08DKYBTPH) | Live fetch ×2 (stable target) + search page, 2026-11-13 |
| Short-link domain behavior | Control `link.amazon/ZZZZZZZZ99` → 403; `amzlinks.in/B0FAKE1234` → 404 "invalid URL"; `amzlinks.in/B0CDY277D3` (real ASIN) → 404. The 3 supplied codes resolve; targets stable across repeat fetches. | link.amazon / amzlinks.in live responses | Control tests, 2026-11-13 |
| Disclosure requirement (exact wording) | "As an Amazon Associate I earn from qualifying purchases." must be stated **clearly and prominently** on the Site | [Associates Program Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement) (Updated Oct 15, 2025) | Live fetch 2026-11-13 |
| Cookie/session rules | 24-hour session from click; cart additions qualify up to **89 days**; shipped/paid within **180 days** | [Associates Program Policies — Commission Income Statement §1](https://affiliate-program.amazon.com/help/operating/policies) (Updated Apr 14, 2026) | Live fetch 2026-11-13 |
| Payment minimums (US) | Deposit $10 · Gift card $10–$2000 · Check $100 min, $15 fee; ~60 days after month end | [Associates Program Policies §6](https://affiliate-program.amazon.com/help/operating/policies) | Live fetch 2026-11-13 |
| FTC disclosure guidance | Disclose material connections; place disclosure hard-to-miss with the endorsement; plain language ("ad", "sponsored"); no vague terms | [FTC — Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) (Nov 2019) | Live fetch 2026-11-13 |
| Commission % by category | **NOT VERIFIED** — official rate schedule redirects to sign-in | [rate schedule (sign-in required)](https://affiliate-program.amazon.com/help/operating/schedule) | Attempted 2026-11-13 → flagged F3 |
| Best Sellers Rank | **NOT VERIFIED** — product detail pages bot-blocked during research | — | Attempted 2026-11-13 → flagged F4 |

## Conflict log

| Date | What happened | Resolution |
|---|---|---|
| 2026-11-13 | Board created; no other sessions active; no conflicts. | — |

## Session handoff / takeover log

| Date | From → To | Reason |
|---|---|---|
| — | — | — |
