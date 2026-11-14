# Verification log — session `54ce6a2b` (2026-11-14)

Repository: `kanlerxz87-cyber/Zone3` · Branch: `arena/54ce6a2b-zone3` · Base: `f618a53`
(This branch was rebased onto `9024b99` during this session; see the 54C conflict log in
`COORDINATION.md`.)

## Scope and method

Every fetch below was made by this session on **2026-11-14**, independently of the earlier
sessions' logs. Nothing here is taken from another session's record; where a result agrees with
the repo's stored value that agreement is noted, and where it differs it would be flagged.

Method: each URL was fetched and read directly. A claim is marked **confirmed** only when the
wording quoted by the repository appears in the page text returned to this session. No value was
inferred, and no value that the page did not state was recorded.

Fetches were made through the session's fetch tool, not an HTTP client, because this sandbox's
outbound network is limited to `github.com`, `codeload.github.com`, `api.github.com`,
`registry.npmjs.org`, `pypi.org` and `files.pythonhosted.org`.

---

## 1. The three submitted links — re-fetched

| # | Submitted URL | Resolved to (`url` returned by the fetch) | Page title as served | Verdict |
|---|---|---|---|---|
| 1 | https://link.amazon/B04G1MEwY | `https://www.amazon.com/dp/B0CDY277D3?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-0740a2e990c9bbb3&channelId=704&plpRedirect=mhFallback` | "Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen" | **Confirmed** — matches `data/products.json` P1 `redirect_observed` |
| 2 | https://link.amazon/B02NbDxp3 | `https://www.amazon.com/dp/B09B7SB46R?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-3541f5edba6b914c&channelId=704&plpRedirect=mhFallback` | "Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen" | **Confirmed** — matches P2 |
| 3 | https://link.amazon/B00hJ57DV | `https://www.amazon.com/dp/B08DKYBTPH?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-507e2d3d167072eb&channelId=704&plpRedirect=mhFallback` | "Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen" | **Confirmed** — matches P3 |

Note on the `btn_ref=srctok-…` parameter: its value differs on every fetch (session-scoped). The
**page id** in the path — `B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH` — is stable across this
session's fetch and every fetch recorded in the repository since 2026-11-13.

### Category breadcrumb (also confirmed on all three)

`Home & Kitchen › Kitchen & Dining › Small Appliances › Fryers › Air Fryers` — read from the
breadcrumb of each of the three destination pages.

**Not established by any of these fetches:** whether the three destinations are the products the
site owner intended. Nothing on an Amazon page states that. This remains `FLG-002`.

---

## 2. Control checks — the raw token is not a product page

| URL | Result | Verdict |
|---|---|---|
| https://www.amazon.com/dp/B04G1MEwY | "Page Not Found" | **Confirmed** (S08) |
| https://www.amazon.com/dp/B02NbDxp3 | "Page Not Found" | **Confirmed** (S09) |
| https://www.amazon.com/dp/B00hJ57DV | "Page Not Found" | **Confirmed** (S10) |

This is the control that shows the 9-character token is a short-link id, not an ASIN: the same
string that resolves through `link.amazon` does not resolve as a product identifier on its own.

---

## 3. ASIN definition — Creators API `GetItems`

Source: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items
(section *ItemIdType Parameter*), read 2026-11-14.

Returned verbatim:

> **ASIN** | Amazon Standard Identification Number: 10-Character alphanumeric unique identifier
> assigned by Amazon. For more details, see ASIN

**Confirmed.** `B04G1MEwY`, `B02NbDxp3` and `B00hJ57DV` are 9 characters each. Each is therefore
not an ASIN. The repository's `FLG-001` and `data/products.json` `link_id_length: 9` are correct.

---

## 4. Operating Agreement

Source: https://affiliate-program.amazon.com/help/operating/agreement, read 2026-11-14.

| Claim | Page text returned | Verdict |
|---|---|---|
| Last-updated date | "**Updated:** October 15, 2025 (Current Associates, see what's changed.)" | **Confirmed** |
| Required disclosure, §5 | "You must clearly and prominently state the following, or any substantially similar statement previously allowed under this Agreement, on your Site or any other location where Amazon may authorize your display or other use of Program Content: **"As an Amazon Associate I earn from qualifying purchases."**" | **Confirmed verbatim** |
| Reviews for compensation | Opening paragraph: "…Content you post on the Amazon.com website must abide by Amazon's Community Guidelines, including the prohibition of customer reviews that are created, edited, or removed in exchange for compensation." | **Confirmed — text present.** This settles the earlier disagreement on the board: session `7f84fea4` withdrew PF-14 saying the text was "not found in any section read"; session `3ead7ac8` (3E-CR-03) corrected that. This session's independent fetch finds the sentence in the page's opening paragraph, i.e. **3E-CR-03 is right and the withdrawal was wrong.** |

---

## 5. Program Policies — Participation Requirements

Source: https://affiliate-program.amazon.com/help/operating/policies, section
*Associates Program Participation Requirements* → **6. Content on your Site**, read 2026-11-14.

| Item | Page text returned | Verdict |
|---|---|---|
| 6(t) | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API and you comply with the requirements for Creators API and PA API described in the License." | **Confirmed verbatim** |
| 6(w) | "You will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site." | **Confirmed verbatim** |
| 6(y) | "Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality." | **Confirmed verbatim** |
| 6(v) | "You will not cloak, hide, spoof, or otherwise obscure the URL of your Site containing Special Links (including by use of Redirecting Links)…" | **Confirmed verbatim** |
| 6(s) | "You will not artificially generate clicks or impressions on your Site or create Sessions on an Amazon Site, whether by way of a robot or software program or otherwise." | **Confirmed verbatim** |

These four items are the basis on which the site withholds prices, star ratings and review
counts. The policy text supports that decision: 6(t) permits star ratings **only** when obtained
through the Creators API or PA API, and this build has no API credentials.

### Commission Income Statement — §6 payment (read 2026-11-14)

"We will pay Standard Commission Income and Special Commission Income in the default currency for
an Amazon Site approximately 60 days following the end of each calendar month in which they were
earned…"

Payment Minimum Chart as returned: Option 1 (Direct Deposit) **10 USD** minimum; Option 2 (Gift
Card) **10 USD** minimum / **2000 USD** maximum; Option 3 (Check) **100 USD** minimum;
**Check Processing Fee 15 USD**.

**Confirmed** — matches the executive summary §2.

---

## 6. Standard Commission Income Statement — Table 1

Source: https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ, read 2026-11-14.
The page renders **without a sign-in**, which confirms the correction already recorded on the site
(as `V-F1`): the earlier text saying all rate data was sign-in gated was wrong. Only the
per-account `/help/operating/schedule` page (S03) is gated.

Rows returned (relevant extract):

| Product Category | Fixed Commission Income Rates |
|---|---|
| Luxury Beauty, Luxury Stores Beauty, Amazon Explore | 10.00% |
| Digital Music, Physical Music, Handmade, Digital Videos | 5.00% |
| **Physical Books, Kitchen, Automotive** | **4.50%** |
| Amazon Fire Tablet Devices, … Handbags & Accessories | 4.00% |
| Toys, Furniture, **Home**, Home Improvement, … Baby Products, Amazon Coins | 3.00% |
| PC, PC Components, DVD & Blu-Ray | 2.50% |
| Televisions, Digital Video Games | 2.00% |
| Amazon Fresh, … Health & Personal Care | 1.00% |
| Gift Cards; … Amazon Pay Places | 0.00% |
| All Other Categories | 4.00% |

**Confirmed: Kitchen 4.50%.** Note that the same table lists **Home at 3.00%**, and the observed
breadcrumb for all three listings is *Home & Kitchen › … › Air Fryers*. Which of the two rates
Amazon applies to a given ASIN is decided by Amazon and is not published per-ASIN, so the
per-product commission cell stays blank. That is `FLG-005` / `FLG-013` and is correct.

---

## 7. What this session did **not** verify

* Prices, star ratings, review counts and "bought in past month" badges. These are visible on the
  pages fetched, but publishing them would breach Participation Requirements 6(t) and 2(b), which
  are quoted verbatim above. They are withheld by design.
* Per-product commission rate (not published per-ASIN by Amazon — see §6).
* Clicks, conversions and revenue (available only inside a logged-in Associates account).
* Whether `link.amazon` redirects without an affirmative click (`FLG-003`; requires a logged-in
  Associates account to test).

---

## 8. Repository-side checks run on this branch

| Check | Command | Result |
|---|---|---|
| Site structure | `python3 scripts/check_site.py` | OK — 12 pages, 3 products, 51 sources, 66 flags |
| Row provenance | `python3 tools/verify_site.py` | PASS — 70 pages, 1,223 rows, 1,022 with official source, 388 flagged, 82 repo-anchored, 0 advisories |
| Dangling source/flag refs | `python3 tools/link_report.py --strict` | exit 0 |
| Internal + external links | `python3 scripts/check_all_links.py` | 116 pages, 0 errors |
| Sitemap coverage | `python3 scripts/build_sitemap.py --check` | exit 0 — 65 pages covered, 0 extra entries |
| Marketing generator | `python3 scripts/build_marketing.py` | built 7 pages, 13 sourced claims, idempotent on re-run |
| Conflict markers | `grep -c '^<<<<<<< \|^>>>>>>> ' COORDINATION.md` | 0 |
