# Verification Log

Line-by-line record of every check performed for this deliverable. Each entry states the
command or page, the observed result, and the conclusion drawn. Nothing in the published
tables exists that is not backed by an entry here or by an official policy citation.

**Method.** Only primary/official hosts were admitted: `amazon.com`,
`affiliate-program.amazon.com`, `sell.amazon.com`, `ftc.gov`. Search engines were used to
*locate* official documents only; a snippet was never treated as evidence.

---

## A. Product link verification (Task 1)

| # | Check | Input | Observed | Conclusion |
| --- | --- | --- | --- | --- |
| A1 | Character count | `B04G1MEwY` | `9` | Fails ASIN format rule |
| A2 | Character count | `B02NbDxp3` | `9` | Fails ASIN format rule |
| A3 | Character count | `B00hJ57DV` | `9` | Fails ASIN format rule |
| A4 | Format rule | — | *"ASIN … is a unique 10-character alphanumeric code assigned to every product listed in the Amazon store"* — https://sell.amazon.com/blog/what-is-an-asin (Amazon, Jun 4 2025) | 10 chars required; rule is Amazon's own |
| A5 | Prefix pattern | all three begin `B0` | consistent with Amazon's stated "typically starts with B0" | Prefix fine; **length** is the defect |
| A6 | Direct probe | `https://www.amazon.com/dp/B04G1MEwY` | Amazon error page: *"Sorry! We couldn't find that page."* | No listing exists |
| A7 | Direct probe | `https://www.amazon.com/dp/B02NbDxp3` | same error page | No listing exists |
| A8 | Direct probe | `https://www.amazon.com/dp/B00hJ57DV` | same error page | No listing exists |
| A9 | **Control probe** | `https://www.amazon.com/dp/B0CDY277D3` | serves a real product page (CHEFMAN 6-Qt air fryer) | Probe detects resolvable ASINs → A6–A8 are not tooling artefacts |
| A10 | Redirect trace | `https://link.amazon/B04G1MEwY` | → `amazon.com/dp/B0CDY277D3?...channelId=704&plpRedirect=mhFallback` | Fallback route, not a deep link |
| A11 | Redirect trace | `https://link.amazon/B02NbDxp3` | → `amazon.com/dp/B09B7SB46R?...plpRedirect=mhFallback` (Emeril Lagasse 26QT) | Different product per input |
| A12 | Redirect trace | `https://link.amazon/B00hJ57DV` | → `amazon.com/dp/B08DKYBTPH?...plpRedirect=mhFallback` (Chefman 8 Qt) | Different product per input |
| A13 | DNS | `link.amazon` | resolves to `18.172.170.20/.59/.77/.98` (AWS range) | Host is real & Amazon-served → defect is the **identifier**, not the domain |
| A14 | DNS | `amzn.to` | resolves to `67.199.248.12/.13` | Third-party shortener range, not an Amazon block — relevant to Part. Req. 5(w) |
| A15 | DNS | `www.amazon.com`, `affiliate-program.amazon.com` | resolve normally | Environment has outbound DNS; A6–A9 valid |

**Decision.** All three rows rejected at intake. 12 attribute fields × 3 SKUs = **36 cells
left blank and flagged.** Landing-page titles from A10–A12 were recorded *as evidence of the
failure* and are **not** used as product data anywhere.

---

## B. Compliance verification (Task 3)

Every statement below was read from the live page on 2026-11-13.

| # | Claim published on the site | Source (fetched) | Verified |
| --- | --- | --- | --- |
| B1 | Required disclosure is exactly *"As an Amazon Associate I earn from qualifying purchases."*, must be "clearly and prominently" | `/help/operating/agreement` §5 | ✔ |
| B2 | Omission of §5 is a deemed **material breach** | Agreement §6 last paragraph | ✔ |
| B3 | Amazon may permanently cease **all** commission income for a violation, whether or not related | Agreement §2 | ✔ |
| B4 | Amazon customers are not your customers; you must not handle their contacts | Agreement §3 | ✔ |
| B5 | Community Guidelines incorporated, incl. ban on reviews made for compensation | Agreement preamble | ✔ |
| B6 | Content disclaimer text (verbatim, all caps) | `/help/operating/policies` IP License §2(k) | ✔ |
| B7 | Price/availability disclaimer text + adjacent timestamp requirement, with Amazon's own example string | IP License §2(i) | ✔ |
| B8 | Images may **not** be stored; other content ≤24h; ASINs indefinitely | IP License §2(h) | ✔ |
| B9 | Client applications may not store/cache Program Advertising Content | IP License §2(h) | ✔ |
| B10 | 40 KB payload ceiling; rate-spec limits | IP License §2(j) | ✔ |
| B11 | No reverse engineering / model-or-weight derivation from API | IP License §2(g) | ✔ |
| B12 | Agent Terms: definition of Agent; `Agent/[name]` in User-Agent; no human mimicry; no CAPTCHA solving; truthful answers; no circumvention; Amazon may limit access | IP License §4(a)–(c) | ✔ |
| B13 | Price tracking / price alerting prohibited | Part. Req. 5(y) | ✔ |
| B14 | No link shortener or unclear destination | Part. Req. 5(w) | ✔ |
| B15 | No cloaking/obscuring URL; no Redirecting Links | Part. Req. 5(v); CIS 2(e) | ✔ |
| B16 | No artificially generating clicks/sessions via robot or software | Part. Req. 5(s) | ✔ |
| B17 | No framing Amazon (incl. WebView) | Part. Req. 5(n) | ✔ |
| B18 | No pop-up / pop-under / transitional / layer ads with links | Part. Req. 5(o) | ✔ |
| B19 | No Special Links in content placed on an Amazon Site (review, forum, Wish List, guide) | Part. Req. 5(p) | ✔ |
| B20 | No bidding on "amazon"/"kindle"/any Amazon Mark; misspellings named | Part. Req. 5(f); CIS 2(c) | ✔ |
| B21 | Reviews/star ratings only if obtained via Creators API or PA API | Part. Req. 5(t) | ✔ |
| B22 | No self-purchase or purchase by relatives/employees/contractors; no resale | Part. Req. 5(u) | ✔ |
| B23 | No incentive/reward/rebate for using Special Links | Part. Req. 5(g) | ✔ |
| B24 | No interception of forms submitted to Amazon; no customer account data | Part. Req. 5(h), 5(i) | ✔ |
| B25 | No modifying/suppressing any Amazon Site button, link or feature | Part. Req. 5(j) | ✔ |
| B26 | No using Program Content to promote non-Amazon products; Excluded Products | Part. Req. 5(z) | ✔ |
| B27 | No bookmarking encouragement for Special Links | Part. Req. 2(b) | ✔ |
| B28 | Tag `XXXXX-##` required as URL parameter; sub-tags may not be per-user dynamic | Part. Req. 2(b) | ✔ |
| B29 | Prices shown only if Amazon serves the link or from Creators/PA API | Part. Req. 2(b) | ✔ |
| B30 | Comparison layouts must show lowest **new** and lowest **used** | Part. Req. 2(b) | ✔ |
| B31 | Expired promotions must be removed as soon as they end | Part. Req. 2(b) | ✔ |
| B32 | No inaccurate/overbroad/deceptive claims (64 GB vs 128 GB example) | Part. Req. 2(b) | ✔ |
| B33 | Product lists (search results, events, dept. homepages) need additional original content | Part. Req. 2(b) | ✔ |
| B34 | Site must contain original content; third-party reuse needs significant commentary/analysis/transformation | Part. Req. 1 | ✔ |
| B35 | Unsuitable-site list (a)–(h), incl. child-directed and under-13 data | Part. Req. 1(a)–(h) | ✔ |
| B36 | Session = 24 h, ends on any non-digital order or another associate's link | CIS §1(b) | ✔ |
| B37 | Cart may be completed ≤89 days after click; ship+pay ≤180 days | CIS §1(b)(iii) | ✔ |
| B38 | Qualifying Revenue = amount received less shipping, gift wrap, handling, taxes, service charges, credits, rebates, card fees, bad debt | CIS §1(c) | ✔ |
| B39 | Disqualified: post-termination, cancelled/returned/refunded, Prohibited Paid Search, search-engine links, Redirecting Links, malformed links, unapproved mobile-app links, Bounty, subscriptions, pre-orders | CIS §2(a)–(k) | ✔ |
| B40 | Payment ~60 days after month end; three payment options | CIS §6 | ✔ |
| B41 | US payment minimums 10 USD deposit / 10 USD gift card (2,000 max) / 100 USD check + 15 USD fee | Payment Minimum Chart | ✔ |
| B42 | 3 years inactivity → accrued income withholdable, 7 days' notice | CIS §6 | ✔ |
| B43 | Rounding to nearest currency unit → effective rate may differ from rate card | CIS §6 | ✔ |
| B44 | Programme free to join; **no** authorised paid set-up or consulting business | Part. Req. 1 | ✔ |
| B45 | Commission "up to 10%"; differs by category; paid ≈60 days | https://affiliate-program.amazon.com/ | ✔ |
| B46 | Per-category rate card **not** publicly retrievable | `/help/operating/schedule` → redirects to `amazon.com/ap/signin` | ✔ (negative) |
| B47 | Agreement updated **October 15, 2025**; Policies updated **April 14, 2026** | page headers | ✔ |

---

## C. Architecture verification

| # | Claim | Source | Verified |
| --- | --- | --- | --- |
| C1 | PA-API 5.0 deprecated; replaced by Creators API | https://webservices.amazon.com/paapi5/documentation/ (serves deprecation notice) | ✔ |
| C2 | Legacy PA-API 5 calls → `HTTP 403`, `com.amazon.paapi5#AccessDeniedException` | same page, quoted response body | ✔ |
| C3 | Creators API = REST; four operations (SearchItems, GetItems, GetVariations, GetBrowseNodes) | `/creatorsapi/docs/en-us/introduction` | ✔ |
| C4 | SDKs: Node.js, Python, PHP, Java | same | ✔ |
| C5 | Prerequisite: Associates enrolment in target marketplace | same | ✔ |
| C6 | Prerequisite: ≥10 qualifying sales in past 30 days for PA API access through Creators API | same | ✔ |
| C7 | Register in Associates Central; generate credentials | same | ✔ |
| C8 | No trend / competitor-count / conversion operation exists in the documented API | operation table, C3 | ✔ (negative) |

---

## D. FTC verification

| # | Claim | Source | Verified |
| --- | --- | --- | --- |
| D1 | Material connection must be disclosed clearly and conspicuously | https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | ✔ |
| D2 | *"if a disclosure is needed in one post for a brand, it's probably needed in all posts"* | same | ✔ |
| D3 | *"Each new endorsement made without a disclosure could be deceptive"* | same | ✔ |
| D4 | Where audience awareness is hard to determine, *"we recommend disclosure"* | same | ✔ |
| D5 | Non-US publishers are covered where U.S. reach is reasonably foreseeable; other countries have analogous rules | same | ✔ |
| D6 | Merely posting a product image can be an endorsement | same | ✔ |
| D7 | A positive review that also lists negatives is still an endorsement | same | ✔ |
| D8 | Disclosing a brand relationship once (e.g. a profile badge) is insufficient | same | ✔ |

---

## E. Repository & deployment verification

| # | Item | Method | Result |
| --- | --- | --- | --- |
| E1 | Baseline commit | `git log --oneline` | `ed1a796 Initial commit` only |
| E2 | Tracked files at baseline | `git ls-tree -r --name-only` | `README.md` (7 bytes, `# Zone3`) |
| E3 | `COORDINATION.md` at baseline | `cat` | **absent** → created this session |
| E4 | Working tree at branch creation | `git status` | clean |
| E5 | Branch | `git branch --show-current` | `arena/3c6cba43-zone3` |
| E6 | Pages config | `gh api repos/…/pages` | `build_type=legacy`, `source={main,/}`, `https_enforced=true`, `html_url=https://kanlerxz87-cyber.github.io/Zone3/` |
| E7 | Pages workflow | `gh api repos/…/actions/workflows` | `pages-build-deployment` present, 1 run |
| E8 | Claim push | `git log origin/arena/3c6cba43-zone3` | `f7db7c5` coordination claim |
| E9 | Build gate | `python3 tools/build_site.py` | passes only when **every** row has a source, a flag, or an existing repo anchor |
| E10 | Output gate | `python3 tools/verify_site.py` | V1–V7 over emitted HTML |

---

## F. Items deliberately left unverified (no official source found)

Recorded so that "blank" is demonstrably *earned*, not laziness.

| Field | Why no value exists here |
| --- | --- |
| Product title / brand / category for all 3 SKUs | Identifier does not resolve (A6–A8); no official record to read |
| Price / lowest new / lowest used | Only obtainable via Creators API (B29) — no credentials, no valid ASIN |
| Star rating / review count | Only displayable if API-sourced (B21) — same blocker |
| Availability | Same as price (B29) |
| Variations | `GetVariations` needs a valid parent ASIN |
| Per-category commission rate | Rate card behind sign-in (B46) |
| Per-product commission | Derived from the above two rows; both unavailable |
| "Trending" score | No official Amazon trend metric for affiliates (C8) |
| "High-converting" score | No official Amazon conversion metric for affiliates (C8) |
| Competition density | No official competitor-count endpoint (C8) |
| Clicks / conversions / EPC | No campaign exists; Amazon is the system of record and reports in-account only |
| Ranked niche list | Four of six scoring inputs unavailable; no imputation (see `tools/niche_score.py`) |

**Total: 12 field families, 36 cells, all blank, all flagged, none guessed.**

---

## G. Corrections made during verification

Recording these matters more than getting them right silently:

| Draft | Issue found | Corrected to |
| --- | --- | --- |
| "`link.amazon` is not an Amazon domain" | A13 disproved it — the host resolves from Amazon/AWS infrastructure | "The host is live and Amazon-served; the **identifier** is the defect" (FLG-001…003 rewritten) |
| "PA-API 5.0 is the only sanctioned data source" | C1/C2 supersede it | "Creators API is the sanctioned path; PA-API 5 is deprecated and returns 403" (FLG-014 added) |
| Guessed help URL `…/help/node/topic/GRXPHTNBHVPA7WA5` for the Agreement | Returned Amazon's 404 page | Replaced with the canonical `/help/operating/agreement`, which was fetched in full |
| Task board initially marked all tasks `done` | Written before the work existed | Reset to `in progress`/`unclaimed`, updated only as each task actually completed |
| Self-referential rows citing no source | Build gate G1 rejected 12 such rows | Each anchored to a repository file that the gate verifies exists |
