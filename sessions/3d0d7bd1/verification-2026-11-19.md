# Verification record — session `3d0d7bd1`, 2026-11-19

Branch `arena/3d0d7bd1-zone3`, based on `0273fb4` (`main` at PR #198), rebased onto `30746b2` (PR #200, the eleventh guide
`thermometer-ice-water-check`), claimed and pushed, then — during implementation — rebased again
onto `9ce02c6` after PRs #199–#206 merged upstream mid-session. Claim pushed before any
implementation (D3B-T1, commit `c126257` after an append-only COORDINATION.md rebase conflict;
upstream file kept in full, this session's Part re-appended, no upstream content dropped).

## What was read from official sources in this pass

| # | Page | What was taken | Where it landed |
|---|---|---|---|
| V01 | `https://developers.google.com/search/updates` (read 2026-11-19, body chunks for May 2026 and June 2026) | May 8, 2026 entry "Deprecating the FAQ rich result feature": "This feature will no longer appear in Google Search starting May 7, 2026." June 2026 entry "Removing documentation for the FAQ rich result feature": "The FAQ rich result feature is no longer shown in Google Search results…" | DEC-3D0D-03; DS-03 `update` in `data/publication.json`; anchor `#faq-deprecation` |
| V02 | Register source rows re-checked for scope only (`data/publication.json → sources`) | `google-faq-update` already carried checked_on 2026-11-19 and the updates-page URL; `google-helpful`, `google-reviews`, `ftc`, `amazon-agreement`, `amazon-policies` rows were re-read by session 6b68afc8 on 2026-11-19 (their record: `sessions/6b68afc8/verification-2026-11-19.md`) and were **not** re-fetched by this session; no checked_on date was changed by this session | suggestions page fine print unchanged; house_style rows cite the existing rows |

No other official page was fetched by this session. No Amazon page was opened; no API or
account action was taken; no network call was made to any retailer host.

## What was measured in this repository (not from official sources; repository observations)

- **Lint discovery scan (2026-11-19, pre-adoption).** All 20 current reader pages (the pages in
  `build_publication.outputs()` except `publication-prior.html`) were scanned against the
  proposed union of the design brief §7 banned list and the `/site/` layer HYPE/TREND patterns.
  19 hits, zero of them a banned construction used as a claim in buyer-facing copy: 2
  meta-usages on `index.html`/`about.html` (rewritten — see `decisions.md` DEC-3D0D-01), 1
  compliance-sentence meta-usage on `about.html` (exempted via `data-lint="quote"`), 16
  register-quotes on `suggestions/index.html` (page-level relaxation, same pattern as the
  `/site/` style-guide page).
- **Gate runs.** `tools/publish.py` (16 generation steps + 25 checks) run to completion twice;
  second run byte-stable (`git status` clean after re-build; `build_publication.py --check`
  passes inside the chain). Record of both runs in `release-checks.md`.
- **Post-change counts, read from the registers after the build (PR #200's guide included):**
  11 guides · 39 decision-readiness questions (38 + D3B-Q1) · 28 proposals · 6 paths ·
  13 design-prompt blocks · 17 scoped official references · 20 indexable URLs (19 + `style.html`)
  · 29 feed entries · campaign ledger 0 rows. README's generated `z3:register-facts` block was
  rewritten by the builder to match; no hand-typed count was touched.

## Irregularities found

- **D3B-F-01 (resolved in this pass).** The first full-chain run failed
  `scripts/check_all_links.py` on `style.html → sessions/3d0d7bd1/decisions.md` because the
  decision record had not yet been written when the page referencing it was built. The record
  was written (`decisions.md`), and the chain re-run clean. Recorded here because it shows the
  link gate catches a record link before the record exists — the intended behaviour.
- **D3B-F-02 (process note, resolved).** Five PRs merged into `main` while this session worked
  (#199 a4f9ee45, #200 787a3aab, #202/#204/#205 0a48cfda, #206 6f16ee11). The `COORDINATION.md`
  rebase conflicts were append-only and were resolved by keeping the complete upstream file and
  re-appending this session's Part; an intermediate rebase commit briefly carried conflict
  markers in that file, corrected in the same rebased series before the PR — recorded here in
  full. `data/publication.json` was merged programmatically by id: upstream's
  `listing_dimensions` rows, rewritten cleanup guide, E41-P1/E41-Q1/P26-Q6 updates and 0A4
  proposals were layered onto this session's decisions (B38-P1/P4/P5, E41-P2) with zero
  semantic collision. `tools/check_publication.py` and `tools/build_publication.py` were merged
  by hand: session 6f16ee11's hard-coded STYLE anti-slop gate and this session's
  register-driven lint now both run and both must pass; their gate scans the same stripped view
  as this session's so the style page's phrase cells are exempt under both; 6f16ee11's
  "popularity status" about-page wording was adopted over this session's `data-lint="quote"`
  span (the token is gone rather than exempted); 6f16ee11 kept the quoted hero mention
  exempt-by-mention, while this session's recorded rewrite removes it outright — the rewrite
  stands and passes both gates. Upstream's product-card dimension notes and the compare
  table's "Listed size" column are preserved unchanged.
- No other irregularity. No flag was closed, and no unverified value was filled in.

## Honest limits of this pass

- The banned-phrase lint is a lexical floor. It cannot tell a well-written sentence from a
  badly written one that avoids the list; the review pass remains the real quality gate.
- The overdue-state gate compares register dates, not the wall clock, by design (byte-stable
  builds). It therefore fires only when a session moves `reverified` past the derived due date
  without publishing a new edition — which is the drift it exists to catch.
- The structural and lexical gates do not re-verify the *factual* claims of historical pages;
  those remain the responsibility of the dated verification records that introduced them.
