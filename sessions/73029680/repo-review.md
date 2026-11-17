# Repo review — session 73029680 (2026-11-17, later)

Base: `d192053` (merge of PR #141). Claim pushed before any edit (`7c7079d`, after a rebase onto
`c67596a` resolved per the keep-both-sides convention — session 59b2194c's Part 83 kept verbatim,
this session's Part renumbered 84; nothing discarded).

## Gate snapshot at the claimed base (before any edit)

| Gate | Result |
|---|---|
| `scripts/check_site.py` | OK — 30 pages, 3 products, 62 sources, 113 flags |
| `tools/link_report.py --strict` | 0 (pass) |
| `tools/i2_gate.py` | PASS — 18 pages / 164 rows / 148 sourced / 16 blanks / 0 flagged |
| `tools/cba81fa5_lint.py` | PASS — 0 new / 22 inherited |
| `tools/verify_site.py` | PASS — 134 pages / 2,068 rows / 1,769 sourced |
| `tools/build_feed.py --check` | current — 9 entries |
| `scripts/build_sitemap.py --check` | 97 pages / 0 extras |
| `scripts/check_all_links.py` | 180 pages / 207 external URLs / 0 errors |
| `tools/build_shop.py` | OK — 11 pages |

## Irregularity sweep — findings

1. **G84-F-01 (Medium, reconciled this session).** Two published confirmation records disagreed
   about submitted links 4–5: `products.html` (from `data/products.json`, session 82372fd1) said
   "No observation on file" for `link.amazon/B0c8moW59` and `B0f3GKalj`, while `/intent-record/`
   (session aebf0747) and `/shop/` (SHOP-04/SHOP-05) showed dated observed ASINs for the same
   links. All three registers were written on the same day; 82372fd1's repo-wide search predates
   the shop/front-page layers landing on main, so the disagreement was a timing artefact — but it
   was live on the site. Resolution: this session fetched all six URLs itself (S70–S75), confirmed
   both destinations independently (B0DHZTCNR5 ThermoMaven; B0DZFD6R9Z CHEF iQ Sense; both
   9-character direct URLs Page Not Found), registered P4/P5 in `data/products.json`, and filled
   the intent rows' observed blocks (intended fields stay empty). "No observation on file" no
   longer occurs anywhere on `products.html`.
2. **Observation (no new flag — already carried).** The tracking ID selected in the owner brief is
   printed as text on `publication-pass.html`, `intent-record/index.html` and three `/shop/`
   pages, always with the same guard sentence ("not attached to any link on this site"; AE-F-01).
   Part 82 recorded the same observation for `publication-pass.html`. Counted again this session:
   `grep -rl shopnow047c-20 --include='*.html'` → 5 public pages, each with the guard wording.
   Owner may prefer redaction; no edit made to other sessions' pages.
3. **Observation (no new flag).** `data/products.json` was a three-product register while the
   front page, shop layer and executive summary carried five links — the mismatch 59b2194c called
   "a separate legacy surface". This session closed the data gap (P4/P5); the register is now
   consistent with the other surfaces. Their separate build remains separate by design.
4. **Non-finding.** No price, rating or availability value was copied out of any fetched page
   (2(b)/6(t); FLG-036), and no page in the reader gates G6/G7 covers slipped.

## What this session changed (see COORDINATION.md Part 84 task board)

- `data/sources.json` +S70–S76 (six own fetches of links 4–5 and their listings; OPM federal
  holidays). All amazon.com/link.amazon rows `status: observed`; OPM read 2026-11-17.
- `data/products.json`: P4/P5 rows (full P1-shaped schema, `confirmed_as_submitted_product: false`),
  intent rows 4–5 reconciled, `intent_records_note` extended.
- `data/flags.json`: +G84-F-01 (114 flags: 3 Critical / 19 High / 32 Medium / 33 Low / 27 Info).
- `data/suggestions.json`: `review_2026_11_17_late` — design-prompt refresh proposals (DP-P-01..05),
  OPM seasonal calendar hooks, decision runbook (order that unblocks Q1–Q12/D1–D10), reconciliation row.
- `scripts/build_site.py`: `build_suggestions()` renders the late review block; one stale static
  sentence in `build_products()` ("opened on 2026-11-13") made date-accurate.
- `EXECUTIVE-SUMMARY.md`: live counts recomputed.
- Full chain rebuilt twice — tree hash-identical after the second run.

## Gate results after this session's changes

`check_site` OK 30/5/69/114 · `verify_site` PASS 134 pages / 2,107 rows / 1,789 sourced ·
`link_report --strict` 0 · `i2_gate` PASS · `cba81fa5_lint` PASS 0 new / 22 inherited ·
no-repr PASS 134 · `build_feed --check` current (9) · `build_sitemap --check` 97/0 ·
`check_all_links` 0 errors (180 pages / 212 URLs) · aebf0747 `audit` missing_sponsored 0 (1,509/1,509) ·
`link_check` 0 · `build_cba81fa5 --check` current · chain ×2 idempotent (md5 over the whole tree).

## What this session did NOT do

- No decision on Q12/canonical layer, no design-brief edit (757efebc's scope — change request logged),
  no link rewrite (gated on the owner's Special Link test), no tracking ID placement change on other
  sessions' pages, no re-probing of links 1–3 (their register rows already carry four dated captures).
