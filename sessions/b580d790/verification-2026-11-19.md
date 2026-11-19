# Session `b580d790` — verification and review record, 2026-11-19

Branch `arena/b580d790-zone3`, base `825f513`. Task T9 on the shared board.
This record answers one question: **what did this session actually check, and what is still unknown?**

Everything below was read on **2026-11-19** with the page-fetch tool. A link next to a claim is the page the
claim was read from. Where a claim could not be checked, it says so and is not softened.

---

## 1. Official sources re-read today

| # | Page | What it establishes | Read |
|---|---|---|---|
| 1 | [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | §5 requires the statement “As an Amazon Associate I earn from qualifying purchases.” to be stated clearly and prominently; §1 defines Special Links as links that properly use the tagged formats Amazon provides. | 2026-11-19 |
| 2 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Participation Requirements 2(a): Special Links must use the Associates ID assigned to you. 2(b): prices and availability may be shown only when Amazon serves the link carrying them, or when the data comes from the Creators/PA API. 3(e): you must disclose accurately and adequately how you and third parties collect and use visitor data. | 2026-11-19 |
| 3 | [FTC — Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Disclose a material connection so it is hard to miss; simple terms such as “sponsored” are acceptable; **“You can't talk about your experience with a product you haven't tried.”** | 2026-11-19 |
| 4 | [Google — Control your snippets](https://developers.google.com/search/docs/appearance/snippet) | “Create unique descriptions for each page on your site.” | 2026-11-19 |
| 5 | [Google — Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | “Mark links that are advertisements or paid placements … with the `sponsored` value.” | 2026-11-19 |

The first three are recorded in the site's own register as **S01**, **S02**, **S07**, and this pass adds **S95**
(the re-verification citation used on the suggestions page). The two Google pages are recorded as **S90** and the
snippet guidance used for B79-F-01.

---

## 2. Claim-by-claim review of the owner's brief (S-04 … S-25)

The brief presents each item with an “Implemented” or “Partly implemented” label. Those labels were checked
against the repository as it stands at `825f513`, not accepted.

| Item | Brief says | What the repository shows on inspection | Status after this pass |
|---|---|---|---|
| **S-04** unique title + description | Implemented 2026-11-16 | **Partly false.** `/shop/` and `/shop/products/` shipped the *same* meta description, and three catalogue pages carried near-identical titles. Google's own guidance is to create unique descriptions. | **Fixed** — each catalogue page now has its own title and description; `tools/check_publication.py` fails on any future duplicate. Recorded as **B79-F-01**. |
| **S-05** `rel="sponsored"` on affiliate links | Implemented 2026-11-16 | **True.** Every `link.amazon` and `amazon.com/dp/` anchor on the site carries `rel="sponsored"`; the publish pass adds it automatically and a gate checks it. | Verified, unchanged. |
| **S-06** “what the appliance is like to live with” | Not adopted (D-06) | Consistent with the FTC line that you cannot describe experience with a product you have not tried. This session did **not** add experience claims; the new fit notes are derived from listing wording plus an explicit question. | Still not adopted — correctly. |
| **S-07** one page per typed question | listed, no status | Six question-shaped guides exist under `/guides/`, each in the sitemap and the feed. | Verified. |
| **S-09** social preview + structured data | Partly implemented | **Now true for the reader pages.** All 14 indexable pages carry `og:image`, `og:type`, `twitter:card` and JSON-LD (`Article` on guides, `WebSite`/`WebPage` elsewhere). Image dimensions and alt text added this pass. Search Console remains unavailable — no property access was supplied. | Improved; measurement half still blocked. |
| **S-10** docs in line with code | Partly implemented | `README.md` documents the current single build command (`python3 tools/publish.py`). All 41 commands pass from a clean tree. | Verified today. |
| **S-11** flag cross-references | Partly implemented | Flags are additive; no existing ID was renumbered in this pass. | Not re-audited in full — see limitation below. |
| **S-12 / S-13 / S-14 / S-15 / S-16 / S-17 / S-19 / S-23 / S-24** | Implemented 2026-11-16 | Spot-checked: voice is consistent, the front page is editorial, six guides are live, internal links reach the comparison and the category pillars. | Structural checks pass; not re-read line by line this pass. |
| **S-18** real product photography | Needs a decision | No Amazon-hosted image is used anywhere; all art is labelled generated or generic. | Correctly unresolved — a decision, not a build task. |
| **S-20** mobile pass | listed, no status | Tap-target and reduced-motion rules are present in the CSS. No browser was available in this sandbox to re-measure, so **no accessibility claim is made**. | Unverified by this session. |
| **S-25** grow traffic on the verification angle | listed, no status | No analytics endpoint and no Search Console property exist, so no traffic claim can be made in either direction. | Blocked on account access — see §5. |

---

## 3. The five supplied product links, re-opened today

Each link was opened once through the fetch tool (a normal browser-style request). The page it landed on is
recorded; the product the owner *intended* is **not** inferred.

| Link | Landed on (ASIN) | Page title served | Same as register? |
|---|---|---|---|
| `link.amazon/B04G1MEwY` | `B0CDY277D3` | CHEFMAN 6 Quart Dual Basket Air Fryer Oven … 2 Independent 3Qt … Black | Yes |
| `link.amazon/B02NbDxp3` | `B09B7SB46R` | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … | Yes |
| `link.amazon/B00hJ57DV` | `B08DKYBTPH` | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 … Stainless Steel | Yes |
| `link.amazon/B0c8moW59` | `B0DHZTCNR5` | (listing reached; breadcrumb Thermometers & Timers › Meat recorded) | Yes |
| `link.amazon/B0f3GKalj` | `B0DZFD6R9Z` | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes … Gen3 | Yes |

**No destination changed** since the 2026-11-17 and 2026-11-19 records. That is the whole of the finding: the
links work and land where the register says. It does **not** establish that these are the products the owner
meant, and it does **not** establish that clicks are credited to `shopnow047c-20`. Both remain open
(**B79-F-02**; FLG-002, FLG-003, FLG-035).

---

## 4. Things a reader can now do that they could not before

| Before | Now | Where |
|---|---|---|
| Five product cards, no way to choose | Three questions, each answer linking to the guide that resolves it. No score, no ranking, nothing sent anywhere. | `/shop/`, `/shop/air-fryers/`, `/shop/meat-thermometers/` |
| Cards described the product, not the buyer | Each card carries “Fits you if” / “Not for you if”, derived from listing wording, plus one editorial question | all product cards |
| Suggestions page was a list of six cards | Each card states what happens if you say go, the facts that would settle it, and whether you or the agent can unblock it | `/suggestions/` |
| Questions table had no owner | A “who can unblock it” column and a dated re-check line | `/suggestions/#questions` |
| Nav labels said “Second source register”, etc. | Labels describe the thing, not its position in a merge | masthead + footer |

---

## 5. What is still missing, and who has to supply it

Nothing below can be produced by a build. Each one is listed with the reason it cannot be faked.

1. **Enrolled Associates access.** Needed to generate one real Special Link per product and to see whether a
   click appears in a tracking report. *(Participation Requirements 2(a).)* Without it, attribution stays unknown.
2. **A durable HTTPS host for the collector.** GitHub Pages is static and cannot run the Python collector.
   Production measurement therefore stays **off** rather than being pointed at a host that does not exist.
   *(Also raised in [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).)*
3. **Search Console ownership.** Needed for real queries. No query, volume or ranking claim is made until then.
4. **Authorized Associates reports.** The campaign ledger stays empty; a click on this site is not an order.
5. **A decision on product photography (S-18).** Amazon imagery may not be republished without the applicable
   licence; the current art is labelled as generated/generic on purpose.
6. **A decision on hands-on testing.** Until someone tests, the site will keep saying it has not tested.

---

## 6. Limits of this pass, stated plainly

- The site was rebuilt and every one of the 41 build/check commands passed from a clean tree. That proves the
  tree is internally consistent and that the gates in `tools/` hold. It does **not** prove any product fact.
- No headless browser is installed in this sandbox. Layout, tap targets and contrast were **not** re-measured
  today; the previous session's Chromium results are not re-used as evidence for changes made after them.
- Prices, ratings and review counts were visible on the Amazon pages during the fetch. They are deliberately
  **not** reproduced anywhere on the site, because Program Policies 2(b)/6(t) allow them only via an
  Amazon-served link or authorized API data. Their absence is a compliance choice, not missing work.
- Historical pages under `/sessions/` and `/docs/` were not re-verified. They are dated records, marked noindex.
