// probe_scape.js — verifies the fixed 3D background renders when forced on
// (?scape=1): canvas present, WebGL context alive, zero console errors.
// Usage: node probe_scape.js [baseUrl]
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

(async () => {
  const base = process.argv[2] || 'http://localhost:5173';
  let browser;
  for (let i = 0; i < 3; i++) {
    try { browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); break; }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  if (!browser) { console.log('FAIL browser'); process.exit(1); }
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('CON:' + m.text().slice(0, 140)); });
  await page.goto(base + '/?scape=1', { waitUntil: 'networkidle', timeout: 45000 }).catch(e => errs.push('NAV:' + e.message.slice(0, 100)));
  await page.waitForTimeout(4000);
  const st = await page.evaluate(() => {
    const c = document.querySelector('canvas');
    if (!c) return { canvas: false };
    const gl = c.getContext('webgl2') || c.getContext('webgl');
    return { canvas: true, w: c.width, h: c.height, gl: !!gl };
  }).catch(e => ({ evalfail: e.message.slice(0, 100) }));
  await page.screenshot({ path: '/tmp/qa_gate/_scape.png' }).catch(() => {});
  await browser.close();
  console.log('scape:', JSON.stringify(st));
  const real = errs.filter(e => !e.includes('Failed to load resource'));
  if (!st.canvas || !st.gl) { console.log('FAIL no canvas/gl'); process.exit(1); }
  if (real.length) { console.log('FAIL console:', real.join(' | ')); process.exit(1); }
  console.log('SCAPE PROBE: PASS');
})();
