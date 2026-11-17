# Verification log — session `2f181cd9` (2026-11-17)

Branch `arena/2f181cd9-zone3`, base `fedc9f66` (main, PR #134 merged).

## Method and its limits

Every URL below was fetched live on 2026-11-17 through the page-fetch tool. Command-line
fetches to `amazon.com` and `link.amazon` were refused at the connection layer in this
session's sandbox, so no `curl`-style check was possible; earlier sessions recorded the
same restriction (`scripts/build_site.py`, verification coverage note). Nothing here is
inferred: a value is either seen on the page that was fetched or left blank and flagged.

The tool returns the final URL after redirects, the served page title and the page body.
Three things were recorded per fetch: the final URL, the title, and the visible category
breadcrumb where the page had one.

## Link resolution (all five links)

| # | Submitted link | Direct `/dp/<identifier>` check | Observed destination | Observed on | Source |
|---|---|---|---|---|---|
| P1 | `link.amazon/B04G1MEwY` | Page Not Found (2026-11-14) | `B0CDY277D3` — CHEFMAN 6 Quart Dual Basket Air Fryer Oven | 2026-11-17 | S76, S14, S08 |
| P2 | `link.amazon/B02NbDxp3` | Page Not Found (2026-11-14) | `B09B7SB46R` — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 2026-11-17 | S77, S15, S09 |
| P3 | `link.amazon/B00hJ57DV` | Page Not Found (2026-11-14) | `B08DKYBTPH` — Chefman Air Fryer 8 Qt TurboFry 4-in-1 | 2026-11-17 | S78, S16, S10 |
| P4 | `link.amazon/B0c8moW59` | Page Not Found (2026-11-17) | `B0DHZTCNR5` — ThermoMaven 1 Sec Professional Digital Meat Thermometer | 2026-11-17 | S70, S72, S74 |
| P5 | `link.amazon/B0f3GKalj` | Page Not Found (2026-11-17) | `B0DZFD6R9Z` — CHEF iQ Sense Smart Wireless Meat Thermometer, Gen3 | 2026-11-17 | S71, S73, S75 |

The first three destinations are identical to every capture since 2026-11-13 (five
sessions including this one). P4 and P5 are first observations: no earlier session had
these links, because the brief that supplied them was first given to this session.

### The finding

Three destinations sit under `Home & Kitchen > Kitchen & Dining > Small Appliances >
Fryers > Air Fryers` (browse node 17659096011). Both new destinations sit under
`Home & Kitchen > Kitchen & Dining > Kitchen Utensils & Gadgets > Thermometers & Timers >
Meat` (browse node 289810). Recorded as F-2F-01 and published as an owner decision
(SUG-2F-01) rather than acted on, because no source read in this project states the
owner's intent for any of the five links.

### Why the identifiers are not ASINs

Amazon defines an ASIN as a *10-character alphanumeric unique identifier assigned by
Amazon* (Creators API, GetItems, ItemIdType table, read 2026-11-17, S82). All five
identifiers are nine characters, and `amazon.com/dp/<identifier>` returns Amazon's Page
Not Found page for each of them. The nine-character tokens are short-link identifiers;
the listings they open are observed destinations, not confirmed identities.

## Policy pages re-read this session

| Page | What was read | Result | Source |
|---|---|---|---|
| Operating Agreement | Section 5 disclosure sentence; Section 6 material-breach clause | Verbatim, unchanged | S79 |
| Program Policies | Participation Requirements 1, 2(b), 6(t), 6(v), 6(w), 6(y) | Verbatim, unchanged | S80 |
| Standard Commission Income Statement | Table 1 | Kitchen 4.50%, Home 3.00%, All Other Categories 4.00% | S81 |
| Creators API GetItems | ItemIdType (ASIN definition) | "10-Character alphanumeric unique identifier assigned by Amazon" | S82 |

Quotes are stored in `data/2f/verification.json` and rendered on
`sessions/2f181cd9/index.html`. Earlier sessions' quotes are kept in
`data/policy_facts.json` with their own dates; this session did not overwrite them.

### What was deliberately not verified

* Per-product commission rate. Table 1 names categories, but no official page read in
  this project maps a browse node to a Table 1 category, so no rate is stated for any of
  the five listings (F-2F-04, question Q2F-04).
* Prices, star ratings and review counts. Participation Requirements 2(b) and 6(t) bar
  displaying them without an Amazon-served link or API data; neither exists here.
* Account status, API credentials and the Associates tag. All are behind the Associates
  login, which no session in this project has.

## Gates run on the final tree

| Gate | Result |
|---|---|
| `python3 scripts/check_site.py` | OK — 36 pages, 5 products, 75 sources, 118 flags |
| `python3 scripts/check_all_links.py` | 0 errors — 167 html pages, 192 distinct external URLs |
| `python3 scripts/build_sitemap.py --check` | sitemap.xml covers every live page (78 pages, 0 extra entries) |
| `python3 tools/verify_site.py` | VERIFY PASS — 121 pages, 2043 table rows |

The `sources.html` rows for S70, S71 and S76–S78 are reported by `verify_site` as
carrying no link to an official host, because those sources are the `link.amazon` short
links themselves. The report is informational and inherited; each of those rows is
always rendered next to the `amazon.com` destination page it opens.
