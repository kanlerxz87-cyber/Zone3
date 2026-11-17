# The measurement collector

This directory holds the collector that receives the events the site's counter posts, and the
test that proves what it does and does not store.

The counter itself is generated — `assets/analytics.js`, built by `tools/build_analytics.py` from
`data/analytics/config.json`. The rules both halves obey are written down in
`data/analytics/events.json` and published on the measurement desk at `/analytics/`.

## Why a collector is needed at all

GitHub Pages is a static site hosting service: it publishes HTML, CSS and JavaScript files from a
repository. It cannot run a program and it cannot accept a POST. The counter on the site is
therefore built so that it works with **no** endpoint at all — events stay in the reader's own
browser — and starts sending the moment an owner-controlled endpoint is configured.

Source: <https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages>
(read 2026-11-17).

## What the collector stores, and what it never stores

Stored, and nothing else:

| Field | Meaning |
|---|---|
| `e` | the event name, one of five |
| `p` | the page path the event happened on |
| `t` | the target — an ASIN when the link exposes one, otherwise the destination path |
| `l` | the link label, trimmed to 60 characters |
| `a` | true/false, used only by the disclosure event |
| `ts` | the event time as a Unix timestamp |
| `d` | the UTC date of the event |

Never stored: the IP address, the User-Agent string, the Referer header, cookies, any visitor
identifier, and any product attribute such as price, rating or review count. The collector drops
every field outside the list above **before** it writes anything, so a later change to the client
cannot quietly widen what is kept.

## Option A — the Python collector (any small server, Raspberry Pi, VPS, container)

Standard library only. No dependencies, no database, no network access of its own.

```bash
# start it
python3 tools/collector/collect.py --dir ./collector-data --host 0.0.0.0 --port 8787

# check it is alive
curl http://127.0.0.1:8787/health

# look at the counts
curl http://127.0.0.1:8787/stats
```

Options:

| Option | Default | What it does |
|---|---|---|
| `--dir` | `collector-data` | directory the event file lives in |
| `--file` | `events.jsonl` | event file name (one JSON object per line) |
| `--host` | `127.0.0.1` | address to bind; use `0.0.0.0` to serve the internet |
| `--port` | `8787` | port to listen on |
| `--allow-origin` | the Zone3 Pages origin | origin allowed to post; repeat for more |
| `--retention-days` | `30` | events older than this are pruned at startup |

Put it behind a TLS terminator (a reverse proxy, or a tunnel) before it faces the internet, and
give it a firewall rule that only allows the site's host.

## Option B — the Cloudflare Worker variant

`worker.js` implements the same contract against Workers KV.

```bash
wrangler kv namespace create KV      # note the namespace id
# put the id in wrangler.toml as a binding named KV
wrangler deploy
```

Then set the endpoint in the site configuration:

```json
{ "endpoint": "https://<worker>.<subdomain>.workers.dev/e" }
```

in `data/analytics/config.json`, and rebuild with `python3 tools/build_analytics.py`.

Sources for the platform this file is written against:
<https://developers.cloudflare.com/workers/> and <https://developers.cloudflare.com/kv/>
(read 2026-11-17).

## The test

```bash
python3 tools/collector/test_collector.py
```

Six checks, all standard library:

1. a valid event is accepted, written and counted;
2. an event outside the contract is rejected and nothing is written;
3. fields outside the contract are dropped rather than stored;
4. no client address, User-Agent or Referer reaches the stored record;
5. the CORS header appears for the allowed origin and not for another one (a request from another
   origin is refused with 403);
6. the counts endpoint reports what was stored.

## What the collector does not decide

It does not choose an event set, a retention window that suits the owner, or a host. Those are
owner decisions and are recorded as DEC-03 in `data/shop/decisions.json` and as Q8 in
`data/decision-queue.json`.
