# Verification record — 2026-11-19 · session `6b68afc8`

Scope of this pass: the facts this session published or relied on. Everything else in the tree
keeps its own recorded date; `P26-F05` (structural checks are not a fresh line-by-line verification of
every historical claim) still stands and is not dissolved by this file.

Method: each official page was opened through the sandbox page-fetch tool on 2026-11-19 (UTC).
Quotes below are copied from that returned text, not paraphrased. The register rows in
`data/sources.json` were **not** duplicated for these re-reads — a second row for the same URL was
already flagged as a hygiene problem in an earlier pass (`G0B2-F-10`, unmerged) — so freshness is
recorded here, and in `data/publication.json`'s six `sources[].scope` lines whose `checked_on` is
2026-11-19.

## 1 · Official pages re-read today

| Row | Page | What was read | Load-bearing text as returned |
|---|---|---|---|
| S01 | `affiliate-program.amazon.com/help/operating/agreement` | chunk 1 of 4 (§4–§7) | "You must clearly and prominently state the following, or any substantially similar statement previously allowed under this Agreement, on your Site or any other location where Amazon may authorize your display or other use of Program Content: 'As an Amazon Associate I earn from qualifying purchases.'" · "For the avoidance of doubt … any violation of Section 5 and as specified in the Program Policies will be deemed a material breach of this Agreement." · "We do not make any representation, warranty, or covenant regarding the amount of traffic or commission income you can expect at any time…" |
| S02 | `affiliate-program.amazon.com/help/operating/policies` | chunk 3 of 11 (§1(f)/(g), §2(a), §2(b), §3) | "Special Links enable accurate tracking, reporting, and accrual of commission income. Special Links must use the Associates ID we have assigned to you." · "You must not encourage customers to bookmark your Special Links. All Special Links must be accessed directly from your Site. … you must include your Associates ID or “tag” (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site." · "Under no circumstances may you associate any sub-tag, other ID or reporting provided in connection with the Associates Program with a specific end user of your Site…" · "When linking to pages with Product lists you must have additional original content on your Site that is relevant to the Special Link." · "You must remove from your Site any links and related references to limited time promotions as soon as that promotion on the relevant Amazon Site ends." · "You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product, an Amazon Site, or any of our policies, promotions, or prices." · "…your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API and you comply with the requirements regarding use of Creators API or PA API in the License." · 1(g): no "trademark of Amazon or its affiliates, or a variant or misspelling … in any domain name, subdomain name, in any “tag” or Associates ID, or in any username, group name, or other identifier" |
| S07 / S51 | `ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers` | whole page (dated November 2019) | "Place it so it's **hard to miss**." · "The disclosure should be placed with the endorsement message itself." · "Disclosures are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE." · "You can't talk about your experience with a product you haven't tried." |
| S90 | `developers.google.com/search/docs/crawling-indexing/qualify-outbound-links` (page updated 2025-12-10) | chunk 0 of 2 | "Mark links that are advertisements or paid placements (commonly called *paid links*) with the `sponsored` value." · "Links marked with these `rel` attributes will generally not be followed." |
| S91 | `docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits` | whole page | "GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS)." · "Published GitHub Pages sites may be no larger than 1 GB" · "a *soft* bandwidth limit of 100 GB per month" · "a *soft* limit of 10 builds per hour" |
| S92 | `foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures` (Date Last Reviewed: November 21, 2024) | whole page | "Always use a food thermometer to check whether meat has reached a safe minimum internal temperature…" · chart: poultry 165°F (74°C) · ground meat and sausage 160°F (71°C) · beef/bison/veal/goat/lamb steaks, roasts, chops 145°F (63°C) **Rest time: 3 minutes** · pork steaks/roasts/chops 145°F (63°C) with a 3-minute rest · casseroles and leftovers 165°F (74°C) · fish 145°F (63°C) or until flesh separates with a fork |

These six pages are the entire external basis of the two guides and the decision-desk rows added by
this pass; nothing else was quoted from outside the repository.

## 2 · Product listings re-opened today

The reader pages publish only titles and destination identity, so that is what was re-checked. Prices,
protection-plan prices, star ratings and review counts were visible in the returned pages and were
**deliberately not recorded** — S02's price clause and the site's own prohibition (R2/R11 in
`DESIGN_PROMPT.md`) both forbid publishing them from a page fetch.

| Row | URL fetched | Returned page `<title>` vs `data/publication.json.listing_title` | Breadcrumb |
|---|---|---|---|
| SHOP-01 | `https://www.amazon.com/dp/B0CDY277D3` | **matches** the recorded text, character for character: "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black" | Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers (node 17659096011) |
| SHOP-02 | `https://www.amazon.com/dp/B09B7SB46R` | **matches**: "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included" | same path |
| SHOP-03 | `https://www.amazon.com/dp/B08DKYBTPH` | **one character of drift**: the live title reads "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results …" while the register stores it without the `®` mark. The register text is a transcription, not a byte copy. Recorded here and left as-is, because the words this pass quotes ("4-in-1", "450°F Hi-Fry Option for Crispier Results", "Bake, Dehydrate, Frozen") are identical in both. | same path |
| SHOP-04, SHOP-05 | not re-fetched in this pass | Both thermometer listings were re-opened on 2026-11-19 by session `1c072a7a` and their titles were unchanged there; this pass quotes neither title, so nothing here depends on them. | — |

No submitted `link.amazon/…` short link was followed in this pass: the destination identity is already
registered, and the open question (`P27-Q6` / `FLG-003`) is about **attribution**, which a redirect
cannot answer.

## 3 · Claims this pass made that no source can answer

Recorded so a reader can see the boundary rather than infer one.

- The paths' cost and risk bands are this session's judgement about work and consequence, labelled as
  such on the page; they are not measurements and they cite no third party.
- "In the recommended order" is an editorial recommendation derived from dependencies (what needs
  which access), not from any performance data — there is none.
- The topic list in `DESIGN_PROMPT.md` §8 is explicitly framed as hypotheses about what buyers ask.
  No search volume, no popularity, no trending claim is made or implied anywhere in this pass.
- The measured inventory (120 pages, 120 canonicals, 29 `og:image`, 115 descriptions ≥60 chars,
  16 sitemap URLs, 26 feed entries) counts files in this checkout with the tree's own skip rules; it
  is a repository observation, not a statement about what Google has indexed.

## 3c · Live read-back after merge

PR **#180** merged 2026-11-19T11:22:35Z as `a61c410`; CI `Publication checks` and
`pages build and deployment` both **success** on that SHA. The deployed pages were then fetched and read,
because a `built` status is not a content check: `suggestions/index.html` shows the sequence strip, all
five path cards with their needs/unblocks/cannot-deliver rails and the merged review round;
`guides/how-do-you-know-its-done.html` shows the FoodSafety.gov figures with the attribution and the
21 Nov 2024 source-review date, the three-listing table with "title only" labels, and the
"not a hands-on review" byline. The five quoted temperature figures and both listing feature strings are
on the live page as verified in §1–§2. No price, rating or review count appears.

## 3b · Post-rebase re-check

The push-time base had moved (PRs #173–#176, 130 files). After re-applying this pass onto
`origin/main` at `530d9d9`, the same six official pages were **not** re-fetched again — the rebase
changed no quote, no date and no claim, only which side of a merge each sentence sits on. What was
re-measured instead: the register counts the brief publishes (120 pages, 120 canonicals, 29
`og:image`, 115 descriptions ≥60 characters, 16 sitemap URLs, 26 feed entries, 87 sources, 164 flags),
because PR #176 moved several of them, and the gate set, which has grown the
`owner_input_needed`/`next_action`/`discoveries` requirements described in §5 of the repo review.

## 4 · Gates run on the final tree

`python3 tools/publish.py` — 16 generation steps + 25 release checks, **0 failures**, run twice; the
second run changed nothing tracked (`git diff --exit-code` clean, no untracked additions besides the
ignored preview directory). Includes `tools/check_publication.py` (provenance structure, under-masthead
non-dismissible disclosure, prohibited-figure lint, one canonical + one robots policy per page,
indexable set == sitemap, every guide once in feed and sitemap, dashboard reachability from nav **and**
footer), `tools/verify_site.py` (V1–V7), `tools/link_report.py --strict`, `tools/i2_gate.py`,
`scripts/check_all_links.py`, the sponsored-marking checks and the analytics/collector self-tests.

Machine-readable output: `release-checks-2026-11-19.json`; idempotency result:
`idempotency-2026-11-19.json`.

## 5 · What was **not** verified in this pass

- No real-browser/Chromium or axe re-run: `sessions/1c072a7a/browser_check.cjs` and its pinned
  dependencies were not installed or executed here, so this pass makes **no** accessibility or
  visual-rendering claim of its own. The new path/brief components inherit the shared stylesheet and
  the existing interaction wiring; the automated CSS/HTML/markup gates passed, which is not the same
  as a visual audit.
- No account-side check of any kind (Associates, Search Console, analytics host), so the attribution,
  demand and hosting questions stay open by design.
- No historical register was re-read row by row; inherited rows keep their own dates and advisories.
