# CBA-T6 completion record — session `cba81fa5` (2026-11-16)

Kept as a file as well as on the shared board, because this session twice had a board section dropped by a
rebase that took `main`'s copy of `COORDINATION.md` (additive blocks survive only if they are re-applied).
This is the same text appended to the board under "CBA-T6 completion record".

---

### CBA-T6 completion record — merge, Pages, and a defect found on the live page

| Step | Result |
|---|---|
| PR | **#124** — https://github.com/kanlerxz87-cyber/Zone3/pull/124 |
| Merge | **`6432f9a`** — `Merge pull request #124 from kanlerxz87-cyber/Zone3/arena/cba81fa5-zone3`, `gh pr merge 124 --merge`, no approval required (owner standing instruction), `main` not force-pushed |
| Rebase history while open | `d6645eb` → `7da5ce2` → `1b4633d` → `e6c800e` (four rebases as PRs #112–#125 landed under it). Conflicts in `COORDINATION.md` / `README.md` / `EXECUTIVE-SUMMARY.md` resolved additively — main's file verbatim + this Part; verified by `git diff origin/main -- COORDINATION.md` = additions only, 0 content deletions, 0 conflict markers. Generated files resolved to main and rebuilt. One resolution did drop this Part and the §12 summary entry mid-flight; both were re-applied and the failure mode was closed by making the reader nav and generated regions self-healing (`tools/build_cba81fa5_site.py --check` now fails when they are missing — tested by stripping a link from `site/evidence.html` and restoring it byte-identically) |
| Files shipped | 33 files, +2,426 / −26 relative to main at merge time; nothing outside this session's scopes and the two declared injected regions was rewritten |
| GitHub Pages | `pages/builds/latest` → **status `built`**, `created_at 2026-11-16T19:10:03Z`, duration 24.7 s (the merge was 19:09:3xZ). The API returns `commit_id: null` for this repository's builds, so the build cannot be tied to a SHA through the API; it is tied by time ordering, per 71-F-06 |
| Live check | `https://kanlerxz87-cyber.github.io/Zone3/` fetched after the build: title `Air Fryer Field Notes — three air fryers, checked line by line`, front-door band present (brand line, the three CTAs, the guide cards, the three listing cards with `B0CDY277D3 / B09B7SB46R / B08DKYBTPH`, the disclosure sentence), `Operations · the audit behind the front door` divider, then the dashboard content below it — i.e. the marketing landing page is live at the canonical URL and the audit trail under it is intact |
| Sandbox limit, stated plainly | the sandbox's proxy could not be used to fetch every one of the 18 `site/` pages individually; the merged tree, the successful Pages build, the site-wide link crawl (152 pages, 165 external URLs, 0 errors) and the live root fetch are the evidence. `robots.txt` on `main` disallows `/docs/` and `/sessions/` (session `81bc99d0`), which the regenerated `sitemap.xml` (71 pages, `--check` exit 0) matches |

**CBA-F-06 (High, found while verifying the live page — fixed by this session).** The published home page was
rendering a Python list as text. `scripts/build_site.py` appended the three product cards to `product_cards` and
then interpolated the list itself (`<div class="product-cards">{product_cards}</div>`), so Python emitted
`['<div class="pcard">…', '…']` — about a kilobyte of escaped repr — where the cards should have been. Every gate
was green: disclosure present, all links resolving, valid HTML, one h1, no placeholder token, sitemap covering the
page. Fixed to `{''.join(product_cards)}` (matching `article_cards` fifteen lines below), root page regenerated, and
guarded by `scripts/cba81fa5_test_no_repr_output.py` (three joined-repr signatures, `<script>`/`<pre>`/`<code>`/
`mono` stripped, with `--selftest` that proves it catches the symptom and ignores clean markup). The permanent
improvement — asserted on `main` but not yet implemented: the shared gates should check that a page's *structure*
matches its data (N cards for N products), because a build that emits the right facts in the wrong shape is exactly
what "verify the site works" is for.

**Gates at merge time, on the final rebased tree** — all exit 0: `scripts/check_site.py` · `tools/verify_site.py` ·
`tools/link_report.py --strict` · `scripts/check_all_links.py` · `scripts/build_sitemap.py --check` ·
`tools/cba81fa5_lint.py` · `tools/build_cba81fa5_site.py --check` · `scripts/test_manifest_regression.py`.
Plus `scripts/cba81fa5_test_no_repr_output.py` (PASS, 112 pages) and its `--selftest`.

**All CBA tasks (T1–T6): done.** Left for the owner, unchanged and still blocking revenue: the Associates tag (Q-1),
Creators API credentials (Q-4), a named human editor (Q-5 / D-10), the canonical-brand decision across
`/read/`, `/site/articles/` and `/site/guides/` (Q-12 / CBA-F-03), and the shared-register consolidation (CBA-F-02's
neighbour, flag FLG-004).
