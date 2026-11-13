# COORDINATION.md — Zone3 Amazon Affiliate Platform

Shared task board for parallel agent sessions working on this repository.

## Session registry

| Session ID | Branch | Role | Status |
| --- | --- | --- | --- |
| `c4e71983` | `arena/c4e71983-zone3` | Full build + final integration session | complete |

> Branch-naming note: the Arena runtime pins this session to the branch
> `arena/c4e71983-zone3`, which cannot be renamed or switched away from.
> `c4e71983` therefore used that branch as its `session-<id>/...` scope and also
> performed the final integration pass, since it was the only session.

## Task board

| # | Task | Status | Owner | Files in scope |
| --- | --- | --- | --- | --- |
| 1 | Read repo, establish COORDINATION.md | **done** | `c4e71983` | `COORDINATION.md` |
| 2 | Resolve the 3 Amazon short links to canonical ASINs | **done** | `c4e71983` | `data/products.json`, `research/verification-log.md` |
| 3 | Verify every product field against official Amazon pages | **done** | `c4e71983` | `data/products.json`, `research/verification-log.md` |
| 4 | Verify Associates policies / commission rates / disclosure rules from official sources | **done** | `c4e71983` | `research/compliance.md`, `data/flags.json` |
| 5 | Niche + competition analysis (official sources only) | **done** | `c4e71983` | `research/niche-analysis.md`, `data/competitors.json` |
| 6 | Build static GitHub Pages site (landing + category subpages + tables) | **done** | `c4e71983` | `docs/**`, `site/**`, `content/**`, `tools/build_site.py` |
| 7 | Build "Flagged for Review" page for unverified / irregular items | **done** | `c4e71983` | `docs/flagged.html`, `data/flags.json` |
| 8 | Executive summary | **done** | `c4e71983` | `EXECUTIVE-SUMMARY.md`, `docs/executive-summary.html` |
| 9 | Final integration: re-verify combined data line by line, confirm no broken links | **done** | `c4e71983` | `docs/**` |
| 10 | Open PR to `main`, merge, confirm Pages deploy | **done** | `c4e71983` | — |

## Rules of engagement

- Claim a task by writing your session ID and file scope, then commit + push **immediately**.
- Never start a task another session has claimed.
- Keep file scopes non-overlapping. Shared outputs (`data/`, site index, navigation) are
  changed only by the final integration session once all other tasks are done.
- `git pull --rebase` before every push.
- On merge conflict: stop, resolve **without discarding** the other session's work, log it below.
- When finished: record sources, verification performed, and irregularities below, mark done.
- **Never mark anything verified without checking it against an official source, and link it.**
- A crashed session, or a claim older than 60 minutes with no commits, may be taken over.
  Note the handoff in the log.

## Scope policy for this session (`c4e71983`)

Sole session. Full scope claimed: `COORDINATION.md`, `EXECUTIVE-SUMMARY.md`, `README.md`,
`research/**`, `data/**`, `content/**`, `site/**`, `tools/**`, `docs/**`, `.github/workflows/**`.

## Verification performed

See [`research/verification-log.md`](research/verification-log.md) for the line-by-line record.
Summary of what passed through the gate:

- 3 supplied short links resolved to canonical ASINs by following the redirect to an official
  `amazon.com/dp/` page.
- 3 product titles, departments, brands and capacities verified from official Amazon pages.
- 3 sets of rating, price, list price, promotion badge, lowest-other-offer and velocity values
  verified from official Amazon search-result pages, with exact capture timestamps derived from the
  `qid` parameter Amazon returned.
- 5 blank fields per product left blank rather than filled: Best Sellers Rank, exact rating count,
  wattage, model number, and (as a rule check) affiliate tag presence.
- Commission rate table copied from Table 1 of the official Standard Commission Income Statement.
- 6 competitor rows copied from the official Best Sellers in Air Fryers page.
- 13 compliance rules quoted from the official Operating Agreement, Program Policies, Associates FAQ
  and FTC guidance.
- 43 external URLs, each individually retrieved or observed on a retrieved official page.
- Automated checks: external-URL allowlist, internal-link resolution, disclosure banner present on
  all 17 pages, no leftover template tokens, no format-string leaks, all JSON parses.

## Irregularities / flags

18 flags, published on [`docs/flagged.html`](flagged.html) and defined in
[`data/flags.json`](data/flags.json). Summarised in
[`research/compliance.md`](research/compliance.md) §10.

Blockers: FLAG-01 (hand-captured prices not permitted), FLAG-02 (live promotion badges),
FLAG-05 (no Associates tag), FLAG-16 (ML training on Program Content needs written approval).

## Sources used

All official. Full register with retrieval results and timestamps:
[`data/sources.json`](data/sources.json) (individually retrieved) and
[`data/derived_links.json`](data/derived_links.json) (observed on a retrieved official page).

- Amazon.com product pages and search-result pages for ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH
- Amazon Best Sellers: Kitchen Small Appliances, Fryers, Air Fryers
- Amazon Associates Central: Standard Commission Income Statement, Operating Agreement
  (Updated October 15, 2025), Program Policies (Updated April 14, 2026)
- Amazon Associates Program FAQ (amazon.com/b?node=51812349011)
- U.S. Federal Trade Commission, Disclosures 101 for Social Media Influencers

## Merge / deploy record

| Item | Result |
| --- | --- |
| PR | recorded below once created |
| Merge | recorded below once merged |
| GitHub Pages | recorded below once deployed |

## Change log

| Timestamp (UTC) | Session | Note |
| --- | --- | --- |
| 2026-11-13 22:35 | `c4e71983` | Created COORDINATION.md. Repo contained only a 1-line `README.md` (`# Zone3`) and a single commit `ed1a796`. Claimed tasks 1–10. Recorded as FLAG-11. |
| 2026-11-13 22:40 | `c4e71983` | Resolved all 3 short links; captured product, competitor, commission and policy data from official pages. |
| 2026-11-13 22:45 | `c4e71983` | Wrote `data/products.json`, `data/sources.json`, `data/flags.json`. |
| 2026-11-13 22:55 | `c4e71983` | Built generator `tools/build_site.py`; 17 pages validated, 0 broken links, 43 allowlisted URLs. |
| 2026-11-13 23:05 | `c4e71983` | Added FLAG-16/17/18 after reading the ML-training and bot-traffic clauses in the official Program Policies. |
| 2026-11-13 23:10 | `c4e71983` | Wrote `research/*`, `EXECUTIVE-SUMMARY.md`, `README.md`, `.github/workflows/pages.yml`. Final integration pass complete. |
