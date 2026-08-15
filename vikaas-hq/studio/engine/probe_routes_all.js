const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 100)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 100)); });
  const routes = ['/', '/boot', '/drawer', '/type', '/proof', '/kabadi', '/arsenal', '/buddy', '/system', '/geneva', '/nope'];
  const results = [];
  for (const r of routes) {
    await page.goto('http://localhost:5173' + r, { waitUntil: 'networkidle', timeout: 45000 }).catch(e => results.push({ r, err: e.message.slice(0, 60) }));
    await page.waitForTimeout(1200);
    const state = await page.evaluate(() => ({
      main: !!document.querySelector('main') || !!document.querySelector('#stage'),
      title: (document.querySelector('h1, .cs-title, .gate-title') || {}).textContent ? (document.querySelector('h1, .cs-title, .gate-title')).textContent.slice(0, 40) : 'none',
      scrollH: document.documentElement.scrollHeight,
    })).catch(e => ({ evalerr: e.message.slice(0, 60) }));
    results.push({ r, ...state });
  }
  console.log(JSON.stringify(results, null, 1));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
