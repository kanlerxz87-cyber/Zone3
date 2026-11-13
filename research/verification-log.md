# Research — Product Verification Log

Session: `session-33226b37-zone3` · Date of checks: **2026-11-13** · Branch: `arena/33226b37-zone3`

> **Integration note (2026-11-13).** This file is the independent verification record of session
> `33226b37-zone3`, merged into the repo after sessions `26634cd5` (PR #1) and `7f84fea4`
> (PRs #5/#6) had already integrated `main`. The canonical ID scheme on `main` is the
> `S01–S29` / `PF-xx` / `FLG-xxx` scheme in `data/*.json`. Mapping of this file's IDs to the
> canonical scheme: S11→PF-18/S18-equivalent (ASIN definition; canonical source is the Creators
> API docs), S12–S14→S08–S10, S15→S27, S16→S24 (FTC 2023 revision), S17→16 CFR 255 (linked
> from S16's page), S18→S01/S07, S19→S28, S20→S29, S21→S02 (Program Policies), S7→S01.
> The canonical site pages are `index.html`, `products.html`, `pricing.html`, `reviews.html`,
> `content.html`, `campaigns.html`, `flagged.html`, `sources.html`, `executive-summary.html`.

Every check below was performed against an official/primary source. Where a value could not be
confirmed from an official source, it is left **blank** and listed on the site's
**Flagged for Review** page. No values were inferred or filled in.

---

## 1. The three provided product links

Provided in the tasking:

1. `https://link.amazon/B04G1MEwY`
2. `https://link.amazon/B02NbDxp3`
3. `https://link.amazon/B00hJ57DV`

### 1.1 Code format check (reproducible)

Official rule: Amazon defines an ASIN as *"a unique 10-character alphanumeric code assigned to
every product listed in the Amazon store."*
Source (Amazon-owned page): https://sell.amazon.com/blog/fba-new-selection-program

| Provided code | Character count | Expected | Result |
|---|---|---|---|
| `B04G1MEwY` | 9 | 10 | FAIL — not a valid ASIN format |
| `B02NbDxp3` | 9 | 10 | FAIL — not a valid ASIN format |
| `B00hJ57DV` | 9 | 10 | FAIL — not a valid ASIN format |

(Counted character-by-character; anyone can reproduce by copying each code into a character counter.)

### 1.2 Direct Amazon catalog lookup (official source: amazon.com itself)

Checked on 2026-11-13 by loading each Amazon product-detail URL directly:

| Code | URL checked | Official result | Source link |
|---|---|---|---|
| `B04G1MEwY` | `https://www.amazon.com/dp/B04G1MEwY` | Amazon's official error page: **"Sorry! We couldn't find that page."** (Page Not Found / Dogs of Amazon) | https://www.amazon.com/dp/B04G1MEwY |
| `B02NbDxp3` | `https://www.amazon.com/dp/B02NbDxp3` | Same official **Page Not Found** error | https://www.amazon.com/dp/B02NbDxp3 |
| `B00hJ57DV` | `https://www.amazon.com/dp/B00hJ57DV` | Same official **Page Not Found** error | https://www.amazon.com/dp/B00hJ57DV |

### 1.3 Control test (validates the lookup method)

To rule out the possibility that every fetch was failing (e.g., bot detection), a known-good
control ASIN was fetched the same way. `B00005N5PF` is Amazon's own published example ASIN
("the ASIN for Hasbro's Monopoly game is B00005N5PF" appears in Amazon's official Seller
Central/Amazon help documentation, e.g. https://www.amazon.com/gp/help/customer/display.html?nodeId=200333520
and Seller Central ASIN help).

| URL checked | Result | Interpretation |
|---|---|---|
| `https://www.amazon.com/dp/B00005N5PF` | Amazon served a **checkpoint interstitial** ("To continue, please click Continue shopping") — **not** the Page-Not-Found error | A cataloged ASIN does **not** return the "Dogs of Amazon" 404. The three provided codes each returned that hard 404, so the 404 results above are meaningful. |

### 1.4 Web search for the codes

Searches for `B04G1MEwY`, `B02NbDxp3`, and `B00hJ57DV` (each in quotes, plus "Amazon" / "ASIN")
returned **zero product-catalog matches** for any of the three codes. Only unrelated results
(e.g., generic searches for "B04" tool-box keys) appeared.

### 1.5 The provided `link.amazon` URLs (observed behavior)

- Fetching `https://link.amazon/B04G1MEwY` did **not** display a product page for that code.
  The request landed on an unrelated Amazon product page (`https://www.amazon.com/dp/B0CDY277D3`,
  a CHEFMAN 6 Quart Dual Basket Air Fryer listing) with fallback parameters
  (`lv=shuf`, `plpRedirect=mhFallback`) — i.e., Amazon's "page you requested could not be shown"
  fallback, not a resolution of the provided code.
- Whether `link.amazon` is an Amazon-operated domain: **UNVERIFIED** — flagged for review.
  Amazon's documented product-link formats are `amazon.com/dp/ASIN` URLs, `amzn.to` short links
  and the Associates linking tools (source: https://affiliate-program.amazon.com/help/operating/policies,
  Participation Requirements §2). No official Amazon documentation for a `link.amazon` link format was found.

### 1.6 Conclusion for the three products

**None of the three products can be identified from an official source.** Therefore, per the
tasking rules ("If a value can't be confirmed from an official source, leave it blank and flag
it as unverified. Never infer or fill in values"):

| Field | Value |
|---|---|
| Product name / title | *(blank — unverified)* |
| Brand | *(blank — unverified)* |
| Category | *(blank — unverified)* |
| Price | *(blank — unverified; see also §3.2 — Amazon policy prohibits hard-coded prices)* |
| Rating / reviews | *(blank — unverified)* |
| Commission rate | *(blank — unverified; see §3.1)* |

All three are listed on the site's **Flagged for Review** page with the source links above.

---

## 2. Repository review (line-by-line)

Checked 2026-11-13, base commit `ed1a796` on `main`:

| Check | Result | Evidence |
|---|---|---|
| Repo contents at base commit | Only `README.md` (7 bytes, contents `# Zone3`). No other files, no docs, no data. | https://github.com/kanlerxz87-cyber/Zone3 (commit `ed1a796`) |
| Git history | Single initial commit `ed1a796` ("Initial commit") | `git log` in local clone; https://github.com/kanlerxz87-cyber/Zone3/commits |
| Remotes | `origin` = https://github.com/kanlerxz87-cyber/Zone3.git | `.git/config` / `git remote -v` |
| GitHub Pages | **Already enabled**: build type `legacy`, deploys from branch `main`, path `/` (repo root). Site URL: https://kanlerxz87-cyber.github.io/Zone3/ | GitHub API `GET /repos/kanlerxz87-cyber/Zone3/pages`; settings page https://github.com/kanlerxz87-cyber/Zone3/settings/pages |
| Irregularities | Repo was empty except for the README — there was **no existing data to verify**. This is logged as informational, not a defect. | — |

---

## 3. Compliance sources (all verified from official pages, 2026-11-13)

### 3.1 Amazon Associates Program (official Amazon pages)

| Fact verified | Exact verified content (condensed, quoted) | Source link |
|---|---|---|
| ASIN definition | ASIN = "unique 10-character alphanumeric code assigned to every product listed in the Amazon store" | https://sell.amazon.com/blog/fba-new-selection-program |
| Associates Program Policies (current version) | Policies page header: "Updated: April 14, 2026" | https://affiliate-program.amazon.com/help/operating/policies |
| Commission session window | A Session begins on the Special Link click and ends at the first of: 24 hours elapsing; customer placing an order; customer clicking another Associate's link | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §1) |
| Cart/purchase window | Purchases via items added to cart during the Session qualify if the order completes **no later than 89 days** after the initial click-through | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §1(b)(i)) |
| New 180-day shipping window (April 2026 update) | "within 180 days of the purchase, the Product is shipped to, streamed or downloaded by, and paid for by the customer" | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §1(b)(iii)); change summary: https://affiliate-program.amazon.com/help/operating/compare |
| Payment timing | Commissions paid "approximately 60 days following the end of each calendar month in which they were earned" | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §6) |
| Payment minimums (US) | Direct deposit min $10; gift card min $10 (max $2000); check min $100 with $15 processing fee | https://affiliate-program.amazon.com/help/operating/policies (Payment Minimum Chart) |
| Required disclosure statement | Operating Agreement §5: "You must clearly and prominently state the following… on your Site: 'As an Amazon Associate I earn from qualifying purchases.'" | https://affiliate-program.amazon.com/help/operating/agreement |
| Disclosure help topic | "you must (1) include a legally compliant disclosure with your links and (2) identify yourself on your Site as an Amazon Associate with the language required by the Operating Agreement" | https://affiliate-program.amazon.com/help/node/topic/GPXFHVYZMTGPUMPE |
| Enrollment gate | "you have 180 days to refer a sale… Your application can be withdrawn if there were not enough qualifying sales for 180 days" | https://affiliate-program.amazon.com/help/node/topic/G7MJTPEP9NC3YKMG |
| Application review | "we require at least three [qualifying sales] within the first 180 days… personal orders do not qualify… All Sites must have robust original content… a good rule of thumb is at least 10 posts" | https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM |
| Original content requirement | Site "must contain original content… Original content utilizing third-party materials must contain significant commentary, analysis, or transformation" | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §1) |
| Price display rule | Site "may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API" | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §2(b)) |
| Truthful claims rule | "You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product" | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §2(b)) |
| Promotional limitations | No offline promotion; Special Links in email/SMS/DM only when solicited (opted in) | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §4) |
| AI / ML restriction | "You will not, without or express prior written approval, use, or allow any third party to use, any Special Links or Program Content to develop machine learning models or related technology." | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §5) |
| Paid-search / trademark rules | No bidding on "amazon"/"Kindle"/Amazon marks or misspellings; no Amazon marks in domains/subdomains/Associate IDs | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §2(c); Participation Requirements §1(g), §6(e)) |
| Disqualified purchases | Includes self-purchases via purchased ads, search-engine-referred links, redirecting links, improperly formatted links | https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement §2) |
| Commission rate card (appendix) | Appendix links "Standard Commission Income" to https://affiliate-program.amazon.com/help/operating/schedule — **that page redirects to a sign-in when not logged in**, so the public rate card could not be verified. Rates left **blank** and flagged. | https://affiliate-program.amazon.com/help/operating/policies (Appendix) |

### 3.2 FTC disclosure law (official .gov sources)

| Fact verified | Source link |
|---|---|
| Endorsements must be honest and not misleading; material connections must be "disclosed clearly and conspicuously"; Guides revised 2023 with new "clearly and conspicuously" definition | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking |
| Guides codified at 16 CFR Part 255 | https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255 (linked from the FTC page above) |
| Amazon's own policies expressly reference the FTC Guides | https://affiliate-program.amazon.com/help/operating/policies (Participation Requirements §3(b)) |

---

## 4. Irregularities flagged (summary)

1. **All three provided ASIN codes are 9 characters** — invalid under Amazon's official 10-character
   definition. Possibly truncated during tasking.
2. **All three codes return Amazon's official "Page Not Found"** at `amazon.com/dp/<code>` (checked
   2026-11-13, with a valid control ASIN proving the method). The products therefore cannot be
   identified, and no product data could be verified.
3. **The provided `link.amazon` URLs do not resolve to product pages for the given codes**; the one
   checked fell back to an unrelated listing. `link.amazon` is not a documented Amazon link format
   in the official Associates Program Policies.
4. **Public commission rate card is account-gated** (`/help/operating/schedule` redirects to sign-in),
   so commission rates are left blank everywhere.
5. **Hard-coding prices would violate Amazon policy** regardless (Participation Requirements §2(b)):
   prices may only be shown via Amazon-served links or PA API data. The site therefore never displays
   prices and instead links to the live Amazon page where a verified product exists.
6. Whether `link.amazon` is Amazon-operated: **unverified**.
