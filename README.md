# Zone3

Static dashboard for three supplied Amazon affiliate products. Published with GitHub Pages from `main` (root).

- **Live site:** https://kanlerxz87-cyber.github.io/Zone3/
- **Data:** `data/products.json`, `data/sources.json`, `data/flags.json`
- **Build:** `python3 scripts/build_site.py` (generates the HTML pages)
- **Check:** `python3 scripts/check_site.py` (broken links, source coverage, unverified values flagged)
- **Coordination board:** `COORDINATION.md`

Rule used throughout: a value is shown only if it was read from an official source. Anything else is left blank and flagged on the *Flagged for Review* page.

Affiliate disclosure: As an Amazon Associate I earn from qualifying purchases.
