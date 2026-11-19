# Repo review — 2026-11-19 · session `6b68afc8`

Read-only pass over the tree at the claim base `825f5132` (merge of PR #172), the changes this
session made and why, and §6 — what the rebase onto `origin/main` (`530d9d9`, PRs #173–#176) required. Findings that are not defects are called out as such, because "flagged" is
otherwise useless as a decision tool.

## 1 · Baseline

| Check | Result on the untouched checkout |
|---|---|
| `git status --porcelain` | empty — the committed tree is what the generators produce |
| `python3 tools/publish.py --check` | **25 commands, 0 failures** before any edit |
| `gh pr list --state open` | #160 (`arena/0b2ffabd-zone3`), #157 (`arena/ed27e766-zone3`), both last updated 2026-11-17 |
| `gh run list --branch main` | latest `Publication checks` and `pages build and deployment` both **success** (4h old at claim) |
| Clone depth | shallow (`git rev-parse --is-shallow-repository` → true); `git log origin/main..HEAD` empty at claim, so this branch had nothing ahead of `main` |

## 2 · How the site is actually assembled, measured rather than assumed

One canonical reader renderer (`tools/build_publication.py`) reads one register
(`data/publication.json`) and shares one chrome module (`tools/publication_chrome.py`); the legacy
flat research pages, `/shop/`, `/site/`, `/read/` and the session surfaces stay reachable behind the
single "Behind the site" group. `tools/publish.py` is the only documented entry point: 16 builders in
a fixed order, then 25 checks, and CI requires the rebuild to produce no diff. That is a good shape,
and it is why this pass added data and renderer code rather than hand-written HTML.

What that shape implies for a reviewer, stated plainly:

- A **new reader page is cheap** (add a register row; the guide, its feed entry, its sitemap entry, its
  canonical and its shell arrive together) — which is why the two new guides were added through
  `data/publication.json` and nothing else.
- A **new table is not free**: `tools/check_publication.py` demands an official HTTPS source in every
  row of every current page. The intake block is therefore a definition list, not a table, and the
  path chooser is cards rather than a fourth table — a path row would have forced a citation the
  owner has not supplied yet.
- **Counts and dates in prose are hazards.** Three places asserted a number a data file owns. Two are
  fixed here (`P27-F02`, `P27-F04`); one belongs to another surface and is flagged instead of edited
  (`P27-F03`).
- **`noindex,follow` is doing real work**: the research/duplicate editions stay reachable for the
  owner and out of the indexable set, which is what keeps "one site for search engines to index"
  true while the registers stay public.

## 3 · Findings taken forward as flags

| ID | Finding | Why it matters to a decision |
|---|---|---|
| `P27-F01` | Two 2026-11-17 PRs are open and unpublished; their registers (`G0B2-*`, `review_2026_11_17b`, `DESIGN_PROMPT.md`) are absent from the tree | The owner is choosing between documents that exist only in unmerged branches; either re-land them or close them, but decide on purpose |
| `P27-F02` | Reader-facing check dates were literals in the renderer | A refreshed register would have made live pages assert a stale read date; now derived |
| `P27-F03` | `/shop/` hard-codes its "last checked" sentence (`CHECKED_HUMAN`) while its register holds the same date in `config.checked_on` | Correct today, unenforced tomorrow; left to the surface owner with the reasoning recorded |
| `P27-F04` | Proposal `P26-S3` asserted "six linked guides" — a count `data/publication.json` owns | A live page would have started lying the day someone added a guide |
| `P27-F05` | 2(b)'s tag-parameter clause re-read verbatim; the five submitted `link.amazon/<9-char>` links still cannot be judged from public text | This is the one open item that can actually cost the account; the flag quotes the clause so the owner is not deciding from a summary |
| `P27-F06` | `sitemap.xml` has no `<lastmod>`; adding a git-derived one was measured, argued and **rejected** against the deterministic-build gate | An owner reading "SEO best practice" lists needs to know which items were considered and refused, not just which were skipped |

All six were appended after the rebase, on a register that had meanwhile grown to 158 rows (the merged
`B79-F-01…04`), so the register now stands at 164 and each row was numbered against that state.
`P27-F05` and the merged `B79-F-02` describe one open item from two sides — the account's link supply
and the policy wording — and both rows say so instead of one being deleted as a duplicate.

## 4 · Observations recorded, no action taken

- Upstream PR #176 added a gate requiring every question row to carry a `owner_input_needed` boolean
  and every proposal a concrete `next_action` plus two `discoveries`. My seven `P27-Q` rows passed the
  prose fields but not the boolean, which the first post-rebase build caught: the flag is now set from
  `answer_by` in the migration, so the desk and the gate agree rather than the desk working around it.
  Worth repeating to anyone else landing on this base: **the gates are the coordination mechanism**, and
  a change that passes locally at claim time can fail at merge time for a reason that is entirely legitimate.
- The five pages titled **"Moved"** (`analysis.html`, `disclosure.html`, `flagged-for-review.html`,
  `marketing.html`, `categories/home-kitchen-air-fryers.html`) share a title and have short
  descriptions. They are meta-refresh stubs, excluded from the sitemap by `scripts/build_sitemap.py`,
  and duplicate titles on non-indexed redirects are correct. Not a defect; measured so the next pass
  does not "fix" it.
- `SHOP-03`'s recorded `listing_title` omits the `®` that appears in today's page title (§2 above): the
  register transcribes rather than byte-copies. Harmless for the wording this site publishes; it is a
  reminder that a title row is an observation with a date, not a fixture.
- `data/flags.json` carries 117 rows with no `status` key at all and 43 with one, spread over four
  vocabularies: `open` (20), `fixed` (16), `needs review` (6, four of them added here) and one
  free-text sentence used as a status. The page renders them; a
  reviewer cannot filter them. Worth an owner decision before the register grows past the point where
  anyone can read it linearly — deliberately not "fixed" by inventing statuses here.
- `EXECUTIVE-SUMMARY.md` opens with a 2026-11-19 section from the previous session that says "six
  practical buyer-question guides". Both statements were true at their own timestamps. This pass adds
  a dated section above it rather than editing that record — the file is a ledger, not a page.
- `data/suggestions.json` (112 KB of rendered register, 23 proposals, 12 questions, ten discovery
  actions, two review rounds) is now a **historical** surface reachable from the reader nav, while the
  canonical decision desk is the generated `suggestions/index.html`. Two suggestion registers on one
  site is a coordination artefact, not a design: this pass left the historical one untouched and added
  the "how to add a suggestion" shape to the current one so future sessions have exactly one place to
  append.

## 5 · Files this session touched, and why nothing else was

| File | Change |
|---|---|
| `data/publication.json` | appended `paths[]`, `design_prompt{}`, `suggestion_intake{}`, two guides, seven questions, the `answer_by`/`answer_form` pair on all 16 questions; refreshed `checked_on`/`scope` for exactly the six sources re-read today; one count-neutral wording fix in `P26-S3` (`P27-F04`) |
| `tools/build_publication.py` | derived dates/counts; path chooser, answer-owner column, intake block, block-structured brief with per-block copy; two new guides flow through the existing article renderer |
| `assets/publication.css`, `assets/publication.js` | new components; generic clipboard handling that strips button labels from copied text |
| `data/flags.json` | six appended rows `P27-F01…06`, on top of the 158-row base |
| `DESIGN_PROMPT.md` | new root brief (rails R1–R12 with the clause quoted, measured inventory, component table, definition of done) |
| `README.md` | ownership section brought in line with the code; design-brief and decision-desk rows added |
| `EXECUTIVE-SUMMARY.md` | one dated section prepended; history left intact |
| `sessions/6b68afc8/**` | this review, the verification record, the data-update script, and the machine-readable gate/idempotency evidence |
| `COORDINATION.md` | this Part's claim and records only |
| generated: `index.html`, `guides/**`, `suggestions/index.html`, `executive-brief.html`, `flagged.html`, `publication-pass.html`, `sitemap.xml`, `feed.xml`, `assets/publication-search.json`, `sessions/aebf0747/**` | written by their own builders, never by hand |

Nothing in `shop/**`, `site/**`, `read/**`, `marketing/**`, `data/products.json`,
`data/decision-queue.json` or another session's `data/cba81fa5/**` was edited: their registers stay
owned by their generators, and no gate required an exception this time.

## 6 · Rebase record (this is the part worth reading before the next session pushes)

`git pull --rebase` was not enough, so here is exactly what happened and what was not done.

| Step | Outcome |
|---|---|
| `git fetch` at push time | `origin/main` had moved `825f513 → 530d9d9`: PRs **#173** (independent re-verification of the five links), **#174**, **#175** (buyer-journey polish: unique titles, review workflow, three-question chooser, two-sided fit notes, og:image dimensions) and **#176** — 130 files, +3085/−2496 |
| Overlap | four files touched by both sides: `data/publication.json`, `data/flags.json`, `tools/build_publication.py`, `assets/publication.css`, plus the generated set |
| `git rebase` on the JSON registers | **not attempted as a line merge**: both sides appended to `flags[]`/`questions[]` and my migration rewrote `flags.json` at a different indent, which produces a whole-file diff and a real risk of a silently renumbered register |
| Method used | rebase the branch onto the new base by construction: reset the working branch to `origin/main`, re-apply this pass's *additive data* through the (guarded, still one-shot) migration script, append the CSS block and the JS file wholesale, and 3-way re-apply only the renderer diff — 5 conflict regions, each resolved below |
| Renderer resolutions | product-card date: upstream's `meta.reverified` semantics, humanised rather than the ISO string they would have printed; guide byline: my derived date **plus** upstream's "Sources re-checked" clause; comparison row: same treatment; `suggestions()`: my desk as the base, carrying upstream's richer proposal card (owner chip, `next_action`, "what it would tell us") and their `owner_input_needed` fallback; `executive()`: upstream's line, my table already carried the desk row |
| Deliberately kept from upstream | `REVERIFIED = DATA['meta']['reverified']` is the better source for a "sources were re-read" date than my `meta.updated`, so the re-check notes now read from it; the register-owned derivation is preserved because `REVERIFIED` is itself register data, not a literal |
| Gate response | first post-rebase build: 1 FAIL on the four prose-complete rows (§5 above) → fixed in the data, not by loosening the gate |
| After | `python3 tools/publish.py` → **41 commands, 0 failed**; second full run changed 0 files; `git diff --exit-code` clean |

What was *not* done, in one line each: no force-push to `main`, no merge commit papering over the
registers, no rewrite of `B79-*` or any other session's row, no deletion of my `P27-F05` in favour of
`B79-F-02`, and no edit to upstream's new gate.
