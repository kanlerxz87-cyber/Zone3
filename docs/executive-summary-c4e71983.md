# Zone3 — Executive summary (session `c4e71983`)

> **This is one session's summary, not the canonical one.** `main` already carries
> `docs/executive-summary.md` from session `7f84fea4` (and `docs/executive-summary-33226b37.md`).
> Following the precedent set for session `33226b37`, this session's summary is preserved under its
> own name rather than overwriting that. It is valued for the parts `main` could not verify at the
> time: **the commercial snapshot and the competitor benchmark**. Source IDs `C4E-Snn` and flags
> `c4e71983-FLG-nn` are namespaced and are not the same items as `main`'s `S01–S29` / `FLG-001–021`.
> Mapping: `research/c4e71983-verification-log.md` §10.

**Prepared:** 2026-11-13 · **Session:** `c4e71983` · **Data captured:** 2026-11-13, 22:33–22:37 UTC
**Verification standard:** every value below was read from an official Amazon or Amazon Associates page.
Anything that could not be confirmed is left blank and flagged — nothing is inferred.

---

## 1. What was asked for

An AI-powered Amazon affiliate platform that automates product research, identifies trending and
high-converting products, analyses pricing, reviews, competition and commission potential, generates
SEO-optimised articles and comparisons, publishes and manages affiliate links, tracks clicks and
conversions, and continuously optimises — while complying with Amazon Associates policies and FTC
disclosure rules. Marketing was to be built around three supplied product links.

## 2. What the three links turned out to be

All three short links were fetched and followed. Each returns an official Amazon.com product page.
**All three are air fryers**, in the same department and the same category path.

| # | Supplied link | Resolves to | ASIN | Product | Price at capture |
| --- | --- | --- | --- | --- | --- |
| P1 | `link.amazon/B04G1MEwY` | `amazon.com/dp/B0CDY277D3` | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | $79.93 (list $99.99) |
| P2 | `link.amazon/B02NbDxp3` | `amazon.com/dp/B09B7SB46R` | B09B7SB46R | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | $149.99 (list $209.99) |
| P3 | `link.amazon/B00hJ57DV` | `amazon.com/dp/B08DKYBTPH` | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | $79.91 (list $119.99) |

Source for every cell: the official Amazon page linked in the table above.

**Category path (from Amazon's own breadcrumb):**
Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers

The niche was discovered, not chosen. Three products in one category, at three different price tiers,
is a coherent starting catalogue — it supports a category hub, sub-category pages, and comparison
content with no further product research.

## 3. Commercial findings

| Product | Rating | Ratings shown | Bought past month | Commission @ Kitchen 4.50% | Commission @ Home 3.00% |
| --- | --- | --- | --- | --- | --- |
| B0CDY277D3 | 4.2 / 5 | 4.8K | 1K+ | **$3.60** | $2.40 |
| B09B7SB46R | 4.3 / 5 | 18.3K | 4K+ | **$6.75** | $4.50 |
| B08DKYBTPH | 4.4 / 5 | 16.8K | 3K+ | **$3.60** | $2.40 |

Rate source: [Associates Program Standard Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ).

- **The premium unit is worth nearly twice as much per conversion**, and it is also the fastest-moving
  and best-reviewed product in the set. There is no tension between "promote the premium option" and
  "promote what sells". It should take the top slot in every comparison.
- **Prime bounties pay $12.00 per sign-up** — more than three air fryer sales at the Kitchen rate.
  Prime is a material part of the revenue model, not an afterthought.
- **Ratings are the competitive gap, not price.** The category leaders rate 4.7 and 4.8; these three
  rate 4.2–4.4.

## 4. Competition

Official *Best Sellers in Air Fryers*, positions 1–6 (only these were enumerated):

| Rank | Product | Rating | Ratings | Price |
| --- | --- | --- | --- | --- |
| 1 | Ninja Air Fryer Pro 5 Qt AF141 | 4.7 | 10,984 | $89.99 |
| 2 | Cosori TurboBlaze 6 Qt | 4.8 | 22,768 | $99.99 |
| 3 | bella Fits-anywhere 4 Qt | 4.5 | 4,015 | $39.99 |
| 4 | Chefman 4 QT Compact | 4.6 | 7,552 | $57.91 |
| 5 | Cuisinart TOA-55 | 4.5 | 126 | $129.95 |
| 6 | Chefman 14-Quart 6-in-1 | 4.3 | 52,301 | $99.95 |

Source: [Amazon Best Sellers: Best Air Fryers](https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/)

The band above $130 is the thinnest part of the captured top six — and it is where the $149.99 unit sits.

## 5. What was actually built

A static GitHub Pages dashboard, generated from a validated JSON dataset by `tools/build_site.py`:

- Landing dashboard, executive summary, master data table, comparison, link resolution
- Four category pages (Air Fryers + three sub-categories)
- Niche and competition analysis, commission model, a working **Special Link builder**
- Compliance checklist, data-sources register, and a **Flagged for Review** page
- Automation architecture and analytics pages

The generator **fails the build** if any external URL falls outside the verified allowlist or if any
internal link is broken, so a bad link cannot silently ship.

## 6. Blockers — three things stop revenue today

| Flag | Issue | Why it blocks |
| --- | --- | --- |
| **FLAG-01** | Prices were hand-captured from Amazon search pages | Program Policies allow price display only if Amazon serves the link, or if the price came from Creators API / PA API. As it stands the price tables break the rules. |
| **FLAG-05** | No Associates tag in any link | Without a `tag=` parameter there is no Special Link and no commission, full stop. |
| **FLAG-16** | Training ML models on Amazon Program Content needs express written approval | Directly constrains the "AI-powered" part of the brief. |

Two more are close behind: **FLAG-02** (live promotion badges must come down when the promotion ends,
which a static page cannot guarantee) and **FLAG-13** (Amazon rejects sites without original content —
a data table is not original content in Amazon's sense).

## 7. Recommended sequence

1. **Decide the marketplace.** All data here is Amazon.com, but the operator is in Norway and Norway
   is not in the Associates country list (FLAG-06). This determines the commission and tax schedules.
2. **Join Associates and get a tag** (FLAG-05). Then use the Link Builder to produce compliant links.
3. **Write original content** (FLAG-13). Category hub, three sub-category pages, comparisons, buying guides.
4. **Fix price display** — Creators API / PA API feed, Amazon-served widget, or delete the price columns
   (FLAG-01).
5. **Add a privacy and cookie page** — required by the Operating Agreement and by GDPR / ePrivacy for an
   EEA-facing site (FLAG-06).
6. **Get three qualifying sales within 180 days** or the application is withdrawn (FLAG-12).
7. **Only then automate** — collector, store, content pipeline, reporting.

## 8. Bottom line

The product research is done, verified and published. The niche is confirmed and coherent. The
economics are thin per unit — $3.60 to $6.75 at the published Kitchen rate — so this only works with
volume, with Prime bounties, or by steering traffic toward the $149.99 unit. Nothing can earn yet:
there is no Associates tag, no original content, and the price display as it currently stands breaks
the Program Policies. Those three items are cheap to fix and are the whole gap between this repository
and a monetised site.

---

**Full detail:**
[`research/c4e71983-verification-log.md`](../research/c4e71983-verification-log.md) ·
[`research/c4e71983-commercial-snapshot.md`](../research/c4e71983-commercial-snapshot.md) ·
[`research/c4e71983-niche-competition.md`](../research/c4e71983-niche-competition.md) ·
[`data/c4e71983-commercial-snapshot.json`](../data/c4e71983-commercial-snapshot.json) ·
[`data/c4e71983-competitors.json`](../data/c4e71983-competitors.json) ·
[`COORDINATION.md`](../COORDINATION.md)

The standalone dashboard this session built — 17 pages, including the master table, comparison,
commission model and a working Special Link builder — is archived intact and browsable at
[`archive/c4e71983/index.html`](../archive/c4e71983/index.html).
