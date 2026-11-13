### The rule

Every value on this site is either read verbatim from an official page, or left blank and flagged. Nothing
is inferred, interpolated, averaged, or copied from a third-party blog, price tracker or review
aggregator. Nothing comes from memory.

### What counts as official

An official source is a page published by Amazon on `amazon.com` or `affiliate-program.amazon.com`, or a
page published by the U.S. Federal Trade Commission on `ftc.gov`. The short links supplied in the brief
are recorded as S12 but are treated as an entry point only: they establish what was given, never a
product fact. The product facts come from the pages they redirect to.

### How each link was resolved

Each `link.amazon/<code>` URL was requested and the HTTP redirect followed to its destination on
`amazon.com`. The destination ASIN was read from the resolved URL and confirmed against the product title
on the resolved page. The first link was resolved twice, once early in the work and once later, and
returned the same ASIN both times, which rules out a random or rotating redirect.

### Why the values come from search pages

Amazon renders the price and rating payload of a product detail page with JavaScript. A static read of
`/dp/<ASIN>` returns the page shell, the title and the footer, but not the price. Amazon's own
search-results rendering of the same ASIN at `/s?k=<ASIN>` does return price, list price, promotion
badge, star rating, ratings count, the *bought in the past month* signal and the lowest alternative
offer, for the one matching product. That is an official Amazon page, so it was used, and it is cited as
such on every row.

### What was deliberately left blank

- **Best Sellers Rank** — JavaScript only, not readable from any official static render.

- **Review sentiment and review text** — JavaScript and sign-in gated.

- **Clicks and conversions** — exist only inside a logged-in Associates Central account.

- **Commission rate per ASIN** — Amazon publishes rates by category, not by ASIN.

- **Associates tag** — none exists in this repository.

Each of these renders as an explicit *Unverified* cell, never as a dash that could be mistaken for zero,
and never as an estimate.

### Derived versus verified

Discount depth is computed from two verified prices on the same row and is labelled *derived* everywhere
it appears, because Amazon does not publish it. Commission scenarios on the Commission Model page are
labelled *modelled* for the same reason. Neither is presented as a fact.

### How to check this yourself

Every source is listed on the Sources page with a direct link. The Verification Log lists every field for
every product with its value, its status and the source id that supports it. The underlying data is
`data/products.json` in this repository, which is the same file the site renders from, so the page and the
data cannot disagree.
