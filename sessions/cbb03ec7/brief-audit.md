# Brief gap audit — session cbb03ec7 (2026-11-17)

Line-by-line coverage of the owner's 2026-11-17 brief against what this repository ships,
read from the repository itself on 2026-11-17. Every "done" names the file or page that
carries it; every "gap" is either published as a flag/suggestion row or recorded here as
missing information. Nothing is inferred: where the brief references something the repo does
not define, the row says so.

Status vocabulary: **done** (shipped and gated), **partial** (shipped, with a named remainder),
**blocked** (cannot be built from this repository; the owner input is named), **gap** (absent).

## A. Brief clauses → repository state

| # | Brief clause | Status | Where / what is missing |
|---|---|---|---|
| A1 | Selected Tracking ID `shopnow047c-20` | **partial** | Recorded in `config/platform.json` (tag + status) and `data/shop/config.json`. Account assignment unverified (login-gated) and the value is in **no link** — flag `CBB-F-02`, question `CBB-Q-01`. |
| A2 | "Make it read like a shop, not an audit" | **done** | `/shop/` (11 pages, PR #135) plus the publication front page at the root (PR #136). The audit surfaces remain reachable from the footer/nav; overlap is flag `FLG-S10` / question `757-Q-11`. |
| A3 | "Make it findable" — one site to index | **done** | `sitemap.xml` (97 pages, `build_sitemap.py --check` green), unique titles/meta per page (`check_site`), `robots.txt`, canonical tags in the flat template. |
| A4 | Search Console | **blocked** | Needs an owner Google account + verification token. Row `SG-29` added to `data/suggestions.json`. |
| A5 | "Make the machinery trustworthy" — automate, gate the rest | **done** | Gates run green on this tree: `check_site`, `verify_site`, `link_report --strict`, `i2_gate`, `cba81fa5_lint`, `build_cba81fa5 --check`, `build_shop --check`, `build_sitemap --check`, `check_all_links`, repr test. One gate defect found and fixed this session (`CBB-F-04`). |
| A6 | "Make it read like a publication" — authorship, nav, brand, imagery, seasons, clusters | **partial** | Publication surface, guides, articles, brand working-name (`DEC-04`) and nav exist; imagery is flag `FLG-S08`/`DEC-05` (no product photography, by policy/decision), seasons/clusters not built. |
| A7 | Nav labels (SG-27) | **partial** | Four surfaces, four navs; row `SG-27` added (blocked on `757-Q-11`). |
| A8 | Shipped RSS feed (SG-28) | **partial** | `feed.xml` shipped with the four guides (PR #136) + autodiscovery markup; Research Desk articles are not in the feed — rows `SG-28` / `CBB-SUG-04`. |
| A9 | Reader capture (SG-30) | **blocked** | No form endpoint exists; GitHub Pages is static. Row `SG-30` added (blocked on Q5/Q8). |
| A10 | Lead with products, not verification | **done** | Publication front page (root `index.html`, PR #136) leads with products and guides; dashboards reachable from footer + nav groups. |
| A11 | Question-shaped guides; add each to sitemap and feed | **done** | The four brief hypotheses shipped verbatim as guides (`guides/basket-or-oven-style.html`, `capacity-checklist.html`, `cleanup-and-counter-space.html`, `multi-function-questions.html`), all in `sitemap.xml` and `feed.xml`. |
| A12 | Publishing cadence | **blocked** | Owner decision `DEC-06` / question `Q5` (named editor + cadence). |
| A13 | Real analytics so the next topic is chosen from measured queries | **blocked** | No analytics endpoint in the repo. Rows `CBB-SUG-03`, `SG-29`; shop record `DEC-03`/`FLG-S06`. |
| A14 | Outbound-click counter + self-hosted endpoint; record the five defined events | **blocked / gap** | Counter and endpoint are owner infrastructure (`DEC-03`). **The "five defined events" are not defined anywhere in this repository** — the brief references them but no event set exists in any data file; the owner must supply the definitions before they can be recorded (missing information, recorded here). |
| A15 | Disclosure above the fold on every page, repeated in the footer | **done** | `sessions/aebf0747/publish_pass.py` strip + footer; enforced by `check_site`, `i2_gate` G1/G2, `build_shop --check`. Re-run after every generator (documented order). |
| A16 | Every outbound product link `rel="sponsored"` | **done** | Same pass + gates (shop gate fails on an unmarked Amazon link; negative-tested by its session). |
| A17 | Product-intent confirmation record (intended ASIN, listing URL, date, source; observed redirects separate) | **done** | `intent-record/index.html` + `sessions/aebf0747/intent-record.json`; flat register keeps `redirect_observed` separate from identity fields (`data/products.json`). Intended ASINs still blank for all five — `FLG-001`, `CBB-F-01`. |
| A18 | Replace ambiguous outbound links with validated Special Links; test one link per product before scaling | **blocked** | Requires the Associates console (`CBB-Q-01`, shop `DEC-01`/`FLG-S04`). The brief's caution is preserved: no claim is made that the supplied short links are invalid (`FLG-003` cross-reference intact). |
| A19 | Buyer-question guide titles as working titles | **done** | Shipped as the four guides; labelled as working titles, no popularity/superiority claims. |
| A20 | Priority 4 — empty campaign ledger, dated provenance, no forecasts | **done** | `campaigns.html` + `data/shop/campaign-ledger.json` (empty by design, columns + provenance rule documented). |
| A21 | Priority 5 — disclosures and API policy checks in the publishing workflow | **done** | `i2_gate`, `cba81fa5_lint`, `build_shop --check`, `publish_pass`; sources `S01`, `S07`, `S24` in the register. |
| A22 | S-04…S-25 status list (titles/meta, sponsored, thin-affiliation, one-page-per-question, social preview/structured data, docs-in-line, flag cross-refs, voice, topic calendar, design brief, brand, evidence rule, editorial front page, photography, chooser, mobile-first, counter-space, internal linking, organic traffic) | **partial** | Per the brief: S-04/05/07/09/12/13/14/15/16/17/19/23/24 implemented; S-06 not adopted (recorded decision); S-10/11 partly; **S-18 (photography) needs a decision first (D-22); S-20 (mobile-first pass) and S-25 (organic traffic on the verification angle) have no implementation record in the repo — gaps recorded here**. |
| A23 | Suggestions section for review before any change | **done** | Four review surfaces: `suggestions.html` (+ `CBB-SUG-01…04`, `SG-27…30` this session), `decision-queue.html` (18 questions), `shop/decisions/`, `site/answers.html`, `publication-pass.html`. |
| A24 | Clear list of questions/information/answers needed before decisions | **done** | `decision-queue.html`: have/missing/questions/discovery/workflow tables; this session added `CBB-Q-01…03`, `CBB-D-01…02`, `CBB-M-01`. |
| A25 | Executive summary | **done** | `EXECUTIVE-SUMMARY.md` + `executive-summary.html` (+ §13 this session) and `shop/executive-summary/`. |
| A26 | Marketing for the five links | **partial** | Flat marketing section: three air-fryer briefs + comparison + buying guide. All five links: `shop/products/` + both category pages, and (this session) `products.html`/`pricing.html`/`reviews.html` rows. **Briefs for products 4–5 are deliberately not written until the scope question `CBB-Q-03` is answered.** |
| A27 | AI-powered platform (research → content → links → tracking → optimisation) | **partial** | Intake/verification/build/gate pipeline shipped; trending/conversion optimisation blocked on official data (`FLG-016` permission problem, `FLG-006` API prerequisite) — recorded in §4 of the executive summary. |
| A28 | Repo review, line by line, flag irregularities, sources for manual review | **done** | This audit + `CBB-F-01…04` on `flagged.html`, each with source links. |
| A29 | GitHub Pages live site, clean landing + subpages by category, tables + analysis | **done** | Pages source `main` `/`; this session's integration verified after deploy (record in `COORDINATION.md`). |
| A30 | Verification: every table row sourced; blank + flag when unconfirmed | **done** | `check_site` + `verify_site` V4 green; P4/P5 identity cells blank by rule; new sources `S70–S75`. |
| A31 | Parallel sessions: COORDINATION claims, non-overlapping scopes, small commits, rebase before push | **done** | Claim `CB-T1…T5` pushed first; two rebase conflicts resolved keeping both sides in full; stale PR #123 closed as superseded, record PR #109 merged first (handoff logged). |
| A32 | PR → merge without waiting → Pages deploy → record | **done** | PR number, merge commit, Pages build and live checks recorded in `COORDINATION.md` (cbb03ec7 Part). |

## B. Missing information this audit discovered (not inferable from any source read)

1. **The "five defined events"** the brief asks the counter to record are not defined in any
   file of this repository. Owner must supply the event names/fields before implementation.
2. **Tag verification evidence** — `shopnow047c-20` exists as a value; its assignment to an
   Associates account has no official confirmation any session can read (`CBB-F-02`).
3. **Intended ASINs for links 4 and 5** (and still for 1–3) — owner input only (`CBB-F-01`).
4. **Category scope** — two of five destinations are meat thermometers; the next content batch
   depends on the owner's choice (`CBB-Q-03`).
5. **S-20 / S-25 implementation records** — the brief marks them blank; the repo contains no
   implementation or decision record for either, so they remain open suggestions.
6. **Analytics endpoint + reader-capture endpoint** — infrastructure decisions, not code
   (`SG-29`, `SG-30`, `DEC-03`).

## C. Irregularities raised by this session (published on `flagged.html`)

| ID | Severity | Summary |
|---|---|---|
| `CBB-F-01` | High | Two further submitted links (P4/P5): 9-char tokens, `/dp/` 404, destinations observed twice 2026-11-17, intent unconfirmed. |
| `CBB-F-02` | High | Tracking ID `shopnow047c-20` owner-supplied; assignment unverified; in no link; Special Link test required before scaling. |
| `CBB-F-03` | Medium | Two of five destinations are meat thermometers while editorial coverage is air fryers — scope decision `CBB-Q-03`. |
| `CBB-F-04` | Low | `check_site`'s nav rule did not accept the PR #136 front page (main's gate was failing from that merge); rule fixed to accept both nav systems. |

## D. Verification performed for this audit

- Two new short links fetched 2026-11-17 (link + bare listing URL each): titles and breadcrumbs
  matched across fetches → sources `S70–S75`.
- Direct `/dp/<token>` checks for both new tokens → Amazon "Page Not Found" (`S72`, `S75`).
- All gates re-run on the final tree (results in `COORDINATION.md`, cbb03ec7 Part).
- PRs on the board at session start: #109 merged (other session's record preserved), #123
  closed as superseded (fix already on main), neither losing work.
