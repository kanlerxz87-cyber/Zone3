/*
 * Zone3 measurement collector — Cloudflare Worker variant.
 *
 * The same contract as tools/collector/collect.py, for owners who would rather run the
 * collector at the edge than on a small server. It stores events in a Workers KV namespace
 * binding named KV and answers the same three routes:
 *
 *   POST /e       {"events": [ ... ]}   204 on success, 400 when the payload breaks the contract
 *   GET  /stats   counts by event, page and target
 *   GET  /health  liveness
 *
 * It keeps the same promise the Python collector keeps: only the seven fields the payload
 * contract allows are stored. The client address, the User-Agent, the Referer, cookies and any
 * visitor identifier are never read into a stored record.
 *
 * Deploy
 *   1. Create a KV namespace:  wrangler kv namespace create KV
 *   2. Put the namespace id in wrangler.toml (or wrangler.jsonc) as a binding named KV
 *   3. Deploy:  wrangler deploy
 *   4. Put the resulting https://<name>.<subdomain>.workers.dev/e URL into
 *      data/analytics/config.json as "endpoint", then rebuild:
 *      python3 tools/build_analytics.py
 *
 * Sources for the platform this file is written against:
 *   https://developers.cloudflare.com/workers/       (Workers overview)
 *   https://developers.cloudflare.com/kv/            (Workers KV and its binding)
 */

const ALLOWED_EVENTS = new Set([
  "outbound_click",
  "guide_view",
  "comparison_view",
  "cta_click",
  "disclosure_impression",
]);

const FIELD_LIMITS = {
  e: 40,
  p: 200,
  t: 120,
  l: 60,
  a: 5,
  ts: 12,
  d: 10,
};

const MAX_EVENTS = 5000;
const STORAGE_KEY = "zone3:events:v1";
const DEFAULT_ORIGINS = ["https://kanlerxz87-cyber.github.io"];

function cleanEvent(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
  if (!ALLOWED_EVENTS.has(raw.e)) return null;
  const out = { e: raw.e };
  for (const field of Object.keys(FIELD_LIMITS)) {
    if (field === "e") continue;
    const value = raw[field];
    if (value === null || typeof value === "undefined") continue;
    if (field === "a") {
      if (value === true || value === false) out.a = value;
      continue;
    }
    if (field === "ts") {
      const stamp = Number(value);
      if (!Number.isFinite(stamp)) return null;
      out.ts = Math.floor(stamp);
      continue;
    }
    if (typeof value !== "string") return null;
    const trimmed = value.trim();
    if (trimmed.length > FIELD_LIMITS[field]) return null;
    if (field === "p" && !trimmed.startsWith("/")) return null;
    if (field === "d" && !/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return null;
    out[field] = trimmed;
  }
  if (!out.p || typeof out.ts === "undefined") return null;
  return out;
}

function json(body, status, headers = {}) {
  return new Response(JSON.stringify(body, null, 1), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      ...headers,
    },
  });
}

function corsHeaders(request, origins) {
  const origin = request.headers.get("Origin");
  if (!origin || !origins.includes(origin)) return {};
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "600",
    Vary: "Origin",
  };
}

function countBy(items, key) {
  const counts = {};
  for (const item of items) {
    const value = item[key];
    if (typeof value === "undefined" || value === null || value === "") continue;
    counts[value] = (counts[value] || 0) + 1;
  }
  return Object.fromEntries(Object.entries(counts).sort((a, b) => b[1] - a[1]));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const origins = env.ALLOWED_ORIGINS
      ? String(env.ALLOWED_ORIGINS).split(",").map((s) => s.trim()).filter(Boolean)
      : DEFAULT_ORIGINS;
    const origin = request.headers.get("Origin");
    if (origin && !origins.includes(origin)) {
      return json({ error: "origin not allowed" }, 403);
    }
    const cors = corsHeaders(request, origins);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    if (request.method === "POST" && path === "/e") {
      let body;
      try {
        body = await request.json();
      } catch (e) {
        return json({ error: "body is not JSON" }, 400, cors);
      }
      const items = body && body.events;
      if (!Array.isArray(items) || items.length === 0) {
        return json({ error: "expected an events array" }, 400, cors);
      }
      const cleaned = items.map(cleanEvent).filter(Boolean);
      if (cleaned.length === 0) {
        return json({ error: "no event matched the contract" }, 400, cors);
      }
      const stored = await env.KV.get(STORAGE_KEY, "json");
      const all = Array.isArray(stored) ? stored : [];
      const merged = all.concat(cleaned).slice(-MAX_EVENTS);
      await env.KV.put(STORAGE_KEY, JSON.stringify(merged));
      return new Response(null, { status: 204, headers: cors });
    }

    if (request.method === "GET" && path === "/stats") {
      const stored = await env.KV.get(STORAGE_KEY, "json");
      const items = Array.isArray(stored) ? stored : [];
      return json({
        events_stored: items.length,
        by_event: countBy(items, "e"),
        by_page: countBy(items, "p"),
        by_target: countBy(items, "t"),
        fields_stored: Array.from(new Set(items.flatMap((i) => Object.keys(i)))).sort(),
      }, 200, cors);
    }

    if (request.method === "GET" && path === "/health") {
      const stored = await env.KV.get(STORAGE_KEY, "json");
      return json({ status: "ok", events: Array.isArray(stored) ? stored.length : 0 }, 200, cors);
    }

    if (request.method === "GET" && path === "/") {
      return json({
        service: "Zone3 measurement collector (Cloudflare Worker)",
        routes: ["POST /e", "GET /stats", "GET /health"],
        never_stores: ["IP address", "User-Agent", "Referer", "cookies", "visitor identifier"],
      }, 200, cors);
    }

    return json({ error: "not found" }, 404, cors);
  },
};
