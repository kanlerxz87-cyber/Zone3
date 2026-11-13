# Session `c4e71983` — niche and competition analysis

Additive contribution. Data captured 2026-11-13 from official Amazon pages. Source IDs `C4E-Snn`;
see `research/c4e71983-verification-log.md` §10 for the mapping to `main`'s `S01–S29`.

## 1. The niche was discovered, not chosen

All three submitted links resolve into the same category. The browse path below is taken from the
breadcrumb Amazon renders on its own Best Sellers pages — not reconstructed.

```
Home & Kitchen  ›  Kitchen & Dining  ›  Small Appliances  ›  Fryers  ›  Air Fryers
```

| Level | Node | Source |
| --- | --- | --- |
| Home & Kitchen | `home-garden` | C4E-S15 |
| Kitchen & Dining | `284507` | C4E-S15 |
| Small Appliances | `289913` | C4E-S15 |
| Fryers | `17659095011` | C4E-S14 |
| Air Fryers | `17659096011` | C4E-S13 |

Sibling sub-categories under Fryers: **Air Fryer Ovens** (`224479505011`), **Air Fryers**
(`17659096011`), **Deep Fryers** (`289918`).

**Correction worth recording.** The node `289742` looks like it should be Air Fryers and fetching it
returns a valid, confidently-titled Amazon Best Sellers page — for *Coffee, Tea & Espresso
Appliances*. It was fetched, found wrong, and discarded. Anyone building against Amazon browse nodes
should verify the node rather than assume it.

## 2. Three products, three tiers, one category

| Sub-category | Product | Capacity | Price | Buying intent |
| --- | --- | --- | --- | --- |
| Dual basket | B0CDY277D3 | 6 Qt (2 × 3 Qt) | $79.93 | Cook two foods with different timings, ready together |
| Air fryer toaster oven | B09B7SB46R | 26 QT | $149.99 | Replace several countertop appliances with one |
| Large capacity | B08DKYBTPH | 8 Qt | $79.91 | Feed more people in one go |

Sub-categories are derived from what the official product titles actually say, not from an external
taxonomy. Three distinct jobs to be done inside one category is what makes a comparison site viable
here rather than a single page.

## 3. Competition

See `research/c4e71983-commercial-snapshot.md` §4 for the full table and the scope limit. Summary:

- Leaders rate **4.7** and **4.8**; the promoted products rate **4.2–4.4**.
- The volume leader (52,301 ratings) and two of the top six are **Chefman**, the brand behind two of
  the three promoted products.
- Only one of the top six is priced above **$130**, and it has 126 ratings. The premium band is the
  thinnest part of the captured set — and the $149.99 promoted unit sits in it.

## 4. Pricing

All three were discounted at capture (20%, 29% and 33% against list). Two carried a *Limited time
deal* badge and one an *Early Black Friday Deal* badge.

The operational consequence matters more than the numbers: printed prices go stale within days, and
two separate clauses of Program Policies §2(b) then bite — the price-display restriction
(`c4e71983-FLG-01`) and the requirement to remove promotion references when the promotion ends
(`c4e71983-FLG-02`).

## 5. Keyword direction — explicitly not measured data

**No search-volume figures appear anywhere in this session's output, on purpose.** No official source
publishes keyword volume for Amazon or Google search. Numbers quoted for "air fryer" search volume on
third-party blogs are that vendor's estimate, and a fabricated figure in a table is indistinguishable
from a measured one.

What *can* be said from the official data that was captured:

- **Intent clusters are visible in the official titles.** Capacity ("6 Quart", "26QT", "8 Qt"),
  function count ("4-in-1", "24 cooking functions", "9-in-1") and feature hooks ("Sync Finish",
  "Hi-Fry", "rotisserie") are the exact phrases a buyer sees on Amazon, and they come from an
  official source.
- **The comparison structure is pre-built.** Three products, three tiers, one category — "versus"
  content needs no further product research.
- **Sub-category pages map to distinct intents**, as set out in §2.

Once the site is live, real query data arrives from Google Search Console and Amazon's own reports.
Until then keyword priority is a hypothesis to test, not data.

## 6. Content angles

Untested — these follow from the captured data, not from keyword research:

- **Dual basket vs one large basket** — a genuine trade-off, and the project owns both products.
- **Replacing three appliances with one** — the real reason someone pays $150.
- **8 Qt vs 6 Qt split across two baskets** — which actually feeds a family of four.
- **Highest-rated unit at the lowest price** — the 8 Qt at 4.4 stars and $79.91 supports a value
  argument on measured data.

Amazon's Participation Requirements §1 require original content with significant commentary or
transformation before a site is approved (`c4e71983-FLG-13`, corroborating `main`'s FLG-012). A table
of Amazon data does not meet that bar on its own.

## 7. One constraint that shapes the whole build

Program Policies, Participation Requirements §5:

> "You will not, without our express prior written approval, use, or allow any third party to use,
> any Special Links or Program Content to develop machine learning models or related technology."

The brief asks for an AI-powered platform. That is compatible with the rule only if the architecture
separates the two activities. Using a general-purpose model to draft or edit copy is a different
thing from training or fine-tuning a model on Amazon-sourced product data, images, reviews or link
data. The second needs written approval first.

`main`'s FLG-016 records this framed around Creators API data. The clause is broader: it covers
**Program Content** generally. That widening is this session's one substantive addition to FLG-016
(`c4e71983-FLG-16`).

A companion restriction: tags must not be used to claim commissions from two programs on the same
traffic, and bot or automated activity is disqualified (`c4e71983-FLG-17`, corroborating part of
`main`'s FLG-019). **Practical rule: automation stays in the back office.** It may read reports,
update pages and draft content for human review. It must never click, visit or transact through its
own Special Links.

## 8. Trend analysis

Not possible from one snapshot — see `c4e71983-FLG-18`. Needs a scheduled collector and eight to
twelve weeks of history.
