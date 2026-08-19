const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  // check step 0 renders devices
  const d0 = await page.evaluate(() => ({ devCards: document.querySelectorAll('.dev-card').length, next: document.querySelector('.bk-next').textContent, nextDim: document.querySelector('.bk-next').className }));
  console.log('step0:', JSON.stringify(d0));
  await page.click('.dev-card .dev-count button:last-child');
  await page.waitForTimeout(300);
  const d0b = await page.evaluate(() => ({ nextDim: document.querySelector('.bk-next').className }));
  console.log('after add:', JSON.stringify(d0b));
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  const d1 = await page.evaluate(() => ({ h: (document.querySelector('.bk-h2')||{}).textContent, kg: !!document.querySelector('.kg-input') }));
  console.log('step1:', JSON.stringify(d1));
  await page.fill('.kg-input', '1.4');
  await page.waitForTimeout(200);
  const d1b = await page.evaluate(() => ({ nextDim: document.querySelector('.bk-next').className }));
  console.log('kg entered, next:', JSON.stringify(d1b));
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  const d2 = await page.evaluate(() => ({ h: (document.querySelector('.bk-h2')||{}).textContent, slots: document.querySelectorAll('.slot').length, addr: !!document.querySelector('.addr-input') }));
  console.log('step2:', JSON.stringify(d2));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
