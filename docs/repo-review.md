# Repo Review — Zone3

**Audited baseline:** `ed1a796dc01f52669864e98a72b9a521a3b7161b` (`main`)
**Reviewed by:** session `3c6cba43` · 2026-11-13
**Live site published from:** `main` / repository root (GitHub Pages `build_type=legacy`)

## 1. State as found

| Aspect | Finding |
| --- | --- |
| Commits | 1 — `ed1a796 "Initial commit"` |
| Branches | `main` only (plus this working branch) |
| Tracked files | 1 — `README.md`, 7 bytes, contents exactly `# Zone3` |
| Tags / releases | none |
| CI workflows | none in-repo (the `pages-build-deployment` workflow is the Pages service default, not a repo file) |
| `LICENSE` | **absent** |
| `.gitignore` | **absent** |
| `COORDINATION.md` | **absent** (brief anticipated it "may not exist" — it did not) |
| Code, data, tests, docs | none |
| Working tree | clean |
| Pages | already enabled and previously deployed an empty Jekyll build of the placeholder README |

## 2. Irregularities flagged

1. **FLG-010 — nothing to review.** The repository is a scaffold. There was no prior
   implementation, dataset, convention or history to reconcile against, and no other
   session's work to coordinate with. Recorded with the exact baseline hash so the audit
   trail has a defined starting point.
2. **No license.** Content on this site includes short quotations from Amazon's Program
   Documents, used under the terms those documents grant for Program Content. Code here
   is original. If Zone3 is meant to be open source, a `LICENSE` must be added — that is
   a legal/business choice, so it was **flagged rather than assumed**.
3. **No `.gitignore`, no manifests.** Added: `.gitignore` (build scratch + local secrets
   excluded, explicitly ignoring `config/*.local.json`, `.env*`, `data/intake-cache.json`).
   No runtime dependency is introduced at all, which is deliberate — see §4.
4. **Pages deployed an empty site before this work.** Confirms the pipeline works and that
   publishing needs no configuration change; only content.

## 3. What was added (all on this branch, then merged)

| Path | Purpose |
| --- | --- |
| `COORDINATION.md` | shared task board, claims, sources, verification, flags |
| `data/*.json` (12 files) | single source of truth for every published table cell |
| `tools/build_site.py` | renders the site **and** enforces the row-provenance gate (G1–G8) |
| `tools/verify_site.py` | post-build audit of emitted HTML (V1–V8) |
| `tools/amazon_intake.py` | ASIN validation → `/dp/` probe → Creators API; Agent-Term-compliant identity |
| `tools/niche_score.py` | niche ranking; refuses to impute missing inputs |
| `tools/link_report.py` | provenance coverage report across all tables |
| `assets/app.css`, `assets/app.js` | dashboard UI; sort/filter only, **no runtime fetching** |
| `config/platform.json` | configuration with credentials explicitly `null` |
| `dashboard/` + 15 page directories | generated |
| `docs/` | this review, `verification-log.md`, `executive-summary.md`, `compliance.md` |
| `README.md` | rewritten from the 7-byte stub |

## 4. Review notes on the code added

* **No dependencies.** `tools/*.py` use only the standard library, so there is no lockfile
  to audit and no supply-chain surface. Consequence for compliance: the project cannot
  acquire a CAPTCHA-solving or browser-automation dependency by accident — those are
  prohibited by the Agent Terms, and nothing in this tree can do it.
* **No secrets.** `config/platform.json` commits `null` values rather than placeholder
  strings, so a reviewer can tell "absent" from "present but redacted". Environment
  overrides are documented in that file.
* **No Amazon content at runtime.** `assets/app.js` fetches nothing, which keeps the site
  inside the 24-hour caching rule by construction rather than by scheduled invalidation.
* **Generated HTML is committed** because Pages deploys from the branch root; `tools/` and
  `data/` are therefore also the reproducible source of the site (`python3
  tools/build_site.py --out .preview` rebuilds it identically apart from the timestamp).
* **The build is the reviewer.** Failures are exit-code 2 (provenance) and 3 (emitted
  output), so a broken claim cannot ship silently.
