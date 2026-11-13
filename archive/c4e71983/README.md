# Zone3 — Amazon affiliate research platform

A GitHub Pages dashboard for an Amazon Associates affiliate project built around three supplied
product links. All three links were resolved and verified; all three turned out to be air fryers.

**Live site:** `https://kanlerxz87-cyber.github.io/Zone3/`

This repository's GitHub Pages is a *legacy* branch build (source branch `main`, path `/`), so Pages
serves the **repository root**. `tools/build_site.py --publish-root` generates into `docs/` and then
copies the tree to the root, so the site is live with no repository-settings change. `docs/` is kept
as the clean build output; the root copies are what Pages serves.

---

## What is in here

| Path | Contents |
| --- | --- |
| `data/` | The verified dataset. `products.json`, `competitors.json`, `flags.json`, `sources.json`, `derived_links.json` |
| `content/` | Long-form page bodies (HTML fragments) |
| `site/` | `style.css`, `app.js` |
| `tools/build_site.py` | Static site generator **and** link-integrity gatekeeper |
| `docs/` | Clean generated output (source of truth for the build) |
| `/` (root) | Published copies served by GitHub Pages — written by `--publish-root` |
| `research/` | `verification-log.md`, `compliance.md`, `niche-analysis.md` |
| `EXECUTIVE-SUMMARY.md` | The executive summary |
| `COORDINATION.md` | Shared task board for parallel agent sessions |

## Build

```bash
python3 tools/build_site.py                    # regenerate docs/
python3 tools/build_site.py --check            # validate only, write nothing
python3 tools/build_site.py --publish-root     # regenerate docs/ and copy to the repo root
```

The build **fails** if:

- any external absolute URL is not in `data/sources.json` or `data/derived_links.json`, or
- any internal `href` / `src` does not resolve to a file the build produces, or
- any page is missing the affiliate disclosure banner.

That means a stray unverified URL or a broken link cannot silently ship.

## Verification standard

1. Sources must be official — Amazon.com, Amazon Associates Central, or a regulator such as the FTC.
   Third-party blogs were read for orientation but never used as a source for a value.
2. A page must have actually been retrieved in this session. Nothing is cited from memory.
3. If a value cannot be read from an official page, the cell is left blank and flagged. Nothing is
   inferred, estimated, interpolated or carried across from a similar product.
4. Volatile values carry the timestamp of the page they came from. Prices and ratings were captured
   from Amazon search pages whose `qid` parameter decodes to the true request time.
5. Every table row links to the official page that backs it.

## The three products

| Supplied link | ASIN | Product | Price at capture |
| --- | --- | --- | --- |
| `link.amazon/B04G1MEwY` | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | $79.93 |
| `link.amazon/B02NbDxp3` | B09B7SB46R | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | $149.99 |
| `link.amazon/B00hJ57DV` | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | $79.91 |

Captured 2026-11-13, 22:33–22:37 UTC, from `amazon.com`. They change continuously — re-check the
linked source before acting on any figure.

## Read this before publishing anything

Three items block revenue, and they are all on the [Flagged for Review](flagged.html) page:

- **FLAG-01** — prices were captured by hand; Amazon permits price display only if Amazon serves the
  link or the price came from Creators API / PA API.
- **FLAG-05** — none of the links carries an Associates tag, so no commission can accrue.
- **FLAG-16** — training ML models on Amazon Program Content requires Amazon's express prior written
  approval, which directly constrains the "AI-powered" part of the brief.

Also open: **FLAG-02** (live promotion badges must be removed when the promotion ends), **FLAG-13**
(Amazon requires original content before approving a site), and **FLAG-06** (the operator is in
Norway, which is not in the Associates country list, and GDPR / ePrivacy apply).

## Disclaimer

Amazon, the Amazon logo and all product names are trademarks of Amazon.com, Inc. or its affiliates.
This project is not endorsed by or affiliated with Amazon. As an Amazon Associate this site would
earn from qualifying purchases.
