const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html?fast=1', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(2500); // fast boot reveal
  const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));
  const read = async (frac) => {
    await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * frac));
    await page.waitForTimeout(900);
    const r = await page.evaluate(() => ({
      lidX: +((window.__lid && window.__lid.rotation.x) || 0).toFixed(3),
      camZ: +((window.__cam && window.__cam.z) || 0).toFixed(2),
      spill: 'n/a',
    }));
    await page.screenshot({ path: `/tmp/suite/lid-${String(frac).replace('.','')}.png` });
    return r;
  };
  console.log('0.10 (creak):', JSON.stringify(await read(0.10)));
  console.log('0.30 (open):', JSON.stringify(await read(0.30)));
  console.log('0.60 (open+):', JSON.stringify(await read(0.60)));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
