const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERROR:\n' + (e.stack || e.message).slice(0, 900)));
  await page.goto('http://localhost:5173/boot?fast=1', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2200);
  await page.click('#enter');
  await page.waitForTimeout(2200);
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
