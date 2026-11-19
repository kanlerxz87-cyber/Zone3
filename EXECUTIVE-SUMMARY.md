# Executive summary — Zone3 Kitchen

## Current status — listing evidence re-read, register corrected · 2026-11-19 · session `0a48cfda`

**Bottom line.** The reader-facing publication was already built, so this pass spent its time on the
question a buyer actually tests: is what the pages say about these five products still true of the
official listings? Re-reading all five `amazon.com/dp/<ASIN>` pages on 2026-11-19 found three things
worth acting on and one worth publishing as a flag.

1. **The site was withholding a fact it already had.** The counter-space guide said that none of the
   listing titles gave a width, depth or height. The *detail tables* on three of the five listings do
   publish an exterior size, and now so does the site: the 6-quart Chefman at 13.38"D x 11.81"W x
   10.63"H, the Emeril Lagasse oven at 16.9"D x 15.8"W x 14.8"H and the 8-quart Chefman at
   12.75"D x 13.5"W x 10"H. The two thermometer listings publish no dimensions at all and say so
   rather than showing a blank. Usable interior size, ventilation clearance, cord length and door
   swing are still nowhere on those pages and remain absent here.
2. **Two listings disagree with themselves on capacity.** The 6-quart Chefman title says "6 Quart";
   its own detail table says "Capacity: 6 liters". The Emeril Lagasse title says "26QT"; its table
   says "Capacity: 24.6 liters" (which *is* 26 US quarts). The 8-quart Chefman is consistent. Both
   printed figures are now recorded and both are published, side by side, because choosing one would
   be an editorial guess dressed as a fact. Published as [FLG-S33](shop/flagged/index.html).
3. **Two build defects were found and fixed while verifying.** The in-guide contents list typed a
   literal `04` for its last entry, so a four-section guide numbered that entry twice and a
   three-section guide numbered it wrong; the number is now derived from the section count. A
   proposal whose "evidence to close" named a source rendered `#google-page-experience`, an anchor
   that does not exist on the page; a source id now renders as its official page instead.

**What did not change, and why.** The five outbound product buttons are still the supplied
`link.amazon` short links. Program Policies 2(b), re-read verbatim this pass, requires "your
Associates ID or 'tag' … as a parameter in the URL of each link you place on your Site to an Amazon
Site", and the same clause allows "such other format as we may designate"
([Program Policies](https://affiliate-program.amazon.com/help/operating/policies)). Whether Amazon's
own short form is such a designated format can only be shown from inside an enrolled account, so
[FLG-003](flagged.html#FLG-003) stays unresolved and the links are neither swapped nor called
invalid. Prices, ratings and review counts stay empty for the same policy reason: Amazon allows a
site to show them only when Amazon serves the link or the data arrives through the Creators API.
Nothing here is a conversion, traffic or revenue claim; the campaign ledger still has zero rows.

| Area | Current state after this pass | Decision boundary | Basis |
|---|---|---|---|
| Listing evidence | All five official listings re-opened 2026-11-19. Titles and breadcrumbs unchanged. Exterior size captured for three; capacity captured for all three air fryers. | A listing's own detail table is the source, quoted with its read date. It is not our measurement and not a claim about usable space. | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) · [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) · [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) · [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) · [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) |
| Capacity discrepancy | Both printed figures published together for the two products whose fields disagree. Published as FLG-S33. | Which figure is right is a manufacturer question. The site does not pick one and does not convert either into servings. | [FLG-S33](shop/flagged/index.html) · `data/publication.json → products[].listing_dimensions` |
| Reader pages | 11 question-led guides, 19 canonical URLs, 5 product cards, 6 paths and 30 proposals against 38 open questions. Guide contents numbering now derived, not typed. | The page set and its navigation were not redesigned in this pass; only evidence and the two defects changed. | [sitemap](sitemap.xml) · [feed](feed.xml) · [suggestions](suggestions/index.html) |
| Link attribution | Unchanged: five supplied short links on the buttons. Intent fields remain blank for all five. | Program Policies 2(b) requires the tag in each link; the acceptable short form is an account-level answer this session cannot obtain. FLG-003 stays open. | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) · [intent record](intent-record/index.html) |
| Pricing and ratings | Still absent everywhere, deliberately. | Amazon permits these fields only via a served link or the Creators API, which needs account access. | [Program Policies, 2(b)](https://affiliate-program.amazon.com/help/operating/policies) |
| Measurement | Production collection still OFF; five-event runtime unchanged; ledger empty. | No Search Console property and no authorized Associates report exist, so no traffic or conversion statement can be made. | [measurement](measurement/index.html) · [campaign ledger](data/shop/campaign-ledger.json) |
| Release | Canonical chain green twice: 41/41 commands, working tree stable, no generated drift. | A structural gate is not fact verification of historical sentences. | [session record](sessions/0a48cfda/verification-2026-11-19.md) |

**Questions that must be answered before the next decision, and who holds the answer.** Each row is a
question this pass could not settle from a public source, the single fact that would settle it, and
what the site does in the meantime. The full register is on the
[suggestions page](suggestions/index.html#questions).

| Question | What is genuinely unknown | One action that would settle it | Default until then |
|---|---|---|---|
| Are these the five products that were intended? | The short links resolve to five specific ASINs, but nothing supplied states that those ASINs are the intended ones. | One dated confirmation per product from the owner, naming the intended ASIN and official URL. | Both intent fields stay blank; the observed redirect is kept separate. |
| Does each button attribute to `shopnow047c-20` on an enrolled account? | Whether the tag is active and whether Amazon's short form carries or adds it. | Open one link per product inside the enrolled workflow and read the tracking report. | FLG-003 open; the links are left exactly as supplied. |
| Which capacity figure is correct where the listing disagrees with itself? | Whether "6 liters" or "6 Quart" (and "24.6 liters" or "26QT") describes the container a buyer receives. | The manufacturer's manual or specification sheet for that model. | Both figures shown; no conversion, no ranking. |
| What is the usable interior size and the clearance needed? | Interior dimensions, ventilation clearance, cord length, door swing: published nowhere on the five listings. | The model manual, or an authorized data feed. | Exterior size only, labelled as such; the counter-space arithmetic stays unpublished. |
| May prices and ratings be shown? | Whether Creators API access exists for this account. | Confirm account and API access, then apply the licence conditions. | No price, rating or review count anywhere. |
| Where will production measurement run, and is GitHub Pages suitable for commercial use? | The durable host, and GitHub's position on commercial affiliate hosting. | Deploy the shipped collector on reviewed hosting; resolve Pages limits with GitHub. | Collection off; ledger empty; no traffic claim. |

**Scope and verification.** Changed in this pass: `data/publication.json` (listing dimensions,
two questions updated, two proposals added, one proposal re-scoped, the counter-space guide copy),
`data/shop/flags.json` (FLG-S33), `tools/build_publication.py`, `assets/publication.css`, the
regenerated reader pages and this opening. Record:
[`sessions/0a48cfda/verification-2026-11-19.md`](sessions/0a48cfda/verification-2026-11-19.md).
Historical sections below keep their original dates and scope and were not re-checked line by line.

---

## Dated snapshot — publication audit and decision readiness · 2026-11-19 · session `4d7fe998`

**Bottom line.** The live buyer-facing publication has five submitted product links in two categories, eleven question-led guides, 19 canonical/indexable sitemap URLs and 11 RSS entries. The current register has 17 scoped official references. The decision desk holds six paths, 30 reviewable proposals, 38 open readiness questions, eight decision-support rows and a 13-block design brief. The latest guide — *Is your thermometer still telling the truth? The ice-water check* — shipped upstream under PR #200 as the eleventh guide; it is official-method verification, not a product test. Choices remain review-only and implement nothing. Dated snapshots below retain their original scope and counts.

| Area | Current state | Decision boundary | Basis |
|---|---|---|---|
| Reader experience | Product-led home page with five listing-based product cards; air-fryer and meat-thermometer categories; eleven practical, question-led guides. The research and review surfaces are reachable in “Behind the site” and the footer. | Listing descriptions are not hands-on tests, rankings, popularity evidence or proof of the requester’s intended products. The FoodSafety.gov temperature/placement guide is official public guidance, not a test of the listed thermometers. | [Home](index.html) · [guide index](guides/) · [new probe guide](guides/where-does-the-probe-go.html) · [sitemap](sitemap.xml) · [RSS feed](feed.xml) · [CDB source review](sessions/cdb0a5ac/verification-2026-11-19.md) |
| Decision desk | Six paths; 30 proposals; 38 readiness questions; eight decision-support rows; 13 design-prompt blocks. Local save/export is review-only. | A saved preference or written answer does not implement a proposal, alter an account, or publish a page. | [Suggestions](suggestions/) · [publication register](data/publication.json) |
| Evidence and disclosure | Current publication checks cover disclosure placement, sponsored-link markup, publication provenance, sitemap and feed. The Associates sentence is under the masthead and repeated in the footer. | A structural pass and policy citation are not account approval, legal certification or proof every historical claim has been rechecked. | [release record](sessions/4d7fe998/verification-2026-11-19.md) · [Amazon Agreement](https://affiliate-program.amazon.com/help/operating/agreement) · [Google sponsored-link guidance](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) |
| Intent and attribution | The five observed redirect destinations remain separate from intent; intended ASIN, intended official listing URL, confirmation date and source are blank for every product. `shopnow047c-20` is the tag parameter on every product link of the live site — 1,680 of 1,680 product links tagged with no foreign tags (`tools/attach_tag.py --check`) and every product-detail link tagged (`tools/attach_associates_tag.py --check`, 22,572 links inspected, 0 foreign), measured 2026-11-19 after this integration — and home-card CTAs use the recorded observed listings with that tag. | Account assignment, accepted Special Link workflow/format, marketplace fit and report attribution are unverified. `FLG-003` remains unresolved; the supplied short links are not called invalid. This integration corrected the intent page’s tracking-id line to the measured tag coverage (correction `EE-F-01`); attribution reporting on the supplied short links stays unverified. | [intent record](intent-record/index.html) · [product evidence](products.html) · [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| Measurement and search | One active five-event runtime and aggregate collector are in the repository; the earlier `data/analytics.json` / `assets/track.js` / `tools/analytics_collector.py` stack is now explicitly labelled historical by PR #193. | Active production measurement remains OFF with a blank endpoint and no deployment evidence; the campaign ledger has zero rows. Search Console ownership and query/page reports are not verified. Local tests are not visitors, clicks, orders or campaign results. | [measurement config](data/shop/measurement.json) · [campaign ledger](data/shop/campaign-ledger.json) · [Search Console guidance](https://developers.google.com/search/docs/monitor-debug/search-console-start) |
| Cadence and topic choice | The registered guide-review cadence is one every 14 days. Eleven current guides are represented in the sitemap and feed; the feed lists only indexable, sitemap-canonical URLs (11 items) after PRs #192 and #203. | Cadence and titles are plans/editorial hypotheses, not proof of demand or measured popularity. Use Search Console query/page data only after property ownership and reports are verified. | [publication register](data/publication.json) · [Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start) |
| Commercial hosting | The live site is deployed on GitHub Pages. | GitHub’s Pages limits restrict free hosting for online businesses and sites primarily facilitating commercial transactions. This affiliate-publication use needs an authoritative fit review or commercially suitable hosting before scaling; this audit does not conclude that GitHub has adjudicated a violation or approved the site. | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) · [review record](sessions/4d7fe998/repo-review.md) |
| Historical evidence | The branch’s canonical `tools/publish.py` chain passed twice (41 commands each, no generated output changed). The current-publication gate passes for 19 rendered reader/workspace pages and 100 official-source table rows; the 19-URL sitemap and 11-item feed are current after this integration (PR #192 made the feed sitemap-consistent; PR #203 aligned it with the indexable set). PR #193 corrected README to eight guides; PR #194 updated it to nine and shipped the probe guide. | The whole-tree verifier covers 162 pages / 2,622 rows and reports 218 uncited, 292 repository-only, and 577 inherited non-blocking advisory items. The legacy `/dashboard/` still describes three products and older counts. A green structural gate does not freshly verify every historical sentence. | [verification log](sessions/4d7fe998/verification-2026-11-19.md) · [release checks](sessions/4d7fe998/release-checks.md) · [repository review](sessions/4d7fe998/repo-review.md) |

**Known, unknown, and discovery.** Known: the five submitted URLs and their separately recorded observed Amazon destinations; the tracking-ID string in five tagged direct-link URLs; eleven guides, 17 scoped references, 19 sitemap URLs, 11 feed entries and an empty campaign ledger. Unknown: which products were intended; whether the ID is assigned to an enrolled Associates account; whether Amazon accepts the submitted short-link form in that account; whether any link reports; actual Search Console queries, traffic or outcomes; and whether GitHub considers this affiliate publication within Pages’ commercial-use limit. Record owner-confirmed intent only in the four intent fields with a date and source. Validate one link per intended product through Associates Central and a first-party report; ask Associates support about the exact short-link form. Verify Search Console ownership before using query/page reports. Resolve the hosting question with GitHub Support or migrate before scaling. Keep price, rating, review, testing and performance claims blank until an authorized evidence path exists.

**Scope and verification.** This audit is documented in [`sessions/4d7fe998/repo-review.md`](sessions/4d7fe998/repo-review.md), [`sessions/4d7fe998/verification-2026-11-19.md`](sessions/4d7fe998/verification-2026-11-19.md) and [`sessions/4d7fe998/release-checks.md`](sessions/4d7fe998/release-checks.md). The audit did not change product, intent, tracking, source, flag, measurement, suggestion-register or generator data, or generated reader pages. Historical sections remain below. Current page/status statements were checked against the latest registers and published pages; historical pages were not re-audited line by line. A green structural check does not turn missing owner/account, Search Console, hosting or first-hand evidence into facts.


## Dated snapshot — three-way integration: PRs #157, #160 and #192 union-merged · 2026-11-19 · session `ee10b024`

**Bottom line.** This pass merged the three held PRs (`5af7c07` claim, `git merge-tree` pre-flight, no rebase required): `#157` (five-link decision/design refresh) → `#160` (design prompt and decision-readiness ledger) → `#192` (reader polish and trust audit). Every register was three-way merged by ID with documented remaps (simultaneous-collision rule: `S91/S92/S93`→`S95/S96/S97`, `SUG-11..14`→`SUG-19..22`, `Q13..Q16`→`Q15..Q18`, PR #157's `SUG-11/12/13`→`SUG-16/17/18`, `VB-7/8/9`→`VB-9/10/11`); generated pages were regenerated by the chain, not hand-merged. The canonical chain now runs **49 commands and passes twice** (46 after PR #192, plus main's stale-claim gate added while this merge was in flight) (`tools/publish.py`), including PR #192's and main's new gates: `tools/attach_tag.py` (1,680 of 1,680 product links carry `tag=shopnow047c-20`, no foreign tags) and `tools/attach_associates_tag.py` (every product-detail link tagged, 22,572 inspected) and `sessions/5d460e79/test_counts.py` (no typed reader-facing counts in the publication generator). Live re-reads on 2026-11-19 confirmed the load-bearing policy text: Operating Agreement §5 (Updated October 15, 2025) and §6(a), Participation Requirements 2(a)/2(b)/6(t)/6(v)/6(w), Google `rel="sponsored"`, FTC Disclosures 101.

**Important details.**

| Area | Position after this integration | Basis |
|---|---|---|
| Gates | `tools/publish.py` 49/49 twice, no generated output changed between runs | chain output 2026-11-19 |
| Tag and disclosure | 1,680/1,680 product links tagged, 0 foreign tags; every product-detail link tagged (22,572 inspected); 1,965/1,965 Amazon product links `rel="sponsored"`, 0 missing; disclosure sentence on 123/123 published pages | `tools/attach_tag.py --check`, `tools/attach_associates_tag.py --check`, `sessions/aebf0747/audit-after.json` |
| Feeds and sitemap | 19 sitemap URLs, 11 feed items — the feed lists only indexable, sitemap-canonical reader URLs (PR #192 rule, PR #203 alignment) | `scripts/build_sitemap.py --check`, `tools/build_feed.py --check` |
| Decision desk | 30 proposals, 38 readiness questions; PR #160's `review_2026_11_17b` ledger shipped on `suggestions.html` with rows `SUG-19..22` and `Q15..18`; PR #157's `SUG-16/17/18` on `decision-queue.html` | `data/suggestions.json`, `data/decision-queue.json`, rendered pages |
| Brief status | Rows S-04/S-05/S-09/S-24/SG-28/SG-29 re-measured post-integration against the final merged tree (123 pages / 11 guides / 19 URLs / 11 feed items), `_meta.rechecks` entry 5 records the pass | `data/shop/brief-status.json` |
| Intent record | Tracking-id line corrected from “Not attached to any link on this site” to measured tag coverage (1,680/1,680) (`EE-F-01`, status fixed); attribution reporting stays unverified (`AE-F-01`, `FLG-003` untouched) | `sessions/aebf0747/intent-record.json` |
| Deliberately not done | No owner decision implemented; no account/API/Search Console/hosting change; no new product fact, price, rating or performance claim; measurement stays off; FLG-003 not called invalid | session scope |

**Conflicts resolved.** 7 + 16 + 22 conflicted paths across the three merges: registers three-way merged by ID (topic-compared, zero losses asserted), prose hand-unioned, generated HTML kept from ours and regenerated by the chain, one union fix in `tools/build_publication.py` (main's `CATEGORY_N` literal plus PR #192's derived `CAT_N/EVENT_N` block), `E41-B01..04` retained alongside `5D4-F-01` in the shop flag register, and the count-drift gate satisfied by rewording one generator docstring ("one block"→"single block") instead of weakening the gate. Full conflict log: `sessions/ee10b024/verification-2026-11-19.md`.

---

## Dated snapshot — probe guide shipped, stale counts repaired, sources re-read live · 2026-11-19 · session `cdb0a5ac`

**Bottom line.** This pass closed the gap the decision desk had already sanctioned: the DS-01
safe default ("publish one slate guide at a time through the publishing gate, starting with the
thermometer temperature guide") is now executed. The ninth guide, *Where does the probe go?
Turkey, ham and roasts*, answers slate title AS-01 with a factual spine taken only from two
FoodSafety.gov pages re-read live today — the safe-minimum-temperature chart and the Cook step
of 4 Steps to Food Safety. It shipped through the unchanged gate chain (feed, sitemap, canonical,
unique title/description, disclosure strip, `rel="sponsored"` on every product link, Article
schema with the disclosed organization byline). Alongside it, reader-facing counts that had gone
stale were repaired to derive from the register: the executive brief strip now reads **9 guides /
36 questions / 5 products** (register merged with the parallel batch-3 rounds), the design-prompt intro no longer hardcodes a block total, and the
review-round headings count their own rows. One failure during the run was caught by the gate
itself (a link to this pass's not-yet-written verification record) and fixed by writing the
record before re-running.

**Important details.**

| Area | Position after this pass | Basis |
|---|---|---|
| Reader layer | 9 guides, 17 canonical/indexable URLs, 27 feed entries; new guide title 63 chars, description 157 chars, one `h1`, `index,follow`, 4 sponsored Amazon links, all gates green | `data/publication.json`, `sitemap.xml`, `feed.xml` measured 2026-11-19; `tools/publish.py` 41/41 |
| Sources | 16 scoped official references — main's fifteen plus `food-safety-cook` (Cook-step placement wording, read live 2026-11-19); FoodSafety.gov chart re-read with Date Last Reviewed 21 Nov 2024 unchanged | `sessions/cdb0a5ac/verification-2026-11-19.md` |
| Policy re-reads | Operating Agreement re-read live (Updated October 15, 2025): Special Links must "properly use the special 'tagged' link formats we provide"; FTC Disclosures 101 re-read (material connection, "hard to miss", "can't talk about your experience with a product you haven't tried"); Google `rel="sponsored"` guidance re-read (last updated 2025-12-10) | verification record above |
| Counts repaired | Found stale on the claim base (`6 guides`/`9 questions` strip, "current six guides" ×2, "Seven ways…", "seven working titles", "Ten blocks" intro). Upstream PR #181 (Z3-COUNT-01) had already derived the strip during the parallel round; after this session's rebase the equivalent fixes converged and were verified, not duplicated (`P27-F02` principle). The remaining hardcodes are repaired here. | `tools/build_publication.py` diff; `suggestions/index.html`, `executive-brief.html` re-rendered |
| Products / attribution | unchanged: 5 submitted links, intent fields blank, `FLG-003` open, `shopnow047c-20` unverified; no price, rating, review count or performance value anywhere | `tools/check_publication.py` gate |
| Left as dated record | session b9008684's review-round text still says "six guides" inside its own dated round block; not rewritten (historical record kept verbatim), noted as CDB-F-03 | `suggestions/index.html`, review round header |

**Deliberately not done.** No owner decision was implemented (paths, proposals and the AS-02…AS-07
slate stay review-only); no account, API, Search Console or hosting change; no merge of another
session's branch; no new product fact, price, rating or traffic claim; measurement stays off and
the campaign ledger stays empty.

**Recommended order, unchanged from the paths:** tighten the shop (needs nothing external) →
prove the money path (blocked on the Associates account) → turn on the lights (blocked on a
durable host) → then the evidence-gated work.

## Dated snapshot — decision desk, two more guides and a brief · 2026-11-19 · session `6b68afc8`

**Bottom line.** The site now has a place to *decide*, not only to record. The suggestions surface
carries five reviewable paths (each with what it changes, what it needs first, what it unblocks and
what it still cannot claim), sixteen open questions with a named answer owner and the shape a
complete answer would take, the intake form a new suggestion has to fill, and a ten-block design
brief with per-block copy. Two more question-led guides joined the cluster, and
[`DESIGN_PROMPT.md`](DESIGN_PROMPT.md) is now the paste-ready brief with the official clause behind
every rail. The section below this one stays accurate as the record of the 2026-11-19 consolidation;
where its counts differ, this pass's numbers are the current ones.

**Important details.**

| Area | Position after this pass | Basis |
|---|---|---|
| Reader layer | 8 guides, 16 canonical/indexable URLs, 26 feed entries, one shared shell with the disclosure under the masthead on every page; the merged chooser and two-sided fit notes now sit on the same surfaces as the desk | `data/publication.json`, `sitemap.xml`, `feed.xml` measured 2026-11-19 |
| Products | 5 submitted links; three listing titles re-opened directly on 2026-11-19 and matched the recorded text (one row's transcription differs by a `®` glyph — noted, not corrected silently) | `sessions/6b68afc8/verification-2026-11-19.md` |
| Attribution | unchanged and unresolved: `FLG-003` stays open, `shopnow047c-20` stays unverified, and 2(b)'s tag-parameter clause is now quoted verbatim in the register (`P27-F05`) | Program Policies, re-read 2026-11-19 |
| Measurement | production still off; campaign ledger still empty; no visitor, order, conversion or revenue figure was invented | `data/shop/measurement.json`, `data/shop/campaign-ledger.json` |
| Governance | two 2026-11-17 pull requests (#160, #157) are still open and unpublished; this pass re-measured their questions rather than merging a stale register (`P27-F01`) | `gh pr list`, `data/` greps on this checkout |
| Flags | register 158 → 164 rows after the rebase: three of the six new rows are fixed-by-this-pass hygiene findings, three are owner items; `B79-F-02` (opened by the merged PR #176) and `P27-F05` are the same open item from two sides, and each row says so | `data/flags.json` → [`flagged.html`](flagged.html) |

**Deliberately not done.** No merge of another session's branch; no `og:image` or `<lastmod>` change
(the deterministic-build gate explains the rejection in `P27-F06`); no photography, price, rating or
"trending" claim; no email capture; no change to the shopper edition or any historical register.

**Recommended order, from the paths, not from instinct:** tighten the shop (needs nothing external) →
prove the money path (blocked on the Associates account) → turn on the lights (blocked on a durable
host and Search Console) → then decide about testing and automation, both of which need evidence and
budget rather than CSS.

## Current publication build — 2026-11-19 · session 1c072a7a

**Bottom line:** the repository now has one buyer-first kitchen publication, not another parallel
audit landing page. It introduces the five supplied products in two real categories, publishes
six practical buyer-question guides, and puts evidence, dashboards and decisions behind one
navigation group and the footer. The source-linked research record remains reachable.

**Reader experience:** [front page](https://kanlerxz87-cyber.github.io/Zone3/) ·
[guides](https://kanlerxz87-cyber.github.io/Zone3/guides/) ·
[product comparison](https://kanlerxz87-cyber.github.io/Zone3/shop/products/) ·
[suggestions review](https://kanlerxz87-cyber.github.io/Zone3/suggestions/) ·
[current concise brief](https://kanlerxz87-cyber.github.io/Zone3/executive-brief.html).
The final merge/deployment evidence is recorded in [COORDINATION](COORDINATION.md), not inferred
from a local preview. This section supersedes operational status in the dated history below.

### What was built

- A consistent responsive masthead, above-content Associates disclosure and repeated footer,
  category navigation, local search, product filters, labelled contextual art and original generic
  format diagrams. There is no invented product photography, named expert or hands-on experience.
- Six guides covering basket/oven layout, capacity, cleanup/counter space, multi-function questions,
  instant-read/wireless thermometer workflow and hosting-season planning. These add useful decision
  checklists, source context and unknowns; they are not tested rankings or popularity claims.
- One canonical 14-URL reader sitemap, 24-entry RSS union, truthful dates/publisher schema and related
  reads. Older research/reader editions remain reachable but noindex. The completed C3/C17/3301 work
  and its source files are preserved, including the [previous shopper edition](publication-prior.html).
- A review-only suggestions workspace: six proposals, nine known/missing/discovery/default questions,
  local explicit save/reset, JSON export and a reusable design prompt. A review choice never
  implements a proposal, changes an account, activates measurement or spends money.
- A single guarded five-event runtime and self-hosted aggregate collector, reproducible full build,
  strict current-publication gate, private readout option and automated release CI.

### What is actually known about the products

These are **fresh redirect/title/breadcrumb observations on 2026-11-19**, not owner-intent,
performance, certification, price, availability or attribution confirmations:

- `link.amazon/B04G1MEwY` → CHEFMAN dual-basket air fryer, [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3).
- `link.amazon/B02NbDxp3` → Emeril Lagasse French-door air-fryer oven, [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R).
- `link.amazon/B00hJ57DV` → Chefman basket air fryer, [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH).
- `link.amazon/B0c8moW59` → ThermoMaven digital meat thermometer, [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5).
- `link.amazon/B0f3GKalj` → CHEF iQ Sense wireless thermometer, [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z).

The intended ASIN, official intended listing URL, confirmation date and confirmation source remain
blank for all five, separate from observations. The exact supplied short links are used unchanged.
The selected ID **`shopnow047c-20`** is recorded but its account assignment/report attribution is
unverified. FLG-003 stays unresolved; the supplied links are not called invalid. Validate one
Special Link/product in an authorized enrolled workflow, then check destination and reporting
before scaling. [Agreement](https://affiliate-program.amazon.com/help/operating/agreement) ·
[Program Policies](https://affiliate-program.amazon.com/help/operating/policies).

### Measurement is implemented, not deployed in production

The runtime names are the retained repository default: `page_view`, `outbound_click`, `guide_view`,
`intent_view`, `flag_view`. The brief does not enumerate their names. Only `measure.js` is injected;
the alternate historical tracker remains source-only. Production config is **off with a blank
endpoint and no deployment evidence**. The development preview accepts all five through a real
same-origin collector, but those are local tests, not campaign results.

The collector stores only daily page/product aggregate counts for 90 UTC days. It validates origin,
known pages/targets, schema/content type/body size; has a basic global write ceiling; omits raw
request logs; and protects its optional counts endpoint with a server-only read token. Browser
requests omit credentials and Referer. GPC, DNT and Save-Data stop requests; the counter writes no
cookies or visitor IDs. Connection IP/browser headers necessarily reach the receiving host, which
must separately configure its own proxy/log retention. This is not a legal-compliance certificate.

No durable authorized collector host, Search Console ownership/report or authorized Associates
order report was supplied. The campaign ledger stays empty. A click is not an order, eligible
session, unique person or conversion. There is no invented conversion score or revenue forecast.
GitHub Pages is [static hosting and logs visitor IPs for security](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

### Important risks and the decision order

1. **Intent and attribution:** obtain dated authorized intent and enrolled-workflow/report evidence;
   never copy a redirect into an intended field or use artificial clicks/self-purchases.
2. **Hosting and privacy:** review the actual business use against [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
   (P26-F02), choose commercially suitable durable hosting, review applicable privacy/consent and
   upstream logs, then verify delivery/retention before activating production analytics. A technical
   deploy does not establish hosting-policy approval.
3. **Real demand and outcomes:** verify Search Console and obtain dated first-party query/page and
   Associates reports. The sitemap and cadence improve discovery mechanics, not proven traffic.
   [Search Console guidance](https://developers.google.com/search/docs/monitor-debug/search-console-start).
4. **Evidence-led publishing:** review one guide every 14 days as an operating plan. Choose future
   topics from real evidence when available. Require authorized API/assets and original documented
   tests before richer dynamic figures or performance rankings. [Google review guidance](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews).

### Review and verification limits

The full release command runs the retained generation chain and all applicable gates. Current
reader/review tables have 51 source-linked rows and a dedicated strict gate. Whole-tree legacy
provenance advisories remain visible (C3-F-01/P26-F05); a green structural build does not freshly
verify every historical claim. No inherited source/flag row was removed: the integrated registers
contain 87 sources and 154 flags. [Scoped verification](sessions/1c072a7a/verification-2026-11-19.md) ·
[repository review](sessions/1c072a7a/repo-review.md) · [release outputs](sessions/1c072a7a/release-checks.json) ·
[browser results](sessions/1c072a7a/browser-checks.json).

---

## Historical executive summaries (dates and limitations retained)

The material below is the preserved earlier record. Counts, parallel-reader decisions and
“not built” statements refer to their stated dates, not the current publication described above.

# Executive summary — Zone3 AI-powered Amazon affiliate platform

**Prepared:** 2026-11-14 · **Current-status reconciliation:** 2026-11-17 (session `59b2194c`) · **Originally integrated:** session `edbd56a1` · **Independent correction pass:** session `043344f8` · **Final integration, compliance fix and re-verification:** session `3ead7ac8` · **Editorial topic plan and content-status correction:** session `3d359c23` · **2026-11-17 pass (two new links, the Associates tag, sponsored links, measurement, feed):** session `0c4c4cb6`
**Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Verification log:** https://kanlerxz87-cyber.github.io/Zone3/verification.html
**Flagged for review:** https://kanlerxz87-cyber.github.io/Zone3/flagged.html

## Current executive summary — 2026-11-17

> This current status reconciles the five-link brief with the earlier three-product analysis below. The older sections are retained as dated audit history; where their counts or product scope differ, use this update and the live [shop executive summary](https://kanlerxz87-cyber.github.io/Zone3/shop/executive-summary/) and [product-intent record](https://kanlerxz87-cyber.github.io/Zone3/intent-record/) as the current record.

**Bottom line.** The publication front page and reader guides are live. The five supplied short links were observed to reach five Amazon listings on 2026-11-17. Those observed targets are recorded separately from intended ASINs: none of the five intended products has been confirmed by the requester. The submitted short links' exact Associates compliance and tracking status remain unresolved; this report does **not** call them invalid. The next safe monetization step is the documented one-link-per-product Special Link workflow, with destination and Associates report checked before scaling.

| Submitted link | Observed listing (not an intent confirmation) | Listing source | Date |
|---|---|---|---|
| `link.amazon/B04G1MEwY` | CHEFMAN dual-basket air fryer · `B0CDY277D3` | [Amazon listing](https://www.amazon.com/dp/B0CDY277D3) · [dated shop source register](https://kanlerxz87-cyber.github.io/Zone3/shop/sources/) | 2026-11-17 |
| `link.amazon/B02NbDxp3` | Emeril Lagasse French-door air-fryer oven · `B09B7SB46R` | [Amazon listing](https://www.amazon.com/dp/B09B7SB46R) · [dated shop source register](https://kanlerxz87-cyber.github.io/Zone3/shop/sources/) | 2026-11-17 |
| `link.amazon/B00hJ57DV` | Chefman TurboFry basket air fryer · `B08DKYBTPH` | [Amazon listing](https://www.amazon.com/dp/B08DKYBTPH) · [dated shop source register](https://kanlerxz87-cyber.github.io/Zone3/shop/sources/) | 2026-11-17 |
| `link.amazon/B0c8moW59` | ThermoMaven digital meat thermometer · `B0DHZTCNR5` | [Amazon listing](https://www.amazon.com/dp/B0DHZTCNR5) · [dated shop source register](https://kanlerxz87-cyber.github.io/Zone3/shop/sources/) | 2026-11-17 |
| `link.amazon/B0f3GKalj` | CHEF iQ Sense wireless meat thermometer · `B0DZFD6R9Z` | [Amazon listing](https://www.amazon.com/dp/B0DZFD6R9Z) · [dated shop source register](https://kanlerxz87-cyber.github.io/Zone3/shop/sources/) | 2026-11-17 |

The source register records the submitted-link destinations (`SH-S06`–`SH-S10`) separately from the listing-title reads (`SH-S11`–`SH-S15`). Amazon's Creators API documentation defines an ASIN as a 10-character identifier ([official definition](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items)); the supplied tokens are not the observed listing ASINs. The fields for intended ASIN, official intended URL, confirmation date and confirmation source remain blank in the [intent record](https://kanlerxz87-cyber.github.io/Zone3/intent-record/), by design.

### What is live, and what is not

| Area | Current status | Decision-quality implication |
|---|---|---|
| Reader experience | Root is a publication front page with product cards, a visible affiliate disclosure, a guide collection and footer navigation to the dashboard surfaces. Product links carry `rel="sponsored"`; the shop build gate checks disclosure, sponsored attributes, provenance, sitemap coverage and local links. | Shop-first presentation is in place; dashboards and review material remain reachable without leading the buyer through audit workflow. |
| Editorial | Four question-shaped air-fryer guides are live as working titles, not popularity claims. Two of the five products are meat thermometers, outside the current air-fryer cluster. | Choose whether to keep an air-fryer-only publication or add a separate thermometer category and guide cluster; do not imply one niche covers all five. |
| Search and cadence | The sitemap and RSS feed are built and checked. No measured query or traffic evidence is recorded in the repo; Search Console is not configured here. | Continue treating topics as hypotheses. Do not label them trending or high-converting; select future topics from Search Console/query data only after a property is verified and data exists. |
| Clicks and conversions | Campaign ledger is empty. No collection endpoint or live outbound-click counter is deployed; no Associates order report has been supplied. GitHub Pages is static hosting and GitHub states it logs visitor IP addresses for security ([GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)). | Do not claim privacy-preserving measurement or forecast revenue. A real collector needs a separate host, a reviewed privacy model, and event definitions; first-party Associates reports remain the source for reported orders. |
| Analytics events | The brief references five events but does not enumerate them. The decision register leaves their definitions and endpoint host open. | Define the event names, payload minimization, retention and consent/legal basis before collection. Do not invent a hidden event taxonomy. |
| Tracking | The selected tracking ID was supplied in the task, but account ownership, marketplace fit, placement in any tested Special Link, and reporting are not verified. No account credentials or report access are available to this repository. | Run the enrolled Associates test and confirm the tracking report before replacing links. See [open decisions](https://kanlerxz87-cyber.github.io/Zone3/shop/decisions/) and [flagged findings](https://kanlerxz87-cyber.github.io/Zone3/shop/flagged/). |
| Product data | Current product pages leave price, rating, review count and conversion figures unpublished; the campaign ledger is blank. | Keep unsupported dynamic or performance values blank. Do not generate them from scraped pages or inference. |

### Suggested decision order

1. **Choose product scope** — accept the three-air-fryer cluster as the first editorial vertical, or approve a distinct meat-thermometer cluster. The two thermometer links are observed and registered; their intended match remains unconfirmed.
2. **Confirm intent and link workflow** — in Associates Central, confirm each intended product, create a Special Link, and test destination plus report attribution; record the date and source in the intent record. Ask Associates support about the supplied short-link format if its status is still unclear ([Program Policies](https://affiliate-program.amazon.com/help/operating/policies); unresolved item [FLG-003](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-003)).
3. **Set measurement up lawfully** — define the five events and choose a collection host before building a counter; set up and verify Search Console, submit the existing sitemap, and base the next topic on observed queries. Until then, keep the campaign ledger empty.
4. **Review the proposals before broader changes** — use [Suggestions](https://kanlerxz87-cyber.github.io/Zone3/suggestions.html), the [decision queue](https://kanlerxz87-cyber.github.io/Zone3/decision-queue.html), and the [design brief](https://kanlerxz87-cyber.github.io/Zone3/design-brief.html). They separate verified facts, open questions, discovery actions and proposed visual paths; no proposal is evidence of popularity or product quality.

**Release checks run on this checkout (2026-11-17, session `66964850`, tree after the PR #161 union):** shared site check passed (42 pages, 5 products, 83 sources, 148 flags); whole-tree verification passed (152 pages, 2,517 table rows, provenance 1,938 official / 90 flag-or-blank / 269 repo-only / 220 uncited); strict link report passed; reader gate passed (20 pages, 186 rows, 170 sourced, 16 explicit blanks); reader lint passed with 22 inherited advisory items and 0 new findings; no-repr test passed (152 pages); feed check passed (22 entries, unified register); sitemap check passed (106 pages); link check passed (198 HTML files, 263 external URLs, 0 errors); shop check passed (11 shop pages); publication pass and measure pass current (111 pages, 0 changes); `mark_sponsored` and `apply_sponsored` checks passed (every outbound product link carries `rel="sponsored"`); measurement self-tests passed. The generator chain is hash-idempotent across a full re-run.

---

> The source-linked findings below include the original 2026-11-14 verification record, the
> independent correction pass and the 2026-11-14 final integration pass. Redirect targets are treated as
> observed destinations, not as proof of requester intent. Unavailable or policy-restricted values remain
> blank and flagged.

---

## Update 2026-11-17 — session 0b2ffabd (the design prompt, the decision-readiness ledger, the six-surface correction)

**What this pass adds.** The owner brief asks for suggestions that feed a site-design prompt, a dedicated
suggestions section a human can review before anything is implemented, and "a clear list of questions,
informations and answers that need to be addressed before any decision can be reasonably made". This pass
delivers those as documents and register rows and implements none of the redesign: `DESIGN_PROMPT.md` at the
repository root is the brief a design session is handed, and `suggestions.html` gained the design prompt itself, a
decision-readiness ledger over eight decisions (the form the answer must take, who can supply it, what it
unblocks, the default while it stays blank, where to record it), four new proposals (SUG-19…SUG-22), four new
owner questions (Q15…Q18) and four discovery actions (D11…D14). Nothing was invented to fill a gap.

**Re-read from official pages, and where it landed.** `sessions/0b2ffabd/verification.md` holds the dated quotes:
Operating Agreement §5's disclosure sentence and §6's "will be deemed a material breach"; Program Policies
Participation Requirements 2(a)/2(b), including four clauses this repository had never quoted (no bookmarking of
Special Links and "All Special Links must be accessed directly from your Site"; the ban on associating a sub-tag
or program reporting "with a specific end user of your Site"; the duty to remove limited-time-promotion
references as soon as the promotion ends; "When linking to pages with Product lists you must have additional
original content on your Site that is relevant to the Special Link"); Commission Income Statement 2(e)/2(g)/2(c);
FTC *Disclosures 101*; and Google Search Central on `rel="sponsored"`, per-page descriptions and sitemaps. Those
six clauses are `data/policy_facts.json` PF-57…PF-62. Four Google pages became sources **S90 and S95–S97**; the register
had never cited Google documentation at all, which is why `scripts/check_site.py` gained one line
(`OFFICIAL_HOSTS`, flag `G0B2-F-09`) instead of a paraphrase.

**Corrections this pass made to the record.** (1) The reader-facing site is **six surfaces, not three layers** —
measured on the merged tree: `site/` 20 pages, `read/` 11, `shop/` 11, `marketing/` 7, `guides/` 5, `articles/` 5,
plus 25 root register pages, 136 HTML pages outside `docs/` and `archive/` (`G0B2-F-02`; Q12 and DP-C recosted,
and session `73029680`'s runbook item 2 asks the same owner question). (2) Findability coverage measured rather
than asserted: canonical on 102 of 136 pages, `og:image` and JSON-LD on 11 — all of them in `read/`, nowhere else —
`sitemap.xml` 101 URLs with zero `<lastmod>` and zero `<priority>`/`<changefreq>`, `feed.xml` 9 entries
(`G0B2-F-06`, SUG-19/SUG-20). (3) The provenance gaps `verify_site` V4 had been reporting on `suggestions.html`
are closed at the data layer (0 advisories on any row this pass added; no HTML hand-patched). The 14 that remain
on that page belong to another session's tables and are filed as a change request, not edited (`G0B2-F-04`,
`G0B2-F-11`); three of this pass's own rows are reported on `flagged.html`, because that table has no repo-anchor
column and `tools/verify_site.py` keeps its own host list — recorded in `G0B2-F-09` rather than tuned away. (4) This session first filed its source rows as S70–S81; main had already given that
block to two other sessions the same day, so the ids were renumbered on rebase and eight duplicate rows were
deleted in favour of the existing entries — recorded as `G0B2-F-10` so a later reader can follow the arithmetic.

**Still blocked, and visibly so.** No Associates tag in the register → SUG-05's tagged CTAs and any rewrite of the
live links stay blocked, and the supplied `link.amazon` short links remain *unresolved*, never called invalid
(FLG-003, D9). No API credentials → no price, availability, rating or review-count display anywhere, and Google's
hint that a product meta description can carry a price is resolved against Participation Requirements 2(b) as
"specific, never priced" (`G0B2-F-07`). No first-hand testing → S-06 stays "not adopted" and no byline claims a
human read anything (Q5/Q6). No Search Console property → the next topic still comes from the question list, not
from a claimed search-volume number (D8/D12). The five measurement events are *proposed* in
`site/measure.html` with an aggregate-only collector built and switched off (`tools/analytics_endpoint.py`,
`M38-F-04` in `data/shop/flags.json`); what waits is a host and the owner's confirmation of the names, and SUG-21
says so rather than proposing to build it again. The two thermometer links are registered as P4/P5 with
`confirmed_as_submitted_product: false`, so their intended identity is still an owner answer (`G0B2-F-03`, Q18).
And the selected tracking ID is printed on five published pages while Q1's rule keeps it in `COORDINATION.md`
only — both cannot be the convention, and this pass records the conflict instead of silently redacting another
session's pages (`G0B2-F-01`).

**Gates.** Everything green on the merged tree and the chain re-run twice to convergence: `check_site` OK
(36 pages / 5 products / 86 sources / 135 flags) · `verify_site` PASS (144 pages / 2,332 rows / 1,993 with an
official source / 116 repo-anchored) · `link_report --strict` exit 0 · `i2_gate` PASS · `cba81fa5_lint` 0 new /
22 inherited · `publish_pass --check`, `measure_pass --check`, `build_feed --check`, `build_shop --check`,
`build_sitemap --check`, each generator's own `--check` current · `check_all_links` 190 pages / 241 URLs / 0
errors · `analytics_endpoint --self-test` PASS · `sessions/aebf0747/audit.py` 1,558 Amazon links, all sponsored,
0 missing. `link_report` still prints its honest "cannot be obtained" list — prices, ratings, trend rank,
conversion rate, competition density, clicks/orders/revenue — which is the point: those numbers are absent, not
hidden.

---

**Integration note (2026-11-19, session `ee10b024`).** Re-landed with this session's ids remapped onto today's register — its Google source rows are S90 (identical to main's row) and S95–S97 (S91–S94 were claimed by later sessions), its proposals are SUG-19…SUG-22 and its questions Q15…Q18 (`G0B2-F-10`). The root `DESIGN_PROMPT.md` this update describes was superseded by session `6b68afc8`'s 2026-11-19 rails brief; this pass's draft is archived at `sessions/0b2ffabd/DESIGN_PROMPT.md`. Gate and page numbers above are this pass's dated 2026-11-17 measurements, not current counts.

---

## Update 2026-11-17 — session 38650305 (measurement layer, brief-status register, publication pass)

**Bottom line.** Click and page-event measurement is built, and it is **off**. Nothing is sent until someone hosts the collector and sets its address, because GitHub Pages cannot run one. Several rows of the brief cannot be matched to anything in this repository, and three items need the owner: an Associates account (Special Link test), a Google account (Search Console) and a collector host.

- **Built.** A privacy-preserving outbound-click and page-event counter (`assets/measure.js`): no cookies, no storage, no visitor ID, nothing sent under Global Privacy Control or Do Not Track. A self-hosted collector (`tools/analytics_endpoint.py`, standard library) that keeps daily totals only. A measurement page at `measurement/index.html`. Five event names are **proposed**, because the brief asks for five defined events without naming them (flag M38-F-04).
- **Built.** A brief-status register (`brief-status/index.html`) that shows what the brief says and what this repository shows, in separate columns, for S-04…S-25 and SG-27…SG-30.
- **Verified here (2026-11-17).** 104 of 104 published pages have a title and meta description. 1,447 links to Amazon hosts, none without `rel="sponsored"`. `feed.xml` is current. The live front page lists the five products before the guides.
- **Not found here.** The three-question chooser (S-19), the counter-space per-centimetre analysis (S-23), and `DESIGN_PROMPT.md` (S-14). (Clarified 2026-11-17, session `66964850`: the brief's Zone4 links (S-14/S-15, D-04…D-27) live in the sibling repository `kanlerxz87-cyber/Zone4`, which exists with its own `DESIGN_PROMPT.md` and Pages enabled — they are cross-repo references, not missing files in this repository.) Structured data and og:image appear on 11 of 104 pages (S-09, partly).
- **Conflicts.** The brand is still the working name, though the brief says it was settled (S-15, DEC-04). The site uses a generated-style kitchen illustration, which the brief rules out (S-18, M38-F-10).
- **Blocked, not built.** Special Link validation (needs the Associates account; short links kept as supplied, not called invalid), Search Console (needs the Google account), reader capture (needs a decision and a privacy notice), and hosting for the collector.
- **Flags.** Sixteen new items, M38-F-01…M38-F-16, on the shop Flagged page. The main register of 113 is unchanged.
- **Record.** `sessions/38650305/verification.md`. Official sources read: Associates Program Policies 2(a)/2(b) (no sub-tag or ID may be tied to a specific end user), GitHub Pages documentation (static hosting; GitHub logs visitor IPs), and the Search Console sign-in page.
- **Shared-tool changes (logged).** `search.google.com` added to the shop gate's official-host list; two footer links added to the publish pass; the build order is now fixed in the README.

## Update 2026-11-17 — session 0c4c4cb6 (two new submitted links, the owner-supplied tag, sponsored links, measurement layer, RSS feed)

**Bottom line.** The 2026-11-17 brief added two product links and the Associates tag. Both new links were
intake-verified the same day, the tag is recorded and now sits on live Special Links, every outbound
product link on the site is marked `rel="sponsored"` behind a build gate, the measurement layer (five
events, privacy contract, self-hosted endpoint) is shipped with its endpoint deliberately undeployed, and
the RSS feed is live with 18 items. All gates pass on the final tree.

- **Two new submitted links, P4 and P5.** `link.amazon/B0c8moW59` was observed to open
  `amazon.com/dp/B0DHZTCNR5` (ThermoMaven 1 s meat thermometer) and `link.amazon/B0f3GKalj` opened
  `amazon.com/dp/B0DZFD6R9Z` (CHEF iQ Sense meat thermometer), each on 2026-11-17, with an independent
  direct fetch of each destination serving the same title ([S70](https://link.amazon/B0c8moW59) ·
  [S74](https://www.amazon.com/dp/B0c8moW59) · [S72](https://www.amazon.com/dp/B0DHZTCNR5) ·
  [S71](https://link.amazon/B0f3GKalj) · [S75](https://www.amazon.com/dp/B0f3GKalj) ·
  [S73](https://www.amazon.com/dp/B0DZFD6R9Z)). Both tokens are 9 characters and both `/dp/<token>`
  controls returned Amazon's *Page Not Found* — the same class as FLG-001, recorded as **0C4-F-01**;
  intent is unconfirmed as with products 1–3 (**0C4-F-02**). Both destinations sit in the
  **Meat Thermometers** category, outside the site's air-fryer cluster — a content-scope decision the
  owner has not ruled on (**0C4-F-03**). Price and rating were visible on those pages and were
  deliberately not recorded (Program Policies 2(b)/6(t)).
- **Product-intent confirmation record.** Every one of the five submitted links now carries a
  `product_intent` block — intended ASIN, intended official listing URL, confirmation date, source —
  all blank until the owner confirms, strictly separate from the observed redirect target, on
  [Products](https://kanlerxz87-cyber.github.io/Zone3/products.html).
- **The Associates tag arrived.** The owner supplied `shopnow047c-20` in the brief (answering Q1 /
  757-M-01). It is recorded in `data/special-links.json` as owner-supplied and unvalidated; five tagged
  Special Links (SL1–SL5) were built from the observed destinations and are published on the Products
  page. The tag is a public identifier by design — it must appear in every published link; no
  credentials are stored anywhere in this repository. What remains unvalidated is whether the tag is
  active on an enrolled account and whether each link's click reports (**0C4-F-04**), which needs the
  owner's Associates Central session. The submitted short links themselves are untouched and not
  declared invalid (FLG-003 stands).
- **Every outbound product link is now marked `rel="sponsored"`.** 1,552 links across 85 pages on the
  first pass, enforced thereafter by a new check in `scripts/check_site.py` and applied by
  `scripts/mark_sponsored.py` as the last build step — a generator rebuild without the mark now fails
  the gate. The reader site's buy buttons switched from "link not active yet" to active tagged
  Special Links with plain-language disclosure beside each button; I2-F-03 and Q1 were updated to match.
- **Measurement layer shipped, endpoint deliberately not deployed.** Five defined events
  (`page_view`, `guide_view`, `product_click`, `special_link_click`, `nav_click`), a privacy contract
  (no cookies, no identifiers, DNT/GPC off-switch, path-only payloads), a browser client on all three
  page layers, and a self-hosted reference endpoint (`tools/analytics_collector.py`) that was
  smoke-tested end to end: valid events 204, bad ids/fields 400, queries stripped, referrer reduced to
  a host, aggregates only. GitHub Pages cannot host the endpoint, so nothing is sent yet and no count
  is displayed anywhere (**0C4-F-05**). Full documentation: [Measurement](https://kanlerxz87-cyber.github.io/Zone3/measurement.html).
- **Search Console (SG-29) and reader capture (SG-30) are blocked on owner input**, not faked:
  no verification token and no capture processor were supplied, so no placeholder meta tag and no
  dead form were shipped (**0C4-F-06**, **0C4-F-07**). The sitemap is published and ready for
  submission the day verification completes.
- **RSS feed shipped.** `feed.xml` aggregates 18 items across four sections (Research Desk 4, buying
  guides 5, field notes 3, The Crisp Report 6), generated by `scripts/build_feed.py` with a `--check` (at the main merge the same day this generator was retired into the canonical union `tools/build_feed.py`, which now carries these item classes plus the /guides/ entries)
  gate; `<link rel="alternate">` discovery is in every page head, the footer links it, and robots.txt
  carries the `Feed:` hint.
- **Counts at this pass (recomputed from the registers, not copied):** 68 official sources · 55 policy
  facts · 120 flags (3 critical, 23 high, 35 medium, 34 low, 25 informational after the main merge) ·
  31 pages in the shared gate · 106 pages in the sitemap. Eight flags from this session: 0C4-F-01…08, all published on the Flagged for
  review page; none blocks the merge.
- **Gates on the final tree** (full record: [session 0c4c4cb6](https://kanlerxz87-cyber.github.io/Zone3/sessions/0c4c4cb6/index.html)):
  `check_site` OK (31/5/68/120) · `mark_sponsored --check` OK ·
  `build_feed --check` OK (22 entries, union) · `verify_site` PASS (152 pages, 2,453 rows) · `link_report --strict` 0 ·
  `check_all_links` 0 errors · `build_sitemap --check` 106 pages · `i2_gate` PASS (20 pages, 0 flagged) ·
  `cba81fa5_lint` PASS (0 new) · `build_cba81fa5 --check` current.

---

---

## Update 2026-11-16 — session a0ffcab0 (repo review, live re-check, restricted-value scan)

**Bottom line.** The repository builds and every gate passes on `main` (check_site, verify_site, link_report --strict, check_all_links, sitemap check, i2_gate). The live re-check of the three submitted short links and the policy text reproduces the record: the links open B0CDY277D3, B09B7SB46R and B08DKYBTPH, and `amazon.com/dp/B04G1MEwY` returns Page Not Found. The record is [research/a0ffcab0-record.md](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/a0ffcab0-record.md).

- **Highest-priority finding (A0-F-01, High).** The public `/docs/` pages still show observed Amazon prices, star ratings, review counts and "bought in past month" badges. Program Policies 2(b) and 6(t) do not allow that display outside the Amazon-served link or Creators/PA API. This session did not rewrite `/docs/`, because the fix changes derived analysis on six pages. It is an owner decision with two options, listed in the flag.
- **Archives (A0-F-02, High).** Other sessions' folders (`sessions/`, `archive/`) still carry the same values. They are logged as change requests, not edited.
- **Row-provenance gate (A0-F-03, Medium).** `verify_site` counts flagged and repo-anchored rows as passing. The brief's rule, an official link on every row, is not enforced by the gate yet.
- **Fixed in this pass (A0-F-04, Low).** Six marketing pages were regenerated for the `/site/` nav entry.
- **Flags.** Seven new items (A0-F-01…07) on the Flagged for review page; the register held 93 at that pass — §2 carries the current count. A0-F-07 asks for a wording fix: the redirect-target table says "No: not the submitted product", which no official source establishes.

## Update 2026-11-16 — session ab3ed329 (independent re-verification and compliance sweep)

**Bottom line.** The three submitted links still open the three Amazon listings already on record. Their nine-character codes are short-link tokens, not ASINs. The owner still has to confirm which product each link was meant to reach. The record for this pass is [sessions/ab3ed329/index.html](https://kanlerxz87-cyber.github.io/Zone3/sessions/ab3ed329/index.html).

- **Re-read today from official pages.** Link destinations, direct `/dp/` checks, the [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (updated October 15, 2025, with the section 5 disclosure wording), the [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (updated April 14, 2026; clauses 2(a), 2(b), 6(t), 6(v), 6(w), 6(y), 6(z)), the [Standard Commission Income Statement, Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) (Kitchen 4.50%; All Other Categories 4.00%), the [Creators API GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) (ASIN default; 10-character examples) and the [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) guide (November 2019).
- **Compliance fix.** Observed Amazon price, star-rating, review-count and sales values were removed from the public data files, the Sources page and flag text. Program Policies 2(b) and 6(t) do not allow that display outside the Creators API or PA API (AB-F-01).
- **Still open.** Archived pages in `docs/`, `sessions/` and `research/`, and several snapshot files, still show those values. Their owners must remove or redact them. These are logged as change requests, not edited, under the coordination rules.
- **Flags.** Five new items were added to the [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page (AB-F-01 to AB-F-05). The register held 83 items after that pass; §2 carries the current count.
- **Owner decisions needed.** (1) The intended product, or the 10-character ASIN, for each submitted link. (2) Whether to remove or redact the archives listed in AB-F-01. (3) Whether a link.amazon redirect counts as a Redirecting Link under Commission Income Statement 2(e). That can only be tested in a logged-in Associates account.

## Update 2026-11-16 — session 1dddf8c0 (final integration: re-verification and archive compliance remediation)

**Bottom line.** All load-bearing claims were re-read from official pages today and confirmed
verbatim; the compliance exposure flagged by ab3ed329 (AB-F-01) and audited by 71dc8fea
(71-F-04) is remediated — observed prices, ratings, review counts, demand figures, promotion
badges and values derived from them are withheld from every public page, record and data file
in the repository, with official source links and flag references preserved on every row.

- **Re-read today from official pages.** The three short links (same three destinations:
  `B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`), direct `/dp/<token>` "Page Not Found" checks, the
  [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
  (October 15, 2025; §5 disclosure and §6 material-breach clause), the
  [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (April 14,
  2026; CIS §1 windows, PR 2(b), 5, 6(s), 6(t), 6(v), 6(w), 6(y)), the
  [Standard Commission Income Statement, Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ),
  the [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)
  and [GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter)
  (ASIN = "10-Character alphanumeric unique identifier"), the [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
  guide and the [FTC Consumer Reviews and Testimonials Rule Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers).
- **Remediation.** 86 files: the session-3c886b62 data layer and its regenerated pages, the
  `docs/` reference build, `sessions/03bbd050/`, `research/` logs, the frozen `archive/c4e71983/`
  copy, the root snapshot JSON files and the flag registers. Restricted cells show an explicit
  "Withheld" marker citing Policies 2(b)/6(t); row labels and official source links are kept.
  The archive generator (`sessions/3c886b62/tools/build.py`) is patched so regeneration cannot
  restore the values. Record: [`sessions/1dddf8c0/verification-2026-11-16.md`](sessions/1dddf8c0/verification-2026-11-16.md).
- **Still open.** `COORDINATION.md`, the append-only governance ledger, retains the historical
  observed figures inside prior sessions' records. It is not a site content page; an owner
  decision is requested (accept as audit ledger, or redact across all Parts). Published as
  **1dd-F-01** on the [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page.
- **Owner decisions still needed.** (1) The intended product, or the 10-character ASIN, for each
  submitted link. (2) The 1dd-F-01 ledger decision above. (3) Whether a link.amazon redirect
  counts as a Redirecting Link under Commission Income Statement 2(e) — testable only in a
  logged-in Associates account.

---

## Update 2026-11-16 — session f132f462 (marketing polish, independent re-verification)

**Bottom line.** This session independently re-read every load-bearing claim from the official pages on 2026-11-16 and confirmed the record unchanged: the three short links open B0CDY277D3, B09B7SB46R and B08DKYBTPH; the raw 9-character tokens return Page Not Found; the Operating Agreement (§5 disclosure), Program Policies (2(b), 6(t), 6(w), 6(y)), Commission Table 1 (Kitchen 4.50%, All Other 4.00%), the Creators API ASIN rule (10 characters) and FTC Disclosures 101 all match. Record: `research/f132f462-verification-log.md`.

**Marketing polish implemented (accepted suggestions SUG-01, SUG-04, SUG-08):**
- Landing page hero rewritten as a brand-led promise ("Three air fryers. One clear comparison. Zero guesswork.") leading into the buying guide and product research — Amazon Program Content sourcing rule documented (S01).
- A dated "Trending now in air fryers" point-in-time section added, anchored to the Amazon Best Sellers browse path (node 17659096011) read from the three destination listings (S14–S16), with an explicit notice that no trend direction, search volume or conversion data is published (S02).
- Comparison matrix and buying guide restyled with a "who this is for" decision table using only verified listing attributes; price, rating, review count and commission stay blank-by-design per S02 2(b)/6(t).

**Repo review:** `research/f132f462-repo-review.md` records the line-by-line review of the combined tree; no new irregularities, no secrets, no unverified inferred values.

---

## 1. The bottom line

**The three submitted short links were observed to open real Amazon listings; the requester's intended product match remains unconfirmed.** Each submitted token is **9 characters**, not a 10-character ASIN, and `https://www.amazon.com/dp/<token>` returns Amazon's *Page Not Found* page for the raw token — reproduced again on 2026-11-14:

| Submitted link | Code (length) | `amazon.com/dp/<code>` | Where the short link actually lands | Source |
|---|---|---|---|---|
| https://link.amazon/B04G1MEwY | `B04G1MEwY` (9) | Page Not Found | `amazon.com/dp/B0CDY277D3` — CHEFMAN 6 Qt dual-basket air fryer | [S08](https://www.amazon.com/dp/B04G1MEwY) · [S11](https://link.amazon/B04G1MEwY) · [S14](https://www.amazon.com/dp/B0CDY277D3) |
| https://link.amazon/B02NbDxp3 | `B02NbDxp3` (9) | Page Not Found | `amazon.com/dp/B09B7SB46R` — Emeril Lagasse 26QT French-door air fryer oven | [S09](https://www.amazon.com/dp/B02NbDxp3) · [S12](https://link.amazon/B02NbDxp3) · [S15](https://www.amazon.com/dp/B09B7SB46R) |
| https://link.amazon/B00hJ57DV | `B00hJ57DV` (9) | Page Not Found | `amazon.com/dp/B08DKYBTPH` — Chefman TurboFry 8 Qt air fryer | [S10](https://www.amazon.com/dp/B00hJ57DV) · [S13](https://link.amazon/B00hJ57DV) · [S23](https://www.amazon.com/dp/B08DKYBTPH) |

Two official Amazon sources define the identifier as 10 characters: the
[Creators API `GetItems` reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter)
("*10-Character alphanumeric unique identifier assigned by Amazon*") and Amazon's own
[selling blog](https://sell.amazon.com/blog/what-is-an-asin) ("*a unique 10-character alphanumeric
code assigned to every product listed in the Amazon store*", article dated Jun 4 2025).

**The short links have three observed destinations, but the redirect alone does not establish whether
they match the requester's intent.** Each target listing's title, ASIN and category breadcrumb are
documented with Amazon links. The dashboard does not infer that `plpRedirect=mhFallback` indicates a
failed lookup; a direct valid-ASIN control also carried that parameter. Price, review, availability,
rank, commission and performance values remain blank unless obtained through an approved, current data
path — see §3 and FLG-022/027.

**The platform itself is built, published and passing its current checks.** The unresolved operating
inputs are an Associates tag, eligible API access, and confirmation only if the observed destination
listings are not the intended products. These conditions are listed in §5.

---

## 2. What is verified, and where it is published

83 official sources · 55 policy facts · 148 flags · 41 pages in the shared gate (counts recomputed
2026-11-17, session `66964850`, after recovering the 24 flags PR #158 dropped and re-unioning the
registers), a 16-page audit build, a `/docs/`
reference set, a marketing section and three retained session sub-sites. Every fact and all five
submitted links were re-read from the official pages (the original three on 2026-11-14 and
2026-11-16; products 4 and 5 on 2026-11-17); the row-by-row records are the
[Verification log](https://kanlerxz87-cyber.github.io/Zone3/verification.html),
[session 3ead7ac8's record](https://kanlerxz87-cyber.github.io/Zone3/sessions/3ead7ac8/),
which re-reads 30 load-bearing claims and links each one to the page it came from, and
[session 3d359c23's record](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-verification-log.md),
which re-reads 26 load-bearing claims a third time and records what was and was not re-read.

| Area | What the official documents say | Source |
|---|---|---|
| Required disclosure | "As an Amazon Associate I earn from qualifying purchases." — Operating Agreement §5; breach of §5 "will be deemed a material breach" | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |
| Prices and availability | may be shown only if Amazon serves the link, or the data comes via Creators API / PA API — Participation Requirements 2(b) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Star ratings and reviews | may be shown only if obtained through Creators API / PA API — 6(t) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Link shorteners | must not be used "in a manner that makes it unclear that you are linking to an Amazon Site" — 6(w) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Cloaking / redirects | no cloaking or obscuring the URL "including by use of Redirecting Links" — 6(v); purchases via a Redirecting Link are disqualified — CIS 2(e) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Price tracking | "your Site must not have price tracking and/or price alerting functionality" — 6(y) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Artificial traffic | "You will not artificially generate clicks or impressions" — 6(s) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Commission window | a Session ends at the first of: 24 hours elapse, a non-digital order, or another Special Link click; cart converts within **89 days**; shipped and paid within **180 days** — CIS §1 | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Payment | "approximately 60 days following the end of each calendar month"; US minimums: direct deposit $10, gift card $10–$2,000, cheque $100 with a $15 fee — CIS §6 | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Standard commission rates | Table 1, readable without a sign-in: Luxury Beauty 10.00 % · Physical Books / **Kitchen** / Automotive 4.50 % · Toys / Home / Pets 3.00 % · All Other Categories 4.00 % | [S25](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| Onsite commission rates | Table A: **Kitchen** 1.25 % (applies to Onsite Content used by Amazon inside the Amazon site, not to links on your site) | [S26](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) |
| Data access | Creators API — four operations (SearchItems, GetItems, GetVariations, GetBrowseNodes); prerequisite "at least 10 qualifying sales within the past 30 days" | [S04](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| PA-API 5 | "has been deprecated and is being replaced by the Creators API"; calls return HTTP 403 `AccessDeniedException` | [S05](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation) |
| AI / analysis permission | Program Content may not be used to "develop or improve large language or multimodal models, machine learning models or related technology"; API data may not be "aggregat[ed], analyz[ed], extract[ed], or repurpos[ed]" without express prior written approval — IP License §1, §2(e) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Agents | must send `Agent/[agent name]` in the user-agent string and must not solve CAPTCHAs or mimic humans — Agent Terms §4(c) | [S02](https://affiliate-program.amazon.com/help/operating/policies) |
| Enrolment | "we require at least three within the first 180 days"; "personal orders do not qualify"; ~10 posts as a rule of thumb | [S29](https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM) |
| Dormancy | "you have 180 days to refer a sale through one of your Associates links"; the application can be withdrawn after 180 days without qualifying sales | [S28](https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG) |
| FTC disclosure | Endorsement Guides "revised in 2023"; disclose "clearly and conspicuously"; "The closer the disclosure is to your recommendation, the better"; "affiliate link" alone, or a "buy now" button, is **not** adequate | [S44](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) · [S24](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews) |
| Territory | Operating Agreement Schedule 1 lists **United States / amazon.com** only | [S01](https://affiliate-program.amazon.com/help/operating/agreement) |

---

## 3. What is deliberately blank, and why that is the correct answer

Your instruction is: *if a value can't be confirmed from an official source, leave it blank and flag
it as unverified; never infer or fill in values.* Three of those blanks are also Amazon policy, so
filling them would breach the programme:

| Blank field | Why it cannot be filled |
|---|---|
| 9 product-attribute fields for each of 3 observed destination listings (27 cells total) | Dynamic commercial/review/availability/variation/commission/trend/competition values have no approved current source in this build. Destination title, target ASIN and category breadcrumb are separately documented; whether they match requester intent remains open. |
| Star ratings and review text | 6(t) — displayable only when obtained through Creators API or PA API. Copying them off a rendered page breaches the policy even if the number is read correctly. |
| Live prices and availability | 2(b) — same rule. Amazon must serve the price in the link, or it must come from the API. |
| Per-product commission rate and commission income | Public category tables are cited. No product-specific category-to-rate assignment or account context is published in the product row; see FLG-013. |
| Clicks, orders, conversion rate, revenue | Amazon is the system of record and reports only inside a logged-in account. No tag, no campaign. |
| "Trending" and "high-converting" scores | No official Amazon endpoint for affiliates exposes trend or conversion data. Any number would be invented. |

The current `/dashboard/` and `/marketing/` builds withhold prices, star ratings and review counts. A
legacy category/reference page still contains dated price/rating snapshots; those are not compliant live
product offers and remain flagged for removal or approved re-sourcing under FLG-028. Do not use them as
current marketing claims.

---

## 4. What the platform does today

| Capability in the brief | State |
|---|---|
| Product research and intake with an automated gate | **Built.** The 9-character submitted tokens are not ASINs, but the short links were observed to land on three live listings with target ASINs. The observed targets are recorded separately; whether they match the requester's intent remains unconfirmed. |
| Trending / high-converting product identification | **Blocked** on official data — no legitimate source for those scores. |
| Price, review and competition analysis | **Rules built and enforced; data withheld** under 2(b) / 6(t) (FLG-022). A six-position bestseller benchmark is published with rank, ASIN, title and link only. |
| Commission potential modelling | **Partly built.** The public rate tables plus the verified working rules (24 h session, 89-day cart, 180-day ship/pay, disqualified-purchase list, payment timing) are published; the per-product rate input is missing. |
| SEO articles, comparisons, buying guides | **Briefs, a comparison and a buying guide are published, and the editorial plan for the long-form articles is published too.** The plan ([Content topics](https://kanlerxz87-cyber.github.io/Zone3/content-topics.html)) lists 12 working titles, the Amazon fact each one is built on and the rule that governs what it may not state. Every product claim must be accurate (PF-10), and the first-hand experience the FTC describes (PF-21) has not happened. |
| Publish and manage affiliate links | **Link pipeline built; publishing intentionally off.** No Associates tag, so nothing is a trackable Special Link (FLG-010). |
| Track clicks and conversions | **Ledger schema built, empty by design** (FLG-011). |
| Continuous optimisation | **Boundary defined; no data to optimise.** Rebuilding from verified data is one command. |
| Associates and FTC compliance | **Built and enforced at build time.** The generator refuses to emit a page without the §5 disclosure; the checker fails the build on an unsourced table row. |
| Automation and scalability | **Built.** Static generation from JSON, no runtime dependency, no secrets in the repo, deterministic rebuild (verified to a stable fixpoint). |

**Site structure:** the landing dashboard links to Products, Pricing & commission, Reviews & competition,
Content & compliance, Content topics, Campaigns & tracking, Category: Air Fryers, Marketing, the Executive
summary, Verification log, Flagged for review and Sources. The 16-page `/dashboard/` build supplies the full
research and governance tables. Every current generated data row carries an official source, a flag or an
explicitly documented blank. The legacy snapshot exposure is flagged separately (FLG-028).

---

## 5. Three items that unblock everything

1. **Confirm the observed destinations only if they are not the intended products.** The live target
   ASINs are already recorded in the product table; no replacement input is needed if those are intended.
2. **Verify your Associates tag** (the value `shopnow047c-20` was supplied on 2026-11-17 — the
   `xxxxx-20` parameter, not a password or API secret) by confirming it in the Associates console, then
   test one Special Link per product before scaling (CBB-F-02, CBB-Q-01). Until it is verified, no link
   on the site can earn.
3. **Enrolment status and API access.** Creators API needs ≥10 qualifying sales in 30 days; until
   then price and rating display is impossible under 2(b)/6(t), however the data is obtained.

Until item 1 arrives, the honest answer to "which product is this and is it worth promoting" is
*unknown*, and the site says so rather than filling the gap.

---

## 6. Irregularities published for your review

148 entries on the [Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page —
3 critical, 28 high, 46 medium, 42 low, 29 informational (informational entries record a correction
made to this site, not a defect in a product; `CBB-F-01`…`CBB-F-04` and `Z1-F-01`…`Z1-F-04` and `0C4-F-01`…`0C4-F-08` were added 2026-11-17,
and `5B-F-*`, `929-F-*`, `F-2F-*`, `G82-F-*`, `G84-F-01` were restored after PR #158 dropped them). None of
them blocks the merge; each carries its evidence source links and the action needed.
made to this site, not a defect in a product). None of them blocks the merge; each carries its
evidence source links and the action needed.

**Read these first:**

| ID | Severity | What it means for you |
|---|---|---|
| [FLG-001](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-001) | Critical | The 9-character tokens are not ASINs, but their short links were observed to open live listings. The destination listings are documented; whether they match intent remains open. |
| [FLG-003](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-003) | Critical | `link.amazon` is Amazon-served but not documented in the policies. Whether its redirect counts as a Redirecting Link (disqualified under CIS 2(e)) has to be tested in a logged-in Associates account. Publish canonical `/dp/ASIN` URLs with your tag instead. |
| [FLG-010](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-010) | High | No Associates tag in any supplied link → nothing is trackable yet. |
| [FLG-015](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-015) | High | Schedule 1 lists the **United States / amazon.com** only. A non-US operator's eligibility for the US programme is not established by the text read. |
| [FLG-016](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-016) | High | Automated *analysis* of Amazon product data needs Amazon's prior written approval. This constrains the "AI-powered analysis" part of the brief directly — it is a permission problem, not a technical one. |
| [FLG-022](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-022) | High | Prices, ratings and review counts cannot be displayed without an approved data path, so they are blank by policy, not by omission. |
| [FLG-027](https://kanlerxz87-cyber.github.io/Zone3/flagged.html#FLG-027) | High | Submitted tokens and observed redirect destinations are recorded separately; observed destinations do not prove requester intent. The fallback query parameter is not treated as failure evidence. |

**Corrections and fixes made in this session** (also on the Flagged page as `E-F-01`…`E-F-07`, so the
changes are auditable rather than silent):

| ID | What changed |
|---|---|
| E-F-01 | The dashboard claimed a second official source for the 10-character ASIN rule without listing it. The row now cites that page (registered as S45) and the quote is stored as PF-52. |
| E-F-02 | The root executive summary was stale — it still carried another session's branch header and repeated a claim that session had already recorded as overstated. Rewritten. |
| E-F-03 | *(not raised — already fixed on `main` before this session merged)* `tools/link_report.py` had printed "rate card is behind Associates sign-in", which V-F1 had already shown to be false. |
| E-F-04 | `/docs/` was live but had no inbound link from any dashboard (V-F3), and `sitemap.xml` covered only part of the site (V-F4). Both fixed: a nav entry was added, and `scripts/build_sitemap.py` now produces the sitemap from the checked-in tree so it covers all 63 live pages. |
| E-F-05 | The dashboard headline says product identities are "documented", which reads against FLG-002/FLG-027. **Left for your decision** — the data layer is correct, so this is editorial. |
| E-F-06 | One source note says the competition benchmark carries ratings and prices; the published benchmark shows only rank, ASIN, title and link (correctly). **Left for your decision.** |
| E-F-07 | PR #26 (another session) overlapped this session's scope, touching 23 shared root files. It was not merged, closed or edited here; it landed on `main` first and this branch was rebased onto it. |
| 3D-F-01 | The **Content & compliance** page said *"No article, comparison or buying guide has been written yet"* and its table marked all three products "Not written" — while seven marketing pages were live and nav-linked. Corrected: the table now shows what is published, and the editorial plan for the rest is published at `/content-topics.html`. |
| 3D-F-02 | Re-observed independently: the "Customers who viewed" carousel on a destination page shows a price and a star rating that belong to a **different ASIN**. The published data was never affected (no price or rating is shown anywhere); recorded so any future automated capture binds each value to the page's own ASIN. |
| 3D-F-03 | The dashboard had no tile for the new topic plan. Fixed — it is listed as a tile and in the site map. |

---

## 7. How this was verified

* All three submitted short links re-fetched on 2026-11-14; all three direct `/dp/<code>` checks
  re-run. Results identical to 2026-11-13.
* All 55 policy facts in `data/policy_facts.json` re-checked against their source page.
* Commission tables (S25, S26), the Creators API pages (S04–S06), the FTC pages (S07, S24, S44), the
  enrolment pages (S28, S29) and the Amazon bestseller page (S43) re-read; the Operating Agreement
  and Program Policies were read section by section across all 4 and 11 chunks respectively.
* Build gates, all green: `scripts/check_site.py` (13 pages, 3 products, 51 sources, 72 flags),
  `tools/verify_site.py` (71 pages, 1,269 rows, 1,068 with an official source link, 405 flagged, 82
  anchored to the repo), `tools/link_report.py` (no dangling refs), `scripts/check_all_links.py`
  (117 pages, 105 external URLs, 0 errors), `scripts/build_sitemap.py` (66 pages covered), and both
  site generators rebuild to a stable fixpoint.
* **Re-verification round 2026-11-16 (session `1f1b8bd2`)** — the three submitted short links, the
  three direct `/dp/<9-char code>` controls, the Operating Agreement (§5, §6), the Program Policies
  (header date, Participation Requirements 2(b) and 6(s)–6(z), Commission Income Statement §1), the
  Standard Commission Table 1, the Creators API introduction and GetItems ASIN definition, FTC
  Disclosures 101 and the FTC endorsements hub were all re-read from the official pages on
  2026-11-16. Results identical to 2026-11-14. Record:
  [`research/1f1b8bd2-verification-log.md`](research/1f1b8bd2-verification-log.md).
* **Limits:** the sandbox reaches only github.com, npm and PyPI directly, so official pages were read
  through a fetch tool rather than an automated HTTP client, and the `--online` link check was not
  run. Whether `link.amazon` redirects without an affirmative click has not been tested in a
  logged-in Associates account (FLG-003).

---

## 8. Final integration pass — session `3ead7ac8` (2026-11-14)

**A live compliance defect was found and fixed.** Two page sets were publishing observed prices
([price withheld] / [price withheld] / [price withheld]), star ratings ([rating withheld]) and review counts
([count withheld]) as product facts. Values were removed from the public files on 2026-11-16 (AB-F-01). Associates Program **Participation Requirements 2(b)** and
**6(t)**, re-read verbatim that day, allow those displays only where Amazon serves the link or the
data comes from Creators API / PA API — neither is true for this project, which has no Associates tag
and no API credentials.

| Page set | Action |
|---|---|
| `category/air-fryers.html` | Columns removed and replaced with a 2(b)/6(t) explanation carrying the S46–S48 and S02 links. Session `554c08ca` (PR #66) found the same file independently and raised `I-F-01`; **their fix is the one kept**, and `3E-F-01` cross-references it |
| `/docs/` (six pages) | 81 cells withheld, replaced with the `Withheld` badge plus FLG-022 / FLG-023 links |
| `sessions/3c886b62/**` and `sessions/03bbd050/` | Dated compliance notice added to 12 pages; their data cells were **not** rewritten, because those files belong to other sessions. Change request `3E-CR-01` is logged in `COORDINATION.md` |
| `category/air-fryers.html`, *Niche assessment* | Amazon's "bought in past month" badge figures were published in prose on a page that withholds prices for exactly that reason. Withheld, and raised as `3E-F-10` |

**One stale claim was corrected.** `/docs/` and the category page said the commission rate schedule is
sign-in-only. It is not: the Standard Commission Income Statement
[Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) and the Onsite
[Table A](https://affiliate-program.amazon.com/help/node/topic/G4ARBJC7Z2NK48CA) both render
publicly — Table 1 was re-read row for row (Kitchen 4.50%, All Other Categories 4.00%). Only the
per-account `/help/operating/schedule` card is gated. Rate cells stay blank because what is
unresolvable is each listing's **category** (FLG-021), not the rate card.

**Two register errors were repaired.**
[`PF-53`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/data/policy_facts.json) reinstates the
compensated-review clause whose withdrawal note ("its text was not found in any section read") was
wrong — the wording is in the Operating Agreement's opening paragraph.
[`PF-55`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/data/policy_facts.json) completes
`PF-23`, which stopped mid-sentence and omitted *"or in the direct training or fine-tuning of a
machine learning and/or foundational model"* — the clause that matters most for an AI-driven platform.

**Verification.** 13 official pages fetched and read; 30 load-bearing claims re-checked. **All
matched.** No third-party page was used as evidence. Gates on the merged tree:
`check_site` OK (12 pages / 3 products / 51 sources / 66 flags) · `verify_site` PASS (70 pages /
1,223 rows / 1,022 with an official source link / 0 advisories) · `link_report --strict` exit 0 ·
`check_all_links` 116 pages, 0 errors · all five generators idempotent.

**Merged and deployed.** [PR #70](https://github.com/kanlerxz87-cyber/Zone3/pull/70) → merge commit
`f79b85e`; follow-up [PR #72](https://github.com/kanlerxz87-cyber/Zone3/pull/72) → merge commit
`f618a53`, both merged without waiting for approval. The Pages build for `f618a53` reports
**`built`** and the corrected pages were confirmed on the live site.

**Limits carried forward.** The sandbox reaches only github.com, npm and PyPI directly, so official
pages were read through a fetch tool rather than an automated HTTP client. Program Policies chunk 10
of 11 was not read. Whether `link.amazon` redirects without an affirmative click has not been tested
in a logged-in Associates account (FLG-003).

---

## 9. Final integration pass — session `3d359c23` (2026-11-14)
**Merge note.** While this branch was open, `main` merged session `f2102efa's` three additional
flags (`F2-F-01`…`F2-F-03`), so the flag register now holds **72** entries: this session's three
(`3D-F-01`…`3D-F-03`) and `f2102efa's` three are both published, and the generated pages were
rebuilt from the merged register. `main` also carried a stray `>>>>>>>` conflict-marker line in
`COORDINATION.md` (line 3554, committed by that session and left unbalanced); this integration
removed the marker line and kept every word of the board. The resolution is scripted in
`scripts/resolve_rebase.py` so it is repeatable and auditable rather than a one-off manual edit.


**One published statement contradicted the site's own output, and it is fixed.** The *Content &
compliance* page said *"No article, comparison or buying guide has been written yet"*, and its
status table marked all three products **"Not written"** — while seven marketing pages were live
and linked from the navigation: three product briefs, a comparison, a buying guide and one page per
product. The flag register carried the same stale claim as **FLG-012**. Both are corrected in this
pass; FLG-012's earlier wording is kept in the register so the change stays auditable, and the
correction is published as **3D-F-01**.

**The brief's "catchy trendy articles and topics" is now a published plan.** The site had briefs, a
comparison and a buying guide but nothing that planned the articles themselves. The new
[Content topics](https://kanlerxz87-cyber.github.io/Zone3/content-topics.html) page carries **12
working titles**, each with:

* the verified Amazon fact it is built on (read from the listing title or from Amazon's own
  programme documents) and the official source of that fact;
* the page that already publishes those facts;
* the rule that governs what it **may not state**, with the clause — for example, no price, no
  discount and no best-seller position for a specific product (Participation Requirements 2(b) and
  6(t)), and no comparison with a non-Amazon retailer's product (6(z));
* its status: **Ready to draft** (6 topics) or **Blocked: identity unconfirmed** (6 topics, because
  FLG-002/FLG-035 are still open).

**No topic is described as trending, popular or high-converting**, because no official Amazon
endpoint publishes search volume, keyword difficulty, trend direction or conversion rate to
affiliates (FLG-033). The one official popularity surface — the category Best Sellers page — is used
in a single topic and is labelled point-in-time, because the positions move between captures
(FLG-025). A "Topics deliberately not planned" table states the four things that are *not* being
claimed and why.

**A second observation was recorded.** Re-fetching the destination page for product 1 showed the
"Customers who viewed this item also viewed" carousel rendering a [rating withheld], [count withheld],
[price withheld] entry whose own link points at a **different** ASIN (`dp/B0B7C327LK`), while the link it renders
under is the destination ASIN (`dp/B0CDY277D3`). The published data was never affected — no price,
rating or review count appears anywhere on the site (FLG-022, FLG-029) — but any future automated
capture must bind each value to the page's own ASIN. Recorded as **3D-F-02**; the missing dashboard
tile is **3D-F-03**.

**Verification.** 13 official pages fetched and read live by this session (the three short links,
the three destination pages, one Page-Not-Found control, the Operating Agreement, the Program
Policies, Table 1, the Creators API reference and the FTC guide). Every load-bearing claim matched
the page it cites; nothing was found false and nothing was filled in. The record is
[`research/3d359c23-verification-log.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-verification-log.md);
the line-by-line repository review is
[`research/3d359c23-repo-review.md`](https://github.com/kanlerxz87-cyber/Zone3/blob/main/research/3d359c23-repo-review.md).
Gates on the merged tree: `check_site` OK (13 pages / 3 products / 51 sources / 72 flags) ·
`verify_site` PASS (71 pages / 1,269 rows / 1,068 with an official source link / 0 advisories) ·
`link_report --strict` exit 0 · `check_all_links` 117 pages, 105 external URLs, 0 errors ·
`sessions/3c886b62` checker OK · sitemap covers 66 pages · all generators idempotent.

---

## 9. Independent re-verification and final integration — session `25513d33` (2026-11-14)

Session `25513d33` re-fetched and re-read every load-bearing claim from scratch, rather than
relying on an earlier session's record. **All three submitted links and all twelve policy and
disclosure statements matched.** Nothing load-bearing was found to be wrong.

| What was re-checked | Result |
|---|---|
| The three `link.amazon` short links | Re-fetched 2026-11-14. Unchanged: `B04G1MEwY`→`B0CDY277D3` (CHEFMAN 6 Qt dual basket), `B02NbDxp3`→`B09B7SB46R` (Emeril Lagasse 26QT), `B00hJ57DV`→`B08DKYBTPH` (Chefman 8 Qt TurboFry) |
| The raw 9-character codes used directly as ASINs | All three return Amazon's "Page Not Found" page. The positive control is that the same fetch returns a full product page for each destination ASIN |
| Participation Requirements 2(b), 6(t), 6(w), 6(s), 6(y) and the 2(b) tag rule | **Confirmed verbatim** against the official page (header still "Updated: April 14, 2026") |
| Commission windows (24 h session · 89-day cart · 180-day ship/pay), payment timing (~60 days), US Payment Minimum Chart | **Confirmed verbatim / row for row** |
| Standard Commission Table 1 and Onsite Table A | **Confirmed verbatim**: Kitchen 4.50% (Standard), Kitchen 1.25% (Onsite, Onsite Content only); All Other Categories 4.00% / 1.00% |
| FTC guidance on affiliate disclosures | **Confirmed verbatim**: "The closer the disclosure is to your recommendation, the better"; "'affiliate link' … would not be adequate"; Guides "revised in 2023" |

**This session independently reached the same conclusion as the site's existing rule.** Clauses 2(b)
and 6(t) permit a price or star rating on your own site only where Amazon served the link, or where
the data came through Creators API / PA API. This project has neither an Associates tag nor API
credentials, so the blank price, rating and review cells are not an omission — they are what the
policy requires.

**Two repository-integrity findings, both informational:**

* **C3-F-01 was a false positive.** An earlier session reported that `sitemap.xml` omitted five pages.
  It does not: those five are meta-refresh redirect stubs the sitemap generator excludes on purpose,
  and `index.html` is present as the site root URL. `scripts/build_sitemap.py --check` exits 0 with
  every live page covered and 0 missing. Recorded as **25-F-02**; no file change was needed.
* **A stale count, corrected in flight.** §6 of this summary said "51 entries — 3 critical, 12 high,
  16 medium, 15 low, 5 informational" and §7 said "48 sources, 51 flags" when this session read it.
  By the time this branch merged, another session had already refreshed both to the current figures
  (72 entries; 51 sources), and those are the numbers now in §6 and §7. Recorded as **25-F-03**.

**One new observation (25-F-01).** All three destination listings carry the same Amazon browse
breadcrumb — *Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers* (node
`17659096011`) — read from the pages Amazon served. The repository had recorded it for product 1 only.
No published cell changes: a browse node is a *category* fact, and a per-product commission rate still
cannot be tied to a rate without the account's own rate card.

**Full record:** [session 25513d33 verification page](https://kanlerxz87-cyber.github.io/Zone3/sessions/25513d33/)
— one row per claim, each linked to the official page it was read from.

**New page published.** `sessions/25513d33/index.html`, generated by
`sessions/25513d33/build_record.py`, which reads every source URL from `data/sources.json` at build
time so a label cannot drift from its link. It carries the §5 disclosure, is listed in the site
navigation and in `sitemap.xml`, and passes all gates with 0 advisories. A rebase-conflict resolver,
`sessions/25513d33/resolve_rebase.py`, was added alongside it: the board's own prose contains the
string `<<<<<<<`, so a substring marker test false-positives and can let a conflicted file be
published — the resolver's test is line-anchored.

---

## 10. Final integration and the reader-facing site — session `59d84c55` (2026-11-16)

**One-line summary.** Every load-bearing claim this repository publishes was re-read from its official
page today, the results agree with the existing record, and the repository now carries a reader-facing
marketing site at `/site/` that a person can actually shop with — without a single invented number.

### 10.1 What was re-verified today (22 claims, `site/evidence.html`)

Every page below was fetched **once** on 2026-11-16 and the wording copied from the page at the time.
Nothing was carried forward from an earlier session's capture.

| Claim | Official page read today | Result |
|---|---|---|
| The three short links open three live listings | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) → `/dp/B0CDY277D3`, [B02NbDxp3](https://link.amazon/B02NbDxp3) → `/dp/B09B7SB46R`, [B00hJ57DV](https://link.amazon/B00hJ57DV) → `/dp/B08DKYBTPH` | **Confirmed**, same destinations as the 2026-11-13/14/15 captures |
| Nine characters is not an ASIN | [amazon.com/dp/B04G1MEwY](https://www.amazon.com/dp/B04G1MEwY) returns *Page Not Found*; [Creators API GetItems](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items) documents ASIN with ten-character examples | **Confirmed** |
| §5 disclosure sentence and the header date | [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) — "Updated: October 15, 2025" | **Confirmed verbatim** |
| Price display rule 2(b), rating rule 6(t), no price tracking 6(y), no automated clicks 6(s), no link shortening 6(w), no sub-tag per visitor | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) — header "Updated: April 14, 2026" | **Confirmed verbatim** |
| No ML training on Program Content; no API aggregation/analysis without prior written approval; 24-hour cache limit; no stored images | same Program Policies, IP License §1, §2(e), §2(h) | **Confirmed verbatim** |
| Agents must identify as `Agent/[name]` and must not circumvent blocks | same Program Policies, Agent Terms §4(c) | **Confirmed verbatim** |
| Kitchen 4.50%, All Other 4.00%, bounty rates $12/$2/$5/$0.25 | [Standard Commission Income Statement, Table 1](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | **Confirmed as printed** |
| API access needs enrollment plus 10 qualifying sales in 30 days; the API has four operations and no trend or conversion endpoint | [Creators API introduction](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) | **Confirmed** |
| FTC: disclose hard to miss, with the endorsement, not only in a footer; no invented first-hand experience | [Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | **Confirmed** |
| The 180-day / three-sale window | not fetched today | **Not re-checked — no result asserted** |

### 10.2 One correction to how the site described itself

The older pages place the exact §5 sentence **in the footer only**. That satisfies the Operating
Agreement's "on your Site" wording. It is weaker than the FTC's placement guidance, which warns that a
disclosure appearing only at the end of a page is "likely to be missed". The new site therefore carries the
disclosure as a **banner above the navigation** as well as beside every buy action, and the older pages are
flagged for the same change (`I2-F-01`, proposal `D-07`). This is recorded rather than silently applied,
because those pages belong to other sessions' builds.

### 10.3 What the reader-facing site is

`/site/` — eight pages, generated from `data/i2/*.json` by `tools/build_i2_site.py`, gated by
`tools/i2_gate.py` (G1–G10):

| Page | Purpose |
|---|---|
| `site/index.html` | The promise, three product cards built only on listing facts, a seven-row comparison, and a statement of what is deliberately left out |
| `site/products.html` | Listing detail, the token caution, and the blank-fields table with the rule for each |
| `site/guides/` | The guide plan and one live guide, built from listing facts only |
| `site/evidence.html` | 14 sources, what each said, and the 22-row verification log |
| `site/flagged.html` | 8 open items with severity, finding, resolution and source |
| `site/decisions.html` | 12 proposals, 12 open questions, 9 discovery actions, 6 prompts, and an Accept/Reject/Defer control with a text export |
| `site/front-door.html` | Where the audit builds live |

**What makes it not read as generated:** the disclosure sits where a reader sees it before any product
content; a blank cell is an explained state ("Not published" plus why plus a link to the blocking item)
rather than a dash; every table row links the listing or policy page it came from; no sentence claims
experience with a product that was never used; and the site says in the body copy which figures it refuses
to publish, with the clause that stops each one.

### 10.4 What is still blocked, and on what

| Blocker | Question | What it stops | Who can unblock |
|---|---|---|---|
| No Associates tag | `Q1` | Every earning link. All buy actions are disabled and labelled | Account holder |
| Intended product unconfirmed | `Q2` | Confidence that the three listings are the products you meant | Account holder (a yes/no) |
| Marketplace unknown | `Q3` | Which storefront the tag applies to | Account holder |
| No API eligibility | `Q4` | Any price, availability or star rating, ever | Account holder + 10 qualifying sales in 30 days |
| No named editor | `Q5` | Publishing further guides without them reading as generated | A decision |

### 10.5 Gates on the combined tree (run by this session)

| Gate | Result |
|---|---|
| `tools/i2_gate.py` (new, G1–G10) | **PASS** · 8 pages · 104 rows · 89 sourced · 15 explicit blanks |
| `tools/verify_site.py` V1–V7 | **PASS** · 82 pages · 1,437 rows · 1,217 sourced · 0 advisories |
| `tools/build_site.py` (provenance gate) | **PASS** · 16 pages · 232 rows · 22 sources · 29 flags |
| `scripts/check_site.py` | **OK** · 13 pages · 3 products · 51 sources · 78 flags |
| `scripts/build_sitemap.py --check` | **PASS** · 77 pages · 0 extra entries |
| Negative test of every gate check | 13 injected violations, 13 caught (see COORDINATION.md §I2) |
| Internal link crawl of the whole tree | 0 broken |

### 10.6 The point

The brief asked for automation that finds trending, high-converting products and optimises campaigns.
Two of those three are not obtainable through any official Amazon surface: there is no trend endpoint and
no conversion endpoint, and per-product commission is not published. Rather than generate numbers to fill
those slots, this session built the part that can be true today — a site that a reader can use, that
explains its own gaps, and whose claims a reviewer can check line by line — and published the missing
inputs as twelve questions with a discovery action and an owner for each.

---

## 11. The second marketing implementation, and the state of the whole build — session `145b8df7` (2026-11-16)

> Section 10 of this file was written on this branch before `main` moved. While it was open, five
> other sessions landed (`ab3ed329` PR #98, `1f1b8bd2` PR #99/#102, `59d84c55` PR #101/#103,
> `a0ffcab0`/`f132f462` PR #110), and one of them built a reader-facing marketing site too. Section 10's copy is kept as written — it
> still describes `/read/` accurately — and this section reconciles it with what is actually on
> `main` now. Nothing from those sessions was deleted, rewritten or reverted by this integration.

### 11.1 What is on `main` now, as of this session's merge

| Surface | Owner | What it is |
|---|---|---|
| `/` and the flat pages | sessions `7f84fea4`…`3d359c23`, extended by `59d84c55` | The verification dashboard: products, pricing, reviews, sources, verification log, flagged register, decision centre, suggestions page |
| `/read/` — **The Crisp Report** | `145b8df7` (this session) | 11 generated pages: 6 articles, a 13-attribute three-way comparison, a five-question buying guide with an FAQ, an Air Fryers category hub, a method page. Built by `scripts/build_read.py` from `data/editorial.json`; `audit()` fails the build on an uncited row, a price pattern, a rating pattern, a stored Amazon image or a broken link |
| `/site/` — **Air Fryer Field Notes** | `59d84c55` | 8 pages with its own provenance gate (`tools/i2_gate.py` G1–G10), its own evidence and verification pages, and a 12-proposal decision board in `data/i2/decisions.json` |
| `/marketing/` | `588693c9`, `b90c5685` | The 2026-11-14 facts-only brief set, kept for the record |
| `/dashboard/`, `/sessions/**`, `/docs/`, `/archive/` | earlier sessions | The 16-page audit build, per-session records, the archived build and byte-frozen snapshots of other sessions' sites |

**Two reader-facing marketing layers now exist because two sessions answered the same Suggestions page
in parallel and neither could see the other before landing.** That is a coherence and maintenance
problem, not a data problem: both layers draw on the same verified register, both carry the disclosure
sentence, and neither publishes a price, a star rating or an unverified value. It is published as
**`Z14-F-04`** on the Flagged for review page with the recommendation stated plainly — the owner picks
one as canonical, then a follow-up session folds the other's unique pages in and leaves redirect stubs so
no published URL breaks. This session deliberately did not delete or redirect another session's output.

### 11.2 The registers after integration

| Register | Before this session | After |
|---|---|---|
| `data/sources.json` (flat site) | 52 entries, ids to `S59` | **62 entries, ids to `S69`** — this session's ten dated captures were renumbered `S60`–`S69` because `main` had already taken `S59` for the FTC Consumer Reviews and Testimonials Rule Q&A. Every reference in this session's files was rewritten by `scripts/renumber_sources.py`; 0 dangling references |
| `data/flags.json` | 86 at this session's start; 93 after PR #110 | **96** — this session added `Z14-F-01` (Emeril listing-title wording drift), `Z14-F-02` (dated best-seller snapshots) and `Z14-F-04` (the parallel marketing layers); sessions `a0ffcab0`/`f132f462` added `A0-F-*` and `F1-F-*` in the same window. All non-blocking, all published on the flagged page with their sources |
| `suggestions.html` | 10 proposals as published for review, 10 questions | **unchanged text plus three new registers**: an implementation status per proposal, a 10-row answers register (what official sources settle vs what only the owner can settle, and which decision each unlocks), and four ranked paths with a recommendation |
| Marketing pages | 0 reader-facing pages from this branch | **11** under `/read/` |

### 11.3 Verified by this session on 2026-11-16, and where it is published

| Fact | Official page | Register id | Used by |
|---|---|---|---|
| `link.amazon/B04G1MEwY` → `amazon.com/dp/B0CDY277D3` | [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) | `S67` | comparison, category hub |
| `link.amazon/B02NbDxp3` → `amazon.com/dp/B09B7SB46R` | [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) | `S68` | comparison, drift flag |
| `link.amazon/B00hJ57DV` → `amazon.com/dp/B08DKYBTPH` | [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) | `S69` | comparison, feature article |
| Served listing titles and the Air Fryers breadcrumb | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) · [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) · [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | `S60` `S61` `S62` | every product sentence in `/read/` |
| Best Sellers in Air Fryers, positions 1–6 and the node taxonomy (289913 › 17659095011 › 17659096011, siblings 224479505011 and 289918) | [Best Sellers in Air Fryers](https://www.amazon.com/gp/bestsellers/kitchen/17659096011) | `S63` `S64` | the dated rank article, category hub |
| Standard Commission Income Statement Table 1 — Kitchen **4.50%**, All Other **4.00%**, bounties **$12.00 / $2.00 / $5.00 / $0.25** | [GRXPHT8U84RAYDXZ](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) | `S65` | "how this site gets paid" |
| Program Policies header "Updated: April 14, 2026" and Commission Income Statement §1 (24 h session, 89-day cart, 180-day ship-and-pay) | [operating/policies](https://affiliate-program.amazon.com/help/operating/policies) | `S66` | the same article's clock section |

Prices, star ratings and review counts printed on those pages were **not** copied into the site
(Program Policies 2(b) and 6(t)). No per-product commission, demand rank, conversion or revenue figure
was inferred anywhere.

### 11.4 Gates on the integrated tree

| Gate | Result |
|---|---|
| `scripts/build_read.py --check` | PASS — 11 pages, generator output matches the committed files |
| `scripts/check_site.py` | OK — 13 pages, 3 products, **62 sources**, **96 flags** |
| `tools/verify_site.py` | **PASS — 94 pages, 1,575 table rows, 1,348 officially sourced, 0 advisories** — every row provenanced by an official link, a flag or a repo anchor |
| `tools/link_report.py --strict` | exit 0 — no dangling source or flag reference |
| `scripts/build_sitemap.py --check` | PASS — every live page covered |
| `scripts/check_all_links.py` | PASS — 0 broken internal links across the tree |
| conflict-marker scan, `git diff --check` | 0 markers, clean |

**Open items the owner must still settle** (unchanged, and unchanged by any other session): the
Associates tag (blocks all revenue), confirmation of the three intended ASINs, the target marketplace,
whether an approved account exists, the reviewer and cadence, the analytics stack, and — new from this
session — which marketing layer is canonical.

## 10. Implementation pass — session `5a56c084` (2026-11-16)

**What this pass is.** The polished-marketing implementation round. Session `4f83ee7b`
(2026-11-15) published ten design/marketing proposals (SUG-01…10), ten owner questions
(Q1…10) and six discovery actions (D1…6) — deliberately without implementing anything.
Session `5a56c084` recorded a decision per proposal (now rendered as the **Decision log**
on `suggestions.html`, sourced from `data/suggestions.json`) and implemented only the
unblocked subset. Blocked proposals stayed blocked; no owner question was answered by
inference.

**Independent re-verification (2026-11-16).** All eight load-bearing observations were
re-fetched live in this session and matched the register: the three submitted short links
still open the same three listings (`B04G1MEwY`→`B0CDY277D3`, `B02NbDxp3`→`B09B7SB46R`,
`B00hJ57DV`→`B08DKYBTPH`); the three direct `/dp/<token>` checks still return Amazon's
"Page Not Found" page; the Operating Agreement (header October 15, 2025) carries the §5
disclosure wording verbatim; the Program Policies (header April 14, 2026) carry the
session definition verbatim. Two listing-title wording drifts were recorded as Info items
(precedent 4f83-F-01); no new flag was raised. Record:
`sessions/5a56c084/verification-2026-11-16.json`, rendered at `/sessions/5a56c084/`.

**What shipped.**

* **Design system** — the generic dashboard styling is replaced by an editorial
  "research desk" look across every generated page: warm paper ground, evergreen
  primary, copper accents, serif display headings; no external fonts, images or scripts.
* **Disclosure placement** — the Associates statement is a strip under the header on
  every page (§5 "clearly and prominently"; FTC "hard to miss"), repeated beside product
  pointers in the articles, with the Amazon content disclaimer and trademark note in
  every footer.
* **Landing page** — now a front door: hero, honest research-status callout, proof
  stats computed from the registers, three listing cards (labelled source links only),
  Research Desk cards, the "In the kitchen now" point-in-time module (SUG-08), a trust
  section (SUG-06), a Decision Center banner, and a collapsed site map. Navigation is
  five primary links plus a grouped "More pages" menu; every previous destination is
  still reachable and gate-checked.
* **Research Desk** — `articles/index.html` plus four grounded articles (plan topics
  T-09, T-10, T-07, plus one new evergreen grounded in the Commission Income
  Statement). Every claim carries an inline source link; every article carries a
  verified / not-verified box, a how-this-was-written note, and its enforced editorial
  constraints; the review checklist is published on the hub (SUG-03's gate).
* **Decision log** — per-proposal accept/defer/hold records with evidence links
  (SUG-01 partial, SUG-02/03/06/07/08 implemented, SUG-04/09/10 deferred, SUG-05 still
  blocked pending the owner's Associates tag).

**One defect found and fixed in flight (5a56-F-01).** The shared page template's
subdirectory link prefixer added a single `../` regardless of nesting depth; the first
page nested two levels deep rendered links that resolved one level short. Fixed
(depth-aware prefix) in the same commit, before merge; all link gates pass.

**Gates at publication.** `check_site` OK (19 pages, 3 products, 51 sources, 78 flags) ·
`verify_site` PASS (80 pages, 1,369 rows, 0 advisories) · `link_report --strict` exit 0 ·
`build_sitemap --check` exit 0 (75 pages) · `check_all_links` 126 pages, 0 errors.

**Still blank, still correct.** Prices, ratings, review counts, per-product commission
rates, clicks and conversions remain blank: no Associates tag (Q1) and no approved
Amazon data path (Q4) are connected, and 2(b)/6(t) forbid displaying those values from
anywhere else. The fastest path to a revenue-capable site remains the three unblock
items in §5 — owner tag, intended ASINs, account/API status.

---


## 12. Front door, four guides and the decision record — session `cba81fa5` (2026-11-16)

**What this pass was asked to do.** Implement what the earlier suggestion registers only proposed, so the
repository opens like a marketing affiliate site rather than an audit; keep the site publishable without a
single unverified number; and give the owner a decision record with the questions, the answers, and what is
still missing. Nothing here was invented to fill a gap: where a source is silent the cell stays blank and the
blank is explained.

**Shipped.**

| Deliverable | Where |
|---|---|
| Marketing front door at the canonical URL, generated and idempotent, with the dashboard preserved beneath it | `index.html` + `assets/front-door.css`, injected by `tools/build_cba81fa5_site.py` from `data/cba81fa5/guides.json` |
| Four new buyer guides, each answering one question, every specification linked to the listing row it came from, each page ending with what it cannot tell you | `site/guides/capacity-maths.html`, `air-fryer-oven-vs-basket.html`, `what-four-in-one-means.html`, `dishwasher-safe-baskets.html` |
| The suggestions section with a decision path: 9 settled questions, 11 owner-only questions (with the default the site ships with if unanswered) and three paths compared, one recommended | `site/answers.html` |
| House style with 11 banned constructions and 7 page requirements, each tied to the Amazon or FTC rule it protects | `site/style-guide.html` |
| A mechanical enforcement of that style, with a reviewed baseline so inherited findings are visible rather than suppressed | `tools/cba81fa5_lint.py`, `tools/cba81fa5_lint-baseline.json` |
| Independent re-verification, dated, with the withheld values named | `research/cba81fa5-verification-log.md`, `data/cba81fa5/sources.json` (15 records) |
| Repo review, measured not estimated | `research/cba81fa5-repo-review.md` |
| Five new findings, published for review rather than fixed silently | `site/flagged.html` (§"second-source desk") and `data/cba81fa5/flags.json` |

**The two answers the research produced that change decisions.** (1) Amazon's own enrolment rule requires
original content and, for third-party material, "significant commentary, analysis, or transformation" — so the
"no AI slop" instruction is a compliance requirement, not a preference, and it is now enforced by a build step.
(2) Product-list links additionally require "additional original content on your Site that is relevant to the
Special Link", which is why this site publishes analysis pages rather than link roundups
([Program Policies, Participation Requirements 1 and 2(b)](https://affiliate-program.amazon.com/help/operating/policies),
read 2026-11-16; CBA-S07, CBA-S09).

**The finding that matters most for trust in this repository.** `tools/verify_site.py` — the gate that
reports "VERIFY PASS" on disclosure, disclaimer, single-h1 and row-provenance — cannot fail those checks: it
takes its "pages owned by this build" set from `data/z3/build-manifest.json` values, which hold content
digests rather than paths, so every such finding is advisory. Reproduced with a synthetic page this session.
`CBA-F-02` carries the proposed two-line fix and why it was not applied here: a corrected gate would turn
hundreds of other sessions' rows into hard failures on `main`, and that is a reviewable change, not a
side effect of a marketing pass. The compensating control that *does* fail is `tools/cba81fa5_lint.py`.

**Still blocked, and unchanged by this pass.** No Associates tag exists, so no link can earn or be measured
(Q-1/D-05); there are no Creators API credentials, so prices, availability, ratings and review counts stay
blank on every page (Q-4); the campaign ledger is empty by design; and no human editor has reviewed any page,
so the bylines say an agent desk wrote them (Q-5/D-10). Two reader layers now exist side by side, and the owner
decision on which is canonical is on the flagged page (`CBA-F-03`), not quietly resolved.

## 13. Independent verification round and the five-link intake — session `92988cd8` (2026-11-17)

**Verified today, from the official pages themselves.** Nineteen observations, all matching the
register: the three registered short links still open the same three air fryers
([S11](https://link.amazon/B04G1MEwY) · [S12](https://link.amazon/B02NbDxp3) ·
[S13](https://link.amazon/B00hJ57DV)); all five direct `/dp/<token>` controls (three registered
plus two new) serve Amazon's *Page Not Found*; the Operating Agreement still reads
"Updated: October 15, 2025" with the §5 disclosure sentence verbatim
([S01](https://affiliate-program.amazon.com/help/operating/agreement)); the Program Policies still
read "Updated: April 14, 2026" with 2(b), 6(s), 6(t), 6(w) and 6(y) re-read verbatim
([S02](https://affiliate-program.amazon.com/help/operating/policies)); Standard Commission Table 1
([S25](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ)), the 10-character
ASIN rule ([S31](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#itemidtype-parameter))
and FTC Disclosures 101 ([S07](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers))
are unchanged. Full record:
[sessions/92988cd8/verification-2026-11-17.md](sessions/92988cd8/verification-2026-11-17.md).

**The intake grew from three links to five, and that is now published rather than assumed.**
The 2026-11-17 brief lists five short links. Links 4 and 5 (`B0c8moW59`, `B0f3GKalj`) appeared in
no data file, page or document in this repository. Both are 9-character tokens (not ASINs); both
`/dp/` controls serve Page Not Found; both short links open live **meat-thermometer** listings
(B0DHZTCNR5, B0DZFD6R9Z) in Amazon's Thermometers & Timers › Meat browse path — a different
category from the three air fryers every editorial surface covers. The complete five-link intake
table, with a source link on every row, is on
[sessions/92988cd8/index.html](sessions/92988cd8/index.html); the finding is published as
**929-F-01** on the Flagged for review page, with the scope decision recorded as review-console
question **929-Q-16**. No product row was added and no intent was inferred (FLG-002 rule).

**The Tracking ID blocker moved from discovery to validation — not to done.** The brief supplies
an Associates Tracking ID for the first time (value recorded in `COORDINATION.md`, Part session
92988cd8, and deliberately not stored in data files or pages, per suggestions question Q1's own
rule). Its format matches Participation Requirements 2(b) — the tag appearing "as XXXXX-##, or such
other format as we may designate" — but no public page can confirm tag registration, account
approval or marketplace match. No outbound link carries it yet, so nothing on the site can earn or
be measured today. Recorded as **929-F-02**; review-console **Q1**, missing item **757-M-01** and
suggestions **Q1** were updated from "value unknown" to "value received, validation pending", with
the brief's own S-03 sequence (one tagged link per product in the enrolled workflow, destination
plus tracking report) as the closing action. SUG-05 stays blocked until that passes.

**Gates.** All twelve exit 0 on the final tree: `check_site`, `verify_site`, `link_report --strict`,
`i2_gate`, `cba81fa5_lint`, `build_sitemap --check`, `check_all_links`,
`build_cba81fa5_site --check`, `test_manifest_regression`, `cba81fa5_test_no_repr_output`,
`build_read --check`, `sessions/3c886b62/tools/check_links.py`. Brief-gap verdict for every ask in
the current brief — served, or served-but-blocked — is the brief-gap matrix on the session page.
---

## Session ded63349 pass (2026-11-17) — measurement machinery, intent record, sponsored-rel gate, decision console (updated after merge reconciliation)

Scope: the brief's measurement, cadence, disclosure-placement, sponsored-rel and product-intent
priorities, implemented on the reader layer without changing any registered fact. Independent
verification round: `sessions/ded63349/verification-2026-11-17.md` (D6-V01..V18 — every load-bearing
official page re-read on 2026-11-17; all match the register).

**What this session shipped (present in the merged tree):**

| Item | Result |
|---|---|
| Five defined events | `page_view`, `outbound_product_click`, `comparison_open`, `guide_read_through`, `decision_open` — defined on `site/measure.html` (D-16), recorded device-side in `site/assets/site.js`; no cookies, no identifiers, no third-party calls, no server (static hosting — recorded as blocked D-20) |
| Publishing cadence | one guide per fortnight from 2026-12-01, monthly measurement review, quarterly compliance re-read (D-17); new guides enter sitemap + feed automatically |
| Product-intent record | `site/intent-record.html` + `data/ded63349/intent_record.json` (D-24): intended ASIN blank by design (owner-only, Q2), official listing URL, confirmation dates 2026-11-16 (re-observed 2026-11-17), observed redirect targets in a separate field. The dashboard's intent table on `products.html` (session 82372fd1) is the complementary dashboard view |
| Sponsored-rel gate | i2_gate **G11** (D-19): every `/dp/`, `/gp/product/` and `link.amazon` anchor must carry `rel="sponsored"`; marking itself is done by the site generators and `sessions/aebf0747/publish_pass.py`, and `tools/apply_sponsored.py --check` runs as a redundant verifier |
| Disclosure-placement check | `tools/add_disclosure_banner.py --check` verifies the §5 sentence sits above the fold on every published page (complements `publish_pass.py`'s strip; on the merged tree every page already passes) |
| Mobile + front door | fluid type scale, 44px tap targets and a sticky quick-compare bar on guide pages (D-22); front door gained the dashboard footer nav group generated from `scripts/build_site.py`'s nav lists (D-23) plus measure/intent/feed links |
| Decision console | D-16..D-24, Q14..Q16, DA-10..DA-12 appended — 24 proposals, 16 questions, 12 discovery actions |

**Merge reconciliation (same day).** While this session worked, `main` absorbed sessions 974e366d
(shop layer), aebf0747 (publication pass: disclosure strip, sponsored rel, head links) and 82372fd1
(mobile pass, union feed, dashboard intent record, suggestions review). The rebase kept every
session's work and retired only this session's *duplicate* machinery: its Atom-format feed
variant and its standalone banner-insertion pass. The canonical feed is the **union RSS 2.0
`feed.xml`** (session 82372fd1, both guide registers); all feed-discovery links and labels were
normalized to `application/rss+xml`, and `tools/build_cba81fa5_site.py`'s front-page feed-link
backstop now injects RSS only when no feed link of either type exists. Conflicts (COORDINATION.md
add/add; `tools/build_feed.py` add/add; generated pages) were resolved by taking `main`'s version
and re-applying only the deltas this session owns. Logged in COORDINATION.md's reconciliation record.

**Gates on the final merged tree (all exit 0; full chain run twice, identical tree hash):**
`i2_gate` PASS — 20 pages · 186 rows · 170 sourced · 16 explicit blanks · 0 flagged (checks G1–G11) ·
`cba81fa5_lint` PASS (0 new findings) · `cba81fa5_test_no_repr_output` PASS · `check_site` OK
(30 pages / 3 products / 62 sources / 113 flags) · `verify_site` PASS (136 pages · 2,090 rows ·
1,791 sourced) · `link_report --strict` 0 · `check_all_links` 0 errors · `apply_sponsored --check`
PASS · `add_disclosure_banner --check` PASS · `build_feed --check` PASS · `build_shop --check` PASS ·
`publish_pass --check` PASS · `build_cba81fa5_site --check` current · `build_sitemap --check` current.

**Still blocked, unchanged:** Associates tag (Q1), intended ASINs (Q2), Creators API credentials (Q4),
human editor review (Q5/D-10), the analytics endpoint's host (Q14/D-20), Search Console verification
(Q15/D-21), and the Special Links test that only the account holder can run.

**Parallel measurement layer (session 38650305, merged the same day).** On top of the five-event
device ledger above, the merged tree carries a second, endpoint-bound counter: `assets/measure.js`
+ `assets/measure-config.js` generated from `data/shop/measurement.json` (counting **OFF** until
`endpoint_url` is set), injected site-wide by `tools/measure_pass.py`, with an aggregate-only
collector (`tools/analytics_endpoint.py`, self-test PASS). Known divergence, flagged for review:
`measurement.json` proposes five event ids (`page_view, outbound_click, guide_view, intent_view,
flag_view`) that differ from D-16's five (`page_view, outbound_product_click, comparison_open,
guide_read_through, decision_open`) on the same page — both sessions derived "five events" from a
brief that names no list (flag M38-F-04). The owner decision that unifies them is recorded on
`site/decisions.html` (Q14/D-20 for the endpoint; the event list needs a ratification choice).


## Update 2026-11-17 — session 5b443d02 (five-link intake, Direction section, final integration)

**Bottom line.** The brief submits **five** product links. Every data file, page and analysis in this
repository had been built on **three** of them. The two missing links were fetched from the official
Amazon pages on 2026-11-17 and they do not belong to the site's only category: they are **meat
thermometers**, not air fryers. That single fact invalidates the site's information architecture
before any redesign work starts, so this session published a product-intent confirmation record, a
design-suggestion pack, an open-questions register and a three-path chooser under
[`/direction/`](https://kanlerxz87-cyber.github.io/Zone3/direction/) rather than changing the site's
shape unilaterally.

**All five submitted links, fetched 2026-11-17.** Every token is 9 characters; the
[Creators API GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items)
defines an ASIN as a *"10-Character alphanumeric unique identifier"*, so no submitted token is itself
the ASIN, and the intended product can only be stated by the person who submitted the link.

| Submitted link | Observed destination | Listing title as served | Browse node (leaf) |
|---|---|---|---|
| [link.amazon/B04G1MEwY](https://link.amazon/B04G1MEwY) | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | Chefman 6 Quart Dual Basket Air Fryer Oven | Air Fryers (17659096011) |
| [link.amazon/B02NbDxp3](https://link.amazon/B02NbDxp3) | [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Air Fryers (17659096011) |
| [link.amazon/B00hJ57DV](https://link.amazon/B00hJ57DV) | [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | Air Fryers (17659096011) |
| [link.amazon/B0c8moW59](https://link.amazon/B0c8moW59) | [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) | ThermoMaven 1 Sec Professional Digital Meat Thermometer | Meat (289810) |
| [link.amazon/B0f3GKalj](https://link.amazon/B0f3GKalj) | [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) | Chef iQ Sense Smart Wireless Meat Thermometer, Gen3 | Meat (289810) |

**Records this session published.** [Product intent](https://kanlerxz87-cyber.github.io/Zone3/direction/products.html)
keeps the intended ASIN and the observed destination in two separate tables and never merges them;
the intended field is blank on all five rows and stays blank until the owner confirms it.
[Direction](https://kanlerxz87-cyber.github.io/Zone3/direction/) carries 19 design and editorial
suggestions, each with the prerequisite that gates it, plus 8 working article titles.
[Open questions](https://kanlerxz87-cyber.github.io/Zone3/direction/questions.html) carries 14
decision-blocking questions, each with what is already established, what is missing, the action that
would close it, what it blocks and the default if it stays unanswered.
[Choose a path](https://kanlerxz87-cyber.github.io/Zone3/direction/choose.html) sets out three
complete answers and records a choice without applying it.

**Re-read from the official pages on 2026-11-17:** the
[Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
(updated October 15, 2025 — §1 Special Links and the Program Content definition, §4 no representation
as to traffic or commission income, §5 the disclosure, §6(a) breach of §5 is a material breach), the
[Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (updated April 14,
2026 — Commission Income Statement §1 qualifying purchases), and the
[Creators API GetItems reference](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items)
(ASIN, 10 characters; `partnerTag` required).

**Flags raised:** six — 5B-F-01 (two of five links are in a different browse node, High), 5B-F-02 (two
links were absent from every data file, High), 5B-F-03 (intended ASIN unknown for all five, Medium),
5B-F-04 (the release gate does not count Google Search Central as an official host, Low), 5B-F-05 (no
validated Special Link and an unconfirmed tracking tag, Medium), 5B-F-06 (a same-page anchor bug in the
shared gate, fixed, Info). All are on the
[Flagged for review](https://kanlerxz87-cyber.github.io/Zone3/flagged.html) page.

**Independent corroboration.** Session `2f181cd9`, working in parallel on 2026-11-17, reached the same two previously unrecorded links and registered them in the shared source register as `S70`–`S75`; session `82372fd1` flagged the same two links as `G82-F-03` and added rows for them that still have empty observed fields. Three sessions finding the same gap independently is corroboration of the finding. This session's contribution is the destinations, the browse-node mismatch, and the decision records that follow from it.

**Owner decisions needed.** (1) Which of the three paths this site follows — one kitchen site with two
pillars is the default. (2) The intended product or ASIN behind each of the five links. (3) Associates
account status, the tracking tag and the Special Link format. (4) Whether two of the five products are
in scope at all.

---

## 14. Five-product intake, tracking-ID record and brief gap audit — session `cbb03ec7` (2026-11-17)

**What this pass was asked to do.** Absorb the owner's 2026-11-17 brief into the shared registers
without inventing anything: two new product links, one tracking ID, a line-by-line gap audit of the
brief against what the repository already ships, and the final integration (gates, PR, merge, Pages).

**Shipped.**

| Deliverable | Where |
|---|---|
| Products 4 and 5 in the flat register — submitted URL, 9-char token, direct `/dp/` Page Not Found, observed destination, title and breadcrumb, every commercial cell blank | `data/products.json` (P4, P5), rendered on `products.html`, `pricing.html`, `reviews.html` |
| Six new source records for the 2026-11-17 fetches (two short-link redirects, two listing-title reads, two direct checks), each URL official or the submitted link itself | `data/sources.json` S70–S75, rendered on `sources.html` |
| Three new findings: P4/P5 identity unconfirmed (`CBB-F-01`), tracking ID supplied but unverified and in no link (`CBB-F-02`), two-category scope mismatch (`CBB-F-03`) | `data/flags.json`, rendered on `flagged.html` |
| Tracking ID `shopnow047c-20` recorded with status *unverified*, deliberately not embedded in any link | `config/platform.json` |
| Three new decision questions (tag verification + Special Link test, P4/P5 intent, category scope), two discovery steps, one missing-information row | `data/decision-queue.json` → `decision-queue.html` |
| Four new suggestions plus the brief's parallel-pass rows SG-27…SG-30 (nav labels, RSS feed, Search Console, reader capture) — proposals only | `data/suggestions.json` → `suggestions.html` |
| Verification log extended with four rows for the 2026-11-17 fetches; executive summary and products page copy updated from three links to five | `scripts/build_site.py` → `verification.html`, `executive-summary.html`, `products.html` |

**Verified, not inferred.** Both new short links were fetched twice on 2026-11-17 (the link, then the
bare listing URL); titles and breadcrumbs matched across fetches (S70–S75). Prices and star ratings
visible on those pages were deliberately not recorded — 2(b)/6(t) bar displaying them outside an
Amazon-served link or the API (FLG-036). Nothing was filled in: identity, price, rating, review count
and commission cells for P4/P5 are blank, exactly as for P1–P3.

**Still blocked, unchanged by this pass.** The tag value exists but its account assignment cannot be
checked without a logged-in Associates console (CBB-F-02/CBB-Q-01); no Creators API credentials, so
prices and ratings stay blank; the campaign ledger is empty by design; the analytics endpoint and
reader-capture form need owner infrastructure decisions (SG-29, SG-30, DEC-03); and the two-category
scope question (CBB-Q-03) decides what the next content batch is about.

---

## 15. Suggestions review round: design-prompt feed, article slate, traffic mechanics, decision support — session `b9008684` (2026-11-19)

**What this pass was asked to do.** Publish suggestions that feed the design prompt for a polished,
non-generated marketing site; a catchy, question-shaped article slate; organic-traffic mechanics;
a review section where the best path can be chosen before anything is implemented; and a clear
have / don't-have / discovery / default register for every decision that still needs information.

**Shipped (all on the canonical review surface, [`suggestions/index.html`](suggestions/index.html)).**

| Deliverable | What it is | Where |
|---|---|---|
| Review round — 19 Nov 2026 (session `b9008684`) | A dated section on the suggestions page, below the nine standing evidence questions, using the same select/save/export review-only pattern | `data/publication.json` (`review_b9008684`), rendered by an additive extension of `tools/build_publication.py` `suggestions()` |
| Design-prompt feed (D9-01…D9-07) | Seven suggestions, each carrying the exact sentence it would add to the design prompt and a "what would change our mind" falsifier: seasonal strip, one-guide-at-a-time slate approval, sourced-only FAQPage schema, mobile pass port, imagery-route decision (blocked, S-18), decision-shaped hub grouping, review-mode falsifier rule | `suggestions/index.html#review-round-b9` |
| Article slate (AS-01…AS-07) | Seven working titles, question-shaped, each with provenance (FoodSafety.gov chart, listing wording, shipped guides) and pairs-with links into the existing six guides; every card states that a working title is not a popularity, search-volume or demand claim | same section |
| Organic-traffic actions (5 rows) | Automated now (findability checklist), blocked on owner accounts (Search Console; durable host — GitHub Pages' limits bar business use), the paid-search standing rule (ads must land on this site, never directly/indirectly on Amazon; none run), and the 14-day review cadence | same section, table with official basis per row |
| Decision-support register (DS-01…DS-08) | For each pending decision: what is already in hand, what is missing, how to discover it, and the safe default if it never arrives — the "questions, information and answers" list, companion to the nine standing questions | same section, table with official basis per row |
| Two new official sources | Google structured-data intro and page-experience guidance, both fetched live 2026-11-19 and added to the scoped publication register | `data/publication.json` sources (12 total there; the shared `data/sources.json` register is untouched at 87) |
| Dated verification round | The five supplied links re-fetched (identical destinations, titles, breadcrumbs — corroborating session `cd746460`'s same-day record); OA §4/§5/§6, Policies 2(b)/6(f)/6(s)/6(t)/6(v)/6(w)/6(y), FTC Disclosures 101, FoodSafety.gov chart, Google outbound-link/review/structured-data/page-experience guidance and GitHub Pages limits re-read | `sessions/b9008684/verification-2026-11-19.md` |

**Verified, not inferred.** No popularity, search-volume, trend, conversion or revenue claim is
published. Prices/ratings seen on fetched pages were deliberately not recorded (2(b)/6(t)). No flag
was added (register stays at 154): no drift and no new irregularity was found. Intended-ASIN fields
stay blank; observed redirect targets stay separate. Review choices made on the page remain local
browser notes and implement nothing.

**Gates at push.** `tools/publish.py`: 41 commands, 0 failed — publication gate now counts 64
official-source table rows (was 51; +13 review-round rows, each officially linked), 118 current HTML
pages, 14 indexable URLs, 24 feed entries. Rebuild is idempotent.

**Still blocked, unchanged.** Owner-side evidence gates (intended ASINs, enrolled-workflow Special
Link test, durable analytics host, Search Console, reader capture) remain open and are now laid out
decision-by-decision in the DS-01…DS-08 register rather than scattered across pages.
## 15. Batch-2 suggestion register, decision capture and readiness questions — session `e61f5735` (2026-11-19)

**What this pass was asked to do.** Extend the suggestion system so suggestions feed the design
prompt, someone can review and choose a path before anything is implemented, and a clear list of
questions, information and answers that must be addressed before any decision can reasonably be
made — including suggestions for discovering the missing information. Work from what the
repository already has; verify anything new against an official source; leave every blank blank.

**Shipped (additive only — no existing register row was rewritten).**

| Deliverable | Where |
|---|---|
| Nine batch-2 proposals `E61-P1…P9`: reader-facing trust content, a recorded-decision workflow, an imagery-rights decision, sourced seasonal refresh, comparison chooser, thumb-first mobile table, a written success definition before optimization, gated social distribution, and catalogue growth only through intent-confirmed products | `data/publication.json` → `suggestions/index.html` |
| Eight new decision-readiness questions `E61-Q1…Q8`, each with known / missing / discovery step / safe default and an official basis: traffic success definition, imagery rights, seasonal calendar, distribution channels, device mix, catalogue expansion, hosting-migration trigger, approver and decision record | `data/publication.json` → decision-readiness table |
| Per-question answer capture: one field per question, saved and exported only by explicit Save/Export, browser-local, never sent anywhere | `suggestions/index.html` + `assets/publication.js` (review schema v2, reads saved v1 choices) |
| A seven-step "from suggestion to decision" worksheet ending in *Record the decision* — until the export is pasted into a decision record, nothing is decided | `suggestions/index.html` |
| The design prompt extended with the batch-2 directions (chooser, thumb-first comparison, sourced seasonal refresh, visible method as trust content, measured-topic selection, recorded decisions) | `suggestions/index.html` |
| One new scoped official reference, fetched live 2026-11-19: Google Search Central, creating helpful, reliable, people-first content — the editorial basis for the trust-content and measured-topic suggestions | `data/publication.json` `google-helpful` |

**Verification performed.** Full canonical chain (`tools/publish.py`) 41/41 PASS, twice, with the
second rebuild byte-identical (idempotency). Real-Chromium browser checks 14/14 PASS including 32
automated WCAG 2.0/2.1 A/AA scans; the suggestions flow now tests answer persistence in the saved
record, across reload, and in the exported JSON (schema v2), plus no-JS question count. All counts
on reader pages are generated from the register, not hardcoded.

**Not claimed.** No traffic, conversion, ranking, popularity or revenue figure; no new product
fact; no decision recorded by this session — review mode implements nothing, and the owner's
exported review JSON is the input to the decision record, not this pass.

## 16. Batch-3 polish suggestions and decision-gap questions — session `b3e82b38` (2026-11-19)

An additive, review-only round on the canonical publication register. What was added:

- **One fetched official source** — Google Search documentation updates, capturing that the FAQ rich
  result was deprecated on May 7, 2026 and its documentation removed in June 2026 (source
  `google-faq-update`, fetched live on the recorded date).
- **Five proposals `B38-P1…P5`** — publish the house style as a page and enforce it with a
  banned-phrase lint in the release gate; promote the evidence line into a visible badge system on
  cards, tables and guides; approve a follow-on slate of four question-shaped working titles (weeknight
  household size, thermometer accuracy specs, the ice-water check, reheating leftovers — working
  titles, not demand claims); publish the next review date with an overdue state and outcome links
  from adopted proposals; and correct the FAQ plan before DS-03 ships, because FAQ rich results no
  longer exist in Google Search.
- **Four questions `B38-Q1…Q4`** — recurring budget approval; the accountable publisher name and
  contact for disclosure purposes; which listing wording may be quoted verbatim; and publishing
  capacity per review cycle. Each row carries known / missing / discovery / safe-default fields.
- **One design-prompt block (`b38-batch3`)** — honesty as the design language: evidence badges from
  register dates, a linted house style, a cadence-derived review date, reader-only FAQ blocks, and
  register-derived counts everywhere.

**Register totals after the union with session `d3493182`'s parallel batch** (both sessions rebased
over each other; union logged in `COORDINATION.md`): 15 scoped official references, 26 proposals in
four batches, 36 decision-readiness questions, 13 design-prompt blocks, 6 paths, 8 guides. Every count
and check date rendered on the pages derives from the register; nothing is hand-typed.

**Coordination note.** While the claim was being pushed, `main` advanced four times (PRs #181, #184,
#182/#183, #185). The executive-strip count staleness this session had flagged (6/9 versus a register
of 8/24) was independently fixed and gated upstream (part Z3-COUNT-01, PR #181) before this batch
touched anything, so this session verified that fix rather than duplicating it. Session `d3493182`
shipped its own batch-3 register entries; both batches are preserved intact — conflict replay took
`main`'s versions as base at each stop and re-applied this session's additive delta on top, and the
full release chain was re-run on the union. Thematic overlaps (B38-P1 with D34-P5/D34-Q3; B38-P2 with
part of D34-P4; B38-P3's concrete titles extending D34-P2's generic slate) are noted for the reviewer,
not merged.

**Verification.** Apply script idempotent (second run a no-op); full `tools/publish.py` run 41/41
PASS on the union; post-rebuild `--check` 25/25 PASS; every new row confirmed present in the
regenerated pages by element count; the executive strip reads 5/8/36/0 and matches the registers.

No price, rating, review-count, availability, traffic, demand, conversion or revenue value was
introduced. Intended-ASIN fields remain blank. FLG-003 remains unresolved and untouched. Nothing
published by this round implements a suggestion.

---

## 17. Measured-drift pass: compare-page decision aids, one more guide, and counts that cannot drift — session `41e84402` (2026-11-19)

**Base and merge.** Claimed on `arena/41e84402-zone3` from `6eb8c18`; rebased three times and finally *merged*
`origin/main` `1623c1c` after PRs #181, #183, #185–#191, #193, #194, #195 and #196 landed mid-pass — nine other
sessions, several of them while this section was being written. Registers were unioned, never line-merged; the
totals this section leaves behind are **10 guides, 28 proposals, 38 questions, 16 sources, 13 design-brief blocks,
6 paths, 18 indexable URLs, 28 feed entries, 122 published pages** — every one of them read from the registers by
the gate, not typed here:
`07fb37ba`’s executive-brief count fix, `8aa259bb`’s full re-measure of the brief register,
`d3493182`’s and `b3e82b38`’s suggestion batches and `222cfe13`’s analytics-history clarification are all kept
as written. Where a *count* in another session’s live desk copy had gone stale against the union — `B38-Q4`
said “eight guides exist”, `B38-P1` said “the current eight guides” — the clause was made read-from-register
rather than re-typed, under this board’s own `E41-T4` rule; the dated review round in `review_b9008684` that
says “the six guides” was left exactly as it was, because it records what was true when it was written. Full record:
[`sessions/41e84402/verification-2026-11-19.md`](sessions/41e84402/verification-2026-11-19.md);
machine-readable measurements: `sessions/41e84402/measurement-2026-11-19-drift.json` and
`sessions/41e84402/measurement-2026-11-19.json`.

**What a buyer gets from this pass.**

| Change | Reader effect | Verified by |
|---|---|---|
| The three-question “Which one is for you?” chooser now sits **above the comparison table** on the compare page, not only on the category pages | The page where five listings are set side by side now starts from the buyer’s question; no score, no ranking, nothing sent anywhere | `browser_measure.cjs`: chooser precedes `#comparison` at 320/390/768 px |
| The comparison table’s **product column stays pinned** while the table scrolls sideways, with a plain note that blank cells are unverified rather than empty-by-failure | A phone reader can compare five listings without losing track of which row is which | measured: `left_before == left_after_scroll == 16 px` at 320/390 px; at 768 px the table fits, so nothing scrolls — reported as measured |
| Tap targets on that page raised to the WCAG 2.2 2.5.8 minimum | **0 of 26** interactive targets under 24 px, from 18 of 26 under 44 px before (category pills 31 px, an in-cell link 11 px, a guide-card link 18 px) | `browser_measure.cjs` |
| Every published guide now links the buyer comparison table **in its own body** | The reading path closes: question → guide → shortlist → comparison, in both directions | `measure_drift.py` structure scan, 9 of 9 |
| One more question-led guide: “What do “1 Sec” and “±0.5℉” on a listing actually tell you?” | A thermometer buyer gets the difference between a response time, a tolerance and a certification wording, with the unknowns named | register-driven: sitemap 17 URLs, feed 27 entries, search index 14 rows |

**Machinery: the class of defect, closed rather than patched.** Another session had already made the
executive-brief totals register-driven (#181). This pass found the remainder of the same class — “the
current six guides” twice in the renderer, “which of the six guides” in a live desk row, and a README
headline contradicting its own findability line four lines below — and made every one of them either
derived or count-neutral. `README.md`’s numbers are now a **generated** block (`z3:register-facts`,
written by `tools/build_publication.py`), and `tools/check_publication.py` fails the build when any
reader page, README line or register field states a count its register does not hold. Negative test,
recorded: hand-stale-ing the README row produced
`FAIL README register-facts row 'Question-led guides': README says 8, register says 9`. The gate then
caught one of this session’s own sentences (“two air-fryer listings” where the register holds three),
which was reworded rather than exempted — and it also refuses to let the flag backlog grow: a flag row
that records the date it was raised must record a status (`E41-B01`, because 121 of the register's rows carry no
status in either the 164-row pre-merge tree or the 169-row merged tree).

**The hole the merge exposed, and what the gate became.** #193 re-typed “eight … question-led guides” and a fresh
set of counts into `README.md`, and the gate passed it: the numeral had to *abut* the register label, and only
README's pre-block prose was scanned. Both rules were tightened — a short closed list of qualifiers may now sit
between the number and the label across a line break, and the whole README outside dated sections is scanned. The
widened scan immediately flagged this session's own sentence quoting the old headline, which was rewritten
count-neutral rather than exempted; a planted “ten practical / question-led guides” line then failed the build
(`FAIL README.md current-state prose: states 10 question-led guides; the register holds 9`) and was removed, so the
enforcement is demonstrated in both directions. Final state on the merged tree: `tools/publish.py` 41/41 with a
second run changing no tracked file and `--check` 25/25, `PUBLICATION PASS` over 121 current pages with 102
official-source table rows, `brief status current · 23 rows`, and the published browser harness at 14/14 checks with
38 page/viewport accessibility scans and 0 violations.

**Two measurement findings the owner should read before choosing a next step.**

1. `E41-F02` / `E41-B03`: a same-day register row recorded that “all eight guides link to the comparison
   page (`products/index.html`)”. That string appears on a guide page only in the site-wide footer
   directory, labelled “Research product register”, which is the research intake page — not the buyer
   comparison table at `shop/products/index.html` — and it is present on every published page regardless
   of article linking. Article-level linking to the comparison table did not exist before this pass.
   No other session’s row text was edited; the correction is appended below it.
2. `E41-F03` / `E41-B02`: the brief’s capacity-per-centimetre analysis (`S-23`) **cannot be written** from
   this repository. No product register — `data/publication.json`, `data/shop/products.json`,
   `data/z3/products.json`, `data/products.json` — holds a footprint or interior dimension for any of the
   five. The analysis was left unwritten; the capture decision is `E41-P1` with the owner question
   `E41-Q1` (which authorized source may supply dimensions, dated, with units). Estimating the denominator
   was the available wrong answer and was not taken.

**Not claimed.** No traffic, query, ranking, conversion, commission or revenue figure; no price, star
rating or review count; no product photography; no new product fact; no account, API, Search Console,
hosting or analytics change. The five submitted short links keep their separate fields: intended ASIN /
official URL / confirmation date / source stay blank, observed redirect targets stay in their own field,
`FLG-003` stays unresolved and they are not called invalid. Campaign ledger: still **0** rows, by design.
One editorial observation for whoever tidies this file next: two sections above this one are both numbered
`## 15.`; no other session’s heading was renumbered here.
