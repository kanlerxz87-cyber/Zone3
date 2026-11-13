# Flagged for Review

17 items: **4 blocking**, **7 needing a decision**, **6 informational**.

**Blocking** means the item must be resolved before this site operates as a live Amazon
Associates property. Flagged items do not block the merge or the deploy; they are published so
they can be reviewed after the site is live.

On the site: [Flagged for Review](../flagged.html). Machine-readable version:
[`data/flags.json`](../data/flags.json).

## Summary

| ID | Severity | Item | Source |
| --- | --- | --- | --- |
| `F01` | BLOCKING | Displaying static prices conflicts with Associates Program Participation Requirements section 2(b) | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F02` | BLOCKING | Displaying star ratings conflicts with Associates Program Participation Requirements section 6(t) | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F03` | BLOCKING | The supplied link.amazon short links may be 'Redirecting Links' under Commission Income Statement section 2(e) | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F07` | BLOCKING | No Amazon Associates tag exists, so no commission can accrue | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F04` | REVIEW | The three short-link codes are 9 characters, so they are not Amazon ASINs | [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) |
| `F05` | REVIEW | link.amazon is not a documented Amazon short domain | [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY) |
| `F06` | REVIEW | Amazon does not publish the commission category for an individual ASIN | [S7 — Amazon Associates — Associates Program Standard Commission Income Statement (Table 1)](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| `F08` | REVIEW | Deal badges must be removed the moment the promotion ends | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F09` | REVIEW | Price-tracking and price-alerting functionality is prohibited by default | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F10` | REVIEW | GitHub Pages is a static host, so there is no runtime for automation or AI | _no official source_ |
| `F11` | REVIEW | No PA API / Creators API credentials | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F12` | INFO | Best Sellers Rank was not captured | _no official source_ |
| `F13` | INFO | Ratings counts are Amazon's rounded display values | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) |
| `F14` | INFO | Star histogram and review text were not captured | _no official source_ |
| `F15` | INFO | Clicks and conversions could not be captured | [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies) |
| `F16` | INFO | The price snapshot is a point-in-time capture | [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3) |
| `F17` | INFO | The repository was effectively empty at the start of this session | _no official source_ |

## Detail

### `F01` — Displaying static prices conflicts with Associates Program Participation Requirements section 2(b)

**Severity:** BLOCKING  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Amazon's Participation Requirements section 2(b) states: 'Product prices and availability may vary from time to time. Because prices for and availability of Products that you have listed on your Site may change, your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API and you comply with the requirements regarding use of Creators API or PA API in the License.' The prices on this site were captured by a one-time read of an Amazon page, not served by Amazon and not obtained via PA API / Creators API.

**Impact.** The price columns cannot go live on an Associates property in their current form without risking a breach of the Operating Agreement.

**Recommended action.** Either (1) obtain PA API / Creators API credentials and rebuild the price columns from that feed, or (2) remove price values from the public pages and keep them only in the internal analysis documents until such credentials exist.

### `F02` — Displaying star ratings conflicts with Associates Program Participation Requirements section 6(t)

**Severity:** BLOCKING  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Amazon's Participation Requirements section 6(t) states: 'You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API and you comply with the requirements for Creators API and PA API described in the License.' The 4.2 / 4.3 / 4.4 star values and the 4.8K / 18.3K / 16.8K ratings counts on this site were not obtained through PA API or Creators API.

**Impact.** The rating columns cannot go live on an Associates property in their current form.

**Recommended action.** Same as F01: source them through PA API / Creators API, or remove them from public pages.

### `F03` — The supplied link.amazon short links may be 'Redirecting Links' under Commission Income Statement section 2(e)

**Severity:** BLOCKING  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Commission Income Statement section 2(e) disqualifies 'any Product purchased by a customer who is referred to an Amazon Site by a link that sends users indirectly to an Amazon Site via an intermediate site, without requiring the customer to click on a link or take some other affirmative action on that intermediate site (a "Redirecting Link").' A link.amazon/<code> URL is an intermediate URL that redirects straight through to the product page with no affirmative action by the customer. Separately, Participation Requirements section 6(w) prohibits using 'a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site.'

**Impact.** If the supplied short links are used as the Special Links themselves, resulting purchases are at risk of being disqualified and the commission forfeited.

**Recommended action.** Tag and publish the resolved canonical /dp/<ASIN> URLs (S1, S3, S5) rather than the link.amazon short links. Keep the short links only as the provenance record of what was supplied.

### `F07` — No Amazon Associates tag exists, so no commission can accrue

**Severity:** BLOCKING  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Participation Requirements section 2(b) requires that 'you must include your Associates ID or "tag" (appearing as XXXXX-##, or such other format as we may designate) as a parameter in the URL of each link you place on your Site to an Amazon Site.' No Associates ID is stored in this repository, so every link here is untagged.

**Impact.** Zero revenue until a tag is added. Also blocks the click and conversion tracking requirements (R14, R15).

**Recommended action.** Add the Associates tag to a single config value, then regenerate the links. Do not place a guessed tag into URLs.

### `F04` — The three short-link codes are 9 characters, so they are not Amazon ASINs

**Severity:** REVIEW  
**Source:** [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY)

**Detail.** B04G1MEwY, B02NbDxp3 and B00hJ57DV are each 9 characters. A standard Amazon ASIN is 10 characters. They also contain mixed-case letters, which ASINs do not. They are opaque short-link slugs that happen to begin with 'B0'.

**Impact.** Anyone reading the brief could mistake the codes for ASINs and build the wrong product set. This site resolves them to the real ASINs B0CDY277D3, B09B7SB46R and B08DKYBTPH.

**Recommended action.** Confirm with the link owner that the three resolved products are the intended ones.

### `F05` — link.amazon is not a documented Amazon short domain

**Severity:** REVIEW  
**Source:** [S12 — Short links supplied in the project brief (HTTP redirect resolved to S1 / S3 / S5)](https://link.amazon/B04G1MEwY)

**Detail.** The links resolve today to live amazon.com product pages (verified). However, link.amazon is not among the Amazon short-link domains Amazon documents for public use; Amazon's commonly documented shortener is amzn.to. No official page was found that documents link.amazon as an Amazon-operated shortener.

**Impact.** The redirect behaviour is not contractually guaranteed and could change or be repurposed.

**Recommended action.** Do not depend on the short links for anything except provenance. Use the canonical /dp/<ASIN> URLs (S1, S3, S5) everywhere.

### `F06` — Amazon does not publish the commission category for an individual ASIN

**Severity:** REVIEW  
**Source:** [S7 — Amazon Associates — Associates Program Standard Commission Income Statement (Table 1)](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ)

**Detail.** The official rate table (S7) has a 'Kitchen' row at 4.50% and a 'Home' row at 3.00%. All three products are in the 'Home & Kitchen' department. Amazon does not publish which of those two rows an individual ASIN maps to, and the difference is material (50% more commission on the Kitchen row).

**Impact.** A per-product commission rate cannot be verified from an official source, so it is left blank rather than guessed.

**Recommended action.** Once an Associates tag is connected, read the realised per-order rate from Associates Central reports and backfill this column.

### `F08` — Deal badges must be removed the moment the promotion ends

**Severity:** REVIEW  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Participation Requirements section 2(b): 'You must remove from your Site any links and related references to limited time promotions as soon as that promotion on the relevant Amazon Site ends.' Two of the three products currently carry a promotion badge ('Limited time deal' x2, 'Early Black Friday Deal' x1).

**Impact.** The badge text on this site will become a policy breach as soon as Amazon ends those promotions, which is outside this project's control.

**Recommended action.** Make the badge field a dated, refreshable value driven by a PA API / Creators API feed, or drop the badge column from public pages.

### `F09` — Price-tracking and price-alerting functionality is prohibited by default

**Severity:** REVIEW  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Participation Requirements section 6(y): 'Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality.'

**Impact.** This constrains requirement R4 (analyze pricing) and R16 (continuously optimize). A historical price graph or 'price dropped' alert on the public site is not permitted unless Amazon agrees in writing.

**Recommended action.** Keep price analysis internal (this repository's analysis documents) and do not ship a price-history or price-alert feature on the public site without Amazon's agreement.

### `F10` — GitHub Pages is a static host, so there is no runtime for automation or AI

**Severity:** REVIEW  
**Source:** _no official source_

**Detail.** The site is served as static files from the main branch. There is no server, database, scheduler, or model endpoint. Requirements R1, R2, R3, R8-R12, R14, R15 and R16 (automated research, content generation, click/conversion tracking, continuous optimisation) cannot execute on this host.

**Impact.** The automation layer is specified and scaffolded in docs/REQUIREMENTS.md, but it is not running.

**Recommended action.** Run the automation in a scheduled environment (GitHub Actions is available on this repo) and publish only its static output to Pages, or move to a hosted backend.

### `F11` — No PA API / Creators API credentials

**Severity:** REVIEW  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Both F01 (prices) and F02 (star ratings) have the same compliant fix: source the data through Amazon's Creators API or Product Advertising API. No credentials for either API exist in this repository.

**Impact.** Blocks the compliant path for the two most important data columns on the site.

**Recommended action.** Apply for Creators API / PA API access through Associates Central, then rebuild those columns from the feed.

### `F12` — Best Sellers Rank was not captured

**Severity:** INFO  
**Source:** _no official source_

**Detail.** Amazon renders Best Sellers Rank via JavaScript on the product detail page, and the value could not be read from any official static render. Per the verification rule the field is left blank rather than estimated.

**Impact.** The 'trending product' requirement (R2) relies on Amazon's own 'N bought in past month' signal instead, which was captured for all three products.

**Recommended action.** Source BSR through PA API together with the F01/F02 fix.

### `F13` — Ratings counts are Amazon's rounded display values

**Severity:** INFO  
**Source:** [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3)

**Detail.** Amazon displays '4.8K', '18.3K' and '16.8K' rather than exact counts. These are Amazon's own rounded figures, recorded verbatim, not exact integers.

**Impact.** Any arithmetic on these counts carries the rounding error.

**Recommended action.** None, unless exact counts are needed, in which case source them from PA API.

### `F14` — Star histogram and review text were not captured

**Severity:** INFO  
**Source:** _no official source_

**Detail.** Amazon's review breakdown and review bodies are served via JavaScript and behind sign-in. Per the verification rule these fields are left blank rather than summarised from third-party sources.

**Impact.** Requirement R5 (analyze reviews) is only partly satisfied: rating and volume are captured, sentiment and themes are not.

**Recommended action.** Source review content through PA API, or analyse it via an approved route.

### `F15` — Clicks and conversions could not be captured

**Severity:** INFO  
**Source:** [S8 — Amazon Associates — Program Policies (incl. Associates Program Commission Income Statement, sections 1-4)](https://affiliate-program.amazon.com/help/operating/policies)

**Detail.** Amazon reports click and conversion data only inside Associates Central, behind a logged-in Associates account. No such account is connected, so both fields are blank.

**Impact.** Requirements R14 and R15 are unmet by data; they are specified as build work instead.

**Recommended action.** Connect an Associates account and ingest the reports.

### `F16` — The price snapshot is a point-in-time capture

**Severity:** INFO  
**Source:** [S2 — Amazon search results for B0CDY277D3](https://www.amazon.com/s?k=B0CDY277D3)

**Detail.** All prices and promotion badges were captured on 2026-11-13 from amazon.com. Amazon changes prices frequently and the values will drift.

**Impact.** Stale values on a live page are both a data-quality problem and, per F01, a policy problem.

**Recommended action.** Automate a refresh, or remove the values from public pages.

### `F17` — The repository was effectively empty at the start of this session

**Severity:** INFO  
**Source:** _no official source_

**Detail.** At the base commit ed1a796 the repository contained a single file, README.md, with the text '# Zone3'. There was no prior code, data, or site to review, and no COORDINATION.md existed.

**Impact.** The 'review the repo line by line' requirement reduces to reviewing the initial commit and the files added by this session. Nothing pre-existing was found to be irregular.

**Recommended action.** None.

