# Decision record — session `3d0d7bd1`, 2026-11-19 (branch `arena/3d0d7bd1-zone3`)

This file is the decision record that the proposal cards and the style page link to. Each record
below follows the intake shape published on the suggestions page: what a reader would see · why
now · which register questions it touches · official basis · safe default · gate status. Nothing
here was decided without reading the register row it changes, and nothing here was implemented
before the decision was written down.

The register edits this session made (`data/publication.json`): new `house_style` block;
`meta.review_cadence_days`; `style.html` added to `indexable_pages`; status + `outcome` on
B38-P1/P4/P5 and E41-P2; a dated `update` on decision row DS-03; one new decision-readiness
question D3B-Q1. No product, source, flag, feed or measurement row was touched.

---

## DEC-3D0D-01 · Adopt B38-P1 — publish the house style and enforce it with a banned-phrase lint

**What a reader sees.** A reader-facing page, `style.html`, that states the six voice rules and
every banned construction with the reason and the official basis; a footer link ("How we write")
and a link from the about page; and a release chain that fails when a banned construction reaches
a strict-scope page.

**Why now.** B38-P1 was priority "Now", `owner_input_needed: false`, and unimplemented. The voice
decision (S-12, 2026-11-16) and the design brief's copy rules (§7) already existed; what was
missing was a published page and mechanical enforcement. This is also the brief's standing
requirement that the site must not read like generated filler.

**Register questions touched.** D3B-Q1 (new, raised by this change: who may edit the list).
E61-Q8 (decision recording) is served by this file. No owner-gated question is needed to run the
lint on the words the site itself writes.

**Official basis.** Google's helpful-content self-assessment (original information, no
exaggeration) — register source `google-helpful`; Google's review guidance (evidence for claims)
— `google-reviews`; FTC *Disclosures 101* (no experience claims without experience) — `ftc`;
Amazon Program Policies and Operating Agreement (no invented urgency, no unheld numbers) —
`amazon-policies`, `amazon-agreement`. The rules and bans in `house_style` each name one of these.

**Discovery performed before adoption (B38-P1's own two required discoveries).**

1. *Which phrases the published guides already avoid.* Command run against the freshly built
   tree on 2026-11-19: a regex scan of the visible text of all 20 current reader pages
   (`build_publication.outputs()`, excluding `publication-prior.html`) against the proposed
   union of the design brief §7 banned list and the `/site/` layer's HYPE/TREND patterns.
   Result: **no buyer-facing page contained a banned construction used as a claim.** All 19
   hits were one of: the front-page hero and about page using a banned token *to reject the
   trope* ("You don't need another 'must-have'"), the about page's compliance sentence
   *declining* a trending claim, and the suggestions page quoting the ban list inside proposal
   text that documents it.

2. *Whether any existing sentence fails the proposed ban list.* Two sentences did, both
   meta-usages, both rewritten rather than exempted, because the style should apply to the site
   that publishes it:
   - `index.html` hero: before `You don’t need another “must-have”.` → after `You don’t need
     another breathless list.`
   - `about.html`: before `…more useful than another must-have list.` → after `…more useful than
     another breathless list.`
   One sentence was exempted instead, because its job is to quote the rule it applies:
   about.html's `Search demand, trending status, conversions and revenue are unverified.` is
   wrapped in `data-lint="quote"` — it *declines* a trending claim; it does not make one. The
   suggestions page is relaxed as a page because the decision register quotes Google's own
   warning wording and the banned list when reviewing them; the same relaxation exists on the
   `/site/` layer for its style-guide page.

**Safe default if nobody answers.** Not applicable — implemented. The D3B-Q1 default holds:
the list grows when shipped copy would have failed it; removals need a dated, recorded decision.

**Gate status.** `tools/check_publication.py` carries the lint (compiles `house_style.banned`
patterns, strips the documented exemptions, fails the release with page, pattern id and context)
and the figure/claim scan now honours the same exemptions. Verified: the full chain passes with
the list adopted (see `verification-2026-11-19.md`).

---

## DEC-3D0D-02 · Adopt B38-P4 — publish the next review date, and close the proposal→decision loop

**What a reader sees.** On the suggestions page, a decision-loop strip: "Next review due 3 Dec
2026 — derived from the edition date (19 Nov 2026) plus the register's 14-day review cadence,
never typed", with an explicit overdue state; and on every decided proposal card, an Outcome
line naming its dated record.

**Why now.** B38-P4 was priority "Next", `owner_input_needed: false`, and unimplemented; the
register told a reviewer what was open but not when the next review was due or what happened to
earlier choices.

**Register questions touched.** E61-Q1 (what defines success and when it is reviewed) — the
derived due date gives that question its missing review date; E61-Q8 (who signs off changes and
where they are recorded) — outcome lines point at this file.

**Official basis.** Google Search Console "get started" guidance (`search-console` source row in
the register) for the review rhythm; the cadence promise itself is published site copy
("Review one guide every 14 days") and now has a register-owned number
(`meta.review_cadence_days = 14`) that the gate ties to that sentence.

**Determinism decision.** The overdue state compares two register dates (`reverified` vs
`updated` + cadence), never the wall clock, so builds stay byte-identical — the definition of
done requires two runs to change nothing. A gate fails the release when the register's latest
recorded activity moves past the due date without a new edition: an overdue review is stated,
not silently stale.

**Safe default.** Implemented. If a future session bumps `reverified` past the due date, the
gate stops the release until a new edition is published or the slip is recorded.

**Gate status.** Two new checks in `tools/check_publication.py` (cadence consistency +
overdue; outcome format `^(Adopted|Closed|Rejected|Superseded) DATE` naming `sessions/`).

---

## DEC-3D0D-03 · Adopt B38-P5 — correct decision row DS-03 before any FAQ work starts

**What a reader sees.** On the suggestions page's answers worksheet, DS-03 carries a dated
correction line under its original wording (the original row is kept verbatim — a record written
on a date is that date's truth).

**Why now.** B38-P5 was priority "Now", `owner_input_needed: false`. DS-03 still offered
"Add FAQPage structured data to a guide" without noting that the premise (a Google rich result)
no longer exists.

**Verification performed today (2026-11-19), from the official page.** Read
`https://developers.google.com/search/updates` fresh, and read the two entries in the body of
the page:

- Under **May 2026 → May 8**, "Deprecating the FAQ rich result feature": "**What**: Added a
  deprecation notice to the FAQ rich result documentation. **Why**: This feature will no longer
  appear in Google Search starting May 7, 2026." (anchor `#faq-deprecation`).
- Under **June 2026**, "Removing documentation for the FAQ rich result feature": "**What**:
  Removed documentation for the FAQ rich result feature. **Why**: The FAQ rich result feature is
  no longer shown in Google Search results, as announced in the changelog entry in May 2026."
  (entry sits between the June 15 and June 12 entries; dated June 2026).

B38-P5's register claim ("deprecated May 7, 2026; documentation removed June 2026") is therefore
confirmed against the official source; the register source row `google-faq-update`
(`developers.google.com/search/updates`) was already dated 2026-11-19 with this scope.

**What changed.** `review_b9008684.decision_rows[DS-03]` gained
`update: {on: 2026-11-19, by: session 3d0d7bd1 (proposal B38-P5), text: …, anchors:
[https://developers.google.com/search/updates#faq-deprecation]}`; the renderer shows the
correction under the row. The sourced-answer requirement (D9-03) is unchanged: FAQ blocks are
decided on reader utility alone, and if FAQPage markup is ever shipped, the decision must name
the non-Google consumer it serves.

**Gate status.** A check pins the correction: DS-03 must keep its `update` dated 2026-11-19
containing "May 7, 2026" and the `faq-deprecation` anchor.

---

## DEC-3D0D-04 · Close E41-P2's measured half — sticky column kept, floating bar stays with E41-Q2

**What a reader sees.** No change on the page; the compare table keeps the sticky product column
and the scroll note that the measurement already validated.

**Why now.** E41-P2's recorded next action was: "Read the 2026-11-19 measurement record in
sessions/41e84402/, then either shortlist a floating compare bar or close the row as done with
the sticky column."

**What the record says** (`sessions/41e84402/measurement-2026-11-19.json` +
`verification-2026-11-19.md`, produced by session 41e84402's browser pass): at 320/390/768 px
the sticky product column holds its left edge (`left_before == left_after_scroll == 16px` at
320/390) while the scroll region moves 160 px sideways; the table needs no sideways scroll at
768 px; the chooser renders above the comparison at all three widths; interactive targets under
24 px went from 4 to 0 of 26 (14 of 26 remain under 44 px, all inline text links, which WCAG
2.5.8 excepts).

**Decision.** The sticky column plus scroll note is the closed outcome of the measured pass; a
floating compare bar would add a second scroll region and can cover content, and E41-Q2
explicitly reserves that choice for the owner with device-mix evidence (E61-Q5) that does not
exist. So the row is closed as: measured pass complete, sticky column retained, floating-bar
option left open under E41-Q2 — not guessed into existence.

**Safe default.** Keep the sticky column and the scroll note; do not add a floating bar until a
reader need is observed (E41-Q2's recorded default).

**Gate status.** E41-P2 status → "Closed 2026-11-19 — measured half done" with outcome; E41-Q2
stays open, owner-input.

---

## New register question raised by this work

**D3B-Q1 — Who may add a phrase to, or remove one from, the house-style banned list, and on what
evidence?** Known: the list shipped 2026-11-19 with B38-P1, register-driven and gate-enforced.
Missing: the editing rule. Discovery: record every proposed addition with the page and sentence
that prompted it; removals go through a dated decision record like this one. Default: the list
grows when shipped copy would have failed it; removals need a dated, recorded decision; nothing
is scheduled for removal. Owner-input: yes. Basis: `google-helpful`.

---

## What this session did *not* do

- No price, rating, review count, test result, demand or popularity value was added anywhere.
- No Amazon product photograph, API call, account action or network call to any retailer was made.
- The campaign ledger stays empty; measurement stays off in production; no tracking change.
- No historical record was rewritten: DS-03 keeps its original row verbatim, with a dated
  correction beneath it; prior sessions' coordination parts are untouched.

---

## Merge note — parallel sessions, reconciled before the PR (2026-11-19)

While this batch was in flight, PRs #199–#206 merged into `main`. Two of them touched the same
proposal this batch implements, and the reconciliation is part of the decision record:

- **Session 6f16ee11 shipped its own anti-slop gate** — a hard-coded STYLE:hype/STYLE:trend scan
  in `tools/check_publication.py` with a quote-mention exemption — an independent implementation
  of the same B38-P1 intent, referencing the `/site/` layer's style guide. The merged release
  chain now runs **both** linters: the register-driven one (this session's, which the style page
  renders from) and 6f16ee11's hard-coded corroboration (which a register edit cannot silently
  weaken). Both scan the same stripped text view, so the style page's phrase cells and
  `data-lint="quote"` elements are exempt under both. 6f16ee11's "popularity status" rewording
  of the about-page compliance sentence was adopted over this session's quoted-token exemption,
  because removing the token is better than exempting it.
- **Session 0a48cfda captured exterior dimensions for the five listings** from the official
  detail tables and rewrote the cleanup guide around them. Merged additively into the register
  alongside this session's decisions; the product cards and comparison table keep their new
  "Listed size" column, and E41-P1/E41-Q1 stay in their upstream (more complete) form. This
  changes nothing in DEC-3D0D-04: the floating-bar question remains E41-Q2's, and the
  counter-space analysis remains blocked on interior dimensions and the capacity-wording
  disagreement the upstream session flagged.
- **Session 4b0e3c7e (PR #203 and follow-ups) added Associates-tagged buy buttons**: the card
  CTA now points at the observed product page with `?tag=shopnow047c-20` (Program Policies
  2(b)), the supplied short links stay on the card as the observed record only, and the release
  chain grew to 44 commands with tag gates. Merged as-is on top of this session's card markup;
  it changes nothing in the decisions above, and the attribution questions (P26-Q2, P27-Q6,
  FLG-003) remain exactly as open as they were.
