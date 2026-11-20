# Verification record — session `2e0d5c15`, 2026-11-20

Branch `arena/2e0d5c15-zone3`. Measured on the merged tree at **`main@957e5ab`** (PRs #212–#215),
after rebasing this branch three times during the session as other sessions landed work. Every number
below was measured on this checkout; nothing is copied from another session's record without saying so.

**What this pass is.** A register-integrity and rendering-integrity audit. It changes no product fact,
no price, no rating, no destination and no tracking ID. It corrects four status cells whose last
sentence disagreed with the registers, fixes two generator bugs that were dropping a word from two
rendered sentences, and adds four reviewable items (two proposals, two questions) plus two flag rows
to the decision desk.

---

## 1. Official sources re-read in this session

Read with a page fetch on **2026-11-20**. Quotes are verbatim from the page as served that day.

| # | Page | What was checked | Verbatim |
|---|---|---|---|
| V1 | FoodSafety.gov — *Cook to a Safe Minimum Internal Temperature* <br>https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | The page's own review date and the reheat figures a reader would use | "Date Last Reviewed **November 21, 2024**"; Leftovers, any type — **165°F (74°C)**; Casseroles — 165°F (74°C); Precooked ham (to reheat) — 165°F (74°C), "Reheat cooked hams packaged in USDA-inspected plants to 140°F (60°C)"; Chicken, turkey and other poultry — 165°F (74°C); Ground meat and sausage — 160°F (71°C); Beef, bison, veal, goat and lamb steaks, roasts, chops — 145°F (63°C) "Rest time: 3 minutes" |
| V2 | USDA FSIS — *Leftovers and Food Safety* <br>https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety | The reheat rule and the danger-zone rule behind proposal 2E0-P1 | "When reheating leftovers, be sure they reach 165° F as measured with a food thermometer." · "Bacteria grow rapidly between the temperatures of 40° F and 140° F." · "Within 2 hours of cooking food or after it is removed from an appliance keeping it warm, leftovers must be refrigerated." · "Leftovers can be kept in the refrigerator for 3 to 4 days or frozen for 3 to 4 months." · page footer: "Last Updated: Jul 31, 2020" |
| V3 | USDA FSIS — *Food Thermometers* <br>https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers | Placement and accuracy statements used by the existing guides | "The food thermometer should be placed in the thickest part of the food, away from bone, fat or gristle." · "Most food thermometers will give an accurate reading within 2 to 4 degrees F" · "Color is Not a Reliable Indicator that Food is Safe" · "Always check each piece of food" |
| V4 | Amazon Associates — *Associates Program Policies* <br>https://affiliate-program.amazon.com/help/operating/policies | Page version header, the Qualifying Purchase definition, and the Redirecting Link definition that FLG-003 turns on | Header: "**Updated:** April 14, 2026." · Commission Income Statement §1(a)–(b): a Qualifying Purchase begins when "a customer clicks through a Special Link on your Site", with the Session measured from that click. · §2(e): "any Product purchased by a customer who is referred to an Amazon Site by a link that sends users indirectly to an Amazon Site via an intermediate site, without requiring the customer to click on a link or take some other affirmative action on that intermediate site (a **Redirecting Link**)" |
| V5 | Google Search Central — *Breadcrumb (`BreadcrumbList`) structured data* <br>https://developers.google.com/search/docs/appearance/structured-data/breadcrumb | The basis for proposal 2E0-P2 | "A breadcrumb trail on a page indicates the page's position in the site hierarchy…" · validate with the Rich Results Test and "fix any critical errors" |

**Scope limit, stated plainly.** This pass did **not** re-read the Operating Agreement §5, the FTC
*Disclosures 101* guide, or the GitHub Pages limits page. Those were re-read earlier the same day by
session `fc812c5e` (`sessions/fc812c5e/verification-2026-11-20.md`) and on 2026-11-19 by the sessions
that record them. The disclosure sentence, the sponsored `rel` and the index policy were re-checked
**in the built tree**, not re-quoted from those pages.

**What V4 does and does not settle.** §2(e) disqualifies purchases made through Redirecting Links —
links that send a user to Amazon indirectly without the customer taking an action on the intermediate
site. Whether the owner-supplied `link.amazon/…` URLs operate that way for this account is an
account-level question no public page answers. FLG-003 therefore stays open; nothing in this pass
changed a destination or an intent field.

---

## 2. Measurements on this tree (`main@957e5ab` + this pass)

| Measured | Command / method | Result |
|---|---|---|
| Published HTML pages (excl. `archive/`, `docs/`, `sessions/`) | tree walk | 131 |
| Indexable reader URLs / sitemap `<loc>` entries | `data/publication.json → indexable_pages`, `sitemap.xml` | 27 / 27 — identical sets |
| RSS items | `feed.xml` | 13, all sitemap-canonical |
| Question-led guides / research-desk articles | `guides/*.html` minus index, `articles/*.html` minus index | 13 / 4 |
| Guides linking the comparison table **in their own body** (footer stripped) | per-file check | 13 of 13 |
| Disclosure sentence present | grep across published pages | 131 of 131 |
| `og:image` and JSON-LD | per-file check | 40 pages carry both; all 27 indexable pages carry both |
| Official-source table rows | `tools/check_publication.py` banner | 139 |
| Flag rows / proposals / questions / paths / sources | registers | 187 / 37 / 46 / 6 / 17 |
| In-page `#fragment` links resolving to a declared id | `sessions/2e0d5c15/fragment_audit.py` | **1,248 checked, 0 broken** |
| External and internal URL links | `scripts/check_all_links.py` | 213 pages, 356 distinct external URLs, **0 errors** |
| HTML nesting | `sessions/2e0d5c15/nesting_audit.py` | 131 pages checked; **6 reported before this pass, 4 after** |
| Release gate | `python3 tools/publish.py` | **51 of 51 PASS**; a second `--check` run left the tree unchanged |

Two of the six nesting reports were not nesting accidents but unescaped prose: the literal strings
`<token>` (`data/articles.json`, rendered by `scripts/build_5a56c084.py`) and `<short-id>`
(`tools/build_site.py`) were written into HTML, so a browser read each as an unknown element and the
word disappeared from the sentence. Both were fixed **in the generators**, not by hand, and the gate
re-ran green.

The four that remain are unclosed inline elements inside list and table cells on `category/kitchen.html`,
`site/flagged.html`, `site/guides/air-fryer-oven-vs-basket.html` and `site/guides/index.html`. All four
are `noindex,follow`, outside the sitemap and the feed, and written by older generators owned by finished
passes. They are published for review (flag `2E0-F02`, question `2E0-Q2`), not hand-edited, because the
next build would overwrite a hand edit.

**One published file carried merge debris.** `COORDINATION.md` on `main@957e5ab` held the line
`>>>>>>> c126257 (D3B-T1: …)` at line 9837 with no matching `<<<<<<<` or `=======` — the tail of a
conflict resolution committed without deleting the marker, on the file every parallel session reads
before claiming work. A scan of the published tree on that commit found it as the only occurrence; it
was removed here and recorded as flag `2E0-F03`, with question `2E0-Q3` asking whether the release gate
should refuse that class of debris. Both sessions' surrounding Parts are untouched.

---

## 3. Register corrections (flag `2E0-F01`)

Flag `EE-F-02` records the 2026-11-19 integration as having re-measured rows S-04, S-05, S-09, S-24,
SG-28 and SG-29 and fixed them in place. Read against the registers on 2026-11-20, four cells still
**closed** on a figure the registers do not hold, and two of them contradicted an earlier sentence
inside the same cell:

| Row | Its last sentence said | Register held at the start of this pass | Register holds on the merged tree | Fix applied |
|---|---|---|---|---|
| S-07 | "ten question-led guides" | 11 | 13 | dated correction appended |
| S-13 | "nine question-shaped guides" | 11 | 13 | dated correction appended |
| S-24 | "every one of the ten published guides links the comparison table" (after stating "all eleven guides" earlier in the same cell) | 11, and 11 of 11 did link it | 13, and 13 of 13 do | dated correction appended |
| SG-29 | "18 URLs on the merged tree" (after stating "20 canonical reader URLs" earlier in the same cell) | 20 | 22 | dated correction appended |

The counts moved again during the session as two guides shipped upstream — which is the finding, not a
complication: a typed count cannot be kept true by hand, it has to be re-measured on a date. No earlier
text was rewritten: each row keeps the record of the tree it was measured on, and a dated sentence names
today's figure and the method. `_meta.rechecks` gained an entry, and `_meta.measured_on` names the
correction. The procedural gap — nothing in the release gate compares a row's final sentence with its
register — is logged as question `2E0-Q1`.

---

## 4. What was added for review, not implemented

| ID | Type | What it asks for | Official basis |
|---|---|---|---|
| `2E0-P1` | Proposal, priority Next | Publish one guide on reheating leftovers in an air fryer, built on the 165°F reheat rule and the two-hour refrigeration rule | V1, V2, V3 |
| `2E0-P2` | Proposal, priority Next | Add `BreadcrumbList` markup to every guide, derived from the trail the page already shows | V5 |
| `2E0-Q1` | Question | Who re-measures the registers at release, and what makes a re-measure line trustworthy | Google: creating helpful content (register row `google-helpful`) |
| `2E0-Q2` | Question | Whether the four remaining malformed pages are kept, repaired or retired — and by whom | Google: page experience (register row `google-page-experience`) |
| `2E0-Q3` | Question | Whether the release gate should refuse a merge-conflict marker anywhere in the published tree | Google: creating helpful content (register row `google-helpful`) |

Choosing any of these on the suggestions page records a local preference only. Nothing in this pass
published a new page, spent money, changed an account, altered a destination or switched measurement on.
`data/shop/measurement.json` remains `enabled: false` with an empty endpoint, and
`data/shop/campaign-ledger.json` still holds zero rows.

---

## 5. Merge handling, so the next session can check it

`main` moved three times while this branch was open (PRs #212, #213, #214, #215). The final rebase onto
`8b32835` conflicted in five files: `data/publication.json`, `COORDINATION.md`, `README.md`,
`executive-brief.html` and `suggestions/index.html`. Resolution, in order:

1. `data/publication.json` — upstream's register was taken whole, then this pass's four entries were
   re-appended programmatically. Nothing upstream wrote was dropped and nothing was hand-typed into the
   file.
2. `executive-brief.html` and `suggestions/index.html` — **generated** pages, so upstream's copies were
   taken and rebuilt from the merged register by `tools/build_publication.py`. Generated HTML was never
   hand-merged.
3. `README.md` — upstream's copy taken; its `z3:register-facts` block is regenerated by the builder.
4. `COORDINATION.md` — upstream's board kept in full and this Part appended, because the board is
   append-only.
5. `data/shop/brief-status.json`, `data/flags.json`, `EXECUTIVE-SUMMARY.md` — this pass rewrote its own
   dated sentences to the counts measured on the merged tree rather than leaving pre-merge figures in
   place.

Gates were re-run after the resolution: 51 of 51 PASS, then `--check` with no drift.

---

## 6. Honest statement of what is still unknown

- Whether the five submitted short links point at the products the owner intended. No official source
  states intent; the intent fields stay blank (FLG-002, FLG-035).
- Whether the selected tracking ID `shopnow047c-20` is assigned to an enrolled account, and whether the
  short-link form attributes correctly. Only Associates Central can answer (FLG-003, `P26-Q2`).
- Whether anyone arrives from search. No Search Console property exists, so no query, impression, click
  or conversion figure is claimed anywhere in this pass (`P26-Q4`).
- Whether GitHub Pages' commercial-use limit applies to this publication. Unresolved (`P27-Q2`); this
  pass did not read the limits page and does not restate it as verified.
