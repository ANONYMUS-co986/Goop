// probe_route.js — the deep per-route check used by verify_all.sh
// Checks: render (main/fonts/height), blank (screenshot std), console
// (0 errors/failed requests). Exits 1 on ANY fail so verify_all counts it.
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const PY = '/tmp/pw_venv/bin/python';
const STD_SCRIPT = path.join(__dirname, 'pix_std.py');

(async () => {
  const url = process.argv[2];
  const outPrefix = process.argv[3] || '/tmp/qa_gate/route';
  let browser;
  for (let i = 0; i < 3; i++) {
    try { browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); break; }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  if (!browser) { console.log(`  ❌ probe ${url} — browser launch failed`); process.exit(1); }
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('CON:' + m.text().slice(0, 140)); });
  page.on('requestfailed', r => errs.push('REQ:' + r.url().slice(0, 100)));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(e => errs.push('NAV:' + e.message.slice(0, 120)));
  await page.waitForTimeout(2800);
  const shot = outPrefix + '.png';
  await page.screenshot({ path: shot }).catch(() => {});
  const state = await page.evaluate(() => ({
    main: !!document.querySelector('main') || !!document.querySelector('#stage'),
    fonts: document.fonts ? document.fonts.size : 0,
    scrollH: document.documentElement.scrollHeight,
    vh: innerHeight,
  })).catch(e => ({ evalfail: e.message.slice(0, 100) }));
  await browser.close();

  let std = -1;
  try {
    std = parseFloat(execFileSync(PY, [STD_SCRIPT, shot], { timeout: 30000 }).toString().trim());
  } catch (e) { console.error("STDERR:", e.message.slice(0,200)); std = -1; }

  let fails = 0;
  const ok = (name, cond, detail) => {
    console.log(`  ${cond ? '✅' : '❌'} ${name} — ${detail}`);
    if (!cond) fails++;
  };
  ok('render', !state.evalfail && state.main && state.fonts >= 4 && state.scrollH > state.vh,
     state.evalfail || `main=${state.main} fonts=${state.fonts} h=${state.scrollH}/${state.vh}`);
  ok('blank', std >= 8, `std=${std} (${shot})`);
  ok('console', errs.length === 0, errs.length ? errs.join(' | ') : 'clean');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.log('  ❌ probe crash ' + e.message.slice(0, 120)); process.exit(1); });
