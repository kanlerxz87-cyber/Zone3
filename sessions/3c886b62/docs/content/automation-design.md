Four requirements are marked blocked: track clicks, track conversions, identify high-converting products,
and continuously optimize campaigns. All four fail for the same two reasons, and both are fixable.

### Why they are blocked

**No Associates account is connected.** Amazon reports clicks, conversions and the realised per-order
commission rate only inside Associates Central. Without that data there is nothing to optimise against,
so the requirement is genuinely blocked rather than deprioritised.

**GitHub Pages has no runtime.** It serves static files. There is no server, database, scheduler or model
endpoint, so nothing can run on a schedule and nothing can be generated per request.

### The shape that fits

The site is already built to be generated. `tools/build.py` reads `data/*.json` and writes every page, so
the whole site is a pure function of the data layer. That means automation only has to produce JSON; it
does not have to produce HTML.

**Ingest, scheduled.** A GitHub Actions workflow on a cron runs a collector that calls the Product
Advertising API or Creators API for each ASIN in the catalogue, writes the response into
`data/products.json` with a fresh capture timestamp and the source id, and opens a pull request. The
price and rating columns then satisfy Participation Requirements 2(b) and 6(t) because they came from the
API, and the staleness problem disappears because the refresh is automatic.

**Attribute, from reports.** A second scheduled job ingests the Associates Central reports into a
time-series store, keyed by the sub-tag in each link. Amazon permits additional sub-tags for exactly this
purpose, and prohibits assigning them dynamically per user, so the sub-tags must be per-placement and
static.

**Decide, on rules.** With clicks and conversions per placement, the optimisation loop becomes a small set
of explicit rules: demote any product whose conversion rate falls below a threshold over a trailing
window, promote any content placement whose earnings per hundred clicks exceeds the catalogue median, and
retire any page whose promotion badge has expired. Each rule writes a proposed change to the data layer as
a pull request, so a human approves before anything ships. That keeps the decision auditable, which
matters because a wrongly automated price claim is a policy breach.

**Generate content, with a human gate.** Article, comparison and buying-guide generation can be templated
from the same verified data layer, because every claim on those pages is already a field in
`data/products.json`. The safe pattern is generation into a pull request with the source id inline on
every claim, never direct publication, so that a hallucinated value is caught at review rather than
published.

### Sequencing

Fix the blocking flags first. Nothing in this design works until an Associates tag exists and API
credentials are in place, because without them the ingest job has no data source and the reports job has
no reports. The order is: tag, then API credentials, then ingest, then attribution, then the optimisation
rules, then content generation.

### What deliberately stays manual

Publishing. Every automated change lands as a pull request. Amazon holds the Associate solely responsible
for the accuracy of everything on the site and can terminate the account without notice for a breach, so
automated direct publication is a bad trade at any traffic level.
