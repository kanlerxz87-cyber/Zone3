# Session 4b0e3c7e — verification and change record (2026-11-19)

Branch `arena/4b0e3c7e-zone3`, base `0273fb400165d231261fd675431ce88f9fe54769` (`main`, the
merge of PR #198). Everything below was measured on that tree or read from the publisher's own
page in this session. No account, login, API key, Search Console property or Associates report
was used, and no claim below depends on one.

---

## 1. What was checked before starting

| Check | How | Result |
|---|---|---|
| Baseline build | `python3 tools/publish.py` | 41 commands, 0 failed |
| Other sessions' claims | `gh pr list`, `gh api .../commits?sha=…` | PR #192 last commit `2026-11-19T13:01:06Z`, 8 h 50 min stale at claim, `mergeStateStatus: DIRTY`; taken over for one defect only (see COORDINATION Part 4b0e3c7e). PR #199 (`arena/a4f9ee45-zone3`) active at claim; its file list respected — no overlap. |
| Feed vs sitemap | compared every `<link>` in `feed.xml` with `<loc>` in `sitemap.xml` | 28 feed items, 18 pointing at `noindex,follow` pages the sitemap excludes |
| Associates ID on links | regex census of every `<a href>` to `amazon.com` | 8 tagged links site-wide (2 legacy pages); 1,483 product links without the tag |
| `tag=` build rule | read `tools/build_shop.py` | the build **failed** on any `tag=` — the omission was enforced |

---

## 2. Official sources read live in this session

### 2.1 Amazon Associates Program Policies

URL <https://affiliate-program.amazon.com/help/operating/policies>. The page header reads
**"Updated: April 14, 2026."** Read in this session: the Commission Income Statement
(sections 1–6), Participation Requirements sections 1, 2 (all), 3, 6 and the Products Statement
opening. The clauses this change depends on, quoted verbatim:

**Participation Requirements 2(a) — Special Links**

> "Special Links must use the Associates ID we have assigned to you."

**Participation Requirements 2(b) — General Requirements Applicable to All Special Links**

> "Special Links may be created by you or made available to you by us. … All Special Links must
> be accessed directly from your Site. For example, you must include your Associates ID or "tag"
> (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of
> each link you place on your Site to an Amazon Site."

**Participation Requirements 6(v) and 6(w)** — the two clauses about obscured and unclear links:

> "(v) You will not cloak, hide, spoof, or otherwise obscure the URL of your Site containing
> Special Links (including by use of Redirecting Links) …"

> "(w) You will not use a link shortening service, button, hyperlink or other ad placement in a
> manner that makes it unclear that you are linking to an Amazon Site."

**Commission Income Statement 5** (read for context, not relied on):

> "Associates' tags should only be used to benefit from Amazon Associates commissions."

### 2.2 What the sources do **not** say

- No public page was found that validates a tag against an account without logging in. The tag's
  **account assignment is therefore unverified** and is not claimed anywhere on the site.
- No public page settles whether a research citation to an Amazon browse page must carry the tag.
  2(b) says "each link you place on your Site to an Amazon Site"; this session reads that as
  covering product links and records the citation boundary as an open item for the owner
  (`FLG-S12`) rather than asserting an answer.

### 2.3 Sources already in the register, not re-read in this session

The operating agreement update date (October 15, 2025), the FTC 2019 disclosure guide and the
Google `rel="sponsored"` guidance are unchanged by this work and keep their recorded dates. The
`rel="sponsored"` token was preserved on every link this session touched and is asserted by
`scripts/mark_sponsored.py --check`, which passes.

---

## 3. What changed, and why each change follows from a source

| Change | Basis |
|---|---|
| Every `/dp/` and `/gp/product/` link with a **10-character ASIN** now carries `?tag=shopnow047c-20` | 2(a) and 2(b), above |
| The five public buy buttons now point at the tagged product page instead of the submitted `link.amazon` short link | 2(b) (tag present in the URL) and 6(v)/6(w) (destination visible, no unexplained shortening). The short links are **not** called invalid: `FLG-003` stays unresolved and `FLG-S11` records the replacement |
| The five submitted short links stay on the page as the observed record | keeps `FLG-002`/`FLG-003` evidence intact; the brief says not to call them invalid |
| 9-character `/dp/` links are **not** tagged | a 9-character token is not an ASIN (Creators API `ItemIdType=ASIN`); those links are the page-not-found evidence and are labelled as such. `FLG-S13` |
| Browse / search / Best-Sellers / help links are **not** tagged | they are citations, not product promotions; recorded as an owner decision (`FLG-S12`) |
| A foreign `?tag=` is never overwritten | it is the other associate's identifier; the tool reports it instead. Today's tree has none |
| `tools/build_shop.py` no longer fails on `tag=` | that assertion contradicted 2(b); it is replaced by the positive assertion "every 10-character product link carries this tag" |
| `feed.xml` items must point at pages `sitemap.xml` offers for indexing | consistency: the site cannot ask search engines to ignore a page and advertise it to feed readers in the same breath. 28 → 10 items; the newest guide (19 Nov 2026) is kept |

---

## 4. Measurements after the change

| Measure | Before | After |
|---|---|---|
| Product-detail links carrying the tag | 8 | **1,111** |
| Product-detail links missing the tag | 1,483 | **0** |
| 9-character token links wrongly tagged | 0 | **0** |
| Browse/search/help citation links tagged | 0 | **0** (boundary held) |
| Submitted `link.amazon` anchors preserved | 414 | **414** |
| RSS items | 28 (18 pointing at `noindex` pages) | **10 (0 noindex)** |
| Sitemap URLs | 18 | 18 (unchanged) |
| Release commands | 41 | **44** (adds the tagger write pass, its `--check` and its 14-rule test) |

Integrity probes on the built tree: double tags `0`; malformed `?&tag=` `0`; tag on a
`link.amazon` URL `0`; disclosure sentence on the front page `2` (strip + footer).

---

## 5. Release checks

- `python3 tools/publish.py` — **44/44 pass**, run twice; a third full run left
  `git status --porcelain` byte-identical (same SHA-256 of the file list), so the build is
  deterministic.
- `python3 tools/publish.py --check` (no builders) — **27/27 pass**.
- `python3 tools/attach_associates_tag.py --check` — `OK: every product-detail link carries
  tag=shopnow047c-20 (21,873 links inspected; foreign tags: 0)`.
- `python3 scripts/test_attach_associates_tag.py` — 14 rules pass, including "a foreign tag is
  preserved", "a 9-character token is not tagged", "a `link.amazon` short link is not touched",
  and "a second run changes nothing".
- Local preview (`python3 -m http.server`): `/`, `/shop/`, `/shop/products/`, `/guides/`,
  `/guides/where-does-the-probe-go.html`, `/intent-record/`, `/suggestions/`, `/flagged/`,
  `/shop/flagged/`, `/feed.xml`, `/sitemap.xml` all return 200.

## 6. What this session did not do

- It did not log in to Associates Central, generate a Special Link, open a tracking report, or
  verify that `shopnow047c-20` is the owner's enrolled account. That remains the owner's step
  (`0C4-F-04`, `FLG-S05`), and the site says so.
- It did not re-read or re-date the operating agreement, FTC or Google sources it did not need.
- It did not touch: `data/sources.json`, `data/products.json`, `data/flags.json`,
  `data/policy_facts.json`, `assets/`, `guides/`, `index.html` by hand (regenerated only through
  its generator), or any file claimed by PR #199.
- It did not adopt PR #192's other work, and makes no claim about whether it is correct.
