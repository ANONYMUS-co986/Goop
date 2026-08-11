const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const route = process.argv[2] || '/';
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE: ' + e.message.slice(0, 250)));
  page.on('console', m => { if (m.type() === 'error') errs.push('CON: ' + m.text().slice(0, 250)); });
  page.on('requestfailed', r => errs.push('REQ: ' + r.url().slice(0, 120)));
  await page.goto('http://localhost:5173' + route, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3200);
  const s = await page.evaluate(() => ({
    main: !!document.querySelector('main'), scrollH: document.documentElement.scrollHeight,
    text: (document.body.innerText || '').slice(0, 100),
    fonts: document.fonts.size,
  }));
  console.log(route, JSON.stringify(s));
  console.log('errs:', errs.length ? errs.join(' | ') : 'NONE');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
