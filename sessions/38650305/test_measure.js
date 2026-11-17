// Offline test of assets/measure.js with stubbed browser globals (session 38650305).
// Run: node sessions/38650305/test_measure.js   (exit 1 on any failure)
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const SRC = fs.readFileSync(path.join(ROOT, 'assets', 'measure.js'), 'utf8');
const CONFIG_JS = fs.readFileSync(path.join(ROOT, 'assets', 'measure-config.js'), 'utf8');
let failures = 0;
function check(cond, label) { console.log((cond ? 'PASS ' : 'FAIL ') + label); if (!cond) failures++; }

// Run one scenario: page path, config JS, navigator flags, and an optional click on a link.
function run({ pathname, configJs, nav = {}, click = null }) {
  const sent = [];
  const cookieWrites = [];
  const listeners = {};
  const doc = {
    readyState: 'complete',
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
  };
  const win = { doNotTrack: undefined };
  const sandbox = {
    window: win,
    document: doc,
    navigator: Object.assign({ sendBeacon: (url, blob) => { sent.push({ url, blob }); return true; } }, nav),
    location: { pathname, href: 'https://kanlerxz87-cyber.github.io' + pathname },
    URL,
    Blob,
    JSON,
    Object,
    console,
    fetch: () => { throw new Error('fetch should not be used when sendBeacon exists'); },
  };
  // Any cookie write would be a document.cookie assignment; make it visible.
  Object.defineProperty(doc, 'cookie', { set(v) { cookieWrites.push(v); }, get() { return ''; } });
  vm.createContext(sandbox);
  vm.runInContext(configJs, sandbox);
  vm.runInContext(SRC, sandbox);
  if (click) {
    const target = { closest: (sel) => (sel === 'a[rel~="sponsored"]' ? click : null) };
    for (const fn of listeners.click || []) fn({ target });
  }
  const bodies = sent.map((s) => ({ url: s.url, text: null, blobP: s.blob }));
  return { sent, bodies, cookieWrites };
}

async function readAll(list) {
  const out = [];
  for (const s of list) out.push({ url: s.url, body: JSON.parse(await s.blob.text()) });
  return out;
}

(async () => {
  const OFF = 'window.Z3_MEASURE = {"enabled": false, "endpoint": ""};';
  const ON = 'window.Z3_MEASURE = {"enabled": true, "endpoint": "https://collector.example.org/collect"};';

  // 1. Default build: counting OFF, nothing sent.
  const r1 = run({ pathname: '/Zone3/index.html', configJs: CONFIG_JS });
  check(r1.sent.length === 0, 'default build (counter off) sends nothing');
  check(/"enabled": ?false/.test(CONFIG_JS) || /"enabled":false/.test(CONFIG_JS), 'generated config is disabled by default');

  // 2. Enabled: page_view on load; guide_view on a guide page.
  const r2 = run({ pathname: '/Zone3/guides/capacity-checklist.html', configJs: ON });
  const b2 = await readAll(r2.sent);
  check(b2.length === 2, 'guide page with counter on sends two events (page_view, guide_view)');
  check(b2.map((x) => x.body.e).join(',') === 'page_view,guide_view', 'event names are page_view then guide_view');
  check(b2.every((x) => x.body.p === '/Zone3/guides/capacity-checklist.html'), 'path is sent without query or hash');
  check(b2.every((x) => Object.keys(x.body).sort().join(',') === 'e,h,p,v'), 'body contains only v, e, p, h (no id, ip, ua, referrer)');
  check(r2.cookieWrites.length === 0, 'no cookie is written');

  // 3. Global Privacy Control blocks everything.
  const r3 = run({ pathname: '/Zone3/guides/capacity-checklist.html', configJs: ON, nav: { globalPrivacyControl: true } });
  check(r3.sent.length === 0, 'Global Privacy Control on: nothing sent');

  // 4. Do Not Track blocks everything.
  const r4 = run({ pathname: '/Zone3/index.html', configJs: ON, nav: { doNotTrack: '1' } });
  check(r4.sent.length === 0, 'Do Not Track on: nothing sent');

  // 5. Outbound click on a sponsored link: one outbound_click with host and token only.
  const link = { href: 'https://link.amazon/B04G1MEwY?ref=abc&tag=x' };
  const r5 = run({ pathname: '/Zone3/index.html', configJs: ON, click: link });
  const b5 = await readAll(r5.sent);
  const oc = b5.find((x) => x.body.e === 'outbound_click');
  check(!!oc, 'click on a sponsored link sends outbound_click');
  check(oc && oc.body.t === 'B04G1MEwY' && oc.body.h === 'link.amazon', 'outbound_click carries token and host only');
  check(oc && !JSON.stringify(oc.body).includes('ref=abc') && !JSON.stringify(oc.body).includes('tag=x'), 'query string of the destination is not sent');

  // 6. Endpoint empty in config: nothing, even when enabled is true.
  const r6 = run({ pathname: '/Zone3/index.html', configJs: 'window.Z3_MEASURE = {"enabled": true, "endpoint": ""};' });
  check(r6.sent.length === 0, 'enabled without an endpoint sends nothing');

  // 7. Intent and flag pages.
  const r7 = run({ pathname: '/Zone3/intent-record/index.html', configJs: ON });
  check((await readAll(r7.sent)).some((x) => x.body.e === 'intent_view'), 'intent-record page sends intent_view');
  const r8 = run({ pathname: '/Zone3/publication-pass.html', configJs: ON });
  check((await readAll(r8.sent)).some((x) => x.body.e === 'flag_view'), 'publication-pass page sends flag_view');

  // 8. Index pages of guides are not guide_view.
  const r9 = run({ pathname: '/Zone3/guides/index.html', configJs: ON });
  check(!(await readAll(r9.sent)).some((x) => x.body.e === 'guide_view'), 'guides index does not fire guide_view');

  console.log(failures ? `TEST FAIL · ${failures} failure(s)` : 'TEST PASS · measure.js offline checks');
  process.exit(failures ? 1 : 0);
})();
