# Archive: session 26634cd5 (merged to main via PR #1)

These files are the copies from `main` at commit 8cc2d4a, saved unchanged before the 7f84fea4 integration.
Their content is merged into the live site's data files (`data/*.json`) and regenerated pages. Nothing is linked from the live site.
The original files also remain in git history.

- `scripts/` — the session's build and check scripts (superseded by `scripts/build_site.py` and `scripts/check_site.py`)
- `data/` — the session's data files (merged, with ID mapping recorded in `data/sources.json` and `data/flags.json`)
- `pages/` — the session's HTML pages (regenerated as part of the live site)
- `assets/style.css`, `README.md`, `COORDINATION.md` — superseded; see the live `COORDINATION.md` for the merged task board

## Status of these files

- Superseded. The live site is generated from `data/*.json` on this branch. These copies were not rebuilt, not checked by `scripts/check_site.py`, and are not linked from the live site.
- Their claims are not verified by this branch. Where they differ from the live data (for example, the S-numbering or flag IDs), the live data and `COORDINATION.md` take precedence.
- The HTML pages here use relative links (for example `assets/style.css`) that do not resolve under `archive/`. That is expected for a reference copy.
