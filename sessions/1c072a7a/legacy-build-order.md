# Earlier build order (reference only)

Captured from main `0ee4153` while integrating the completed C3/C17/3301 passes on 2026-11-19. This is **not** the current release command. Use `python3 tools/publish.py` from the repository root. The current renderer composes the two old front-page patchers on a scratch file for the retained previous edition, never on the current root.

**Build order matters for the reader layer.** `scripts/build_site.py` still emits the dashboard as
`index.html`, and `tools/build_cba81fa5_site.py` then injects the front-door band, the guide plan table and
the `site/` index entries from `data/cba81fa5/guides.json`. Run them in this order — and note that the lint
fails the build if the band has been dropped (`SITE:generated-region-stale`), because a marketing front door
that silently disappears on the next rebuild is worse than no front door:

```bash
python3 scripts/build_site.py             # dashboard pages from data/*.json
python3 tools/build_i2_site.py            # reader site  -> site/
python3 tools/build_cba81fa5_site.py      # front-door band + guide plan + site index (idempotent)
python3 tools/cba81fa5_lint.py            # style + compliance lint over site/** (baseline = reviewed inherited items)
python3 scripts/cba81fa5_test_no_repr_output.py   # no Python repr in any published page (CBA-F-06)
python3 tools/build_shop.py                     # shop layer from data/shop/*.json (session 974e366d; also self-checks)
python3 tools/build_measurement.py          # measurement page + assets/measure-config.js from data/shop/measurement.json (session 38650305; counting OFF until an endpoint is set)
python3 tools/build_brief_status.py        # brief-status/index.html from data/shop/brief-status.json (session 38650305)
python3 scripts/build_marketing.py         # marketing/*.html (ded63349: re-added to the chain)
python3 scripts/build_read.py              # read/ editorial layer (ded63349: re-added to the chain)
python3 scripts/build_5a56c084.py          # articles/ research desk (ded63349: re-added to the chain)
python3 tools/build_site.py                # second audit pass — picks up pages created by the layers above (ded63349)
python3 sessions/aebf0747/build_pass.py         # publication pages + guide pages (writes an initial feed draft)
python3 sessions/aebf0747/publish_pass.py       # mechanical pass: disclosure strip, footer, sponsored rel and head links
python3 sessions/c3be74f2/build_front_page.py   # source-linked buyer questions, observed listings and decision table (PR #164; idempotent)
python3 sessions/c17d25fd/build_shopfront.py    # product-first publication layout composed over the C3 evidence/decision layer (this session; idempotent)
python3 tools/measure_pass.py              # analytics script tags on every published page (markers; idempotent; session 38650305)
python3 tools/build_feed.py               # feed.xml = UNION of both guide registers; runs after every HTML generator, --check gates drift (session 82372fd1)
python3 scripts/mark_sponsored.py         # rel="sponsored" on every outbound product link, whole tree incl. sessions/ (0C4-T3; added to the chain by session 66964850 after the PR #161 union — without it check_site rule 10 fails on regenerated session pages)
python3 scripts/build_sitemap.py          # sitemap for the whole published tree

# Measurement self-tests (session 38650305):
python3 tools/analytics_endpoint.py --self-test   # collector allow-list, field filter, aggregate-only store
node sessions/38650305/test_measure.js            # counter in a stubbed browser: off by default, GPC/DNT, click shape (needs Node)
```
