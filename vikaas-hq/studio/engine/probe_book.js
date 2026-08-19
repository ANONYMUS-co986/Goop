const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  // step 0: add 2 phones
  await page.click('.dev-card:has-text("Phone") .dev-count button:last-child');
  await page.click('.dev-card:has-text("Phone") .dev-count button:last-child');
  await page.click('.dev-card:has-text("Charger") .dev-count button:last-child');
  const s0 = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent, total: document.querySelectorAll('.dev-card.sel').length }));
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  // step 1: enter kg
  await page.fill('.kg-input', '1.4');
  const s1 = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent, val: (document.querySelector('.value-live b')||{}).textContent }));
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  // step 2: addr + slot
  await page.fill('.addr-input', 'Gurugram, Sector 45');
  await page.click('.slot:has-text("Tomorrow 10")');
  const s2 = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent }));
  await page.click('.bk-next');
  await page.waitForTimeout(500);
  const s3 = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent, rows: document.querySelectorAll('.sum-row').length }));
  await page.click('.bk-next');
  await page.waitForTimeout(700);
  const done = await page.evaluate(() => ({ done: !!document.querySelector('.bk-done'), h: document.querySelector('.bk-done h2') ? document.querySelector('.bk-done h2').textContent : 'none', receipt: (document.querySelector('.done-receipt')||{}).textContent || '' }));
  console.log('s0:', JSON.stringify(s0));
  console.log('s1:', JSON.stringify(s1));
  console.log('s2:', JSON.stringify(s2), 's3:', JSON.stringify(s3));
  console.log('done:', JSON.stringify(done));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/book-done.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
