# Zone3 — AI-powered Amazon affiliate platform

An affiliate research, analysis and publishing dashboard for three Amazon products supplied as
`link.amazon` short links. Every number on the site is read from an official Amazon or FTC page, or left
blank and flagged.

**Live site:** <https://kanlerxz87-cyber.github.io/Zone3/>
**Status:** merged to `main`, deployed via GitHub Pages (source: `main` branch, path `/`).

## What it does

- Resolves the three supplied short links to real Amazon products and records the resolution.
- Captures the facts Amazon publishes about each product: price, list price, promotion badge, star
  rating, ratings volume, the *bought in the past month* demand signal, and the lowest alternative offer.
- Reproduces Amazon's official Associates commission rate table and the qualifying-purchase rules, and
  models the economics against them.
- Maps every Amazon Associates policy obligation and the FTC disclosure requirement to the exact source
  text.
- Tracks 30 decomposed requirements and 17 flagged irregularities, each with its official source.

## The three products

| Supplied link | Resolves to | Product | Department |
| --- | --- | --- | --- |
| <https://link.amazon/B04G1MEwY> | `B0CDY277D3` | CHEFMAN 6 Qt dual basket air fryer | Home & Kitchen |
| <https://link.amazon/B02NbDxp3> | `B09B7SB46R` | Emeril Lagasse 26QT French door air fryer oven | Home & Kitchen |
| <https://link.amazon/B00hJ57DV> | `B08DKYBTPH` | Chefman 8 Qt TurboFry air fryer | Home & Kitchen |

The supplied codes are 9 characters and mixed case, so they are **not** ASINs — an ASIN is 10
characters. They are short-link slugs that redirect to the products above.

## Read these first

| Document | What it is |
| --- | --- |
| [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) | One-page summary of the build, the findings and the blockers |
| [`COORDINATION.md`](COORDINATION.md) | Shared task board for parallel agent sessions |
| [`docs/RESEARCH.md`](docs/RESEARCH.md) | How the links were resolved and where each value came from |
| [`docs/VERIFICATION.md`](docs/VERIFICATION.md) | Every field, its value, its status and its official source |
| [`docs/FLAGGED.md`](docs/FLAGGED.md) | 17 irregularities, 4 of them blocking, with the policy text |
| [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) | The decomposed requirements list and the automation design |

## Four things block this from being a live Associates property

1. **Prices.** Amazon's Participation Requirements [section 2(b)](https://affiliate-program.amazon.com/help/operating/policies)
   allows a site to show prices only if Amazon serves them, or if they come from the Creators API or
   Product Advertising API. These were captured another way. (`F01`)
2. **Star ratings.** [Section 6(t)](https://affiliate-program.amazon.com/help/operating/policies) says the
   same about customer reviews and star ratings. (`F02`)
3. **The supplied short links.** The Commission Income Statement [section 2(e)](https://affiliate-program.amazon.com/help/operating/policies)
   disqualifies purchases made through a *Redirecting Link*, which is what a `link.amazon/<code>` URL is.
   The site publishes canonical `/dp/<ASIN>` URLs instead. (`F03`)
4. **No Associates tag.** Nothing on the site can currently earn a commission. (`F07`)

None of these block the merge or the deploy. They are published on the site's
[Flagged for Review](flagged.html) page.

## Layout

```
data/              verified data layer — the single source of truth
  products.json      per-field values, each with status + source id
  commission.json    official rate table, bounty events, qualifying-purchase rules
  sources.json       the 12 sources, 11 of them official
  requirements.json  30 decomposed requirements with delivery status
  flags.json         17 irregularities with severity, impact and action
docs/              generated repository documentation
docs/content/      prose rendered into the site (single source, no drift)
tools/
  build.py           generates every HTML page from data/*.json
  gen_docs.py        generates the markdown documents from the same data
  check_links.py     link checker + enforces a source cell on every data row
assets/            one stylesheet, one small vanilla-JS file
*.html             generated site pages (do not hand-edit)
```

## Rebuilding

```bash
python3 tools/build.py      # regenerate every HTML page
python3 tools/gen_docs.py   # regenerate the markdown documents
python3 tools/check_links.py # verify links and per-row source cells
```

All three exit non-zero on failure. No build step, no dependencies beyond Python 3, no framework.

## Verification rule

A value appears only if it was read from a page published by Amazon (`amazon.com`,
`affiliate-program.amazon.com`) or the U.S. Federal Trade Commission (`ftc.gov`). Anything else is left
blank and listed as unverified. Nothing is inferred, interpolated, or taken from a price tracker, review
aggregator or third-party blog.

Amazon, Amazon.com and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. This project
is not endorsed by or affiliated with Amazon.com, Inc.
