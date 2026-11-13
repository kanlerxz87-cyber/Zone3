# Session `c4e71983` — verification log (additive)

Independent verification run in parallel from baseline `ed1a796`, before this session knew that
`main` had already moved. Every value below was read from an official page (Amazon.com, Amazon
Associates Central, or the FTC) that was actually retrieved. Anything that could not be confirmed is
left blank and flagged.

**Namespacing.** This session's IDs are `C4E-Snn` (sources) and `c4e71983-FLG-nn` (flags). They are
**not** the same items as `main`'s `S01–S29` or `FLG-001–021`. The mapping table at the end says
where they overlap.

Capture window: 2026-11-13 22:31–22:41 UTC.

---

## 1. Link resolution — reproduces `main`'s S11–S13 exactly

| Submitted | Redirect final URL | Page ID | Source |
| --- | --- | --- | --- |
| `link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3?...` | **B0CDY277D3** | C4E-S01 |
| `link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R?...` | **B09B7SB46R** | C4E-S02 |
| `link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH?...` | **B08DKYBTPH** | C4E-S03 |

This is independent confirmation of `main`'s `redirect_observed.page_id` values. The redirects are
deterministic — they reproduced identically on repeated fetches across two different sessions.

Titles read from the `/dp/` page `<title>`:

- B0CDY277D3 — "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish,
  Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double
  Air Fryer - Black" (C4E-S04)
- B09B7SB46R — "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 26QT air
  fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family
  meals." (C4E-S05)
- B08DKYBTPH — "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier
  Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel" (C4E-S06)

All three carry the department suffix ": Home & Kitchen".

**Corroborates** `main`'s FLG-001 (identifiers are 9 characters, not 10-character ASINs) and FLG-002
(redirects land on three products, not confirmed as the submitted ones). This session reached the
same conclusion independently and adds nothing that contradicts it.

## 2. The new part — commercial values were retrievable

`main`'s FLG-004 records product name, brand, price, rating, review count, competitor count,
best-seller rank and availability as unverified, and its verification note says "prices and ratings
are not present in the text returned."

This session found that **Amazon search-result pages do return them.** Querying
`amazon.com/s?k=<ASIN>` returns the listing with price, list price, star rating, rating count,
promotion badge, lowest other offer and the "bought in past month" signal. That is how the values
below were obtained.

| Product | Star rating | Ratings (as shown) | Price | List price | Promotion badge | Lowest other offer | Bought past month | Captured (UTC) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B0CDY277D3 | 4.2 / 5 | 4.8K | $79.93 | $99.99 | Limited time deal | $57.45 (2+ used & new) | 1K+ | 2026-11-13T22:37:14Z |
| B09B7SB46R | 4.3 / 5 | 18.3K | $149.99 | $209.99 | Early Black Friday Deal | $92.99 (2+ used & new) | 4K+ | 2026-11-13T22:33:46Z |
| B08DKYBTPH | 4.4 / 5 | 16.8K | $79.91 | $119.99 | Limited time deal | $49.54 (3+ used & new) | 3K+ | 2026-11-13T22:37:34Z |

Sources: C4E-S07, C4E-S08, C4E-S09.

**Timestamp method.** Amazon returns a `qid` parameter with each search-result page. It is a Unix
epoch value. Decoding it gives the true request time, so the timestamps above are exact rather than
approximate:

- `qid=1794609434` → 2026-11-13T22:37:14Z
- `qid=1794609226` → 2026-11-13T22:33:46Z
- `qid=1794609454` → 2026-11-13T22:37:34Z

Machine-readable: `data/c4e71983-commercial-snapshot.json`.

### What this does and does not resolve

It **partially resolves** FLG-004 for price, rating and review count. It does **not** resolve the
other items in that flag (competitor count, best-seller rank, availability), which remain unverified.

It also comes with a constraint that matters more than the data itself: Program Policies
§2(b) says a site may only show prices if Amazon serves the link or the data came from Creators API
or PA API. Hand-captured search-page prices are neither. **These values are evidence for a flag,
not figures to publish** — logged as `c4e71983-FLG-01`.

## 3. Rating counts are rounded

Amazon search pages render rating counts as `4.8K`, `18.3K` and `16.8K`. The exact counts sit behind
`/product-reviews/<ASIN>`, which redirected to the Amazon sign-in wall (C4E-S23). So
`rating_count_exact` is **null** for all three, and the displayed values are labelled as rounded
everywhere they appear. → `c4e71983-FLG-04`

Note that Best Sellers pages print **exact** counts (see §4), which is why the competitor table has
precise figures and the product table does not.

## 4. Competitor benchmark — entirely new

`main` has no competitor data. This session captured the official *Best Sellers in Air Fryers*
listing, node `17659096011`:

| Rank | Product | Brand | Capacity | Rating | Ratings (exact) | Price |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ninja Air Fryer Pro 5 Qt AF141 | Ninja | 5 Qt | 4.7 | 10,984 | $89.99 |
| 2 | Cosori TurboBlaze 6 Qt | Cosori | 6 Qt | 4.8 | 22,768 | $99.99 |
| 3 | bella Fits-anywhere 4 Qt | bella | 4 Qt | 4.5 | 4,015 | $39.99 |
| 4 | Chefman 4 QT Compact | Chefman | 4 Qt | 4.6 | 7,552 | $57.91 |
| 5 | Cuisinart TOA-55 | Cuisinart | 0.6 cu ft | 4.5 | 126 | $129.95 |
| 6 | Chefman 14-Quart 6-in-1 | Chefman | 14 Qt | 4.3 | 52,301 | $99.95 |

Source: C4E-S13. Machine-readable: `data/c4e71983-competitors.json`.

**Scope limit, stated plainly:** positions 1–6 were captured in full; position 7 partially; 8–100 not
enumerated. No claim is made that any of the three products is absent from the full list.

## 5. Category taxonomy — includes a correction

| Claim | Source | Result |
| --- | --- | --- |
| Small Appliances sits under Kitchen & Dining under Home & Kitchen | C4E-S15 | confirmed from the breadcrumb |
| Fryers has three children: Air Fryer Ovens, Air Fryers, Deep Fryers | C4E-S14 | confirmed |
| The Air Fryers node is **17659096011** | C4E-S13 | confirmed |
| Node **289742** is *Coffee, Tea & Espresso Appliances*, **not** Air Fryers | C4E-S13 vs C4E-S07 | **correction** |

The last row is worth recording because `289742` is a plausible guess for the Air Fryers node and
fetching it returns a valid, confidently-titled Amazon page for the wrong category. Anyone building
against Amazon browse nodes should verify the node rather than assume it.

## 6. Commission rates — read directly from Table 1

`main`'s FLG-005 says commission rates are unverified and the official rate schedule is not
accessible, and its verification note records that the commission schedule (S03) was login-gated and
that "rates are not stated anywhere on the site."

This session reached the rate table through the Associates Central **help** route rather than the
operating-agreement route:
`affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ` returned Table 1 in full without a
login (C4E-S16). Verified rows include:

| Category | Rate |
| --- | --- |
| Luxury Beauty, Luxury Stores Beauty, Amazon Explore | 10.00% |
| Digital Music, Physical Music, Handmade, Digital Videos | 5.00% |
| Physical Books, **Kitchen**, Automotive | **4.50%** |
| Amazon devices, apparel, watches, jewellery, luggage, shoes, handbags | 4.00% |
| All Other Categories | 4.00% |
| Toys, Furniture, **Home**, Home Improvement, Lawn & Garden, Pets, Headphones, Beauty, Musical Instruments, Business & Industrial, Outdoors, Tools, Sports, Baby, Amazon Coins | **3.00%** |
| PC, PC Components, DVD & Blu-Ray | 2.50% |
| Televisions, Digital Video Games | 2.00% |
| Amazon Fresh, Physical Video Games & Consoles, Grocery, Health & Personal Care | 1.00% |

Bounty events also read: Prime free trial and Prime paid membership **$12.00** each; Prime Video free
trial $2.00; Prime Video first stream $5.00; Prime Video stream $0.25. Payment ≈60 days after month
end; US minimums $10 direct deposit / $10 gift card / $100 check, plus a $15 check fee.

This **corroborates** `main`'s PF-38/PF-39 and FLG-021 (Kitchen 4.50% verified; the listings'
category is not). It does not resolve which rate applies per ASIN: Amazon lists Kitchen and Home
separately and does not publish its per-ASIN assignment. → `c4e71983-FLG-09`

## 7. Program rules read in this session

| Rule | Source | Outcome |
| --- | --- | --- |
| Operating Agreement dated **October 15, 2025** | C4E-S17 | read from the page header |
| Program Policies dated **April 14, 2026** | C4E-S18 | read from the page header |
| Session 24 hours; cart order within 89 days; shipped and paid within 180 days | C4E-S18 §1(b) | confirmed |
| Prices only if Amazon-served or API-sourced | C4E-S18 §2(b) | confirmed → `c4e71983-FLG-01` |
| Tag must appear as a URL parameter | C4E-S18 §2(b) | confirmed → `c4e71983-FLG-05` |
| Promotion references must be removed when the promotion ends | C4E-S18 §2(b) | confirmed → `c4e71983-FLG-02` |
| **No ML training on Special Links or Program Content without express prior written approval** | C4E-S18 §5 | confirmed → corroborates FLG-016 |
| No Special Links in browser extensions, plug-ins or similar client software | C4E-S18 §5 | confirmed |
| Original content required for approval | C4E-S18 §1 | confirmed → corroborates FLG-012 |
| Program Content must not be altered | C4E-S18 §6(a) | confirmed → `c4e71983-FLG-08` |
| Cookie / pixel / GDPR / ePrivacy disclosure is the associate's responsibility | C4E-S18 §3(e) | confirmed → corroborates FLG-015 |
| Amazon may monitor, record and crawl the site | C4E-S17 §12 | confirmed |
| Tags must not claim commissions from two programs on the same traffic; bot activity disqualified | C4E-S18 §5, Bonus Event provisions | confirmed → `c4e71983-FLG-17` |
| ≥3 qualifying sales within 180 days; personal orders excluded | C4E-S19 | confirms PF-40 |
| Required disclosure wording | C4E-S19 | see caveat below |

**Caveat on the disclosure sentence.** The Associates FAQ (C4E-S19) gives the wording as "As an
Amazon Associate I earn from qualifying purchases." The Operating Agreement chunks retrieved in full
in this session (1–3 and 7–12) do not contain that sentence. → `c4e71983-FLG-12`: re-copy the exact
wording from the current Operating Agreement before relying on it.

**On FLG-016.** `main` already records the ML restriction, framed around Creators API data. This
session read the underlying clause directly and quotes it:

> "You will not, without our express prior written approval, use, or allow any third party to use,
> any Special Links or Program Content to develop machine learning models or related technology."
> — Program Policies, Participation Requirements §5

The clause is broader than Creators API data: it covers **Program Content** generally. That widening
is the one substantive addition this session makes to FLG-016.

## 8. FTC rules

Read from C4E-S20 (FTC, *Disclosures 101 for Social Media Influencers*, November 2019):

- Disclose any financial, employment, personal or family relationship with a brand.
- The disclosure must be hard to miss, placed with the endorsement, in simple language — not only on
  an About page, not at the end of a post, not behind "more", not mixed into hashtags or links.
- You cannot talk about experience with a product you have not tried.
- You cannot make claims about a product that would require proof the advertiser does not have.

This corroborates `main`'s FLG-017 (the 2019 guidance predates the 2023 Endorsement Guides revision);
`main` already resolved that by citing the current topic page.

## 9. Retrievals that failed

| Attempt | Result | Cost |
| --- | --- | --- |
| `/dp/<ASIN>` (all three) | HTTP 200, "shuffle" landing variant, no extractable detail block | Lost best-seller rank, wattage, model number, spec table |
| `/gp/aw/d/<ASIN>` (mobile) | Same shuffle landing | No additional data |
| `/product-reviews/<ASIN>` | Redirected to the Amazon sign-in wall | Lost exact rating counts |
| Best Sellers positions 7+ | Not enumerated | No absence claim |

## 10. ID mapping to `main`'s scheme

| This session | `main` | Relationship |
| --- | --- | --- |
| C4E-S01–S03 | S11–S13 | Same redirect targets, independently re-fetched |
| C4E-S04–S06 | S14–S16 | Same `/dp/` titles |
| C4E-S07–S09 | — | **New** — search-result pages carrying price and rating |
| C4E-S10–S12 | — | **New** — canonical slug URLs |
| C4E-S13 | — | **New** — Best Sellers in Air Fryers (node 17659096011) |
| C4E-S14, S15 | — | **New** — Fryers and Small Appliances nodes |
| C4E-S16 | vs S03 (login-gated) | **New route** — commission table via Associates help, not login-gated |
| C4E-S17 | S01 | Same document |
| C4E-S18 | S02 | Same document |
| C4E-S19 | — | **New** — Associates FAQ |
| C4E-S20 | S07 | Same document |
| C4E-S21 | S24 | FTC topic page |
| C4E-S22, S23 | S08–S10 | Retrieval attempts that failed |
| `c4e71983-FLG-01` | — | **New** — hand-captured prices not permitted |
| `c4e71983-FLG-02` | — | **New** — live promotion badges |
| `c4e71983-FLG-03` | part of FLG-004 | Best-seller rank still unverified |
| `c4e71983-FLG-04` | part of FLG-004 | Rating counts rounded |
| `c4e71983-FLG-05` | FLG-010 | Same finding |
| `c4e71983-FLG-06` | FLG-015 | Same finding |
| `c4e71983-FLG-07` | FLG-003 | Same finding |
| `c4e71983-FLG-08` | — | **New** — "bought in past month" is Program Content |
| `c4e71983-FLG-09` | FLG-021 | Same finding |
| `c4e71983-FLG-10` | part of FLG-004 | Specifications unverified |
| `c4e71983-FLG-12` | — | **New** — disclosure wording not found in the Agreement body |
| `c4e71983-FLG-13` | FLG-012 | Same finding |
| `c4e71983-FLG-16` | FLG-016 | **Widens it** — the clause covers Program Content, not just Creators API data |
| `c4e71983-FLG-17` | part of FLG-019 | Same finding |
| `c4e71983-FLG-18` | — | **New** — no trend analysis possible from one snapshot |
| `c4e71983-FLG-19` | — | **New** — noindex recommended until blockers clear |

## 11. Automated checks run in this session

Before the branch was reduced, the standalone build this session produced passed:

- external-URL allowlist — 43 URLs, all in the verified register
- internal-link resolution — 17 pages, 0 broken
- disclosure banner present — 17/17 pages
- no leftover template tokens, no Python format-string leaks
- all `data/*.json` parse

Those checks applied to the archived dashboard, not to `main`'s site. `main`'s own
`scripts/check_site.py` was re-run after the additive merge and passes (see COORDINATION.md).
