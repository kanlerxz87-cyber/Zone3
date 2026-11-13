# COORDINATION.md — shared task board

Repo: `kanlerxz87-cyber/Zone3`
Published site: <https://kanlerxz87-cyber.github.io/Zone3/> (GitHub Pages, source = `main` branch, path `/`)

## How to use this file

1. Read the whole file before touching anything.
2. Claim a task by writing your session ID into **Owner** and the files you will touch into **Files**,
   set **Status** to `in progress`, then `git commit && git push` *immediately*.
3. Never edit a file inside another session's claimed **Files** scope. If you need to, add a line to
   the **Cross-session requests** log instead.
4. `git pull --rebase` before every push. Small, frequent commits.
5. On conflict: stop, resolve **without discarding the other session's work**, and log it below.
6. On finish: fill in **Sources**, **Verification performed**, **Irregularities**, set Status = `done`.
7. Status `needs review` = the item is published on the site's **Flagged for Review** page. It does not
   block anything.
8. A claim older than 60 minutes with no commits may be taken over by any session (log the handoff).

## Session registry

| Session ID | Branch | Started | Scope summary |
| --- | --- | --- | --- |
| `3c886b62` | `arena/3c886b62-zone3` | 2026-11-13 | Single-session build: repo review, product research + verification, docs, site, GitHub Pages publish. |

## Task board

| # | Task | Status | Owner | Files |
| --- | --- | --- | --- | --- |
| T1 | Repo review + read every file, flag irregularities | done | `3c886b62` | *(read-only)* `README.md`, `.git` history |
| T2 | Resolve the 3 `link.amazon` short links to canonical Amazon product pages | done | `3c886b62` | `docs/RESEARCH.md` |
| T3 | Capture verified product facts (price, rating, demand signal) from amazon.com | done | `3c886b62` | `data/products.json`, `docs/RESEARCH.md` |
| T4 | Capture official Amazon Associates commission + policy sources | done | `3c886b62` | `data/sources.json`, `data/commission.json` |
| T5 | Capture official FTC disclosure requirement source | done | `3c886b62` | `data/sources.json` |
| T6 | Requirements matrix (decompose the brief into a tracked list) | done | `3c886b62` | `docs/REQUIREMENTS.md` |
| T7 | Verification log — every table row field mapped to an official source | done | `3c886b62` | `docs/VERIFICATION.md`, `data/products.json` |
| T8 | Flagged-for-review register | done | `3c886b62` | `docs/FLAGGED.md` |
| T9 | Site build (landing dashboard + category/product/analysis subpages) | done | `3c886b62` | `index.html`, `products.html`, `categories.html`, `category-home-kitchen.html`, `product-*.html`, `comparison.html`, `commission.html`, `analysis.html`, `compliance.html`, `flagged.html`, `sources.html`, `verification.html`, `executive-summary.html`, `assets/*` |
| T10 | Shared outputs: `index.html` nav + table data + site integration | done | `3c886b62` | `index.html`, `data/*.json`, `assets/app.js` |
| T11 | Link check — no broken internal links, no unverified rows | done | `3c886b62` | *(tooling)* `tools/check_links.py` |
| T12 | PR to `main`, merge, confirm GitHub Pages deploy | done | `3c886b62` | *(git)* |

## Cross-session requests

*(none logged)*

## Conflict log

*(none logged)*

## Sources (all official)

| ID | Source | URL | Used for |
| --- | --- | --- | --- |
| S1 | Amazon product page (CHEFMAN 6 Qt Dual Basket) | <https://www.amazon.com/dp/B0CDY277D3> | Title, department, brand, ASIN |
| S2 | Amazon search result for `B0CDY277D3` | <https://www.amazon.com/s?k=B0CDY277D3> | Price, list price, rating, ratings count, demand signal, offers |
| S3 | Amazon product page (Emeril Lagasse 26QT) | <https://www.amazon.com/dp/B09B7SB46R> | Title, department, brand, ASIN |
| S4 | Amazon search result for `B09B7SB46R` | <https://www.amazon.com/s?k=B09B7SB46R> | Price, list price, rating, ratings count, demand signal, offers |
| S5 | Amazon product page (Chefman 8 Qt TurboFry) | <https://www.amazon.com/dp/B08DKYBTPH> | Title, department, brand, ASIN |
| S6 | Amazon search result for `B08DKYBTPH` | <https://www.amazon.com/s?k=B08DKYBTPH> | Price, list price, rating, ratings count, demand signal, offers |
| S7 | Amazon Associates **Standard Commission Income Statement** | <https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ> | Fixed commission rates by product category; bounty rates |
| S8 | Amazon Associates **Program Policies** (Commission Income Statement sections 1–4) | <https://affiliate-program.amazon.com/help/operating/policies> | Qualifying purchase definition, session windows, disqualified purchases |
| S9 | Amazon Associates **Operating Agreement** (updated Oct 15, 2025) | <https://affiliate-program.amazon.com/help/operating/agreement> | Program terms, compliance obligations |
| S10 | FTC — **Disclosures 101 for Social Media Influencers** | <https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers> | Disclosure (material connection) requirement |
| S11 | Amazon trademark list (US) — referenced by S8 §2(c) | <https://www.amazon.com/gp/help/customer/display.html/?nodeId=200738910/> | Prohibited paid search placement context |
| S12 | `link.amazon` short links supplied in the brief | <https://link.amazon/B04G1MEwY> · <https://link.amazon/B02NbDxp3> · <https://link.amazon/B00hJ57DV> | Short-link → ASIN resolution (HTTP redirect) |

## Verification performed

- Each `link.amazon/<code>` short link was resolved by following the HTTP redirect to a live
  `amazon.com` product page. The first link was fetched twice (start and later) and resolved to the
  **same** ASIN both times, confirming the redirect is stable rather than random.
- Every product value on the site was read from a rendered `amazon.com` page or an
  `affiliate-program.amazon.com` page. Nothing was copied from a third-party blog, price tracker,
  or model memory.
- Values that could not be read from an official page are left **blank** on the site and listed on the
  **Flagged for Review** page with the reason. Nothing is inferred or interpolated.
- Internal links were checked by a script (`tools/check_links.py`) run against the built site.

## Irregularities

See `docs/FLAGGED.md` and the site page **Flagged for Review** (`flagged.html`). Summary:

1. The three short-link codes are **9 characters**; a standard Amazon ASIN is 10. The codes are
   therefore **not** ASINs — they are opaque short-link slugs that redirect to a real ASIN.
2. `link.amazon` is not one of the Amazon short domains documented for public use (`amzn.to` is).
   The redirect works today but is not guaranteed to be stable or owned by Amazon.
3. Amazon does not publish the commission **category** for an individual ASIN. The site therefore
   publishes the official rate table and leaves the per-ASIN rate **unverified**.
4. No Amazon Associates **tag** exists in this repository. All links are untagged, so no commission
   can accrue until a tag is added.
5. Amazon product detail pages serve their price/rating payload via JavaScript and could not be read
   directly; the values on this site were read from Amazon's own search-results rendering of the same
   ASIN, which is an official Amazon page.

## Integration session handoff

Session `3c886b62` performed all tasks including the final integration (T10–T12) because no other
session registered a claim in this file. If a later session needs to change shared outputs
(`index.html` navigation, `data/*.json`, `assets/app.js`), take T10/T11/T12 again, re-run
`tools/check_links.py`, and re-verify before publishing.
