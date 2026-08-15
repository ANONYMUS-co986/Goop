const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  await page.click('.gnav-menu');
  await page.waitForTimeout(500);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(1200);
  const r = await page.evaluate(() => ({ mounted: !!document.querySelector('.gnov'), pe: document.querySelector('.gnov') ? getComputedStyle(document.querySelector('.gnov')).pointerEvents : 'gone' }));
  console.log(JSON.stringify(r));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0, 120)); process.exit(1); });
