const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERROR:', e.message.slice(0,150), '||', (e.stack||'').split('\n')[1]));
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(800);
  const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));
  await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * 0.5));
  await page.waitForTimeout(1000);
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
