# Release checks — session `3d0d7bd1`, 2026-11-19

Canonical chain: `python3 tools/publish.py` — 41 commands when this session started; the upstream 4B0 pass (Associates-tagged product links) grew it to **44 commands**, and the final runs below use that chain.

| Run | When | Result | Notes |
|---|---|---|---|
| 1 | 2026-11-19, before the session records existed | 40/41 — FAIL `scripts/check_all_links.py` | `style.html → sessions/3d0d7bd1/decisions.md` did not exist yet (D3B-F-01). Builder stopped at the broken link as designed. |
| 2 | 2026-11-19, after `decisions.md` + `verification-2026-11-19.md` written | **41/41 PASS** | Working tree after run: 134 pending files (all expected outputs + records). |
| 3 | 2026-11-19, immediately after run 2 | **41/41 PASS, byte-stable** | `git diff` between the post-run-2 tree and the post-run-3 tree shows no output drift: the second build changed nothing (definition-of-done item 1). |
| 4 (M1) | 2026-11-19, after rebasing onto `9ce02c6` (PRs #199–#206 merged upstream mid-session, including session 6f16ee11's parallel anti-slop gate and session 0a48cfda's listing-dimension register rows) | **41/41 PASS** | Both lint layers run and pass together: the register-driven D3B lint and 6f16ee11's hard-coded STYLE corroboration. 11 regenerated files from the merged sources. |
| 5 (M2) | 2026-11-19, immediately after M1 + amend | **41/41 PASS, byte-stable** | Second full run on the rebased tree changed nothing; working tree clean. |
| 6 (N1–N3) | 2026-11-19, after a second mid-session upstream move (`ebaf2c7`: PR #203's Associates-tagged buy buttons + two follow-ups; chain grew 41 → 44) | **44/44 PASS, byte-stable** | N1 failed once at `sessions/aebf0747/build_pass.py` because the hand-merge of `build_publication.py` had dropped the `privacy()` renderer (function order differs between the merged variants); restored, N2/N3 green and byte-stable. |

Gate highlights from the passing runs:

- `tools/build_publication.py --check` — current, including `style.html` (23 rendered pages).
- `tools/check_publication.py` — **PUBLICATION PASS**: 124 current HTML pages, 22 rendered
  reader/workspace pages, 122 official-source table rows, 20 indexable URLs, 29 feed entries.
  New gates inside: house-style lint (B38-P1), cadence/overdue + outcome-format checks (B38-P4),
  DS-03 correction pin (B38-P5) — all green on the shipped tree.
- `scripts/build_sitemap.py --check` — sitemap holds exactly the 20 canonical reader URLs.
- `tools/build_feed.py --check` — feed current, 29 items.
- Link report strict + all-links check — no broken internal links after the records existed.
- Disclosure/sponsored/markup/measurement/collector self-tests — unchanged behaviour, all pass.
