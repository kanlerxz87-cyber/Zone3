# Session `6f16ee11` — independent line-by-line verification, 2026-11-19

Branch: `arena/6f16ee11-zone3` (base `0273fb4`, the tip of `main` at session start).
Scope: re-verify the load-bearing policy claims the live site rests on, against the official
page each one cites, fetched live in this session. No product fact beyond listing wording is
re-asserted here; no price, rating, review count, traffic, demand, conversion or revenue value
is claimed.

Method: each claim below was fetched directly from the official host with `fetch_page` and read
against the register's recorded wording. Where a claim could not be fetched, it is marked
`not re-fetched` and left at its recorded date rather than re-dated or re-claimed.

## Live official fetches performed this session

| # | Official source | What was read and confirmed | Outcome vs register |
|---|---|---|---|
| V1 | [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (chunk 0–1) | Header **"Updated: October 15, 2025"**. §1: Special Links must "properly use the special 'tagged' link formats we provide". §4: "We do not make any representation, warranty, or covenant regarding the amount of traffic or commission income you can expect at any time." §5: "You must clearly and prominently state ... 'As an Amazon Associate I earn from qualifying purchases.'" §6: "any violation of Section 5 and as specified in the Program Policies will be deemed a material breach of this Agreement." | **Confirmed.** Matches register sources `amazon-agreement` and `S95` wording and dates. |
| V2 | [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (chunk 0–5) | Header **"Updated: April 14, 2026"**. Participation Requirements **1(f)** child-directed ban; **1(g)** no Amazon trademark or variant in any domain, subdomain, tag/Associate ID, or social username. **2(a)** "Special Links must use the Associates ID we have assigned to you." **2(b)** "you must include your Associates ID or 'tag' (appearing as XXXXX-## ...) as a parameter in the URL of each link you place on your Site to an Amazon Site"; no bookmarking inducement; sub-tag must not be associated with a specific end user; original content on listing-list pages; promotion-removal duty; no inaccurate/overbroad/misleading claims; price display only via an Amazon-served link or Creators/PA API. **6(t)** no customer reviews or star ratings without Creators/PA API. **6(v)** "You will not cloak, hide, spoof, or otherwise obscure the URL of your Site containing Special Links (including by use of Redirecting Links) ...". **6(w)** no link-shortening that obscures the Amazon destination. | **Confirmed.** Matches register `amazon-policies` wording and the 2(a)/2(b)/6(v) clauses PR #192 relies on. |
| V3 | [FTC: Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | "Place it so it's **hard to miss**"; "The disclosure should be placed **with the endorsement message itself**"; disclosures likely missed if only on an About page or at the end of a post; "**You can't talk about your experience with a product you haven't tried**"; page dated **November 2019**. | **Confirmed.** Matches register `ftc`. |
| V4 | [Google Search Central: Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | `rel="sponsored"` marks links that are "advertisements or paid placements"; marked links "will generally not be followed"; page **"Last updated 2025-12-10 UTC"**. | **Confirmed.** Matches register `google-links`. |
| V5 | [GitHub Docs: GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | "GitHub Pages is **not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions** or providing commercial software as a service (SaaS)." 1 GB published-site limit; soft 100 GB/month bandwidth; soft 10 builds/hour. | **Confirmed.** Matches register `github-limits` and the P26-Q8 / P27-Q2 hosting caveat. |

## Claims checked line by line

| Claim | Register source | Official source read | Result |
|---|---|---|---|
| The required disclosure sentence and "clearly and prominently" placement | `amazon-agreement`, `S95` | Operating Agreement §5 (V1) | **Verified** — exact sentence and placement wording present. |
| A §5 violation is a material breach | `amazon-agreement` | Operating Agreement §6 (V1) | **Verified**. |
| No traffic or income representation | `amazon-agreement` | Operating Agreement §4 (V1) | **Verified**. |
| Special Links must use the assigned Associates ID | `amazon-policies` | Policies 2(a) (V2) | **Verified**. |
| Each link to an Amazon Site must carry the tag as a URL parameter | `amazon-policies` | Policies 2(b) (V2) | **Verified** — and see the irregularity below. |
| No Amazon trademark in domain/tag/username | `amazon-policies` | Policies 1(g) (V2) | **Verified**. |
| No reviews/ratings without Creators/PA API | `amazon-policies` | Policies 6(t) (V2) | **Verified**. |
| No obscuring the Special Link URL via Redirecting Links | `amazon-policies` | Policies 6(v) (V2) | **Verified** — the clause behind FLG-003's unresolved status. |
| FTC: disclosure hard to miss, with the endorsement, no untried-experience talk | `ftc` | FTC Disclosures 101 (V3) | **Verified**. |
| Paid/product links marked `rel="sponsored"` | `google-links` | Google qualify outbound links (V4) | **Verified**. |
| GitHub Pages is not a commercial-hosting surface | `github-limits` | GitHub Pages limits (V5) | **Verified**. |

## Irregularities found and how they were handled

**IRR-01 — the live product links do not carry the required `tag` parameter (cross-scope, logged not fixed).**
Participation Requirements 2(b), read live (V2), requires the Associates ID/"tag" as a URL
parameter on each link to an Amazon Site. The current live product links render as
`https://link.amazon/<token>` and `https://www.amazon.com/dp/<ASIN>` with no `tag=` parameter.
This is the same finding PR [#192](https://github.com/kanlerxz87-cyber/Zone3/pull/192) (session
`5d460e79`) is implementing via `tools/attach_tag.py`. Per the board's cross-scope rule, this
session **does not edit** the tagging task; it independently confirms the clause is real, logs
the irregularity here, and records a coordination note in `COORDINATION.md`. FLG-003 stays
unresolved exactly as the brief instructs — this session makes no claim that the supplied short
links are valid or invalid.

**IRR-02 — the published anti-slop lint did not cover the live publication (fixed this session).**
The house style is published at `site/style-guide.html` ("the sentences we are not allowed to
write ... and a script that fails the build when a page slips") and the banned hype/trend
phrases are enforced by `tools/cba81fa5_lint.py`, but that lint scans only the `site/` archive.
The **current live publication** pages (`index.html`, `guides/*`, `shop/*`, `about.html`,
`privacy.html`, `suggestions/index.html`, `executive-brief.html`) were scanned for price,
rating, review-count and experience claims by `tools/check_publication.py` — but **not** for the
banned hype/trend phrases. A scan this session found two genuine banned-phrase uses on the live
`about.html`: "another **must-have** list" and "**trending** status". Both were fixed in the
generator source (`tools/build_publication.py`), and a HYPE + TREND scan with the same
use/mention distinction the archive lint uses was added to `tools/check_publication.py` so the
rule now covers the live publication too. See the task board in `COORDINATION.md`.

## Not claimed

No price, rating, review count, availability, traffic, demand, trend, conversion or revenue
value. Intended-ASIN fields remain blank. FLG-003 remains unresolved. The two live fetches
above are the only official sources re-read this session; all other register rows keep their
recorded dates and were not re-dated or re-claimed as re-read.
