# Repo review — session `3c96f21d` (2026-11-17)

**Base reviewed:** `main` at `d192053` (merge of PR #141, session `82372fd1`).
**Branch:** `arena/3c96f21d-zone3`.
**Scope of this session:** the measurement layer the owner brief asks for first — *"Turn on click and
conversion measurement before writing anything else."*

---

## 1. Gate snapshot at the claimed base (before any edit)

| Gate | Result at `d192053` |
|---|---|
| `python3 scripts/check_site.py` | OK — 30 pages, 3 products, 62 sources, 113 flags |
| `python3 tools/verify_site.py` | PASS — 134 pages, 2,068 table rows, 1,769 with an official source |
| `python3 tools/link_report.py --strict` | exit 0 |
| `python3 tools/i2_gate.py` | PASS — 18 pages, 164 rows, 148 sourced, 16 explicit blanks, 0 flagged |
| `python3 tools/cba81fa5_lint.py` | PASS — 0 new findings, 22 inherited advisories |
| `python3 tools/build_cba81fa5_site.py --check` | already current |
| `python3 scripts/build_sitemap.py --check` | 97 pages, 0 extra entries |
| `python3 scripts/check_all_links.py` | 0 errors — 180 pages, 207 external URLs |
| `python3 scripts/cba81fa5_test_no_repr_output.py` | PASS — 134 pages, 0 repr-shaped text |

Every gate was green before this session changed anything, so any failure recorded below was
produced by this session's own edits and was fixed before the push.

## 2. Live spot check at the claimed base

Read on 2026-11-17, before the push (the site was serving `5bc965a`/`d192053`):

| URL | Result |
|---|---|
| `https://kanlerxz87-cyber.github.io/Zone3/` | 200 — publication front page, disclosure strip first, five product cards, four guide cards |
| `https://kanlerxz87-cyber.github.io/Zone3/guides/index.html` | 200 — the four question-shaped guides, each labelled "working title" |
| `https://kanlerxz87-cyber.github.io/Zone3/feed.xml` | 200 — RSS with 10 items: four `/guides/` pages and five `/site/guides/` pages, plus the guides index |

## 3. Repository hygiene

| Check | Command | Result |
|---|---|---|
| Conflict markers | `grep -rln '^<<<<<<< \|^>>>>>>> '` over html/py/json/md, excluding `archive/` | 0 files |
| Secrets | `grep -rniE '(api[_-]?key\|secret\|password\|token)\s*[:=]\s*["\'][A-Za-z0-9]{8,}'` | 0 hits |
| Python repr leakage in published pages | `scripts/cba81fa5_test_no_repr_output.py` | PASS |
| Tracked files / repository size | `git ls-files \| wc -l`; `du -sh .git` | 443 files, 7.8 MB |
| Feed ↔ sitemap coverage | compared `feed.xml` links with `sitemap.xml` locations | one mismatch, recorded as G3c-F-07 |

## 4. Findings raised by this session

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| G3c-F-01 | Medium | The counter is live on every published page but no collection endpoint is configured, so nothing leaves any browser and the site holds no traffic evidence. GitHub Pages is a static site hosting service and cannot receive a POST. | **Needs owner** — one line in `data/analytics/config.json`; both hosting options documented in `tools/collector/README.md` |
| G3c-F-02 | Medium | The five recorded events are this session's proposal. The brief asks for "the five defined events" without defining them. | **Needs owner** — accept or amend in DEC-03 / Q8 |
| G3c-F-03 | Low | Five shared files were edited to add the measurement layer (publication pass ×2, `check_site.py`, `verify_site.py`, `link_report.py`). Each change is additive; before/after counts recorded. | Fixed |
| G3c-F-04 | Info | The release gate's flag pattern did not recognise session-prefixed flag ids, so rows citing a real flag were reported as uncited. Rows with a flag reference went 369 → 461; uncited rows fell 174 → 162; a whole-tree scan confirmed no false positives. | Fixed |
| G3c-F-05 | Info | The counter creates no visitor identifier, so unique-visitor counts are impossible by design. | By design — recorded so no later session adds a fingerprint to "fix" it |
| G3c-F-06 | Low | The counter runs on published pages only; `docs/`, `sessions/` and `archive/` are not measured. | By design |
| G3c-F-07 | Info | The feed's first item uses the URL form `/guides/index.html` while the sitemap lists `/guides/`. Both resolve — the live `/guides/index.html` was fetched and returns the guides index — so this is a canonical-form inconsistency, not a broken link. | **Not fixed here**: `feed.xml` is produced by `tools/build_feed.py`, whose union rules belong to session `82372fd1`. Logged for the integration session. |

## 5. Observations carried forward, not re-raised

These were already open before this session and are unchanged by it. They are listed so the
integration session does not have to rediscover them:

- **Five reader-facing surfaces** (`read/`, `marketing/`, `site/`, `shop/`, `guides/`) answer the
  same questions in five voices. Already open as Q12 and design path DP-C.
- **The three (five) submitted short links** still open the same three destination listings, and the
  intended ASINs are still unconfirmed. FLG-001, FLG-002, FLG-035, G82-F-03.
- **The Associates tag, the enrolled account and the marketplace decision** are unchanged and still
  block every commission-bearing element. Q1, Q3, Q4.
- **The archives under `archive/`, `docs/` and `sessions/`** still carry historical values that are
  not publishable today. Owned by other sessions; not edited here, per the coordination rules.

## 6. What this session did not do, and why

- It did not set a collection endpoint. The host is an owner decision (DEC-03); guessing one would
  point the site at a third party the owner never chose.
- It did not add an identifier, a cookie or a fingerprint. Counting unique visitors needs a consent
  decision the owner has not made (G3c-F-05).
- It did not change `feed.xml`'s URL form. That file belongs to another session's generator (G3c-F-07).
- It did not implement any of the design paths (DP-A, DP-B, DP-C) or the design brief. They are
  proposals awaiting a recorded choice, and the brief asks that suggestions be reviewed before they
  are implemented.
