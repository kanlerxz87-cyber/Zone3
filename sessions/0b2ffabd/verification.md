# Dated verification record — session `0b2ffabd`, 2026-11-17 (G0B2-T2)

Every row below is something this session read itself on 2026-11-17 through the sandbox fetch tool. The quote
column is what the page returned at that moment. Anything not re-read today is named as inherited, not claimed.
Restricted values (price, star rating, review count, "bought in past month") were **seen** on the listing pages
and deliberately **not transcribed**, because Program Policies 2(b)/6(t) do not allow displaying them without an
Amazon-served link or Creators/PA API data — the rule is quoted in §2.3 below.

## 1. Register rows this record produces

| New source ID | Page read | Where it is used |
|---|---|---|
| S70 | Associates Program Operating Agreement, §5 and §6 (chunk 1 of 4) | disclosure wording; §6 material-breach consequence |
| S71 | Associates Program Policies, Participation Requirements §2(a)/2(b) (chunk 3 of 11) | the six rails of `DESIGN_PROMPT.md`; Q1; Q8 |
| S72 | Associates Program Policies, Commission Income Statement §2 (chunk 1 of 11) | Redirecting Link and malformed-link disqualifications |
| S73 | Google Search Central — Qualify your outbound links to Google | `rel="sponsored"` marking |
| S74 | Google Search Central — Control your snippets in search results | page-level titles/descriptions |
| S75 | Google Search Central — Build and submit a sitemap | sitemap hygiene, Search Console submission |
| S76 | FTC — Disclosures 101 for Social Media Influencers (November 2019) | "hard to miss"; no-experience rule |
| S77 | `link.amazon/B0c8moW59` → `amazon.com/dp/B0DHZTCNR5` | the canonical capture missing from `data/sources.json` |
| S78 | `link.amazon/B0f3GKalj` → `amazon.com/dp/B0DZFD6R9Z` | the canonical capture missing from `data/sources.json` |
| S79 | Google Search Central — What's new (updates page) + the FAQPage doc redirect | "add FAQ schema" is not a ranking play |

## 2. Verbatim, with what was and was not read

### 2.1 Operating Agreement (S70, chunk 1 of 4)

> **5. Identifying Yourself as an Associate**
> "You must clearly and prominently state the following, or any substantially similar statement previously
> allowed under this Agreement, on your Site or any other location where Amazon may authorize your display or
> other use of Program Content: 'As an Amazon Associate I earn from qualifying purchases.'"

> "Except for this disclosure, and other than as required by applicable law, you will not make any public
> communication with respect to this Agreement or your participation in the Associates Program without our
> advance written permission."

> **6. Term and Termination** — "For the avoidance of doubt and without limitation for purposes of the foregoing
> subsection (a) any violation of Section 5 and as specified in the Program Policies will be deemed a material
> breach of this Agreement."

Comparison with the repo: the §5 sentence is **identical** to `data/policy_facts.json` PF-01 and to the string
`DISCLOSURE` enforced by `scripts/check_site.py`, `tools/verify_site.py` and `tools/i2_gate.py`. The page header
("Updated October 15, 2025", as recorded at S49) was not inside the chunk read today, so that date stays an
inherited observation, not a 2026-11-17 one.

### 2.2 Associates Program Policies — Participation Requirements §2 (S71, chunk 3 of 11)

> **2. Links on Your Site — (a) Special Links**
> "After you have applied to the Associates Program, you are permitted to display Special Links on your Site.
> Special Links enable accurate tracking, reporting, and accrual of commission income. Special Links must use the
> Associates ID we have assigned to you."

> **(b) General Requirements Applicable to All Special Links**
> "You must include your Associates ID or 'tag' (appearing as XXXXX-##, or such other format as we may designate)
> as a parameter in the URL of each link you place on your Site to an Amazon Site."
> — matches PF-03 verbatim.

> "You must not encourage customers to bookmark your Special Links. All Special Links must be accessed directly
> from your Site."

> "Upon your request but subject to our approval, we may issue you additional 'sub-tag' Associate IDs that permit
> you to monitor and optimize the performance of your Special Links … Under no circumstances may you associate any
> sub-tag, other ID or reporting provided in connection with the Associates Program with a specific end user of
> your Site (e.g., you may not dynamically assign sub-tags to users as they arrive on your Site for purposes of
> monitoring such users' behavior)."

> "You may add or delete Products (and related Special Links) from your Site at any time without our approval.
> Special Links must link to Products (as defined in the Products Statement). When linking to pages with Product
> lists you must have additional original content on your Site that is relevant to the Special Link. Product
> lists include search results, events (e.g. Prime Day), or a department homepage (e.g. grocery)."

> "You must remove from your Site any links and related references to limited time promotions as soon as that
> promotion on the relevant Amazon Site ends."

> "You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product, an
> Amazon Site, or any of our policies, promotions, or prices."
> — matches PF-10 verbatim.

> "Product prices and availability may vary from time to time. Because prices for and availability of Products
> that you have listed on your Site may change, your Site may only show prices and availability if: (a) we serve
> the link in which that price and availability data are displayed, or (b) you obtain Product pricing and
> availability data via Creators API or PA API and you comply with the requirements regarding use of Creators API
> or PA API in the License."
> — matches PF-04 / PF-44 / PF-54 verbatim.

> "In addition, if you choose to display prices for any Product on your Site in any 'comparison' format (including
> through the use of any price-comparison tool or engine) together with prices for the same or similar products
> offered through any web site or other means other than an Amazon Site, you must display both the lowest 'new'
> price and, if we provide it to you, the lowest 'used' price at which the Product is available on the Amazon Site."

Also in the same chunk (suitability list): content must not "be directed toward children or knowingly collect,
use, or disclose personal information from children under 13 years of age", and must not "include any trademark
of Amazon or its affiliates … in any domain name, subdomain name, in any 'tag' or Associates ID, or in any
username, group name, or other identifier on any social networking site".

### 2.3 Associates Program Policies — Commission Income Statement §2 (S72, chunk 1 of 11)

> "(e) any Product purchased by a customer who is referred to an Amazon Site by a link that sends users
> indirectly to an Amazon Site via an intermediate site, without requiring the customer to click on a link or
> take some other affirmative action on that intermediate site (a 'Redirecting Link'),"

> "(g) any Product purchase that is not correctly tracked or reported because the links from your site to the
> relevant Amazon Site are not properly formatted,"

> "(c) … (a 'Prohibited Paid Search Placement')" — bidding on Amazon-marked keywords disqualifies the purchase.

Why it matters here: the site's outbound links are the owner's `link.amazon/<code>` short links, and the question
whether that path is a Redirecting Link is exactly what remains open (FLG-003 family; the recorded decision is
"do not claim the supplied short links are invalid"). The clause text is now re-read and dated.

### 2.4 FTC — Disclosures 101 for Social Media Influencers (S76, whole page, 1 chunk, "November 2019")

> "Make sure people will **see and understand** the disclosure." / "Place it so it's **hard to miss**." /
> "The disclosure should be placed with the endorsement message itself." /
> "Disclosures are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or
> videos, or anywhere that requires a person to click MORE." /
> "So are terms like 'advertisement,' 'ad,' and 'sponsored.'" /
> "You can't talk about your experience with a product you haven't tried."

Matches the corrected quotes recorded in Part D of `COORDINATION.md` and in `data/policy_facts.json`. It is also
the reason `SUG-05` (conversion CTAs) cannot be shipped by decoration: a "Buy now" affordance needs the
disclosure beside it, not only in the footer.

### 2.5 Google Search Central — `rel="sponsored"` (S73, whole page, 1 chunk; "Last updated 2025-12-10 UTC")

> "Mark links that are advertisements or paid placements (commonly called *paid links*) with the `sponsored` value."
> "Links marked with these `rel` attributes will generally not be followed."

### 2.6 Google Search Central — snippets and meta descriptions (S74, chunks 0–1; "Last updated 2026-04-20 UTC")

> "Identical or similar descriptions on every page of a site aren't helpful when individual pages appear in
> search results. Wherever possible, create descriptions that accurately describe the specific page."
> "product pages might have the key bits of information—price, age, manufacturer—scattered throughout a page. A
> good meta description can bring all this data together."
> "Keep in mind that meta descriptions comprised of long strings of keywords don't give users a clear idea of the
> page's content, and are less likely to be displayed as a snippet."

Note the tension the second quote creates for this project: Google's example puts a price in a meta description;
Amazon's 2(b) (S71) forbids showing a price unless Amazon serves the link or the data comes from the API.
Resolution recorded in the design prompt: page-level descriptions name what the page checked and where, never a
price. This is a documented choice, not an oversight — see G0B2-F-07 in the flag register.

### 2.7 Google Search Central — sitemaps (S75, chunks 0–1)

> "All formats limit a single sitemap to 50MB (uncompressed) or 50,000 URLs."
> "unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent
> directory. Therefore, a sitemap posted at the site root can affect all files on the site, which is where we
> recommend posting your sitemaps."
> "Include the URLs in your sitemap that you want to see in Google's search results."
> "Google ignores `<priority>` and `<changefreq>` values."
> "Google uses the `<lastmod>` value if it's consistently and verifiably (for example by comparing to the last
> modification of the page) accurate."
> "If your CMS generates an RSS or Atom feed, you can submit the feed's URL as a sitemap … keep in mind that this
> feed only provides information on recent URLs." / "Google accepts RSS 2.0 and Atom 1.0 feeds."

### 2.8 FAQ rich results (S79)

`https://developers.google.com/search/docs/appearance/structured-data/faqpage` now serves the Search Central
"What's new" page at the anchor `#removing-faq-rich-result`, under the June 2026 entry titled
"Removing documentation for the FAQ rich result feature". Read 2026-11-17. Consequence recorded: the question-
shaped guides are kept because readers ask questions, not because a FAQ rich result is available; no `FAQPage`
JSON-LD is added. (I did not read the removal paragraph's body text — only the entry title and the redirect — so
no body wording is quoted.)

## 3. The two unregistered links, captured by this session

| # | Submitted link | Final URL observed 2026-11-17 | `<title>` as served | Breadcrumb as served |
|---|---|---|---|---|
| 4 | `https://link.amazon/B0c8moW59` | `https://www.amazon.com/dp/B0DHZTCNR5?...` | "Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill BBQ Camping, Black : Home & Kitchen" | Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat |
| 5 | `https://link.amazon/B0f3GKalj` | `https://www.amazon.com/dp/B0DZFD6R9Z?...` | "Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3: Home & Kitchen" | Home & Kitchen › Kitchen & Dining › Kitchen Utensils & Gadgets › Thermometers & Timers › Meat |

Both destinations match what session `aebf0747` recorded on the same date in `sessions/aebf0747/intent-record.json`
and in the shop layer's own register; this session's captures are what put them in `data/sources.json` at all.
The submitted codes are 9 characters, so they are not ASINs (the 10-character rule is documented in
`data/policy_facts.json` and cited at S31; not re-read today). **Whether these listings are the products that
were intended remains unconfirmed** — the destination of a redirect is an observation, not proof of intent.

Editorially relevant, and stated only because the listing says it: the CHEF iQ title itself lists "Air Fryer"
among the uses ("BBQ, Grill, Oven, Smoker, Air Fryer"). That is the listing's own wording and is the only basis
on which a thermometer guide may be linked to the air-fryer cluster; anything beyond it would be invented.

## 4. Inherited, explicitly not re-read today

Creators API `GetItems` / `ItemIdType` (S06, S31), the Standard and Onsite commission tables (S25, S26), the
enrolment and dormancy help topics (S28, S29), and the three air-fryer short links (S11–S13 / S52–S55 / S63–S69).
Those rows keep their own dates; nothing in this record restates them as a 2026-11-17 observation.
