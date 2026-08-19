const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.click('.dev-card .dev-count button:last-child');
  await page.waitForTimeout(300);
  // click NEXT via evaluate (bypass any overlay)
  const r = await page.evaluate(() => {
    const btn = document.querySelector('.bk-next');
    const before = document.querySelector('.bk-h2').textContent;
    btn.click();
    return { before, btnClass: btn.className };
  });
  await page.waitForTimeout(600);
  const after = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent, kg: !!document.querySelector('.kg-input') }));
  console.log('clicked via evaluate:', JSON.stringify(r));
  console.log('after:', JSON.stringify(after));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
