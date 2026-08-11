const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERROR:', e.message.slice(0,160), '||', (e.stack||'').split('\n')[1]));
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/index.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(1200);
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0,120)); process.exit(1); });
