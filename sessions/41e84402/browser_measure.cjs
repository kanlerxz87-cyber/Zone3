/* E41-T3 measurement (session 41e84402). Local Chromium only: no retailer navigation, no campaign
 * evidence, no traffic claim. Start the dev preview first, then run:
 *   python3 tools/preview.py --host 127.0.0.1 --port 3000 &
 *   node sessions/41e84402/browser_measure.cjs
 * Measures, at three widths, the two things this pass changed on the compare page:
 *   1. does the sticky product column hold its left edge while the table is scrolled sideways?
 *   2. does the three-question chooser really render above the comparison section?
 *   3. how many interactive targets on that page are under a 44 px high tap box?
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium: playwright } = require('playwright');   // the pinned copy in sessions/1c072a7a/node_modules (set NODE_PATH)

// Same launcher the published browser harness uses: npm-distributed Chromium, web security left ON.
async function launch() {
  const options = { headless: true };
  if (process.env.CHROMIUM_EXECUTABLE) options.executablePath = process.env.CHROMIUM_EXECUTABLE;
  else {
    try {
      const chromium = require('@sparticuz/chromium').default;
      const packageBuild = path.dirname(require.resolve('@sparticuz/chromium'));
      const { inflate } = await import(pathToFileURL(path.join(packageBuild, 'lambdafs.js')).href);
      const libraries = await inflate(path.join(packageBuild, '../bin/al2023.tar.br'));
      options.executablePath = await chromium.executablePath();
      options.args = chromium.args.filter(a => !['--disable-web-security', '--allow-running-insecure-content', '--single-process'].includes(a));
      options.env = { ...process.env, LD_LIBRARY_PATH: path.join(libraries, 'lib') + ':' + (process.env.LD_LIBRARY_PATH || '') };
    } catch (error) { if (error.code !== 'MODULE_NOT_FOUND') throw error; }
  }
  return playwright.launch(options);
}
const ROOT = path.resolve(__dirname, '../..');
const BASE = (process.env.Z3_PREVIEW_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
assert(['127.0.0.1', 'localhost'].includes(new URL(BASE).hostname), 'local preview only');
const OUT = path.join(__dirname, 'screenshots');
fs.mkdirSync(OUT, { recursive: true });
const MIN = 44;
const report = { measured_at: '2026-11-19', tool: 'Chromium via @sparticuz/chromium + playwright',
  scope: 'Local dev preview at three widths. Measures layout and tap geometry only: no traffic, conversion, device-mix or ranking claim.',
  tap_target_minimum_px: MIN, viewports: [] };
async function at(browser, [w, h]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  await ctx.route('**/*', r => (new URL(r.request().url()).origin === new URL(BASE).origin ? r.continue() : r.abort()));
  const page = await ctx.newPage();
  await page.goto(BASE + '/shop/products/index.html', { waitUntil: 'load' });
  const sticky = await page.evaluate(() => {
    const cell = document.querySelector('.p26-compare .p26-table tbody th');
    const wrap = document.querySelector('.p26-table-scroll');
    if (!cell || !wrap) return { found: false };
    const before = Math.round(cell.getBoundingClientRect().left);
    wrap.scrollLeft = 160;
    const after = Math.round(cell.getBoundingClientRect().left);
    const cs = getComputedStyle(cell);
    return { found: true, position: cs.position, left_before: before, left_after_scroll_160px: after,
             stayed_pinned: Math.abs(before - after) <= 2, region_scrolls_sideways: wrap.scrollWidth > wrap.clientWidth,
             column_width: Math.round(cell.getBoundingClientRect().width), row_count: document.querySelectorAll('.p26-compare .p26-table tbody th').length };
  });
  const order = await page.evaluate(() => {
    const c = document.querySelector('#chooser'), m = document.querySelector('#comparison');
    return { chooser: !!c, comparison: !!m, chooser_above_table: !!c && !!m && c.getBoundingClientRect().top < m.getBoundingClientRect().top,
             chooser_steps: document.querySelectorAll('.p26-chooser-step').length, hint: !!document.querySelector('.p26-scroll-hint') };
  });
  const taps = await page.evaluate((min) => {
    const sel = 'a.p26-choice, .p26-category-links a, main a[href^="https://www.amazon.com"], main a.p26-button, main a.p26-text-link, .p26-table a';
    const under = [];
    let n = 0;
    document.querySelectorAll(sel).forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      n++;
      if (r.height < min) under.push({ text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30), height_px: Math.round(r.height), width_px: Math.round(r.width) });
    });
    return { examined: n, under_minimum: under };
  }, MIN);
  await page.screenshot({ path: path.join(OUT, `compare-${w}x${h}.png`) });
  await ctx.close();
  return { width: w, height: h, sticky_product_column: sticky, page_order: order, tap_targets: taps };
}
(async () => {
  const browser = await launch();
  for (const vp of [[320, 720], [390, 844], [768, 1024]]) report.viewports.push(await at(browser, vp));
  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'measurement-2026-11-19.json'), JSON.stringify(report, null, 1) + '\n');
  for (const v of report.viewports) {
    console.log(`${String(v.width).padStart(4)}px  pinned=${v.sticky_product_column.stayed_pinned} pos=${v.sticky_product_column.position} col_w=${v.sticky_product_column.column_width} chooser_above_table=${v.page_order.chooser_above_table} steps=${v.page_order.chooser_steps} hint=${v.page_order.hint} taps<${MIN}px=${v.tap_targets.under_minimum.length}/${v.tap_targets.examined}`);
    if (v.tap_targets.under_minimum.length) console.log('      under:', JSON.stringify(v.tap_targets.under_minimum.slice(0, 5)));
  }
  assert.ok(report.viewports.every(v => v.sticky_product_column.stayed_pinned), 'the sticky column must hold its left edge while the region scrolls');
  const scrollable = report.viewports.filter(v => v.sticky_product_column.region_scrolls_sideways).map(v => v.width);
  console.log('      the table region scrolls sideways at these widths:', scrollable.join(', ') || 'none (the table fits)');
  const stillSmall = report.viewports.map(v => v.tap_targets.under_minimum.length);
  console.log(`      interactive targets under ${MIN}px tall, per width:`, stillSmall.join(' / '), '(inline links in table cells are the WCAG 2.2 2.5.8 inline exception)');
  assert.ok(report.viewports.every(v => v.page_order.chooser_above_table && v.page_order.chooser_steps === 3), 'chooser with three steps must sit above the comparison section');
  console.log(`PASS ${report.viewports.length} viewports; report + screenshots in sessions/41e84402/`);
})().catch(e => { console.error('FAIL ' + e.message); process.exit(1); });
