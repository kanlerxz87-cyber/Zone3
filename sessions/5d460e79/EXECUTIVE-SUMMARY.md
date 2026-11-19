# Executive summary — Zone3 Kitchen, session 5d460e79 (19 November 2026)

This is the short version of what this session found, fixed, and could not settle.
It replaces no earlier record; the full line-by-line audit is in
`sessions/5d460e79/audit-2026-11-19.md` and the shared board is `COORDINATION.md` (Part 5D4).

---

## 1. The one that mattered most

**No link on the site carried the Associates tracking ID.**

The site presented five Amazon products and earned nothing attributable from any of them. The
build did not merely omit the tag: `tools/build_shop.py` failed the build if a `tag=` appeared in
any link, so the omission was enforced. 1,491 product links across 81 pages were affected.

Program Policies, Participation Requirements 2(b), read live on 2026-11-19, requires the
Associates ID or "tag" as a parameter in the URL of *each* link placed on the site to an Amazon
Site. That is a rule, not an optimisation.

**Fixed.** Every product link the site emits now goes directly to
`https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` and is marked `rel="sponsored"`.
1,499 links carry the tag; 0 conflicts. A foreign tag is reported and never overwritten.

**Still not claimed.** That the tag is enrolled on an account, or that Amazon credits the click.
Both need a logged-in Associates workflow. They stay flagged.

## 2. A compliance question the owner has to settle

The supplied `https://link.amazon/...` links resolve through a **third-party redirect chain**
carrying a `linktw.in` token, and the site's own pages cite `linktw.in` as the shortener.
Participation Requirements 6(v) forbids obscuring the site containing Special Links by Redirecting
Links. This is now `5D4-F-01` on the Flagged for Review page.

It is recorded as a question, **not** a verdict. The links are not called invalid, and FLG-003
stays unresolved exactly as the brief instructs.

## 3. Numbers the site published that were false

| Page said | Register held |
|---|---|
| 6 buyer guides | 8 |
| 9 decision-readiness questions | 24 (32 after upstream's later batch) |
| "the current six guides" | 8 |
| "FIVE PRODUCTS" in a heading | 5 links, 0 intent-confirmed products |

Every one was a numeral typed into the generator. **Fixed:** all counts derive from
`data/publication.json`, and a release gate now fails if a typed numeral returns to prose or if a
rendered figure disagrees with the register. Both were proved to fire by reintroducing the defect.

## 4. Two URLs that did the same job

`index.html` and `shop/index.html` were **65 % the same words**, both `index,follow`, both in the
sitemap — two pages competing for the same queries with the same copy. The front page is now an
editorial front page: one teaser line per product with the deciding question and a direct tagged
CTA, with the full cards living only in the catalogue. **Measured distinctness: 20.4 %.**

**A defect I introduced and caught:** removing the duplicate cards also removed the only Amazon
links from the front page. Reachability is now itself a gate — the build fails if any product lacks
a tagged, sponsored link on `index.html`. Distinctness must never be bought with reachability.

## 5. A feed that contradicted the sitemap

`feed.xml` carried 27 items while `sitemap.xml` listed 16 pages. 18 feed items pointed at
`noindex,follow` archive pages the sitemap deliberately skips. A subscriber and a crawler were
being shown two different sites. **Fixed:** 9 items, every one now present in the sitemap, gated.

## 6. The suggestions desk now closes its loop

The page asked 32 questions and put a 4-way `<select>` on every card, but a reviewer's choice had
nowhere to become a decision. A new `#decision-record` section states the five fields a decision
must carry — Decision, Date, Decided by, Evidence, what would change it — each with its official
basis, names the register that holds decided items, and offers a copy-ready template. It still
implements nothing when read.

## 7. What is still open, and who can close it

| Open item | Who can close it | Why it cannot be closed here |
|---|---|---|
| Is the tracking ID enrolled on the account? | Owner, in Associates Central | Needs a logged-in account. |
| Which of the five products is intended per link? | Owner states it | A redirect is an observation, not an intent. The intended-ASIN field stays blank. |
| Does the `linktw.in` chain credit this account? | Owner, in Associates Central | Ownership of the redirect chain was not tested. |
| Is production analytics running? | Owner supplies a durable HTTPS host | Code is built and locally testable; no host was given. |
| Is Search Console connected? | Owner | Needs the owner's Google account. |
| Which questions actually bring search visitors? | Measured query data | No Search Console report exists. No traffic claim is made. |
| Are these the products' real attributes? | Hand-on testing or permitted API data | No testing was performed. Prices, ratings and review counts stay blank. |

## 8. Where to review it

- **Flagged for review:** `flagged.html` (research flags) and `shop/flagged/index.html` (shop
  flags, 29 items including the new `5D4-F-01`).
- **Suggestions and the decision record:** `suggestions/index.html`.
- **Audit and verification:** `sessions/5d460e79/audit-2026-11-19.md`.
- **Shared board and conflict log:** `COORDINATION.md`, Part 5D4.

## 9. What was not done, stated plainly

No product was purchased, no account was touched, no API was called, no traffic figure, ranking,
conversion score or revenue forecast is presented, and no product fact beyond listing wording is
asserted. The site is honest about an empty evidence base; it is not yet a proven earner.

**Release status:** `python3 tools/publish.py` — 46 commands, 0 failed, deterministic rebuild.
