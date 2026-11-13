## What is unverified, and why

Every blank cell on this site is a deliberate omission, not a gap in the work. Something is left blank
only when it could not be read from an official Amazon or FTC page.

- **Best Sellers Rank.** Amazon renders BSR with JavaScript on the product detail page. It could not be
  read from any official static render, so it is blank. Amazon's own *N bought in past month* signal is
  used as the demand measure instead, and that was captured for all three products.
- **Commission rate per ASIN.** Amazon publishes rates by category, not by ASIN. Both the Kitchen row at
  4.50% and the Home row at 3.00% are plausible for an air fryer, and the difference is 50% of the
  commission, so guessing would be worse than leaving it blank.
- **Review sentiment.** Amazon's star histogram and review bodies are behind JavaScript and sign-in. Only
  the aggregate star value and the review volume were publicly readable.
- **Clicks and conversions.** These exist only inside a logged-in Associates Central account. No account
  is connected.
- **Associates tag.** None exists in this repository. Every link on the site is untagged, which is stated
  on each product page rather than papered over.

The full field-by-field log is on the **Verification Log** page.
