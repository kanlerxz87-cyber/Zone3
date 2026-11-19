/* Privacy/deduplication regressions; no network or Amazon navigation. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.resolve(__dirname, '../../assets/measure.js'), 'utf8');
function scenario({ endpoint = 'https://collector.example.invalid/collect', enabled = true, navigator = {}, pathname = '/Zone3/guides/capacity-checklist.html', twice = false, click = null, loading = false } = {}) {
  const calls = [];
  const listeners = {};
  const document = { readyState: loading ? 'loading' : 'complete', addEventListener(name, fn) { (listeners[name] ||= []).push(fn); } };
  const sandbox = { window: { Z3_MEASURE: { enabled, endpoint } }, navigator, document, location: { href: 'https://kanlerxz87-cyber.github.io' + pathname + '?email=private#fragment', pathname }, URL, JSON,
    fetch(url, options) { calls.push({ url, options, body: JSON.parse(options.body) }); return Promise.resolve({ status: 204 }); }
  };
  Object.defineProperty(document, 'cookie', { get() { return ''; }, set() { throw new Error('cookie write'); } });
  for (const key of ['localStorage', 'sessionStorage']) Object.defineProperty(sandbox, key, { get() { throw new Error('analytics storage access'); } });
  vm.createContext(sandbox); vm.runInContext(source, sandbox);
  if (twice) vm.runInContext(source, sandbox);
  if (loading) (listeners.DOMContentLoaded || []).forEach(fn => fn());
  if (click) (listeners.click || []).forEach(fn => fn({ target: { closest: () => ({ href: click }) } }));
  return { calls, listeners };
}
let checks = 0;
function check(label, fn) { fn(); checks++; console.log('PASS ' + label); }
check('duplicate script initialization does not double count', () => assert.equal(scenario({ twice: true }).calls.length, 2));
check('DOMContentLoaded path dispatches once', () => assert.equal(scenario({ loading: true, twice: true }).calls.length, 2));
for (const flags of [{ globalPrivacyControl: true }, { doNotTrack: '1' }, { connection: { saveData: true } }]) {
  check('privacy signal disables all requests: ' + JSON.stringify(flags), () => assert.equal(scenario({ navigator: flags }).calls.length, 0));
}
for (const endpoint of ['', 'http://collector.example.invalid/collect', 'https://user:secret@collector.example.invalid/collect', 'https://collector.example.invalid/collect?secret=1', 'https://collector.example.invalid/collect#secret', 'javascript:alert(1)', '//collector.example.invalid/not-collect']) {
  check('invalid endpoint fails closed: ' + endpoint, () => assert.equal(scenario({ endpoint }).calls.length, 0));
}
check('off means no requests', () => assert.equal(scenario({ enabled: false }).calls.length, 0));
check('query, fragment, credentials and Referer are absent', () => {
  const { calls } = scenario();
  for (const call of calls) {
    assert.equal(call.options.credentials, 'omit'); assert.equal(call.options.referrerPolicy, 'no-referrer'); assert.equal(call.options.redirect, 'error');
    assert.equal(call.body.p, '/Zone3/guides/capacity-checklist.html'); assert(!JSON.stringify(call.body).includes('private'));
    assert.deepEqual(Object.keys(call.body).sort(), ['e', 'h', 'p', 'v']);
  }
});
check('product URLs ending in /ref retain the actual ASIN, never the query or ref path', () => {
  const { calls } = scenario({ click: 'https://www.amazon.com/example-product/dp/B0CDY277D3/ref=example?tag=secret&ref=private#fragment' });
  const click = calls.find(x => x.body.e === 'outbound_click'); assert(click); assert.equal(click.body.t, 'B0CDY277D3'); assert.equal(click.body.h, 'www.amazon.com');
  assert(!JSON.stringify(click.body).includes('secret'));
});
check('non-product sponsored destinations are not product clicks', () => {
  const { calls } = scenario({ click: 'https://www.amazon.com/b?node=123' }); assert(!calls.some(x => x.body.e === 'outbound_click'));
});
check('lookalike Amazon hosts are rejected', () => {
  const { calls } = scenario({ click: 'https://www.amazon.com.attacker.invalid/dp/B0CDY277D3' }); assert(!calls.some(x => x.body.e === 'outbound_click'));
});
check('an unknown event such as purchase is never manufactured', () => {
  const { calls } = scenario({ click: 'https://link.amazon/B04G1MEwY?tag=secret' }); assert.deepEqual(calls.map(x => x.body.e), ['page_view', 'guide_view', 'outbound_click']);
});
console.log('TEST PASS · ' + checks + ' extended measurement checks');
