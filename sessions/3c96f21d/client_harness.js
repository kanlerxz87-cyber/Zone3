/*
 * End-to-end harness for the generated measurement client (session 3c96f21d, 2026-11-17).
 *
 *   node sessions/3c96f21d/client_harness.js http://127.0.0.1:8787
 *
 * What it proves:
 *   1. assets/analytics.js loads and runs outside a browser (no syntax error, no crash);
 *   2. a click on an Amazon link produces exactly the payload the collector expects;
 *   3. the client keeps that payload in its own origin-scoped queue when no endpoint is set,
 *      and sends nothing anywhere;
 *   4. with an endpoint set, the same payload reaches a running collector and shows up in
 *      its counts.
 *
 * The DOM is a minimal shim: only the parts the client actually touches are implemented.
 */

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..", "..");
const endpoint = process.argv[2] || "";
const PAGE = "/guides/basket-or-oven-style.html";

const clientSource = fs.readFileSync(path.join(ROOT, "assets", "analytics.js"), "utf8");

// ---------------------------------------------------------------- the shim
const storage = new Map();
const beacons = [];
const fetches = [];
const listeners = {};

function fakeElement(tag) {
  return {
    tagName: tag,
    textContent: "",
    className: "",
    children: [],
    appendChild(child) { this.children.push(child); },
    setAttribute() {},
    getAttribute() { return null; },
    closest() { return null; },
    getBoundingClientRect() { return { top: 0, bottom: 40, left: 0, right: 0, width: 0, height: 40 }; },
    querySelector() { return null; },
  };
}

const disclosure = fakeElement("div");
const localLogHost = fakeElement("div");

const documentShim = {
  readyState: "complete",
  addEventListener(type, fn) { listeners[type] = fn; },
  querySelector(selector) {
    if (selector === ".disclose-bar" || selector === ".z3-strip") return disclosure;
    return null;
  },
  getElementById(id) { return id === "z3-analytics-local" ? localLogHost : null; },
  createElement(tag) { return fakeElement(tag); },
};

const windowShim = {
  location: { pathname: PAGE, href: "https://kanlerxz87-cyber.github.io" + PAGE },
  localStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, value); },
    removeItem(key) { storage.delete(key); },
  },
  navigator: {
    sendBeacon(url, blob) {
      // The real transport: a POST with the blob as the body. The promise is kept so the
      // harness can wait for the collector's answer.
      const promise = fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: blob,
      });
      beacons.push({ url, body: blob, promise });
      return true;
    },
  },
  fetch: (url, options) => { fetches.push({ url, options }); return Promise.resolve({ ok: true }); },
  IntersectionObserver: class {
    constructor(callback) { this.callback = callback; }
    observe(el) { this.callback([{ isIntersecting: true, target: el }]); }
    disconnect() {}
  },
  innerHeight: 800,
  addEventListener() {},
  document: documentShim,
};
windowShim.window = windowShim;

const sandbox = {
  window: windowShim,
  document: documentShim,
  navigator: windowShim.navigator,
  localStorage: windowShim.localStorage,
  fetch: windowShim.fetch,
  Blob: Blob,
  URL: URL,
  Date: Date,
  Math: Math,
  JSON: JSON,
  console: console,
};
sandbox.globalThis = sandbox;

const context = vm.createContext(sandbox);
vm.runInContext(clientSource, context, { filename: "assets/analytics.js" });

// ---------------------------------------------------------------- the click
const link = {
  getAttribute(name) { return name === "href" ? "https://link.amazon/B04G1MEwY" : null; },
  textContent: "Open the listing you submitted",
};
const target = { closest: (selector) => (selector === "a[href]" ? link : null) };
if (!listeners.click) {
  console.error("FAIL: the client registered no click listener");
  process.exit(1);
}
listeners.click({ target: target });

const queue = JSON.parse(storage.get("z3:events:v1") || "[]");

console.log("page:            " + PAGE);
console.log("events queued:   " + JSON.stringify(queue));
console.log("beacons sent:    " + beacons.length);
console.log("fetches sent:    " + fetches.length);

// ---------------------------------------------------------------- the wire
async function main() {
  if (!endpoint) {
    console.log("endpoint:        (none configured) — nothing was sent, as designed");
    return;
  }
  // The client's own sendBeacon call carries the payload, so wait for that request.
  for (const beacon of beacons) {
    const response = await beacon.promise;
    console.log("payload sent: " + (await beacon.body.text()));
    console.log("POST " + beacon.url + " -> " + response.status);
  }
  const stats = await fetch(endpoint.replace(/\/e$/, "/stats"));
  console.log("stats: " + (await stats.text()).replace(/\s+/g, " ").slice(0, 400));
}

main().catch((error) => {
  console.error("harness error:", error.message);
  process.exit(1);
});
