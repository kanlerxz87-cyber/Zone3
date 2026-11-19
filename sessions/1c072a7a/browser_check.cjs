/* Local Chromium integration checks. Never navigates to Amazon or creates campaign evidence.
 * Start: python3 tools/preview.py --host 0.0.0.0 --port 3000
 * Install optional pinned dependencies from package.json (see README in this folder).
 * Run: node sessions/1c072a7a/browser_check.cjs
 * Results/screenshots default to ignored .preview/browser/. Set Z3_BROWSER_OUTPUT to preserve a run.
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium: playwright } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const ROOT = path.resolve(__dirname, '../..');
const BASE = (process.env.Z3_PREVIEW_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
assert(['127.0.0.1', 'localhost'].includes(new URL(BASE).hostname), 'Run only against the local test preview, not production');
const OUT = path.resolve(ROOT, process.env.Z3_BROWSER_OUTPUT || '.preview/browser');
fs.mkdirSync(OUT, { recursive: true });
const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/publication.json'), 'utf8'));
const pages = ['index.html', 'guides/index.html', ...data.guides.map(g => 'guides/' + g.slug + '.html'), 'shop/index.html', 'shop/air-fryers/index.html', 'shop/meat-thermometers/index.html', 'shop/products/index.html', 'suggestions/index.html', 'about.html', 'privacy.html', 'executive-brief.html'];
const report = { tested_at: new Date().toISOString(), scope: 'Local-only preview; synthetic test traffic, not campaign, sales or organic-traffic evidence. Automated WCAG 2.0/2.1 A/AA checks are not an accessibility certification.', checks: [], responsive: [], accessibility: [], screenshots: [] };
const requests = [];
const errors = [];
const external = [];
let browser;
async function check(label, fn) {
  try { const result = await fn(); report.checks.push({ label, pass: true, ...(result || {}) }); console.log('PASS ' + label); }
  catch (error) { report.checks.push({ label, pass: false, error: error.message }); console.log('FAIL ' + label + '\n' + error.stack); throw error; }
}
async function goto(page, rel = '', basePath = '') {
  const response = await page.goto(BASE + basePath + '/' + rel, { waitUntil: 'networkidle' });
  assert.equal(response.status(), 200, rel);
}
async function screenshot(page, name) {
  await page.screenshot({ path: path.join(OUT, name) });
  report.screenshots.push(name);
}
async function context(options = {}, observe = true) {
  const ctx = await browser.newContext(options);
  await ctx.route('**/*', async route => {
    const url = route.request().url();
    if (/^https?:/.test(url) && new URL(url).origin !== new URL(BASE).origin) {
      external.push(new URL(url).hostname); return route.abort();
    }
    return route.continue();
  });
  if (observe) {
    ctx.on('page', page => {
      page.on('pageerror', error => errors.push(error.message));
      page.on('request', request => {
        if (new URL(request.url()).pathname === '/collect') requests.push({ body: request.postDataJSON(), headers: request.headers() });
      });
      page.on('response', response => { if (response.status() >= 400) errors.push(response.status() + ' ' + new URL(response.url()).pathname); });
    });
  }
  return ctx;
}
async function launch() {
  const options = { headless: true };
  if (process.env.CHROMIUM_EXECUTABLE) options.executablePath = process.env.CHROMIUM_EXECUTABLE;
  else {
    // npm-distributed Chromium works in restricted-network sandboxes. Keep web security ON:
    // its default --disable-web-security flag removes the Origin needed by the collector.
    try {
      const chromium = require('@sparticuz/chromium').default;
      const packageBuild = path.dirname(require.resolve('@sparticuz/chromium'));
      const { inflate } = await import(pathToFileURL(path.join(packageBuild, 'lambdafs.js')).href);
      const libraries = await inflate(path.join(packageBuild, '../bin/al2023.tar.br'));
      options.executablePath = await chromium.executablePath();
      // Single-process Chromium can crash when closing an isolated privacy-test context.
      options.args = chromium.args.filter(a => !['--disable-web-security', '--allow-running-insecure-content', '--single-process'].includes(a));
      options.env = { ...process.env, LD_LIBRARY_PATH: path.join(libraries, 'lib') + ':' + (process.env.LD_LIBRARY_PATH || '') };
    } catch (error) {
      if (error.code !== 'MODULE_NOT_FOUND') throw error;
      // Otherwise use a normal Playwright-installed Chromium.
    }
  }
  return playwright.launch(options);
}
(async () => {
  browser = await launch();
  report.browser = browser.version();
  const ctx = await context({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await check('Root preview: real collector accepts page_view and no browser storage/cookies are created', async () => {
    await goto(page);
    assert.equal(await page.locator('h1').count(), 1);
    assert(requests.some(r => r.body.e === 'page_view'));
    assert.deepEqual(await ctx.cookies(), []);
    assert.deepEqual(await page.evaluate(() => [Object.keys(localStorage), Object.keys(sessionStorage)]), [[], []]);
    await screenshot(page, 'home-desktop.png');
    await page.locator('#products').scrollIntoViewIfNeeded();
    await screenshot(page, 'products-desktop.png');
  });
  await check('Product filters update actual cards and pressed/live state', async () => {
    for (const [category, count] of [['air-fryers', 3], ['meat-thermometers', 2], ['all', 5]]) {
      const button = page.locator('[data-filter="' + category + '"]');
      await button.click();
      assert.equal(await page.locator('[data-product-card]:visible').count(), count);
      assert.equal(await button.getAttribute('aria-pressed'), 'true');
      assert((await page.locator('#p26-filter-status').textContent()).includes(String(count)));
    }
  });
  await check('Search: local index, matching result, empty state, Escape and focus restoration', async () => {
    await page.locator('[data-search-open]').click();
    await page.locator('#p26-query').fill('capacity');
    await page.locator('#p26-search-results a').first().waitFor();
    assert((await page.locator('#p26-search-results').textContent()).toLowerCase().includes('capacity'));
    await page.locator('#p26-query').fill('no-such-local-guide');
    assert((await page.locator('#p26-search-results').textContent()).includes('No match yet'));
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#p26-search').evaluate(d => d.open), false);
    assert.equal(await page.locator('[data-search-open]').evaluate(e => e === document.activeElement), true);
  });
  await check('One research navigation group, Escape/outside close, and full footer tools', async () => {
    assert.equal(await page.locator('.p26-nav .p26-workspace').count(), 1);
    const summary = page.locator('.p26-workspace > summary');
    await summary.click();
    assert.equal(await page.locator('.p26-workspace').getAttribute('open'), '');
    assert(await page.locator('.p26-workspace-panel a').count() >= 40);
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.p26-workspace').getAttribute('open'), null);
    assert.equal(await summary.evaluate(e => e === document.activeElement), true);
    await summary.click(); await page.locator('.p26-disclosure').click({ position: { x: 12, y: 12 } });
    assert.equal(await page.locator('.p26-workspace').getAttribute('open'), null);
    await page.locator('.p26-research-tools > summary').click();
    assert(await page.locator('.p26-tools-grid a:visible').count() >= 40);
  });
  await check('Suggestions: priority filter, unsaved state, explicit local save, reload, export, clear, copy prompt', async () => {
    await goto(page, 'suggestions/index.html');
    for (const priority of ['Now', 'Next', 'Later', 'all']) {
      await page.locator('[data-proposal-filter="' + priority + '"]').click();
      assert.equal(await page.locator('[data-proposal]:visible').count(), priority === 'all' ? 6 : data.proposals.filter(p => p.priority === priority).length);
    }
    const first = page.locator('[data-decision-id]').first();
    const id = await first.getAttribute('data-decision-id');
    await first.selectOption('shortlist');
    assert.equal(await page.evaluate(() => localStorage.getItem('zone3-publication-review-v1')), null);
    assert((await page.locator('#p26-review-status').textContent()).includes('Unsaved'));
    await page.locator('[data-save-review]').click();
    let record = await page.evaluate(() => JSON.parse(localStorage.getItem('zone3-publication-review-v1')));
    assert.equal(record.choices[id], 'shortlist');
    assert.equal(record.implementation, 'none; review only');
    await page.reload({ waitUntil: 'networkidle' });
    assert.equal(await page.locator('[data-decision-id]').first().inputValue(), 'shortlist');
    const downloadPromise = page.waitForEvent('download');
    await page.locator('[data-export-review]').click();
    const download = await downloadPromise;
    const downloadPath = path.join(OUT, 'review-export.test.json');
    await download.saveAs(downloadPath);
    record = JSON.parse(fs.readFileSync(downloadPath, 'utf8'));
    fs.unlinkSync(downloadPath); // synthetic review is not an owner decision or deliverable
    assert.equal(record.schema, 'zone3.editorial-review.v1'); assert.equal(record.choices[id], 'shortlist');
    assert(!('email' in record));
    await page.locator('[data-reset-review]').click();
    assert.equal(await page.evaluate(() => localStorage.getItem('zone3-publication-review-v1')), null);
    assert.equal(await page.locator('[data-decision-id]').first().inputValue(), 'unreviewed');
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
    await page.locator('[data-copy-prompt]').click();
    await page.waitForFunction(() => document.getElementById('p26-copy-status').textContent.includes('copied'));
    assert((await page.evaluate(() => navigator.clipboard.readText())).startsWith('Design Zone3 Kitchen'));
  });
  await check('Project-site /Zone3/ links, search and real five-event delivery; no Amazon navigation', async () => {
    await goto(page, '', '/Zone3');
    await page.locator('[data-search-open]').click();
    await page.locator('#p26-query').fill('thermometer');
    const result = page.locator('#p26-search-results a').first(); await result.waitFor();
    assert((await result.getAttribute('href')).startsWith('guides/'));
    assert(new URL(await result.getAttribute('href'), page.url()).pathname.startsWith('/Zone3/guides/'));
    await page.keyboard.press('Escape');
    await page.evaluate(() => {
      for (const kind of ['click', 'auxclick']) document.addEventListener(kind, event => { if (event.target.closest('a[rel~="sponsored"]')) event.preventDefault(); });
    });
    const accepted = page.waitForResponse(r => new URL(r.url()).pathname === '/collect' && r.request().postDataJSON().e === 'outbound_click');
    await page.locator('a.p26-product-cta').first().click();
    assert.equal((await accepted).status(), 204);
    const middleAccepted = page.waitForResponse(r => new URL(r.url()).pathname === '/collect' && r.request().postDataJSON().e === 'outbound_click');
    await page.locator('a.p26-product-cta').first().click({ button: 'middle' });
    assert.equal((await middleAccepted).status(), 204);
    assert(new URL(page.url()).pathname === '/Zone3/');
    await goto(page, 'guides/basket-or-oven-style.html', '/Zone3');
    await goto(page, 'intent-record/index.html', '/Zone3');
    await goto(page, 'flagged.html', '/Zone3');
    assert.deepEqual([...new Set(requests.map(r => r.body.e))].sort(), ['flag_view', 'guide_view', 'intent_view', 'outbound_click', 'page_view']);
  });
  await check('Duplicate runtime does not double count; query/hash/referrer/cookies/identifiers absent from event body', async () => {
    await ctx.addCookies([{ name: 'test-cookie-must-not-be-sent', value: 'test', url: BASE }]);
    await goto(page, 'guides/capacity-checklist.html?test_private_query=not-a-person#section-1');
    const before = requests.length;
    await page.addScriptTag({ url: BASE + '/assets/measure.js' });
    assert.equal(requests.length, before);
    for (const r of requests) {
      assert(!r.headers.cookie); assert(!r.headers.referer);
      assert(!JSON.stringify(r.body).includes('test_private_query'));
      assert(!JSON.stringify(r.body).includes('not-a-person'));
      assert(Object.keys(r.body).every(k => ['v', 'e', 'p', 'h', 't'].includes(k)));
    }
    await ctx.clearCookies();
  });
  await check('Mobile menu: expanded state, hidden navigation, Escape and focus restoration', async () => {
    await page.setViewportSize({ width: 390, height: 844 }); await goto(page);
    assert.equal(await page.locator('.p26-nav').isVisible(), false);
    await page.locator('.p26-menu-toggle').click();
    assert.equal(await page.locator('.p26-nav').isVisible(), true);
    assert.equal(await page.locator('.p26-menu-toggle').getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.p26-nav').isVisible(), false);
    assert.equal(await page.locator('.p26-menu-toggle').evaluate(e => e === document.activeElement), true);
  });
  await check('All 16 reader/review pages: desktop/mobile layout, above-fold disclosure and automated WCAG 2.0/2.1 A/AA', async () => {
    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: width === 1440 ? 1000 : 844 });
      for (const rel of pages) {
        await goto(page, rel);
        const layout = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth, disclosureBottom: document.querySelector('.p26-disclosure').getBoundingClientRect().bottom, mainTop: document.querySelector('main').getBoundingClientRect().top, height: innerHeight }));
        report.responsive.push({ page: rel, ...layout });
        assert(layout.scroll <= width + 1, rel + ' horizontal overflow at ' + width);
        assert(layout.disclosureBottom < layout.height && layout.disclosureBottom <= layout.mainTop + 1, rel + ' disclosure placement');
        const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
        const violations = result.violations.map(v => ({ id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target) }));
        report.accessibility.push({ page: rel, width, violations, incompleteRules: result.incomplete.map(i => i.id) });
        assert.deepEqual(violations, [], rel + ' accessibility findings at ' + width);
        if (width === 390 && rel === 'index.html') await screenshot(page, 'home-mobile.png');
        if (width === 390 && rel === 'suggestions/index.html') await screenshot(page, 'suggestions-mobile.png');
        if (width === 390 && rel === 'guides/instant-read-or-wireless-thermometer.html') await screenshot(page, 'guide-mobile.png');
      }
    }
    for (const width of [320, 768]) {
      await page.setViewportSize({ width, height: 1000 }); await goto(page);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    }
  });
  await check('GPC, DNT and Save-Data each disable ALL real browser analytics requests', async () => {
    for (const property of ['globalPrivacyControl', 'doNotTrack', 'connection']) {
      const isolated = await context({}, false);
      const sent = [];
      isolated.on('request', request => { if (new URL(request.url()).pathname === '/collect') sent.push(request.url()); });
      await isolated.addInitScript(p => Object.defineProperty(navigator, p, { configurable: true, get: () => p === 'doNotTrack' ? '1' : p === 'connection' ? { saveData: true } : true }), property);
      const p = await isolated.newPage(); await goto(p, 'guides/capacity-checklist.html');
      assert.deepEqual(sent, [], property);
      await isolated.close();
    }
  });
  await check('Production disabled config is inert in a real browser', async () => {
    const isolated = await context({}, false); const sent = [];
    isolated.on('request', request => { if (new URL(request.url()).pathname === '/collect') sent.push(request.url()); });
    await isolated.route('**/assets/measure-config.js', route => route.fulfill({ contentType: 'application/javascript', body: fs.readFileSync(path.join(ROOT, 'assets/measure-config.js'), 'utf8') }));
    const p = await isolated.newPage(); await goto(p, 'guides/capacity-checklist.html'); assert.deepEqual(sent, []);
    await isolated.close();
  });
  await check('Search failure keeps working guide navigation; storage denial keeps review/export available', async () => {
    const isolated = await context({}, false);
    await isolated.route('**/publication-search.json', route => route.fulfill({ status: 503, body: 'deliberate local test failure' }));
    await isolated.addInitScript(() => Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('test storage denial', 'SecurityError'); } }));
    const p = await isolated.newPage(); await goto(p, 'suggestions/index.html');
    assert((await p.locator('#p26-review-status').textContent()).includes('storage is unavailable'));
    await p.locator('[data-save-review]').click(); assert((await p.locator('#p26-review-status').textContent()).includes('could not save'));
    const download = p.waitForEvent('download'); await p.locator('[data-export-review]').click(); await download;
    await p.locator('[data-search-open]').click(); await p.locator('#p26-search-results a').waitFor();
    assert((await p.locator('#p26-search-results').textContent()).includes('Search is unavailable'));
    await p.locator('#p26-search-results a').click(); assert(new URL(p.url()).pathname.endsWith('/guides/index.html'));
    await isolated.close();
  });
  await check('No-JavaScript fallback: visible navigation, all products, guides and evidence questions', async () => {
    const isolated = await context({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } }, false);
    const p = await isolated.newPage(); await goto(p);
    assert.equal(await p.locator('.p26-nav').isVisible(), true); assert.equal(await p.locator('[data-product-card]:visible').count(), 5);
    await p.locator('.p26-nav a[href="guides/index.html"]').click(); assert.equal(await p.locator('.p26-guide-card').count(), 6);
    await goto(p, 'suggestions/index.html'); assert.equal(await p.locator('.p26-question-table tbody tr').count(), 9);
    await isolated.close();
  });
  await check('All ordinary page requests and collector responses succeed; no page errors or retailer requests', async () => {
    assert.deepEqual(errors, []); assert.deepEqual(external, []);
    const store = JSON.parse(fs.readFileSync(path.join(ROOT, '.preview/aggregate-counts.json'), 'utf8'));
    const events = new Set(Object.values(store).flatMap(day => Object.keys(day)));
    for (const event of ['page_view', 'outbound_click', 'guide_view', 'intent_view', 'flag_view']) assert(events.has(event));
    return { note: 'All five event names exist in the LOCAL test aggregate store. Counts are not reported as campaign evidence.' };
  });
  await ctx.close();
  report.status = 'PASS';
})().catch(error => { report.status = 'FAIL'; report.error = error.stack; process.exitCode = 1; }).finally(async () => {
  if (browser) await browser.close();
  report.completed_at = new Date().toISOString();
  fs.writeFileSync(path.join(OUT, 'browser-checks.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(report.status + ' · ' + report.checks.filter(c => c.pass).length + ' browser checks; ' + report.accessibility.length + ' page/viewport accessibility scans. ' + OUT);
});
