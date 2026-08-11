const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERROR:', e.message.slice(0, 300), '\n  at:', (e.stack || '').split('\n')[1]));
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(800);
  const r = await page.evaluate(() => ({ reduce: matchMedia('(prefers-reduced-motion: reduce)').matches, img404: (() => { const im = document.querySelector('#rebeeFly img'); return im ? im.complete && im.naturalWidth === 0 : 'no-img'; })() }));
  console.log('ENV:', JSON.stringify(r));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
