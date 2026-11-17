# Verification record — session 82372fd1 (2026-11-17)

## What this session changed, and what each claim rests on

1. **Feed** (`tools/build_feed.py`, `feed.xml`, head links in `site/index.html`,
   `site/guides/index.html`; README chain line). Feed entries are exactly the `status:"live"`
   rows of `data/cba81fa5/guides.json`; dates copied from the same register; prohibited-figure
   patterns fail the build (same families as i2 G6/G7). XML validity checked with
   `xml.etree.ElementTree`. Self-heal proven: full i2+cba rebuild drops the region →
   `--check` fails (exit 1, listing both files) → re-run restores → all reader gates green.
2. **Mobile pass** — see `mobile-audit.md` (measurements, before/after, WCAG 2.2 reference).
3. **Intent confirmation record** (`data/products.json.intent_records`,
   renderer in `scripts/build_site.py`, rendered on `products.html`). Intended fields
   (ASIN / official listing URL / confirmation date / confirmation source) are null-by-design
   and render `Unverified`; observed fields render only from the dated readings already in
   the register (S11, S52–S55, S67–S69) — the renderer reads two disjoint JSON blocks, so
   the "never merge the two fields" rule is structural. The two unregistered links are shown
   as "not registered", with an explicit statement that this session performed no observation.
4. **Suggestions review 2026-11-17** (`data/suggestions.json.review_2026_11_17`, Q11–Q12,
   D7–D10; renderer extension in `build_suggestions()`). Design paths DP-A/B/C are labelled
   proposals; every "shipped" row cites its own commit/flag/register in this repo.
5. **Flags** G82-F-01/02/03; `EXECUTIVE-SUMMARY.md` live counts recomputed from the register
   (111 flags: 3 Critical / 19 High / 31 Medium / 32 Low / 26 Info). Dated historical gate
   records in the same file were left as history.

## What was NOT touched

- No new Amazon observations, no re-probing of the short links (the register already carries
  the dated 2026-11-16 observations S67–S69; FLG-003 remains unresolved by design).
- `data/i2/*.json`, `data/cba81fa5/guides.json`, `data/decision-queue.json`, all checker
  scripts, `read/` generators: unchanged; everything under `site/` is generator output.
- The two-layer question (site/ vs read/ vs marketing/) was NOT decided — it is Q12/DP-C for
  the owner; implementing it unilaterally is exactly what the coordination rules forbid here.

## Owner input received via the 2026-11-17 brief, recorded here per the register's own rule

Selected tracking ID for the enrolled Associates account: **shopnow047c-20** (this value is
kept in this coordination log only, not on public pages, per Q1's how_to_discover). Its
effectiveness can only be confirmed owner-side: generate one Special Link with it, click
through, and check the Associates reports line — the brief's "test one link before scaling"
step. Until that is recorded, all outbound links stay evidence-mode (untracked), which the
disclosure bar already states honestly.

## Sources for statements made on public pages by this session

- WCAG 2.2 SC 2.5.8/2.5.5 target sizes: w3.org (cited in mobile-audit.md; internal finding G82-F-01).
- Everything else cited on-page links either a sources.json register id (S01–S69) or this
  repo (flagged rows use the standing repo-link fallback).
