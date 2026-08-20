// real-browser simulation: spoofs navigator.webdriver=false so Scape mounts
// (like the user's browser), renders the Gate, catches EVERY error/warning.
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  // spoof: make the app think it's a real user browser (Scape mounts)
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  const errs = [];
  const warns = [];
  page.on('pageerror', (e) => errs.push('PAGEERR: ' + e.message.slice(0, 220)));
  page.on('console', (m) => {
    const t = m.text();
    if (m.type() === 'error') errs.push('CONERR: ' + t.slice(0, 220));
    if (m.type() === 'warning') warns.push('WARN: ' + t.slice(0, 180));
  });
  page.on('requestfailed', (r) => errs.push('REQFAIL: ' + r.url().slice(0, 100)));
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(6000);
  const st = await page.evaluate(() => ({
    main: !!document.querySelector('main'),
    canvases: document.querySelectorAll('canvas').length,
    bodyText: (document.body.innerText || '').slice(0, 120).replace(/\n/g, ' | '),
    scape: !!document.querySelector('div[style*="position: fixed"] canvas'),
    appPhone: !!document.querySelector('.theapp-3d canvas'),
    monolith: !!document.querySelector('.mono-wrap canvas'),
    scrollH: document.documentElement.scrollHeight,
  }));
  console.log('STATE:', JSON.stringify(st, null, 1));
  console.log('ERRORS:', errs.length ? errs.join('\n') : 'NONE');
  console.log('WARNINGS:', warns.length ? warns.slice(0, 6).join('\n') : 'NONE');
  await page.screenshot({ path: '/tmp/qa_gate/_realbrowser.png' });
  await browser.close();
  process.exit(errs.length ? 1 : 0);
})();
