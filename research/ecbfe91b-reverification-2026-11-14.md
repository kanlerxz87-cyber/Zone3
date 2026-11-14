# Re-verification record — session `ecbfe91b`, 2026-11-14

Branch `arena/ecbfe91b-zone3`. Every row below was re-checked **live on 2026-11-14** with the
session's web-fetch tool against the official page itself. Nothing here is taken from a search
snippet or a third-party restatement. Where a value could not be confirmed from the official
page, it stays blank and flagged — no value in this record was inferred.

Manual-review links are given in full in the "Source" column.

## A. Identifier and product checks

| # | Check | Observed result (2026-11-14) | What it confirms | Source (official) |
|---|---|---|---|---|
| A1 | `amazon.com/dp/B04G1MEwY` | Amazon "Page Not Found" error page | Identifier 1 has no product page (root S08; re-confirmed) | https://www.amazon.com/dp/B04G1MEwY |
| A2 | `amazon.com/dp/B02NbDxp3` | Amazon "Page Not Found" error page | Identifier 2 has no product page (root S09; re-confirmed) | https://www.amazon.com/dp/B02NbDxp3 |
| A3 | `amazon.com/dp/B00hJ57DV` | Amazon "Page Not Found" error page | Identifier 3 has no product page (root S10; re-confirmed) | https://www.amazon.com/dp/B00hJ57DV |
| A4 | `amazon.com/dp/B0CDY277D3` (control) | Product page: "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows…" | Control: a real 10-character ASIN resolves, so the three 404s in A1–A3 are meaningful, not a fetch artifact (root S14) | https://www.amazon.com/dp/B0CDY277D3 |
| A5 | `link.amazon/B04G1MEwY` followed to its destination | Landed on `amazon.com/dp/B0CDY277D3` (same CHEFMAN page as A4) | Short-link → B0CDY277D3 mapping is stable across days and sessions (third independent session to observe it; root S11) | https://link.amazon/B04G1MEwY |
| A6 | Sell on Amazon ASIN guide | Page states an ASIN is "a unique 10-character alphanumeric code assigned to every product listed in the Amazon store"; typical form "B07FZ8S74R" | The submitted identifiers (9 characters) are not ASINs (FLG-001). Added on merge as **S45** (main's S30/S31 were already taken). | https://sell.amazon.com/blog/what-is-an-asin |

Observation: the control fetch A4 also ended with `plpRedirect=mhFallback` in the URL while
serving the correct product — independently reproducing session `79f85104`'s Z-V13 finding that
this parameter is not evidence the short link "selected nothing". It does not change the
conclusion in FLG-001/FLG-002: the nine-character identifiers themselves resolve nothing.

## B. Policy and rate checks

| # | Check | Observed result (2026-11-14) | What it confirms | Source (official) |
|---|---|---|---|---|
| B1 | Operating Agreement §5 "Identifying Yourself as an Associate" | Verbatim: "You must clearly and prominently state the following … on your Site … : 'As an Amazon Associate I earn from qualifying purchases.'" | The disclosure sentence **is in the Agreement body** — resolves `c4e71983-FLG-12` (which suspected it was FAQ-only). Root S01 re-verified. | https://affiliate-program.amazon.com/help/operating/agreement |
| B2 | Operating Agreement §6 | "any violation of Section 5 … will be deemed a material breach of this Agreement" | Disclosure breach = material breach (already on the site's compliance pages) | https://affiliate-program.amazon.com/help/operating/agreement |
| B3 | Program Policies, Participation Requirements §5 (Software and Devices) | Verbatim: "You will not, without or express prior written approval, use, or allow any third party to use, any Special Links or Program Content to develop machine learning models or related technology." | **FLG-016 widened**: the ML bar covers *Special Links or Program Content* generally, not only Creators API data (`c4e71983-FLG-16` adopted). The wording "without or express" is Amazon's own typo on the live page; the quote in `data/policy_facts.json` reproduces it verbatim and is correct. | https://affiliate-program.amazon.com/help/operating/policies |
| B4 | Program Policies, Participation Requirements 2(b) | "your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…" | Competitor prices must not be displayed from hand captures (basis for FLG-022) | https://affiliate-program.amazon.com/help/operating/policies |
| B5 | Standard Commission Income Statement, Table 1 (public help node) | Page is publicly readable without sign-in. Table 1: "Physical Books, Kitchen, Automotive | 4.50%"; "… Home … | 3.00%"; "All Other Categories | 4.00%"; plus the 34-row bounty table | The rate card is **not** sign-in-gated at this URL (re-confirms sessions `3c886b62`/`c4e71983`; root S25 re-verified). Per-listing rate stays blank because each listing's category is unverified (FLG-021). | https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ |
| B6 | FTC Disclosures 101 for Social Media Influencers | Page re-read; still dated November 2019; requires clear, hard-to-miss, plain-language disclosure of material connections | FTC basis for the disclosure checklist (root S07 re-verified) | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |

## C. Competition benchmark check

| # | Check | Observed result (2026-11-14) | What it confirms | Source (official) |
|---|---|---|---|---|
| C1 | Amazon Best Sellers: Best Air Fryers (node 17659096011) | Page live; category path Kitchen & Dining › Small Appliances › Fryers › Air Fryers. Top 6 today: B0CSZ7WBYW, B0CYJDVT31, B0C33CHG99, B0CNY1F31S, B0GVVJZDQV, B0GTBN7CS2 | The 2026-11-13 capture (session `c4e71983`, `data/c4e71983-competitors.json`) is from the correct official page (**S43** in main's registry). Ranks 2 and 3 (Bella/Cosori) have **swapped** since the capture — proof that ranks are point-in-time; the published table keeps the dated snapshot and labels it. | https://www.amazon.com/Best-Sellers-Kitchen-Dining-Air-Fryers/zgbs/kitchen/17659096011/ |

## D. Repo review findings (line by line)

Run results on the tree at `6bf308f` + this branch's edits:

| Tool | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 9 pages, 3 products, 31 sources, 22 flags (was 29/21 before this pass) |
| `python3 tools/build_site.py` | OK — 16 pages · 231 verified table rows · gate PASS · rebuild idempotent |
| `python3 tools/verify_site.py` | PASS — 57 pages · 892 table rows · V1–V7 (only pre-existing non-blocking V4 notes on the inherited `sessions/3c886b62/verification.html` page) |
| `python3 tools/link_report.py --strict` | PASS — 100% row provenance across all 10 table groups; no dangling source/flag refs |

Defects found and fixed in this pass:

| ID | Finding | Fix |
|---|---|---|
| E-F1 | `reviews.html` (root build) cited source **S08** (product 1's `/dp/` check) in the source cell of **all three** product rows — the same defect class PR #6 fixed on the pricing page, but the reviews loop was missed. | `scripts/build_site.py` now cites `p["direct_check"]["source"]` per row (S08/S09/S10). Rebuilt and re-checked. |
| E-F2 | `tools/link_report.py` printed "per-category commission: rate card is behind Associates sign-in" — contradicted by S25 (public help node, re-verified 2026-11-14) and by this repo's own `/commission/` page, which publishes Table 1. | Text corrected: the rate card is public; what is unresolvable is each listing's category (FLG-021). |
| E-F3 | c4e71983's open item: competitor benchmark had "no equivalent on `main`". | Surfaced on `reviews.html`, rendered from main's shared `data/competition.json` (S43) so it cannot drift from the `air-fryers.html` category page; per-row official links; prices/ratings withheld by policy (FLG-022). |
| E-F4 | c4e71983's open item: FLG-016 framed the ML bar around Creators API data only. | Widened in `data/flags.json` with the verbatim §5 clause (B3 above). |
| E-F5 | c4e71983's open item: `c4e71983-FLG-12` — disclosure sentence suspected to be FAQ-only. | **Resolved** (B1 above): the sentence is verbatim in the Operating Agreement body §5. |
| E-F6 | Stale open PR #10 (broken links on `disclosure.html`/`executive-summary.html`, >60 min with no commits, CONFLICTING). | Task taken over per the 60-minute rule; both pages re-verified against current `main` (now generated/redirect pages; `check_site.py` and V5 report 0 broken links across the tree); PR #10 closed as superseded with an explanatory comment. |
| E-F7 | `scripts/check_site.py` OFFICIAL_HOSTS did not include `sell.amazon.com` (Amazon-operated official seller education), blocking citation of the ASIN rule page. | Host added with a comment; S45 cites it. `tools/verify_site.py` V4 already matches it via its `amazon.com` pattern. |

Decisions logged (c4e71983 open items):

1. **Commercial snapshot** (`data/c4e71983-commercial-snapshot.json`): stays internal — not
   rendered on any live page — because its price/rating values were hand-captured and
   Participation Requirements 2(b)/6(t)-equivalents (PF-04/PF-05) bar displaying them without an
   API route. Revisit only after Creators API access (FLG-006).
2. **Competitor benchmark**: surfaced with identity + dated rank only; price/rating/review-count
   withheld (FLG-022). Values remain in the capture file.

## E. Irregularities still open (unchanged, non-blocking)

All existing FLG-001–FLG-021 items remain open and published on `/flagged/`, plus the new
FLG-022 and the newer FLG-022–027 items from sessions `a86f1d09`/`51fcb80d`. Nothing in this pass verified any product value: the three submitted identifiers still
select nothing, so product identity, price, rating, review count, commission rate, niche scores
and click/conversion figures remain blank by design across the site.


## F. Merge note (2026-11-14)

While this record was being written, `main` advanced through PRs #18–#25 (sessions `a86f1d09`,
`b8beb448`, `51fcb80d`), which independently published: the display-rules flag (their FLG-022,
kept instead of this session's duplicate), the rank-drift flag (their FLG-025, matching §C1), the
`plpRedirect=mhFallback` correction (their FLG-026, matching the §A observation), the
`air-fryers.html` category page with the same benchmark, and sources S40–S44 (S43 = the Best
Sellers page of §C1). On merge, this session's findings were folded into main's registers
(S45 added; FLG-016 widened; dated notes appended) — see COORDINATION.md Part E for the full
conflict log. Nothing in sections A–E above was changed except the ID remappings marked inline.
