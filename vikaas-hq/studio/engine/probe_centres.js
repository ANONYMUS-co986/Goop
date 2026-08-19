const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/app/centres', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  const s0 = await page.evaluate(() => ({
    cards: document.querySelectorAll('.centre-card').length,
    accepting: document.querySelectorAll('.centre-status.accepting').length,
    title: (document.querySelector('.centres-title')||{}).textContent ? document.querySelector('.centres-title').textContent.slice(0, 30) : 'none',
  }));
  // register flow
  await page.fill('.reg-form input:nth-child(1)', 'Sharma Kabadi House');
  await page.fill('.reg-form input:nth-child(3)', 'Sector 12, Gurugram');
  await page.fill('.reg-form input:nth-child(4)', '9812345678');
  await page.click('.reg-submit');
  await page.waitForTimeout(600);
  const s1 = await page.evaluate(() => ({ done: !!document.querySelector('.reg-done'), h: (document.querySelector('.reg-done h3')||{}).textContent || 'none' }));
  console.log('roster:', JSON.stringify(s0));
  console.log('register:', JSON.stringify(s1));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/centres.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
