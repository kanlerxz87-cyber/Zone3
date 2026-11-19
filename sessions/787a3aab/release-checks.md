# Release checks — session 787a3aab, 2026-11-19

Canonical command: `python3 tools/publish.py` (16 builders + 25 checks).

## Run 1 (after adding guide #11 + FSIS source + allowlist)

41 commands checked; 0 failed. All builders PASS, all checks PASS, including:
`scripts/check_site.py`, `tools/check_publication.py`, `tools/verify_site.py`,
`tools/link_report.py --strict`, `scripts/build_sitemap.py --check`,
`tools/build_feed.py --check`, `tools/analytics_endpoint.py --self-test`,
`test_collector.py`, node measure tests, `node --check assets/publication.js`.

Generated diff (expected, register-derived only):
- `data/publication.json`: +1 guide, +1 source, +1 indexable URL (11/17/19).
- `guides/thermometer-ice-water-check.html`: new (title, meta, canonical, disclosure
  ×2, FSIS source link, 4 sponsored Amazon links, 0 unsponsored).
- `sitemap.xml`: 18 → 19 URLs. `feed.xml`: 28 → 29 items (new guide first).
- `guides/index.html`: "Eleven practical, question-led guides".
- `README.md` register-facts block: 10→11, 18→19, 16→17.
- `publication-pass.html` + `sessions/aebf0747/*`: page count 122→123,
  sponsored 1799→1803 (generated audit counts).
- `tools/check_publication.py` + `scripts/check_site.py`: `www.fsis.usda.gov`
  added to official-hostname allowlists (USDA FSIS, U.S. federal .gov).

## Run 2 (idempotency)

`python3 tools/publish.py` again: 41/41 PASS, `git status` identical to Run 1
(no new diff). `python3 tools/publish.py --check`: 25/25 PASS.

## Local sweeps (2026-11-19, this session)

- Disclosure strip before `<main` + footer repeat: 19/19 indexable pages.
- Unsponsored product anchors: 0 on every indexable page.
- Unique title + meta description + canonical: 19/19 indexable pages.
- `assets/measure-config.js`: `{"enabled": false, "endpoint": ""}` (no requests).
- Campaign ledger: 0 rows. Intent fields: blank ×5, separate from observed.
- Price/rating/review-count/tested-performance: null ×5 (gate-enforced).

## Not run / limitations

- Chromium/Playwright harness not re-run (dependencies not installed in this
  environment); structural gates + live read-back stand in for it. Recorded as a
  limitation, not a pass.
- No Amazon account, Search Console, or production host access in this session;
  attribution, traffic and revenue remain unverified by design.
