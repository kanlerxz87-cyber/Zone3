# Zone3 — AI Amazon Affiliate Marketing Platform

Full-stack affiliate marketing intelligence for Amazon Associates: product intake and
verification, niche / pricing / review analysis, grounded SEO content generation,
campaign tracking, and compliance enforcement — with a build-time gate that refuses to
publish any value that cannot be traced to an official source.

**Live site:** https://kanlerxz87-cyber.github.io/Zone3/

---

## Status at a glance

| | |
| --- | --- |
| Products submitted | 3 |
| Products that passed intake verification | **0 of 3** |
| Data cells left blank because no official source exists | **36** |
| Official sources cited | 17 |
| Open items published for review | 24 |
| Compliance rules enforced in the build | 25 prohibitions + 5 mandatory text blocks |

The three submitted links (`link.amazon/B04G1MEwY`, `link.amazon/B02NbDxp3`,
`link.amazon/B00hJ57DV`) carry **9-character** identifiers. An Amazon ASIN is 10
characters, and `https://www.amazon.com/dp/<id>` returns Amazon's *Page Not Found* page for
all three. Following each link landed on a **different** unrelated product through Amazon's
`plpRedirect=mhFallback` route, which confirms the identifiers select nothing.

Rather than invent a product, the pipeline rejects them at intake and publishes the evidence.
Full audit trail: [`docs/verification-log.md`](docs/verification-log.md).

---

## Pages

| Category | Path | What it holds |
| --- | --- | --- |
| Dashboard | `/` | KPIs, findings, navigation |
| Executive summary | `/executive-summary/` | The whole story in one read |
| Products | `/products/` | Intake + verification register, 12-field attribute sheet, link pipeline |
| Niches | `/niches/` | Scoring model, input availability, 10 verified category constraints |
| Pricing | `/pricing/` | Price sheet, pricing rules engine, unblock sequence |
| Reviews | `/reviews/` | Review metrics, integrity constraints, compliant sentiment design |
| Content | `/content/` | Inventory, templates, claim-grounding contract, SEO mechanics |
| Campaigns | `/campaigns/` | Performance ledger, schema provenance, optimiser boundary |
| Compliance | `/compliance/` | Mandatory text blocks, programme economics, 25 prohibitions |
| Agent terms | `/agent-terms/` | Amazon's AI-agent rules, mapped clause by clause |
| Methodology | `/methodology/` | 8-stage pipeline, verification protocol, scalability, limits |
| Requirements | `/requirements/` | All 30 brief clauses traced to status |
| Sources | `/sources/` | Every official document cited, with what was observed |
| Flagged | `/flagged/` | 24 open items with source links and resolutions |
| Repo review | `/repo-review/` | Audit of the repository as found |

---

## Layout

```
index.html + 15 subpages   generated static site (committed, served by GitHub Pages)
assets/app.css, app.js     dashboard styling; sort/filter; no runtime fetching
data/*.json                single source of truth for every published cell
config/platform.json       configuration; credentials committed as null on purpose
tools/build_site.py        renders the site + enforces the provenance gate (G1–G8)
tools/verify_site.py       audits the emitted HTML (V1–V7)
tools/amazon_intake.py     ASIN validation → /dp/ probe → Creators API
tools/niche_score.py       niche ranking; never imputes a missing input
tools/link_report.py       provenance coverage report
docs/                      executive summary, verification log, repo review, compliance
COORDINATION.md            shared task board for parallel agent sessions
```

---

## Working with it

```bash
python3 tools/build_site.py            # rebuild + run the provenance gate (exit 2 on violation)
python3 tools/verify_site.py           # audit the emitted HTML    (exit 3 on violation)
python3 tools/link_report.py           # provenance coverage report
python3 tools/link_report.py --strict  # fail if any table is under-covered

# verify the finding yourself
for a in B04G1MEwY B02NbDxp3 B00hJ57DV; do
  echo "$a chars=${#a}"; curl -sSI "https://www.amazon.com/dp/$a" | head -1
done
curl -sSI https://www.amazon.com/dp/B0CDY277D3 | head -1   # control: 10 chars, resolves

python3 tools/amazon_intake.py --link 'https://link.amazon/B04G1MEwY' --validate-only
python3 tools/amazon_intake.py --asin B0CDY277D3 --offline   # exit 0, queued for API
```

No third-party dependencies: the standard library only.

---

## Design rule

**Automation without fabrication.** Every stage has an explicit failure mode: when a value
cannot be obtained from an official source, the field is set to `null`, a flag is raised, and
the pipeline continues. The gate is what makes that a guarantee rather than a style guide —
`build_site.py` exits non-zero if any table row has neither a source, nor a flag, nor a
repository anchor that actually exists.

Amazon's rules deliberately bound what the agent may do: no price-alerting features, no
per-visitor sub-tag attribution, no automated clicks, no link shortening, no storing Amazon
images, and no caching of Program Content beyond 24 hours. The agent identifies itself as
`Agent/Zone3ProductResearch` in its User-Agent, as the Program Policies' Agent Terms require,
and treats a block response as a result rather than an obstacle. Details on
`/agent-terms/` and `/compliance/`.

---

## Disclosure

As an Amazon Associate I earn from qualifying purchases.

CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED ‘AS IS’
AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.

Zone3 is independent and is not affiliated with, endorsed or sponsored by Amazon. Amazon,
Amazon Associates and ASIN are trademarks of Amazon.com, Inc. or its affiliates.

*No license file is present — see the flagged item in `docs/repo-review.md` §2.2.*
