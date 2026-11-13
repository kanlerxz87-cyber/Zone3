# Northstar — Amazon affiliate research dashboard

A lightweight static dashboard for transparent product research and affiliate editorial planning. It currently contains the three Amazon short links supplied by the project owner. Product identity and listing details are intentionally unverified and blank pending official listing review.

## Pages
- `index.html` — overview and executive summary
- `products.html` — product research table
- `guides.html` — editorial workflow and disclosure resources
- `review.html` — flagged items and source links

## Local preview
Open `index.html` in a browser, or run `python3 -m http.server 8000` from the repository root.

## Deployment
`.github/workflows/pages.yml` deploys the static site to GitHub Pages when pushed to `main` or manually dispatched. Enable GitHub Pages with GitHub Actions in repository settings. The workflow checks local links and uploads the project files.

## Limitations
This is a static research interface, not a live AI or affiliate analytics platform. It has no Amazon API integration, automated product discovery, content generation backend, affiliate link management, click/conversion tracking, or optimization engine. Do not treat blanks as zero. Review the product links, official Amazon Associates terms, and relevant disclosure obligations before publishing affiliate content.

See [COORDINATION.md](COORDINATION.md) for verification and review notes.
