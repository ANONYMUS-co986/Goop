const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('console', m => console.log('CON:', m.text().slice(0, 120)));
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  await page.click('.dev-card .dev-count button:last-child');
  await page.waitForTimeout(400);
  console.log('--- clicking next ---');
  await page.click('.bk-next');
  await page.waitForTimeout(800);
  const after = await page.evaluate(() => document.querySelector('.bk-h2').textContent);
  console.log('after:', after);
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
