# Design brief — Zone3 Kitchen, the polished affiliate edition

**Status: a proposal to build from, not a change that was made.**
Dated 2026-11-19 · written by session `6b68afc8` against `main` at `825f513` · owner of the numbers below is this repository, measured, not admired.
Read it with [`suggestions/index.html`](https://kanlerxz87-cyber.github.io/Zone3/suggestions/index.html): the paths and open questions that decide *whether* each section below may be built live there.

Every clause quoted here was opened on 2026-11-19 from the official page, and each rail names the register row that carries it (`data/sources.json` in this repository).

---

## 1. The one-sentence goal

Make a buyer who lands from a search about a kitchen appliance leave with a better question than they arrived with — and make the link they follow obvious about what it is.

Not "make it look like a big affiliate site". A big affiliate site is exactly the thing both Google and Amazon penalise when it has nothing to say: thin affiliation is rewritten retailer copy; the fix is a page with a point of view, sources within reach, and blanks that stay blank.

---

## 2. The rails — rules a design must not cross

Each rail states the official clause, and what it does to the layout. A design idea that breaks a rail is not a style disagreement; it is a policy problem. The fit note above is the test case that shows the rails working: it states only what the listing's own wording supports, asks the buyer to check the rest, and declines to name a winner (R7, R8).

| # | Rail | The clause, and the row that holds it | What it does to the layout |
|---|---|---|---|
| R1 | The Associates statement stays above the fold, everywhere, undismissable. | "You must clearly and prominently state the following … 'As an Amazon Associate I earn from qualifying purchases.'" — Operating Agreement §5; a §5 violation is called a material breach in §6 (S01, re-read 2026-11-19). | A disclosure strip sits between the masthead and the first content block on every page, and the sentence is repeated in the footer. No cookie-banner pattern, no "×", no collapse. |
| R2 | No price, no star rating, no review count unless Amazon serves it or a licence covers it. | "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API and you comply with the requirements …" — Program Policies 2(b) (S02, re-read 2026-11-19). | Product cards carry the listing's own words, a format illustration and a "no current price is reproduced" line. There is no price-comparison module to design, and no green/red price chips. A design that assumes a price slot will need this rail changed first — by evidence, not by CSS. |
| R3 | No urgency, no countdown, no "deal ends tonight". | "You must remove from your Site any links and related references to limited time promotions as soon as that promotion on the relevant Amazon Site ends." — Program Policies 2(b) (S02). | No banner slot, no countdown component, no "trending now" rail. A seasonal module is allowed as dated context ("it is hosting season"), never as scarcity. |
| R4 | Links are accessed directly; nobody is taught to bookmark them. | "You must not encourage customers to bookmark your Special Links. All Special Links must be accessed directly from your Site." — 2(b) (S02). | CTAs are inline actions, not "save this page" prompts. No share-sheet component that advertises saving. |
| R5 | No per-visitor tracking, no sub-tag against a person. | "Under no circumstances may you associate any sub-tag, other ID or reporting … with a specific end user of your Site (e.g., you may not dynamically assign sub-tags to users as they arrive…)" — 2(b) (S02). | Measurement is aggregate-by-day with no identifier; a design must not add a per-user badge, a "we remember you" strip or a personalised rail. |
| R6 | A page that links a product list has to earn it. | "When linking to pages with Product lists you must have additional original content on your Site that is relevant to the Special Link." — 2(b) (S02). | Category and shortlist pages need real editorial above the cards — the format explanation, the questions, the unknowns — not a grid of thumbnails. |
| R7 | No experience we do not have. | "You can't talk about your experience with a product you haven't tried." — FTC, *Disclosures 101* (S07/S51, re-read 2026-11-19). | No "we tested" ribbon, no quote-cards from imaginary reviewers, no before/after food photography. Authorship says *Zone3 Editorial*, an organisation, and every guide states "not a hands-on review". |
| R8 | Any "best" claim needs original evidence behind it. | Google's review guidance asks for original evidence, and for support for "best-in-class" claims (S94). | No winner column in the comparison table. Blank cells are labelled, not filled. Ranking modules stay unbuilt until path P27-P4 exists. |
| R9 | Program Content is Amazon's to serve; images are ours or labelled. | Program Content (data, images, text, link formats, widgets) is made available for displaying the items; it is not a licence to republish Amazon product photos as our own — Operating Agreement §1 and the Program Content/asset conditions (S01). | Two kinds of image only: the labelled AI editorial still life, and original generic format diagrams. `check_publication.py` enforces "images must be local approved editorial assets" on every current page. Do not add a `<figure>` that pretends to be a product photo. |
| R10 | Sponsored is a machine-readable thing, not a caption. | Mark links that are advertisements or paid links with `rel="sponsored"`; marked links "will generally not be followed" — Google, *Qualify your outbound links* (S90, re-read 2026-11-19). | Every Amazon anchor carries `rel="sponsored"`, and a lint gate fails the build if one does not. A redesign may restyle the CTA, never re-route it through a component that drops the attribute. |
| R11 | No invented market data. | No report exists in this repository for search volume, popularity or conversions; Amazon states it "do[es] not make any representation, warranty, or covenant regarding the amount of traffic or commission income you can expect" (S01 §4). | Zero "10,000+ happy cooks" counters, no fabricated review-count badges, no "most popular this week" chip. If a number appears in a design comp, the brief must name the dated first-party source that will supply it, or the number goes. |
| R12 | Names, domains and tags stay clean of Amazon marks; no child-directed design. | "include any trademark of Amazon or its affiliates, or a variant or misspelling … in any domain name, subdomain name, in any 'tag' or Associates ID, or in any username, group name, or other identifier" is prohibited, as is a site "directed toward children" — Program Policies 1(f)/(g) (S02). | The brand decision (Q1 in the register) must produce a kitchen name, not an Amazon-adjacent one. Nothing in the UI is aimed at children, so no playful mascot, no toy-like type, no "kids' recipes" rail. |

Hosting sits outside the design brief but constrains it: GitHub Pages "is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions" and publishes a 1 GB published-site size with a soft 100 GB/month bandwidth ceiling (S91, re-read 2026-11-19). Treat that as an owner decision (`P27-Q2`), not a rendering problem, and keep heavy assets out of the plan while it is open.

---

## 3. What is actually on the site today (measured 2026-11-19)

Re-measured 2026-11-19 after PRs #198, #199, #200 and #201 and session `3d0d7bd1`'s batch by
counting the checked-in tree and the registers, not by retyping: the two readings are recorded
in `sessions/3d0d7bd1/verification-2026-11-19.md`. The 8-guide and 16-URL rows below were this
brief's original 2026-11-19 reading; the "now" column is the current one.

| Surface | Count (now) | Note |
|---|---|---|
| HTML pages outside `docs/`, `sessions/`, `archive/` | 124 | the whole published tree |
| Indexable reader set (canonical + in `sitemap.xml`) | 20 | front page, guide index, 11 guides, four shop surfaces, about, privacy, **and the new house-style page `style.html`** |
| Question-led guides | 11 | 2026-11-17 four · 2026-11-19 three more · "Hi-Fry/Sync Finish/4-in-1", "How do you know when an air-fryer cook is actually done?", "Where does the probe go?", "1 Sec / ±0.5℉ on the label", "the ice-water check" |
| Submitted product links registered | 5 | 3 air fryers, 2 meat thermometers; titles re-opened 2026-11-19 |
| Pages carrying `rel="canonical"` | 124 / 124 | |
| Pages carrying `og:image` | 33 / 124 | the reader layer and its archives; the legacy registers do not |
| Pages with a meta description ≥ 60 characters | 119 / 124 | the five exceptions are meta-refresh stubs titled "Moved", excluded from the sitemap on purpose |
| `sitemap.xml` `<url>` entries | 20 | 0 `<lastmod>`; see the rejected-idea note in `P27-F06` |
| `feed.xml` entries | 29 | union of the guide registers, desk notes and archive items |
| Decision-desk rows on the suggestions page | 6 paths · 30 proposals · 39 questions · 13 brief blocks | each with an answer owner and a safe default; decided proposals now carry dated Outcome lines (B38-P4) |
| Source register | 17 rows | official-host only |
| Flag register | 164 rows | published on the Flagged-for-review page |
| House-style lint | 15 banned-construction rows | enforced by a release gate since 2026-11-19 (`house_style` in the register; B38-P1) |

---

## 4. Layout, top to bottom

Shared chrome is composed once, in `tools/publication_chrome.py`, so masthead, disclosure strip, search dialog and footer cannot drift between pages.

1. **Masthead** — brand, four reader destinations (The edit, Buying guides, Air fryers, Thermometers), then *one* "Behind the site" group holding every research surface, plus the search trigger.
2. **Disclosure strip** — R1. Non-dismissible, above all content.
3. **Hero** — one editorial promise and one image, with a single "start here" story overlaid. A shortlist, not a value proposition.
4. **Principles row** — three lines. This is where honesty earns its place in the layout rather than hiding in a footer.
5. **The shortlist** — filterable product cards: format illustration, brand line, the listing's own wording as chips, a Sponsored CTA, and a collapsible "Listing & source" note carrying the observation date and the intent-record link.
6. **Question router** — three numbered buyer questions that map to guides. The catalogue pages carry the fuller version: a three-question chooser (`tools/build_publication.py → chooser`) that narrows to a guide and never names a winner, which is exactly the pattern a marketing site needs and a data register does not have.
7. **Reading room** — guide cards with art, then a "Just added to this edition" line derived from the register's dates.
8. **Seasonal cluster** — one dated moment, not a campaign.
9. **Editor's note + RSS follow** — the voice of the publication, then the only subscription affordance that currently works without storing a person.
10. **Footer** — three columns of reader links, the disclosure again, the Amazon content notice, and a collapsed "all research tools & source registers" block that keeps every dashboard reachable.

Category and guide pages reuse the same order, with the article layout (breadcrumb → heading → dek → byline → sticky table of contents → short-answer box → sections → the listings behind the questions → what we have not established → related reads).

---

## 5. Visual system (from `assets/publication.css`, not from a mood board)

```
--p26-paper  #faf9f5   ivory canvas
--p26-ink    #263e31   deep green for headlines and controls
--p26-body   #4d594f   body copy
--p26-muted  #697368   meta, captions, fine print
--p26-line   #dedfd5   hairline rules (1px, never a card shadow)
--p26-sage   #e9eddf   quiet fills: callouts, notes, chips
--p26-orange #b45533   the single accent: rules, focus, the recommended ribbon
--p26-serif  Georgia   display, 46–79px, letter-spacing −0.02 to −0.055em
--p26-sans   Inter     body and UI, 11–17px, line-height 1.75–2
```

Rules that keep it a publication rather than a dashboard: serif for statements, sans for interface; hairlines instead of elevation; one accent, used for the three things that need it (an editorial rule, a focus state, a recommendation); minimum 44px tap targets; visible focus outline; tables scroll inside a labelled region and keep their captions; small type is deliberate — the fine print is read, not skimmed, because it is where the honesty lives.

No gradient headline, no glass, no shadow soup, no hero illustration that promises a lifestyle, no icon set borrowed from a dashboard kit, no dark "analytics" panel. If a design token has to be invented to make a screen look impressive, the screen is the problem.

---

## 6. Components — allowed, and forbidden

| Component | Allowed today | Forbidden until its rail is answered |
|---|---|---|
| Product card | Format illustration, listing wording as chips, a two-sided fit note ("Fits you if / Not for you if" plus one question for the buyer), Sponsored CTA, dated "Listing & source" note | Price chip, rating stars, review-count badge, "best value" corner flag (R2, R8, R11) |
| Comparison table | Source-linked rows, blank cells labelled as unverified | A winner column, a "scored out of 10" cell, a verdict row (R7, R8) |
| Category page | Editorial intro, format explanation, guide links, the shortlist | A bare grid of products with no original content (R6) |
| Newsletter | RSS follow block | An email form with no owner, no consent flow and no sending identity (Q9, R5) |
| Deal / seasonal module | Dated context: "the hosting-season edit", published date | Countdowns, stock or discount claims, "everyone's buying" framing (R3, R11) |
| Imagery | Labelled AI still life, original format diagrams, our own dated photography once it exists | Any stored Amazon Program Content asset, scraped photography, generated "test results" (R9) |
| Measurement | Aggregate, first-party, five events, off until a durable host | Anything identifying a visitor or a session (R5) |

---

## 7. Copy rules

Short declarative sentences. Second person. One idea per paragraph, then a checklist when the reader has to *do* something.

Banned vocabulary, because it is the fingerprint of generated filler: *must-have, game-changer, obsessed, top-rated, unbeatable, elevate your cooking, dive in, in today's fast-paced world, look no further, in conclusion, we loved, readers rave*. Also banned: an invented expert, a fake first name in a byline, a quote with no source, an emoji in a heading, and any sentence whose claim could not survive being highlighted and asked "from where?".

Every product statement names its listing and the date it was read. Every guide ends with what it did **not** establish. Where the answer is "we cannot know from a listing", say that and let the reader keep their money.

---

## 8. Editorial system

- **One question per page, question-shaped title.** The title is what somebody typed, not what the site wants to sell.
- **The ladder.** *Published* → *buildable from the listings already read* → *held until evidence exists*. Held means held: the difference between a publication and a content farm is refusing to soften the gate to ship a piece (that is decision S-06, recorded as not adopted, and path `P27-P4`).
- **Cadence.** Review one guide every 14 days; publish through the gate, not through a calendar. Each new guide is register-driven, so the feed and sitemap update without anyone remembering.
- **Clusters.** Air-fryer formats → capacity → cleanup/counter space → label words → doneness; thermometers split by reading workflow, and both meet the seasonal page. Every article reaches the comparison, a buying guide and its category page.
- **A new suggestion takes this shape:** what a reader would see · why now · which register questions it needs answered · official basis · safe default if nobody answers · gate status. That is the intake block on the suggestions page, and it is what makes two suggestions comparable.

Buildable next, from the listings already read — hypotheses about what buyers ask, not claims about volume: "Is a dual-basket air fryer two small fryers or one big one?", "What does a quart count, and what does the number not tell you?", "Dishwasher-safe baskets: what the wording covers", "What to measure on your counter before an oven-style fryer arrives". Held, and visibly held: any "best value" piece (R2), any "what it's like to live with" piece (R7).

---

## 9. Measurement loop

Five first-party events (`page_view`, `outbound_click`, `guide_view`, `intent_view`, `flag_view`), aggregate by UTC day, no cookies, no identifiers, honouring Global Privacy Control, Do Not Track and Save-Data. Production stays off until a durable host exists and its logging is switched off. A verified Search Console property for the Pages path, plus dated first-party Associates reports, are the only inputs allowed to choose the next topic; the campaign ledger stays empty until a row can name its report. A click is not an order, and an order is not a trend.

---

## 10. Definition of done

1. `python3 tools/publish.py` — 16 generation steps and 25 release gates — run **twice**; the second run must change nothing (`git diff --exit-code`, clean `git status`).
2. Every current table row carries a dated official source or a labelled blank; no page loses its disclosure, its sponsored rels or its footer access.
3. `feed.xml` and `sitemap.xml` gained the new guide automatically, and the indexable set still equals the canonical set.
4. The deployed page is fetched and read back after merge — a Pages build status of `built` is not a content check.
5. Re-measure the section 3 numbers and put both readings in the register. "Polished" has to be a number that moved, not a sentence in a changelog.

---

## 11. What this brief deliberately does not decide

It takes no position on the sixteen open questions in the decision-readiness register — the brand name (`P27-Q1`), hosting suitability (`P27-Q2`), review sign-off (`P27-Q3`), whether testing gets a budget (`P27-Q4`), the refresh policy (`P27-Q5`), the Associates account's view of the supplied links (`P27-Q6`, with `FLG-003` unresolved), and the category scope (`P27-Q7`) — because a design brief cannot answer those, and pretending otherwise is how an unverified assumption becomes a layout.

## 12. How this relates to the other design artifacts

| Artifact | Holds | Does not hold |
|---|---|---|
| `design-brief.html` (session 757efebc) | the earlier six-prompt pack and the visual direction as adopted on 2026-11-16 | the official clause behind each rule; three-product, pre-consolidation inventory |
| `suggestions/index.html` (this pass) | paths, open questions with answer owners, safe defaults, the intake shape and the ten copy-ready brief blocks | a completed change: a saved choice implements nothing |
| this file | the rails R1–R12, the component table, the measured inventory, and a definition of done keyed to the gates as they run today | any colour, name or copy it invented |

Where they disagree, the rails win, because the rails are the ones with a source.

---

## 13. Batch 3 — polished affiliate shopfront (session d3493182, 2026-11-19)

Review-only proposals D34-P1…P6, questions D34-Q1…Q8, path P34-P1 and prompt block 12 on
[`suggestions/index.html`](suggestions/index.html). Nothing here is implemented by reading it.
Each line below quotes the official clause it rests on; where it needs an answer, it names the
question.

- **The shopfront job.** Front page, top to bottom: masthead with the disclosure directly
  underneath; a hero that names the reader's question; the five-product shortlist as cards
  (format illustration, listing capacity wording, two-sided fit note, one sponsored call to
  action); a comparison table whose every cell is sourced or visibly blank; the guide index as
  question-shaped cards; one restrained dated seasonal strip; a footer directory. Basis:
  [Google: understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)
  (overall great page experience, not one or two aspects). Needs D34-Q1 (brand promise) and
  D34-Q2 (per-page goal) before any build.
- **The article slate.** One catchy question-led guide per review cycle, each through the same
  publishing gate. Working titles (editorial hypotheses, never demand claims): "Two baskets or
  one big one? What to compare before you buy." · "How many quarts is dinner for two — and for
  four?" · "What does 'Hi-Fry' actually promise on the label?" · "Where does the probe go?
  Turkey, ham and roasts, checked the boring way." · "Counter-space math: measure before you
  believe the quart number." · "Is it done? Check the food, not the timer." · "Hosting season:
  make a shortlist before you buy." · "Instant-read or wireless: which questions matter first?"
  Basis: [Google: creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
  — "Are you writing about things simply because they seem trending?" is a warning sign, so no
  title is ever described as trending, popular or searched-for. Needs D34-Q5 (cluster map).
- **Findability discipline.** One canonical home, question-shaped titles, internal links from
  two existing guides, sitemap and RSS entry for every new guide. Basis:
  [Google: canonical URL methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
  (signals, not guarantees). Needs a verified Search Console property and a dated query report
  (P26-Q4) before topic choice follows demand.
- **Decision aids, not verdicts.** Question router, fit notes, comparison table, checklists —
  every aid a question, never a score. Basis:
  [Google: write high quality reviews](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews)
  (original evidence, user perspective, support for best-in-class claims). Needs D34-Q6
  (measured engagement per aid).
- **Anti-slop rules.** Second person, plain verbs, short sentences; never must-have,
  game-changer, obsessed, top-rated, we loved, In conclusion, countdowns, invented urgency, a
  fake expert, or any trending/best/price/rating/test claim the register does not hold. Labelled
  generic art only until a licensed-photo decision is recorded (E61-Q2). Basis: Google helpful
  content self-assessment (original information, insight beyond the obvious, descriptive titles
  without exaggeration). Needs D34-Q3 (voice approval).
- **Written success definition.** Queries, pages, outbound clicks and a review date, recorded
  before any optimization is automated. Basis: Agreement §4 (Amazon makes no traffic or income
  representation) and [Google: get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
  Needs E61-Q1, P26-Q4, P26-Q5.
- **What this batch deliberately does not decide.** The brand promise (D34-Q1), per-page goal
  (D34-Q2), voice list (D34-Q3), reader capture (D34-Q4), cluster map (D34-Q5), aid priority
  (D34-Q6), catalogue minimum (D34-Q7) and polish baseline (D34-Q8) — because a design brief
  cannot answer those, and pretending otherwise is how an unverified assumption becomes a layout.

---

## 14. Batch 4 — the decision loop closes (session 3d0d7bd1, 2026-11-19)

Implemented proposals B38-P1, B38-P4 and B38-P5, and closed the measured half of E41-P2; each
decision is recorded with its evidence in `sessions/3d0d7bd1/decisions.md` and rendered as a
dated Outcome line on its proposal card. Nothing here was built before the decision was written.

- **The house style is a page and a lint, not a mood board (B38-P1).** `style.html` renders from
  the same register block the release gate reads (`house_style` in `data/publication.json`), so
  the page a reader sees and the gate the build enforces cannot drift. The lint fails the release
  on any banned construction in strict-scope text; exemptions are mechanical and documented
  (quoted rules, the style page's own phrase cells, the suggestions register that reviews the
  list). Before adoption, every current reader page was scanned against the proposed list —
  buyer-facing copy was already clean, two meta-usages were rewritten, one honest compliance
  sentence was exempted, and all of it is recorded. Basis:
  [Google: creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).
  New open question: **D3B-Q1** — who may edit the list, and on what evidence.
- **The review date is derived, and overdue is stated, never stale (B38-P4).** "Next review due
  3 Dec 2026" comes from the edition date plus the register-owned 14-day cadence; the overdue
  state compares register dates so builds stay byte-stable, and a gate fails the release when the
  register moves past the due date without a new edition. Decided proposals carry Outcome lines.
  Basis: [Google: get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
- **DS-03 is corrected before any FAQ work starts (B38-P5).** Google's own documentation updates
  page, re-read 2026-11-19: the FAQ rich result "will no longer appear in Google Search starting
  May 7, 2026" (notice published May 8, 2026), and its documentation was removed in June 2026.
  The original DS-03 row is kept verbatim; the dated correction sits beneath it with the official
  anchor, and a gate pins the correction so it cannot be silently dropped.
- **The thumb-first comparison closes on measurement, not assumption (E41-P2).** The 2026-11-19
  browser record shows the sticky product column holds at 320/390/768 px with every column
  reachable; the sticky column is the closed outcome, and the floating-bar idea stays where the
  register put it — open question E41-Q2, waiting on device-mix evidence that does not exist.
- **What this batch deliberately does not decide.** The banned-list editing rule (D3B-Q1), the
  floating compare bar (E41-Q2), the authorized source for product dimensions (E41-P1/E41-Q1),
  the brand promise (D34-Q1) and every owner-gated question in the decision-readiness register —
  a design brief cannot answer those, and pretending otherwise is how an unverified assumption
  becomes a layout.

---

## 15. Batch 5 — the anti-slop feed (session ae4e29b6, 2026-11-20)

This addendum feeds the *design* question the owner keeps returning to: why does the site still read
like an audit, and what exactly would make it read like a shop a person would trust? It is written
after re-opening all five listings and seven policy pages on 2026-11-20 (record:
`sessions/ae4e29b6/verification-2026-11-20.md`). Nothing here is a claim about search volume,
popularity or conversion — no such data exists in this repository, and rail R11 still forbids
inventing it.

### 15.1 The diagnosis: the pages explain the rule instead of answering the question

The registry language is the tell. A shop says *take the 6-quart dual basket if you cook two things
at once and hate timing them*. An audit says *P1 observes a 6 Quart capacity per the destination
title, unconfirmed as the submitted product*. Both statements are true; only the first is a page a
buyer finishes reading. The fix is not to delete the honesty — it is to move it one layer down:
answer first, footnote the provenance inline, and keep the full register reachable.

Concretely, three habits to break:

1. **Register IDs in body copy.** `P1`, `SHOP-03`, `FLG-022` belong in a provenance drawer, not in a
   sentence a stranger reads. Keep them in the table and the flag pages.
2. **Hedging stacked three deep.** "Reported by the listing title, not independently verified, and
   not a claim of superiority" in one paragraph reads as machine caution. One short line — *"from the
   listing's own wording; we haven't handled it"* — carries the same honesty.
3. **Symmetric treatment of unequal things.** Five products and nineteen open questions are not the
   same editorial weight. The front page should be five products and one door to the research.

### 15.2 The anti-slop test — a page passes if a stranger can answer all five in ten seconds

- What is this thing, in the first twelve words?
- Who is it for, and who should skip it?
- What does it *not* tell me, stated once?
- What do I do next — and is the link visibly a paid link?
- Who wrote this, and when was it last checked?

A block that cannot answer one of those is decoration. This is the acceptance test for every
redesign comp.

### 15.3 Trend-shaped article plan (hypotheses, not volume claims)

The owner asked for "catchy trendy articles that generate organic traffic". Search demand for these
is **unmeasured** in this repo; each row is an editorial hypothesis with the evidence that would
promote or kill it. Publish order should follow measured arrivals once measurement is on — not
instinct.

| Working title | Buyer question it answers | Why it could earn a click | Killed by |
|---|---|---|---|
| "Two baskets, one plug: what a dual-basket air fryer actually changes about dinner" | Do I need two zones? | The format is genuinely confusing and the listings only describe features | Nothing arrives in 90 days of measured queries |
| "The 6-quart lie: why capacity numbers don't compare across brands" | Is a bigger number a bigger basket? | Contradicts the number the shopper is anchored on, backed by the listing's own Qt-per-basket wording | A source that shows comparable measurement standards |
| "French-door vs basket: the counter-space question nobody answers" | Which fits my counter? | Ties directly to the dimension rows already verified | Authorized dimension source unavailable (E41-P1) |
| "What 'Hi-Fry' and 'Sync Finish' mean before you pay for them" | Are these features or marketing? | Decodes label words a shopper sees but can't evaluate | Already covered by `guides/air-fryer-label-words.html` — extend, don't duplicate |
| "Probe in, phone out: when a wireless thermometer beats a $17 instant-read" | Is the expensive one worth it? | Price-gap framing without quoting a price | Any statement of price or rating (R2) |
| "Thanksgiving timing, without the guesswork" | How do I not ruin the bird? | Seasonal, genuinely searched, links to the thermometer cluster | Framing as urgency or a limited-time promotion (R3) |
| "The ice-water check: five minutes that tells you if your thermometer lies" | Can I trust this thing? | Useful with zero purchase, which is what makes it linkable | — (already published; this is the model to copy) |

**Clusters, not one-offs.** Air-fryer format (4 guides live) and thermometer accuracy (5 guides live)
are the two clusters the site can defend. A third cluster should not start until one of these two
shows measured arrivals. Cluster rule: every new guide links to two siblings and one category page,
and the category page lists it — otherwise it is an orphan.

### 15.4 Organic-traffic mechanics that are actually in our control

- **One site, one index surface.** 20 canonical URLs, one sitemap, one feed, `robots.txt` declaring
  it. Any new guide must be added to all three in the same commit or the gate fails.
- **Question-shaped titles and H1s**, matching how the query is typed. The eleven live guides already
  do this; the front page should borrow the shape rather than listing sections.
- **Internal links with descriptive anchors** ("capacity checklist", not "read more") — the cheapest
  ranking and retention lever available and entirely within the rails.
- **Freshness a reader can see**: a dated "last checked" line per guide, which is honest because the
  register genuinely records the date.
- **Search Console is the missing instrument** (blocked, owner-gated). Until it is connected, no
  claim about queries, impressions or rankings may appear anywhere on the site.

### 15.5 What to stop doing on the front page

- Stop leading with the verification method. Lead with the five products, then one line on how they
  were chosen, then the door to the research.
- Stop equal-weighting the nine dashboard surfaces. Footer, one navigation group, as the brief says.
- Stop describing the disclosure twice in the same viewport; once above the fold, once in the footer,
  exactly as the rail requires — not a third time in body copy.
- Stop any visual that implies a hands-on test we did not run (R7). Illustrations labelled as
  illustrations are the only imagery permitted (R9).

### 15.6 The decision gate stays in front of all of this

Every item above is a proposal. It goes live only after the owner picks a path on
[`suggestions/index.html`](https://kanlerxz87-cyber.github.io/Zone3/suggestions/index.html), where each
carries its answer owner and a safe default. The specific blockers a designer will hit on day one:
brand name and promise (Q1/D34-Q1), the authorized dimension source (E41-P1/Q1), imagery licensing
(S-18), and whether a human editor exists at all (editor/cadence question). A comp that assumes those
are settled is not a design, it is a guess wearing a typeface.
