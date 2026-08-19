const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERR:', e.message.slice(0, 200)));
  page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE:', m.text().slice(0, 200)); });
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  await page.click('.dev-card .dev-count button:last-child');
  await page.waitForTimeout(400);
  // click and capture any error
  const r = await page.evaluate(() => {
    try {
      const btn = document.querySelector('.bk-next');
      btn.click();
      return 'clicked-no-throw';
    } catch (e) { return 'THREW: ' + e.message.slice(0, 100); }
  });
  console.log('eval click:', r);
  await page.waitForTimeout(800);
  const after = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent }));
  console.log('after:', JSON.stringify(after));
  // check React state via the component — inspect if there are multiple .bk-pane (exit stuck)
  const panes = await page.evaluate(() => document.querySelectorAll('.bk-pane').length);
  console.log('panes:', panes);
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
