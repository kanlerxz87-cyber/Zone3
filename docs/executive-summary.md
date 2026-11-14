# Executive Summary — Zone3 AI Amazon Affiliate Marketing Platform

**Prepared:** 2026-11-13 · **Session:** `3c6cba43` · **Branch:** `arena/3c6cba43-zone3`
**Live site:** https://kanlerxz87-cyber.github.io/Zone3/
**Full version with every table:** `/executive-summary/` on the site.

---

## 1. Bottom line

The platform described in the brief is specified, built and published. **It cannot
market the three listed products, because the three submitted links do not identify
any product.** Every product-level field is therefore blank and flagged — not
estimated.

| | |
| --- | --- |
| Products submitted | 3 |
| Products passing intake verification | **0 of 3** |
| Product attribute cells left blank | **36** (12 fields × 3 SKUs) |
| Official sources cited | 17 primary documents |
| Open flags published for review | 28 |
| Compliance rules enforced in the build | 25 prohibitions + 5 mandatory text blocks |
| Verdict | Not launchable until inputs 1–2 below are supplied |

---

## 2. The product-list problem, with reproducible proof

Submitted: `link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`, `link.amazon/B00hJ57DV`.

1. **Length.** All three identifiers are **9 characters**. Amazon: an ASIN is
   *"a unique 10-character alphanumeric code assigned to every product listed in the
   Amazon store"* — https://sell.amazon.com/blog/what-is-an-asin
2. **Direct probe.** `https://www.amazon.com/dp/<id>` returns Amazon's
   **"Sorry! We couldn't find that page"** error for each of the three.
3. **Control.** The same probe against a real 10-char ASIN (`B0CDY277D3`) serves a
   normal product page — so the 404s describe the identifiers, not the tooling.
4. **Redirect trace.** Each submitted link resolved to a **different** unrelated
   product, all tagged `channelId=704&plpRedirect=mhFallback`:

   | Submitted | Landed on | Amazon's own marker |
   | --- | --- | --- |
   | `B04G1MEwY` | `B0CDY277D3` — CHEFMAN 6-Qt dual-basket air fryer | `plpRedirect=mhFallback` |
   | `B02NbDxp3` | `B09B7SB46R` — Emeril Lagasse 26QT air fryer toaster oven | `plpRedirect=mhFallback` |
   | `B00hJ57DV` | `B08DKYBTPH` — Chefman Air Fryer 8 Qt TurboFry | `plpRedirect=mhFallback` |

   `mhFallback` is Amazon's *fallback* route. Three different answers to three
   different inputs is conclusive: the links carry no product identity.

Most likely cause: **one character dropped per identifier while copying.**

> **Why this matters beyond these three links.** A conventional affiliate bot would
> have accepted the redirect, recorded "CHEFMAN air fryer" as product 1, and produced
> three fluent, entirely fabricated buying guides. The intake gate is what prevents
> that failure mode, and it is why the correct output here is an empty table plus a
> flag.

---

## 3. Three briefed features that Amazon prohibits

This is the highest-value part of the analysis, because it is where affiliate
automation gets accounts terminated.

| Briefed feature | Blocking rule (official) | Adopted design |
| --- | --- | --- |
| "analyzes pricing" → price alerts / price watch | *"Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality."* (Part. Req. 5(y)) | Price analysis stays **internal** (ranking, deal-claim thresholds). No alerts, no history charts. |
| "track clicks" → per-visitor attribution | *"Under no circumstances may you associate any sub-tag … with a specific end user … (e.g., you may not dynamically assign sub-tags to users as they arrive on your Site for purposes of monitoring such users' behavior)."* (Part. Req. 2(b)) | **Static** sub-tags per page/slot only. No per-user identity joins. |
| "automate … continuously optimize" → self-testing the funnel | 5(s) bars artificially generating clicks or creating Amazon Sessions *"by way of a robot or software program or otherwise"*; 5(u) bars buying through your own links | Agent has **no** click-through capability. Funnel tests are structural (link format, HTTP status), never behavioural. |

Also excluded as a matter of design: link shorteners / obscured destinations
(5(v)–(w)), framing or embedding Amazon (5(n)), pop-ups carrying links (5(o)),
Special Links inside any content placed **on** Amazon including reviews and forums
(5(p)), paid search on "amazon"/"kindle"/any Amazon Mark (CIS 2(c) — those purchases
are simply disqualified), storing Amazon images at all, or caching other Program
Content beyond 24 hours (IP License 2(h)), and using Program Content to promote any
non-Amazon retailer (5(z)).

---

## 4. Economics — only what is officially stated

**Public:** commissions are *"up to 10%"* and *"differ based on product category"*;
payment lands ≈60 days after month end; US minimums are 10 USD (direct deposit or
gift card, gift card capped at 2,000 USD) and 100 USD by check + 15 USD fee.

**The mechanics that actually decide earnings:**

* attribution is a **24-hour session that dies the moment the customer buys anything
  or clicks another associate's link** — last click wins, and it is fragile;
* a cart may be completed up to **89 days** after the click;
* the **whole basket** in that session pays, not just the linked item;
* commission is computed on **Qualifying Revenue net of** shipping, gift wrap,
  handling, taxes, service charges, credits, rebates, card fees and bad debt;
* any order with a **cancellation, return or refund** is excluded entirely;
* rounding per purchase means the effective rate drifts slightly from the rate card.

**Published in full on `/commission/`** — after a correction during review. The Appendix link at
`/help/operating/schedule` does redirect to sign-in, but the Standard Commission Income Statement is
publicly available in the Associates help centre: eleven fixed bands from **10.00 % down to 0.00 %**,
with **4.00 % as the "All Other Categories" default**, plus the Bounty schedule ($12.00 per Prime
registration or membership; $0.25–$5.00 per Prime Video action).

| Band | Categories (abridged) |
| --- | --- |
| **10.00 %** | Luxury Beauty, Luxury Stores Beauty, Amazon Explore |
| 5.00 % | Digital/Physical Music, Handmade, Digital Videos |
| 4.50 % | Physical Books, **Kitchen**, Automotive |
| 4.00 % | Amazon devices, Luxury Stores Fashion, Apparel, Watches, Jewelry, Luggage, Shoes, Handbags |
| 3.00 % | Toys, Furniture, Home, Home Improvement, Lawn & Garden, Pets, Headphones, Beauty, Tools, Sports, Baby |
| 2.50 % / 2.00 % | PC & components, DVD/Blu-Ray · Televisions, Digital Video Games |
| 1.00 % | Amazon Fresh, Video Games & Consoles, Grocery, Health & Personal Care |
| **0.00 %** | Gift cards, wireless plans, alcohol, Kindle subscriptions, vehicles, pet Rx, restaurant delivery, Coach |

Two consequences. **The default band beats four named bands**, so an unlisted niche is often the better
bet. And **Kitchen 4.50 % versus Home 3.00 % is a 1.5× spread between categories that look like the same
shelf** — so a rate may never be inferred from a product's topic, only from its browse node. What remains
blank is the *per-product* commission for these three SKUs, because no category can be attached to an
unresolvable listing. (FLG-013 resolved; FLG-008 still open.)

**Strategic read.** Because the entire basket pays, *traffic quality beats item
relevance*. Because the session is fragile, *direct-to-product links on fast pages
beat content that routes the reader off-site first*. Because shipping and tax are
excluded and returns void the commission, *sticker-price revenue models overstate
earnings*.

---

## 5. Two facts that change the architecture

**a) PA-API 5.0 is dead.** Amazon's own documentation host now serves a deprecation
notice; live callers get `HTTP 403` with `com.amazon.paapi5#AccessDeniedException`.
The **Creators API** replaces it and exposes exactly **four operations** —
`SearchItems`, `GetItems`, `GetVariations`, `GetBrowseNodes`.

Two consequences: the feature ceiling of any affiliate agent is bounded by four read
operations — there is **no** trend endpoint, no competitor-count endpoint and no
conversion endpoint, which is why "trending" and "high-converting" are flagged rather
than fabricated (FLG-016). And access requires enrolment plus **10 qualifying sales
in the past 30 days**, so cold-start cannot be automated away (FLG-020).

**b) Amazon wrote rules specifically for AI agents.** The IP License gained
Section 4 "Agent Terms": an *Agent* is *"any software or service that takes autonomous
or semi-autonomous action on behalf of, or at the instruction of, any person or
entity"*. It must put `Agent/[agent name]` in every User-Agent, must not mimic human
keystroke or navigation patterns, must not complete CAPTCHAs, must answer
human-or-computer prompts truthfully, and must not circumvent access controls. Amazon
may also limit agent access by technical means at its sole discretion.

So a compliant agent **announces itself and stops when blocked** — it does not
disguise itself as a browser. `tools/amazon_intake.py` is built to exactly that rule
(`Agent/Zone3ProductResearch`, block responses are terminal). This is the honest
answer to "prioritise automation": automation of *research, grounding, generation and
gating*, not unattended browsing of Amazon's consumer site.

---

## 6. Content generation state

Zero articles, comparisons or guides were produced — because zero verified product
facts exist. Shipped instead: four templates, the claim-grounding contract (every
sentence bound to a named API field), and renderer refusals — a comparison cannot
render without lowest-new **and** lowest-used prices; a price cannot render without a
timestamp and the availability disclaimer; a page cannot publish without the
disclosures. Structured data (`Product`/`Review` schema) is **deliberately omitted**
rather than populated with invented values.

Compliance is a build gate, not a page: `tools/verify_site.py` fails if any page drops
*"As an Amazon Associate I earn from qualifying purchases."* (Operating Agreement §5,
whose omission is a deemed material breach), or if any table row lacks a source.
The FTC duty is tracked separately — disclose the material connection clearly and
conspicuously, with the endorsement, in **every** endorsement: *"if a disclosure is
needed in one post for a brand, it's probably needed in all posts."*

---

## 7. What unblocks this — priority order

| # | Needed from you | Why it gates |
| --- | --- | --- |
| 1 | **Correct the three ASINs** (10 characters), or send listing names/screenshots | Unblocks attributes, pricing, reviews, content, niches |
| 2 | **Your Associates tag** `XXXXX-##` → `config/platform.json` | No Special Link can be built or tested; malformed tags silently zero earnings (CIS 2(g)) |
| 3 | **Creators API credentials** (after the 10-sales threshold) | The only sanctioned product-data intake |
| — | *(self-corrected, no action)* category rates were found public after an initial "inaccessible" read | Demonstrates why every cell cites the fetched page, not the first endpoint tried |
| 3b | *(no action — self-corrected)* category rates were found public after an initial "inaccessible" read | Shows why the verification gate cites the fetched page, not the first endpoint tried |
| 4 | **Decision on the 3 prohibited features** | Price alerts / per-visitor attribution require written agreement from Amazon |
| 5 | **Target categories** for niche work | Shortlisting needs no API access; only scoring does |

Nothing here waits on your review to deploy — the site is live and every open item is
published for post-launch review at `/flagged/`.

---

## 8. Risk register (top three)

1. **Account termination.** Amazon may permanently cease **all** commission income for
   a violation, including a disclosure violation, whether or not the affected earnings
   relate to it. Mitigated by treating disclosure and sourcing as build gates.
2. **Empty-dataset risk.** An agent forbidden from guessing publishes little. Mitigated
   by publishing the verified rule set and the evidence, which has standalone value.
3. **Third-party dependency.** Rates, thresholds, API surface and the rules themselves
   change at Amazon's discretion without notice. Mitigated by a quarterly source
   re-verification step and by dating every table.

---

## 9. Where to look

| | |
| --- | --- |
| Products & verification | `/products/` |
| Niches | `/niches/` · Pricing `/pricing/` · Reviews `/reviews/` |
| Content engine | `/content/` · Campaigns `/campaigns/` |
| Compliance register (25 rules) | `/compliance/` · Agent terms `/agent-terms/` |
| Architecture & verification protocol | `/methodology/` |
| All 30 brief clauses traced | `/requirements/` |
| Every official source | `/sources/` |
| Open items | `/flagged/` |
| Repo audit | `/repo-review/` |
| Coordination & claims | `COORDINATION.md` |

---

## 10. Status update — 2026-11-14 (session `ecbfe91b`)

Everything official was re-checked live on 2026-11-14; full evidence table in
[`research/ecbfe91b-reverification-2026-11-14.md`](../research/ecbfe91b-reverification-2026-11-14.md).

- **Nothing about the three submitted links changed.** `amazon.com/dp/` still returns
  *Page Not Found* for all nine-character identifiers; a real-ASIN control still resolves;
  `link.amazon/B04G1MEwY` still lands on `B0CDY277D3`. Product values remain blank by design —
  no value was inferred. ([S08](https://www.amazon.com/dp/B04G1MEwY) ·
  [S09](https://www.amazon.com/dp/B02NbDxp3) ·
  [S10](https://www.amazon.com/dp/B00hJ57DV) ·
  [control](https://www.amazon.com/dp/B0CDY277D3) ·
  [ASIN rule](https://sell.amazon.com/blog/what-is-an-asin))
- **The commission rate card is public.** Table 1 (Kitchen 4.50%, Home 3.00%, All Other
  Categories 4.00%, bounty schedule) re-read without sign-in at the
  [help node](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ). Per-product
  rates still cannot be assigned because each listing's category is unverified (FLG-021).
- **The disclosure sentence is in the Operating Agreement body** (§5, re-read verbatim) — this
  resolves `c4e71983-FLG-12`.
  ([agreement](https://affiliate-program.amazon.com/help/operating/agreement))
- **FLG-016 widened:** the machine-learning bar covers *Special Links or Program Content*
  generally, not only Creators API data (Program Policies §5, verbatim quote in the flag).
  ([policies](https://affiliate-program.amazon.com/help/operating/policies))
- **Competition benchmark published** on the flat build's `reviews.html` and the
  `air-fryers.html` category page: the official
  [Best Sellers in Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/)
  page read 2026-11-14 (an earlier 2026-11-13 capture ordered ranks 2–3 differently — ranks are
  point-in-time, FLG-025). Both views render the same `data/competition.json` rows. Prices and
  star ratings are withheld by policy (FLG-022) and live only in internal capture files.
- **Two defects fixed:** `reviews.html` cited product 1's source (S08) for all three product
  rows (now S08/S09/S10 per row); `tools/link_report.py` repeated the outdated claim that the
  rate card is sign-in-gated.
- **PR #10** (stale >60 min, conflicting) was taken over and closed as superseded — its
  broken-link target pages no longer exist in that form; the current tree reports 0 broken
  links across 57 pages. Handoff logged in `COORDINATION.md`.
- New source S45 (ASIN rule page); the Best Sellers page was already S43 in main's registry.
  The proposed duplicate FLG-022 was dropped in favour of main's FLG-022 (same rule). Main also
  gained FLG-023–027 from parallel sessions (including the `plpRedirect=mhFallback` correction,
  which matches this session's control observation). Re-verification dates appended to
  S01, S07–S11, S14, S25. Full merge log: `COORDINATION.md` Part E.
