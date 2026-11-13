# Compliance Implementation Notes

Operational companion to the on-site register: https://kanlerxz87-cyber.github.io/Zone3/compliance/
All rule text below was read from the live official pages on 2026-11-13.

**Governing documents**

| Document | Version | URL |
| --- | --- | --- |
| Associates Program Operating Agreement | updated **October 15, 2025** | https://affiliate-program.amazon.com/help/operating/agreement |
| Associates Program Policies (Commission Income Statement, Participation Requirements, Products Statement, Mobile App Policy, Trademark Guidelines, IP License incl. Agent Terms) | updated **April 14, 2026** | https://affiliate-program.amazon.com/help/operating/policies |
| Standard/Special Commission Income Appendix (rate card) | not public — sign-in required | https://affiliate-program.amazon.com/help/operating/schedule |
| FTC Endorsement Guides guidance | current | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking |

The Program Policies are incorporated by reference into the Agreement. Violation of
Participation Requirements, the IP License, or Influencer Policy §1 is expressly *deemed a
material breach*.

---

## 1. Text this platform must emit (and where)

| # | Requirement | Exact text | Enforced by |
| --- | --- | --- | --- |
| 1 | OA §5 associate identification, "clearly and prominently" | `As an Amazon Associate I earn from qualifying purchases.` | `verify_site.py` **V1** — every page carries it in the top bar |
| 2 | IP License §2(k) content disclaimer, plain view | `CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED ‘AS IS’ AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.` | **V2** — every page footer |
| 3 | IP License §2(i) price/availability disclaimer | `Product prices and availability are accurate as of the date/time indicated and are subject to change. Any price and availability information displayed on [relevant Amazon Site(s), as applicable] at the time of purchase will apply to the purchase of this product.` | attached by the price component; not emitted on this site because no price is displayed |
| 4 | IP License §2(i) timestamp adjacent to price | e.g. `Amazon.com Price: $ 32.77 (as of 01/07/2008 14:11 PST- Details)` | required by the price component; same status |
| 5 | FTC material-connection disclosure, with the endorsement, every time | site-specific wording adjacent to each affiliate link | rendered per article; the site-wide banner supplements, never replaces, it |

---

## 2. Where the code enforces it

| Rule | Mechanism | File |
| --- | --- | --- |
| Row provenance (every value sourced or flagged) | build fails, exit 2 | `tools/build_site.py` G1–G2 |
| Source / flag references must resolve | build fails, exit 2 | G3–G4 |
| Repository anchor must exist | build fails, exit 2 | G5 |
| No placeholder text shipped | build fails, exit 2 | G7 |
| Every flag carries a resolution action | build fails, exit 2 | G8 |
| Disclosure + disclaimer present in output | verify fails, exit 3 | `tools/verify_site.py` V1–V2 |
| One `<h1>` per page | V3 | ditto |
| No unsourced table row in emitted HTML | V4 | ditto |
| No broken internal link | V5 | ditto |
| No iframe/embed/object, no Amazon image, no non-HTTPS, no shortener domain | V6 | ditto |
| No TODO/FIXME/TBD/lorem | V7 | ditto |
| Agent identity on the wire | constant + comment; no override path | `tools/amazon_intake.py` |
| 40 KB request ceiling | raises before send | `creators_request()` |
| Block responses are terminal (401/403/429) | returns, never retries into submission | `creators_request()` |
| Image storage disabled; 24h TTL; ASINs exempt | `store_images: false`, `CACHE_TTL_HOURS = 24` | `config/platform.json`, `amazon_intake.py` |
| No imputation of missing analysis inputs | `insufficient_data` + exclusion | `tools/niche_score.py` |
| Cover-price-only comparison, alerts disabled | `analysis.*` flags | `config/platform.json` |
| Static sub-tags only | `sub_tags: []` + rule string; no dynamic assignment path exists | `config/platform.json` |

---

## 3. Agent Terms (IP License §4) — implementation map

| Clause | Requirement | Implementation |
| --- | --- | --- |
| 4 def. | "Agent" = software taking autonomous or semi-autonomous action for a person | applies to this repo's intake, generation and publishing automation in full |
| 4(a) | Agent must identify itself; must stop if asked to refrain | fixed User-Agent `Zone3AffiliatePlatform/1.0 (Agent/Zone3ProductResearch)`; `agent_identity.refrain_hosts` checked pre-flight |
| 4(b) | Amazon may limit agent access by technical means | `obey_block_responses: [401,403,429]` treated as terminal |
| 4(c)(i) | `Agent/[name]` in the User-Agent of every HTTP/HTTPS request | single constant, no override path |
| 4(c)(ii) | no mimicking human keystrokes/navigation, no CAPTCHA solving | no browser automation anywhere; stdlib-only dependency set makes it structurally impossible |
| 4(c)(iii) | answer human-or-computer prompts truthfully | declared identity is the only identity |
| 4(c)(iv) | no circumventing blocking measures | failure → field `null` + flag → human review; never proxy rotation or retry escalation |

---

## 4. Commission mechanics that a model must not get wrong

* **Session:** starts at the Special Link click; ends at the first of 24 h elapsed, any
  non-digital Product order, or a click through another associate's link. Last click wins.
* **Cart:** may complete up to **89 days** after the click; product must ship/stream/download
  and be paid for **within 180 days** of purchase.
* **Qualifying Revenue:** amount actually received **less** shipping, gift wrapping, handling,
  taxes, service charges, credits, rebates, card-processing fees and bad debt.
* **Rounding:** per purchase, to the nearest currency unit — effective rate drifts from the card.
* **Payment:** ≈60 days after month end. US minimums: 10 USD deposit, 10 USD gift card
  (2,000 USD max), 100 USD check (+15 USD fee).
* **Disqualified:** post-termination purchases; any order with a cancellation, return or
  refund; Prohibited Paid Search Placements; links displayed on a search engine; Redirecting
  Links; malformed links; unapproved mobile-app links; Bounty-linked products; subscriptions;
  pre-release/pre-order items not on a listing page.
* **Limit:** Amazon may withhold accrued unpaid income after **3 years** of no substantial
  activity, on 7 days' notice, up to the gift-card minimum.

**Never modelled here:** per-category rates (not public), Amazon-side conversion rate (not
published to affiliates), "trending" rank (no endpoint).

---

## 5. Disclosure placement policy adopted

1. Site-wide bar at the top of every page (satisfies "clearly and prominently" globally).
2. Per-article block immediately above the first affiliate link, in the reading order —
   because the FTC warns a disclosure outside the content itself may be overlooked.
3. Repeated on every page that carries an affiliate link, not just a template index.
4. Never reworded: Amazon's sentence is reproduced verbatim, since §5 prescribes the wording.
5. No implication of Amazon endorsement anywhere in the surrounding copy (OA §5).

---

## 6. What "compliance" means for the three submitted links

| Check | Result |
| --- | --- |
| Is the link a valid tagged Special Link (`?tag=XXXXX-##`)? | **No** — no tag parameter present |
| Is the destination identifiable before the click? | **No** — opaque short path; discouraged by Part. Req. 5(v)–(w) |
| Does it resolve to a product listing? | **No** — 404 on direct probe; fallback redirect otherwise |
| May we publish marketing copy about the product it points to? | **No** — it points to nothing identifiable; publishing would be a misleading claim under 2(b) |
| Correct action | reject at intake, flag, leave the dependent fields blank |

That table is the entire compliance story of the supplied product list, and it is the reason
this site presents an audit rather than three product pages.
