const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.click('.dev-card:has-text("Phone") .dev-count button:last-child');
  await page.click('.bk-next');
  await page.waitForTimeout(400);
  await page.fill('.kg-input', '1.4');
  await page.click('.bk-next');
  await page.waitForTimeout(400);
  // inspect the slot buttons
  const slots = await page.evaluate(() => Array.from(document.querySelectorAll('.slot')).map(s => s.textContent.trim()));
  console.log('slots:', JSON.stringify(slots));
  await page.fill('.addr-input', 'Gurugram');
  // click the FIRST slot by index
  await page.evaluate(() => document.querySelectorAll('.slot')[0].click());
  await page.waitForTimeout(300);
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  const s3 = await page.evaluate(() => ({ h: (document.querySelector('.bk-h2')||{}).textContent || 'none', rows: document.querySelectorAll('.sum-row').length }));
  console.log('after slot+next:', JSON.stringify(s3));
  await page.click('.bk-next');
  await page.waitForTimeout(700);
  const done = await page.evaluate(() => ({ done: !!document.querySelector('.bk-done'), h: (document.querySelector('.bk-done h2')||{}).textContent || 'none' }));
  console.log('done:', JSON.stringify(done));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
