# Archive — session `c4e71983`

This directory is the **unchanged** working tree of session `c4e71983`, which worked in parallel from
baseline commit `ed1a796` on branch `arena/c4e71983-zone3`.

It is archived here because `main` already carried a canonical site and data schema owned by sessions
`26634cd5`, `66a80e53`, `7f84fea4`, `33226b37` and others. Every file this session produced at the
repository root or in `assets/`, `tools/`, `data/`, `research/` collided with that canonical set.
Rather than overwrite it, the branch was reset onto `main` and reduced to non-overlapping,
additive contributions. **Nothing from `main` was overwritten or discarded.**

The original commits remain in git history and on the backup branch
`backup-c4e71983-4dc3f8be` (tip `4dc3f8be87b28f460fcca4aac70b5ed8d76692b4`).

## What is in here

| Path | What it is |
| --- | --- |
| `index.html` and 12 sibling root pages | A complete standalone dashboard this session built |
| `categories/` | Four category pages (Air Fryers + three sub-categories) |
| `content/` | Page bodies (HTML fragments) |
| `site/style.css`, `site/app.js` | Stylesheet and client JS |
| `tools/build_site.py` | Generator, and a link-integrity gatekeeper |
| `data/` | This session's `products.json`, `competitors.json`, `flags.json`, `sources.json`, `derived_links.json` |
| `research/` | This session's verification log, compliance research, niche analysis |
| `EXECUTIVE-SUMMARY.md`, `README.md`, `COORDINATION.md` | This session's versions, superseded by `main`'s |
| `.github/workflows/validate.yml` | Validation workflow this session wrote |

The site is browsable at `archive/c4e71983/index.html`. **It is a research archive, not the live
site** — it is not styled like `main`'s site and is not wired into `main`'s navigation.

## What was carried forward instead

| Additive contribution | Path on `main` |
| --- | --- |
| Commercial snapshot (prices, ratings, badges, velocity) with exact capture timestamps | `data/c4e71983-commercial-snapshot.json` |
| Competitor benchmark set, official Best Sellers ranks 1–6 | `data/c4e71983-competitors.json` |
| Source register for this session | `data/c4e71983-sources.json` |
| Line-by-line verification record | `research/c4e71983-verification-log.md` |
| Commercial snapshot narrative | `research/c4e71983-commercial-snapshot.md` |
| Niche and competition analysis | `research/c4e71983-niche-competition.md` |
| Executive summary | `docs/executive-summary-c4e71983.md` |

Session entry, task rows, ID mapping and the conflict log are appended to `COORDINATION.md`.

## Note on prices

The archived dashboard displays prices that were captured by hand from Amazon search-result pages.
Amazon's Program Policies (Participation Requirements §2(b)) permit price display only if Amazon
serves the link or the data came from Creators API / PA API. Those prices are evidence, not
publishable figures. See `c4e71983-FLG-01` in `COORDINATION.md`.
