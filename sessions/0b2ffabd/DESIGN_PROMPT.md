# DESIGN_PROMPT — the brief a design pass is run from

> **Integration addendum (2026-11-19, session `ee10b024`, PR #160 re-land).** This is session `0b2ffabd`'s 2026-11-17 draft, archived unchanged except that three source ids were re-pointed to the merged register: S91→S95 (Search Console snippet guidance), S92→S96 (sitemaps), S93→S97 (search updates) — later sessions had already claimed S91–S94 on `main`. Its S90 citation (qualify-outbound-links) is identical to main's S90 row. The repository root's `DESIGN_PROMPT.md` is now session `6b68afc8`'s 2026-11-19 rails brief; this draft remains here as the record of what PR #160 proposed.


**Status:** draft, for review. **Assembled:** 2026-11-17 by session `0b2ffabd`.
**Applies to:** the reader-facing surfaces of <https://kanlerxz87-cyber.github.io/Zone3/> — today that is six
surfaces (`site/`, `read/`, `shop/`, `marketing/`, `guides/`, `articles/`) plus the root publication front page.
**Not implemented by this document.** Nothing here changes a live page. It is the prompt a later session is
handed, and the checklist the owner marks up first.

**Where each rule comes from.** Source IDs `S01`–`S97` are rows in `data/sources.json` naming the official page
and the date it was read (the register runs to S97 with gaps, because ids are reserved by the session that reads
the page — see flag `G0B2-F-10` for how this brief's own citations were re-pointed onto existing rows when three
sessions read the same documents on the same day); `PF-nn` rows are verbatim clause quotes in `data/policy_facts.json`. The six clauses
this brief leans on hardest (PF-57…PF-62) were read from the live Program Policies page on 2026-11-17. Every
number quoted below was measured in this repository on 2026-11-17 with the commands recorded in
`sessions/0b2ffabd/repo-review.md`. **If a future edit to this file drops a source ID, it has become marketing
copy, which is the thing this project exists to avoid.**

---

## 0. How to use this file

1. Answer the eight rows of the decision-readiness ledger on `suggestions.html` (most are one word). The
   register is `data/suggestions.json → review_2026_11_17b`; the console is `decision-queue.html`.
2. Mark this file up: keep / cut / reword, per section. A design session implements the marked-up version and
   nothing else.
3. Q12 first. It picks the surface this brief is applied to; the polish must not be written six times.
4. Then the look (sections 2–5), then the cadence (section 6), then measurement (section 7).

---

## 1. The one-sentence brief

> Make it read like a shop that happens to keep receipts — not like a lab that occasionally sells things.
> The product and the buyer's question are above the fold; the verification is one click away and never above it.

**Measured on** `main@2868a3a` plus this pass — the numbers below are the merged tree, re-run after the rebase,
not the ones this file was drafted against; the difference is recorded so nobody has to guess which is which.
The register now holds **five** products (three air fryers P1–P3, two meat thermometers P4–P5 whose intended
identity is still unconfirmed), so "the three listings" in the existing copy is a wording debt, not a rule.

**Why this phrasing.** The site already has the receipts (136 HTML pages outside `docs/` and `archive/`, 86 source rows,
121 flagged items, disclosure above the fold on every page). What it does not yet have is a shelf. The
differentiator available to it is not enthusiasm — with no API feed and no first-hand testing there is no legal
adjective to reach for — it is dated, sourced specificity, which is also the only thing a competitor cannot copy
without doing the work.

---

## 2. Rails (hard constraints; the build fails if they move)

| # | Constraint | The rule | Effect on the design |
|---|---|---|---|
| R1 | Disclosure wording and position are fixed | "You must clearly and prominently state … *As an Amazon Associate I earn from qualifying purchases.*" — Operating Agreement §5; a §5 breach "will be deemed a material breach" (S79, PF-01) | Restyle the strip; never move, shrink or drop it. Strip under the masthead on every page, repeated in the footer (already true). FTC: place it so it is "hard to miss" and "with the endorsement message itself"; a disclosure on an ABOUT page or behind a MORE click is "likely to be missed" (S07) |
| R2 | No price, availability, star rating or review count | A site may show prices/availability only if Amazon serves the link or the data comes from Creators/PA API (2(b), S80, PF-04/44/54); reviews and star ratings likewise only via API (6(t), PF-05/45) | No price chip, no strikethrough "was" price, no star row, no review count — in the body, the table, the meta description or the preview image. The layout must look confident without them |
| R3 | No urgency module without an owner | "You must remove from your Site any links and related references to limited time promotions as soon as that promotion on the relevant Amazon Site ends." (2(b), S80, PF-61) | No countdown, no "deal ends soon", no seasonal discount banner, until a named owner plus a dated re-check exists. This is a maintenance rule, and it is why the site's badge is a *checked date* instead |
| R4 | Comparison = features, not prices | Displaying prices "in any *comparison* format … together with prices for the same or similar products offered through any web site … other than an Amazon Site" obliges you to show Amazon's lowest new (and, if provided, lowest used) price (2(b), S80, PF-62) | The comparison table stays capacity / dimensions / quoted-claim based. A price column is not a copy edit; it is an obligation the site cannot satisfy |
| R5 | Links stay direct, honest and un-bookmarked | "You must not encourage customers to bookmark your Special Links. All Special Links must be accessed directly from your Site." (2(b), S80, PF-58); no shortening or presentation that "makes it unclear that you are linking to an Amazon Site" (6(w), PF-06); purchases via a "Redirecting Link" are disqualified (CIS 2(e), S30) | Button text names Amazon. No interstitial hop, no "save for later" on a buy link, no clever redirect wrapper. `rel="sponsored"` on every outbound product link — Google: "Mark links that are advertisements or paid placements … with the `sponsored` value" (S90) |
| R6 | A page that links to listings must earn it | "When linking to pages with Product lists you must have additional original content on your Site that is relevant to the Special Link." (2(b), S80, PF-60); enrolment-side: original content required, and third-party material needs "significant commentary, analysis, or transformation" (PF-15) | A card grid is not a landing page. Every surface that links to Amazon carries analysis the listing does not provide: the dated observation, the capacity maths, the counter-space trade-off, the category-tree fact |
| R7 | Measurement is aggregate | "Under no circumstances may you associate any sub-tag, other ID or reporting provided in connection with the Associates Program with a specific end user of your Site (e.g., you may not dynamically assign sub-tags to users as they arrive on your Site for purposes of monitoring such users' behavior)." (2(b), S80, PF-59) | Per-page and per-date counts are buildable; per-visitor journeys, dynamic sub-tagging and user-level joins to Associates reports are not. Segment by page, guide and date — never by person |
| R8 | No artificial traffic | "You will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site, whether by way of a robot or software program or otherwise." (6(s), PF-33) | No self-pinging prefetch of buy links, no click-bait auto-navigation, no synthetic "activity" |
| R9 | Imagery is our own, or there is none | Program Content (which includes the listing's images and text) is Amazon's; this repository's gate `verify_site` V6 fails any `<img>` whose `src` is an Amazon asset or CDN host. Photography of the real products is S-18, recorded as "needs a decision first" | Typographic cards, diagrams, and the three illustrations already in `assets/img/` (each figure states "Illustration: our own"). No stock, no Amazon assets, no generated photograph of a product, no copied press shot |
| R10 | Nothing about experience, until someone has any | FTC: "You can't talk about your experience with a product you haven't tried." (S07); S-06 recorded as "not adopted" | No "we tested it", no invented persona byline, no "our experts". The byline says what it is: an agent desk with a dated source list, until Q5 names a human |
| R11 | No invented market data | No official Amazon affiliate endpoint for trend rank, conversion rate or competition density exists (recorded in `tools/link_report.py --strict`); the site's own evidence rule requires a dated first-party snapshot for any "trending" claim (S-16, adopted) | "Best", "top-rated", "most popular", "trending", "selling fast" are unavailable words, in headlines, badges, alt text and meta descriptions alike |
| R12 | Site content must not be child-directed, and must not use Amazon marks in identifiers | Participation Requirements suitability clauses read 2026-11-17: content must not be "directed toward children or knowingly collect … personal information from children under 13", and must not include an Amazon trademark "in any domain name, subdomain name, in any 'tag' or Associates ID, or in any username, group name, or other identifier on any social networking site" (S80) | Brand naming stays clear of "Amazon", "Prime" and similar marks in the site name, handle, tag and social handles. Audience is adults buying kitchen appliances; no kids'-snack framing |

**On the meta description specifically.** Google invites a price into a product page's description ("product
pages might have the key bits of information—price, age, manufacturer—scattered throughout a page. A good meta
description can bring all this data together", S95). R2 forbids us to display one. The recorded resolution is
**specificity without price**: describe what the page checked and when, e.g. *"Three air-fryer listings read on
17 Nov 2026 — the ASIN each short link opened, the title as served, and what is still unconfirmed."* That
satisfies Google's "unique descriptions for each page" rule without touching R2 (flag `G0B2-F-07`).

---

## 3. Layout: the shelf, not the audit

1. **Masthead.** Wordmark, one-line promise, a navigation group of six items maximum. Disclosure strip directly
   beneath it, full width, contrast-checked.
2. **Front page shelf.** Five product cards — three air fryers, two thermometers labelled *outside the
   air-fryer guides* until Q16 is answered. Each card: the listing title exactly as served, the observed ASIN
   with its date, one "fits you if / not for you if" pair generated **only** from quoted listing features (the
   reader lint already refuses any other sentence), and one sponsored button. The three-question chooser
   (S-19/D-23) sits **above** the shelf, and each answer deep-links to the comparison row it affects.
3. **Guides desk.** Question-shaped titles, a dated byline block, and a "what changed since this was written"
   line only a re-read can produce.
4. **Comparison.** One source cell per row, sticky mobile bar, no price column. The counter-space analysis
   (capacity per centimetre of counter depth) leads; the spec grid follows.
5. **Governance footer.** Every dashboard, register, verification log and flagged page reachable from the footer
   in a single group. Readers never see the audit; auditors never lose the page.
6. **Type.** One display face for the questions, a text face for the answers, a wide measure, generous rhythm.
   The badge style is used exactly once per card ("Checked 17 Nov 2026 — from the listing") and links to the
   dated source row.

---

## 4. Components that are allowed, and what each one may say

| Component | Allowed content | Forbidden, by rule |
|---|---|---|
| Product card | Title as served; observed ASIN; date; quoted feature phrases; sponsored link | Price, rating, review count (R2); "best value" (R11) |
| Checked-date chip | Date, "from the listing", link to the source register row | Anything implying testing (R10) |
| Feature comparison row | The claim, quoted; which listing it came from; what the listing does not say | Non-Amazon prices (R4); derived scores presented as data |
| Capacity/clearance diagram | Our own arithmetic on listed dimensions, shown as arithmetic | Rounded-up marketing numbers |
| Guide header | Question as title; date; desk byline; source count | "Popular", "trending", "most asked" (R11) |
| Social card | The question, the site name, the checked date | Product imagery (R9); price (R2) |
| Newsletter/lead capture | Only if it exists: what it sends and how often | A form with no stated owner; any per-user tagging (R7) |
| Deal banner / countdown | — | R3, until an owner and a dated check exist |

---

## 5. Head block (identical shape on all six surfaces)

Per page, in this order: `<title>` (unique), `<meta name="description">` (unique, no price — R2), `link
rel=canonical`, `og:title` / `og:description` / `og:image` (own artwork only, R9), `twitter:card`, one
JSON-LD block of `Article` + `BreadcrumbList`. `feed.xml` and `sitemap.xml` stay register-generated.

**Measured today, so a pass can be verified rather than admired:** canonical on 102 of 136 pages; `og:image` and
JSON-LD on 11 of 136 (all in `read/`, nowhere else); 0 missing titles and 0 missing or sub-60-character
descriptions across the 50 root + `site/` + `guides/` pages checked (four share the title "Moved" — the
redirect stubs); `sitemap.xml` 101 URLs with 0 `<lastmod>` and 0
`<priority>`/`<changefreq>`; `404.html` in the sitemap. Google: "Include the URLs in your sitemap that you want
to see in Google's search results", "`<lastmod>` … [used] if it's consistently and verifiably … accurate", and
"Google ignores `<priority>` and `<changefreq>` values" (S96). So: lastmod from the file's git date, not from the
build clock; `404.html` and the meta-refresh stubs out of the published URL set; the omitting of
priority/changefreq is already correct.

**Do not add `FAQPage` markup.** The FAQ rich-result documentation is gone: as of 2026-11-17 the
`…/structured-data/faqpage` URL serves Google's "What's new" page at the June 2026 entry "Removing documentation
for the FAQ rich result feature" (S97). The question-shaped guides stay, because readers type questions — not for
a rich result that no longer exists.

---

## 6. Content: what can be published, and what is held

Cadence (proposed, not adopted): **one guide a week**, each one register-driven so the feed and sitemap follow
automatically. Titles stay question-shaped; the four editorial hypotheses in the owner brief are all published
already. Working titles for the next tranche — **hypotheses about what a buyer asks, not claims about volume**:

1. "Basket or oven-style air fryer: what should you compare?" *(published)*
2. "A no-hype checklist for comparing air fryer capacity" *(published)*
3. "How to assess cleanup and counter-space trade-offs" *(published)*
4. "Questions to ask before buying a multi-function kitchen appliance" *(published)*
5. "How do you know when an air-fryer cook is actually done?" — buildable now: the CHEF iQ listing's own title
   names "Air Fryer" among its uses (the listing read, S73; the submitted link that opens it, S71), and both
   thermometer listings are filed under Kitchen Utensils & Gadgets › Thermometers & Timers › Meat (S72, S73).
   That is the only bridge available; anything beyond it is
   invention. Held until Q16 decides whether thermometers are in scope.
6. "What does 'quart' mean on an air fryer, and what does the number not tell you?" — buildable now from the
   listings already captured (S08–S10 family) and the counter-space method.
7. "What '4-in-1' and '24 presets' count, listing by listing" — partially published in `site/guides/what-four-in-
   one-means.html`; the follow-up needs nothing new.
8. "Is a dual-basket air fryer two small fryers or one big one?" — buildable from the 6 Qt dual-basket listing.
9. *Held:* the "best value" piece and every comparison that wants a price → needs Q4 (API access).
10. *Held:* "what it's like to live with" → needs Q6 (someone actually lives with it). Do not soften these to
    ship them; that is the difference between a shop and a content farm, and it is policy-visible (R10, R2).

Seasonal framing is allowed as **dated context, not as a claim**: "November, turkey season, and a 26 QT oven-style
unit: what the listing says it fits" is fine; "everyone's buying this for the holidays" is not (R11), and any
promotion reference inherits R3's removal duty.

---

## 7. Measurement loop (the part that decides the next topic)

Today: no clicks, no conversions, no Search Console property in this repository's records; the campaign ledger is
empty **by design**, with each column naming the authorized first-party report its value must come from, and no
forecast anywhere. The order that stays inside R7 and works on a static host:

1. **Search Console** — create a **URL-prefix property for `https://kanlerxz87-cyber.github.io/Zone3/`** and
   submit `sitemap.xml`. A domain property is not verifiable for a project page under someone else's apex, so the
   property type is fixed by the host, not chosen (S96). This is the only input that picks a topic from real
   queries without inventing a search-volume number.
2. **Aggregate outbound counter** — per page, per date, first-party, no cookies, no identifiers (SUG-13). GitHub
   Pages serves static files: an endpoint needs somewhere else to run, which is Q15's answer, not this brief's.
3. **Associates reports** — clicks, eligible sessions and orders enter the ledger only from the account's own
   reports, dated, with the source named.
4. **The five events** the owner brief asks to record stay undefined in this repository's records — the gap is
   flagged (AE-F-04/05), not filled in. Writing them down is an owner line, and until it exists no counter is
   built "for them".

---

## 8. Definition of done, for whoever implements a path

- Every gate green in the chain order documented in `README.md` (that list, not a remembered one — it grew on
  2026-11-17 to include `tools/build_measurement.py`, `tools/build_brief_status.py`, `scripts/build_marketing.py`,
  `scripts/build_read.py`, `scripts/build_5a56c084.py`, `tools/build_site.py` and `tools/measure_pass.py`), and
  **run the whole chain twice**: the layer generators rewrite pages that the publish, measure and front-door
  passes post-process, so a single pass leaves ~30 pages without their injected `z3:css` / `z3:rss` / `z3:strip`
  / `z3:measure` blocks. Converged means the second run changes nothing.
- Then the checks: `scripts/check_site.py`, `tools/verify_site.py`, `tools/link_report.py --strict`,
  `tools/i2_gate.py`, `tools/cba81fa5_lint.py`, each generator's own `--check`,
  `scripts/check_all_links.py`, `scripts/cba81fa5_test_no_repr_output.py`,
  `tools/analytics_endpoint.py --self-test`, `sessions/aebf0747/audit.py` and `link_check.py`.
- Re-measure the section 5 numbers and put both readings in the flag register (`G0B2-F-06`, D13). "Polished" has
  to be a number that moved, not a sentence in a changelog.
- No page loses its disclosure, its sponsored rel, or its source row. No new file contains a price, a rating, a
  review count or a popularity claim.
- The path not chosen is not deleted: the archive rule stands.

---

## 9. What this brief deliberately does not do

It does not pick a layer, a name or a colour — those are Q12/Q7-family answers, and the register ships with the
gaps visible on purpose: a site that shows which cell is empty and why is the only version of this project whose
filled cells mean something. It does not add photography, prices or "trending" while their sources are missing.
And it does not implement anything: the design paths, the four new proposals (SUG-11…SUG-14) and the eight
decision rows are published on `suggestions.html` for the owner to choose from first.

## 10. How this brief relates to the other two design artifacts on the same page

Two other documents propose design direction, and a design session should read all three, because they cover
different halves:

| Artifact | What it holds | What it does not hold |
|---|---|---|
| `data/design-brief.json` → `design-brief.html` (session `757efebc`, 2026-11-16) | the six-prompt pack and the visual system: palette, type, spacing, the "field notes" register | the official clause behind each rule; it also still describes three products and one surface |
| `review_2026_11_17_late` on `suggestions.html` (session `73029680`) | exact **replacement lines** for that prompt pack (`DP-P-01`… — five products, five surfaces), the OPM-dated seasonal hooks, and the decision runbook that orders Q1–Q12 by what unblocks what | the rails: no rule is quoted from a policy page there, so it cannot be used to decide whether a design idea is allowed |
| this file | the rails (R1–R12), each quoting the clause and its source row, the component table, the head-block spec with the measured numbers, and a definition of done that matches the gates as they now run | any choice, any copy, any colour — and it is not itself a register row, so it changes nothing when read |

Where they disagree, the rails win, because they are the ones with a source: `DP-P-01`'s "five registered
products" is the correct count and this file has already adopted it; the seasonal hooks in the late review are
usable as editorial moments but not as urgency copy, which is what R3 forbids until a named owner re-checks a
promotion. Measurement is a solved problem waiting on a host, not a design question:
`tools/analytics_endpoint.py`, `assets/measure.js` and `site/measure.html` already implement the aggregate-only
counter this brief's R7 describes (five event names proposed, counting off until `endpoint_url` is set,
`M38-F-04` in `data/shop/flags.json` asking the owner to confirm them) — a redesign must reuse that and add
nothing that identifies a visitor.
