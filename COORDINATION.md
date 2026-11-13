# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/Zone3` · Live site (GitHub Pages, source `main` `/`): https://kanlerxz87-cyber.github.io/Zone3/

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything).

## Session registry

| Session ID | Branch | Role | Claimed at (UTC) | Last heartbeat (UTC) |
|---|---|---|---|---|
| 7f84fea4 | `arena/7f84fea4-zone3` | Repo review, source verification, site build, integration, PR, merge | 2026-11-13 22:55 | 2026-11-13 22:55 |

### Branch note (read first)

- The brief asks for `session-<id>/<task>` branches. The Arena session rule for this run fixes the working branch to `arena/7f84fea4-zone3`. This session creates and pushes no other branch. Every task below is therefore done on this one branch.
- Other session branches exist on the remote and were observed read-only (no edits were made to them): `arena/26634cd5-zone3`, `arena/3c6cba43-zone3`, `arena/a9cafea1-zone3`. Each also created a `COORDINATION.md` and claimed overlapping tasks on its own branch. **Integration conflicts with those branches are expected** when they are merged to `main`. The integration session that merges them must reconcile the task board, the data files and the site. Nothing from those branches was copied or overwritten here.

## Task board

| Task | Status | Owner | Files in scope |
|---|---|---|---|
| T1 — Repo review (baseline audit, irregularities) | in progress | 7f84fea4 | `COORDINATION.md`, `README.md` |
| T2 — Source verification (official sources, line-by-line) | in progress | 7f84fea4 | `data/sources.json`, `data/products.json`, `data/policy_facts.json` |
| T3 — Site build (landing dashboard + category subpages + flagged page) | in progress | 7f84fea4 | `index.html`, `executive-summary.html`, `products.html`, `pricing.html`, `reviews.html`, `content.html`, `campaigns.html`, `flagged.html`, `sources.html`, `assets/**`, `.nojekyll` |
| T4 — Generator + link/row verification script | in progress | 7f84fea4 | `scripts/build_site.py`, `scripts/check_site.py`, `data/**` |
| T5 — Executive summary | in progress | 7f84fea4 | `executive-summary.html`, `EXECUTIVE_SUMMARY.md` |
| T6 — Integration: build, link check, PR → `main`, merge, Pages deploy confirmation | unclaimed | 7f84fea4 (after T1–T5) | all (integration only) |

## Task log

- **2026-11-13 22:55 UTC — 7f84fea4** claimed T1–T6 on `arena/7f84fea4-zone3`. This commit is the claim and is pushed before any other work.
- Initial read-only checks (no edits): the three Amazon product links were fetched and each `amazon.com/dp/<9-char ID>` URL was checked; Amazon Associates Operating Agreement and Program Policies were read (see `data/sources.json`).
