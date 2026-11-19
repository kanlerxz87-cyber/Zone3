# Publication consolidation — session 1c072a7a

Date: 2026-11-19 UTC. Fixed Arena branch: `arena/1c072a7a-zone3`.
Original base: `3883a0b`; integration base: `0ee4153` (completed C3/C17/3301 passes).
The final PR/merge/deployment identifiers are recorded in `COORDINATION.md` only after they exist.

## Reproduce the release

From the repository root, Python 3.11+ and Node 22+:

```bash
python3 tools/publish.py
python3 tools/publish.py --check
```

The first command runs the retained generators and every applicable release gate. It does not
access Amazon, manufacture traffic, alter any account or provision a service. `--report PATH`
optionally saves each command's real exit code and output. The canonical command is also the CI
entry point. The C3/C17 source renderers are unchanged; their earlier shopper edition is composed
on a scratch page and retained at `publication-prior.html`. They must not patch the current root.

Current test evidence:

- `baseline-checks.json`: 19 pre-change commands, all passing on the original base.
- `release-checks.json`: full final chain/check output; includes non-blocking historical advisories.
- `browser-checks.json`: real local Chromium interaction, privacy and automated accessibility results.
- `idempotency.json`: a second full chain changed zero of 550 nonignored workspace files (the record itself excluded).
- `screenshots/`: representative desktop/mobile renders inspected during this session.
- `verification-2026-11-19.md`: exactly which official pages and products were read, and what was not.
- `repo-review.md`: architecture, provenance, privacy, generated ownership and risk review.

Passing a structural gate does **not** establish that every historical fact has been freshly
verified. C3-F-01 and P26-F05 remain published; legacy advisories are not suppressed or relabelled
as confirmed findings. Automated axe scans are not a full accessibility certification.

## Optional real-browser checks

The production site has no npm runtime dependency. Optional verification dependencies are pinned
in this folder. The npm-distributed Chromium avoids a separate browser download in restricted
sandboxes. The script inflates its bundled libraries and keeps web security enabled.

```bash
npm ci --prefix sessions/1c072a7a --ignore-scripts --no-audit --no-fund
python3 tools/preview.py --host 0.0.0.0 --port 3000
# In a second terminal:
node sessions/1c072a7a/browser_check.cjs
```

The script accepts `Z3_PREVIEW_URL` for a different local port and `CHROMIUM_EXECUTABLE` for a normal
installed Chromium. `Z3_BROWSER_OUTPUT` changes the output folder (default `.preview/browser`). It
refuses non-local test targets, blocks retailer/external requests, and prevents Amazon navigation
while checking outbound delivery. Its export test is a synthetic review, **not** the owner's choice.
Do not import test counts or that synthetic review into any campaign or decision evidence.

Coverage includes all 16 current reader/review pages at 1440 and 390px, additional 320/768px root
layout, filters, one research menu, native-dialog keyboard/focus behavior, local search and its
failure fallback, review save/reload/clear/export, clipboard, storage denial, no-JS navigation,
project-site `/Zone3/` paths, duplicate runtime guard, five accepted HTTP event types, privacy
signals, omitted credentials/Referer and disabled production configuration. The previous edition
is checked structurally and remains noindex; it is not represented as a newly accessible review.

## Collector: local tests versus deployment

```bash
python3 tools/analytics_endpoint.py --self-test
python3 sessions/1c072a7a/test_collector.py
node sessions/38650305/test_measure.js
node sessions/1c072a7a/test_measure.cjs
```

Production remains disabled in `data/shop/measurement.json`. The preview overrides only the
**served** config response with `/collect`; the file on disk stays disabled. Its local aggregate
store is ignored `.preview/aggregate-counts.json`. Readout is disabled unless a server-side
`Z3_ANALYTICS_READ_TOKEN` is supplied, and then requires a Bearer header. Never put that token in
browser code, a URL, a public JSON file, Git or chat.

To activate later, an authorized operator must first:

1. Resolve commercially suitable durable hosting, HTTPS termination and applicable privacy /
   consent requirements. GitHub Pages cannot execute this Python server.
2. Keep the store on private persistent storage; restrict file access and service access. Run one
   collector process per store (the in-process lock does not coordinate multiple server processes).
3. Disable/review upstream access logs, CDN/proxy logs and error tracing. The app's no-request-log
   implementation cannot certify an undeployed host or prevent a transport IP from reaching it.
4. Set the exact approved production origin; no wildcard. Keep the five-event/page/product schema
   in sync. Origin validation is not bot authentication or proof of human visits.
5. Confirm accepted/rejected requests, absence of raw identifiers, persistence across a restart,
   90-UTC-day retention, private optional readout and privacy opt-outs at the real HTTPS endpoint.
6. Record a dated verification report and host/logging evidence; only then set `enabled`, the
   HTTPS `/collect` endpoint and deployment-verification fields. The build rejects missing,
   malformed or future dates and invalid endpoint credentials/queries/ports. This release also
   deliberately asserts production-off/empty-ledger because no such evidence exists. A later
   activation release must update those assertions to validate the actual new evidence, and update
   the publication's off-status/privacy copy together; changing a boolean alone is not approval.
7. Keep campaign attribution separate. Authorized Associates reports establish reported orders;
   counter events do not establish unique people, eligible sessions or conversions.

No deployment, account permission, legal basis, traffic improvement, order or revenue is implied
by these instructions. Outstanding gates are on `suggestions/index.html` and `flagged.html`.
