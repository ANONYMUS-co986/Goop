const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/app/map', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  const s0 = await page.evaluate(() => ({
    centres: document.querySelectorAll('.centre').length,
    households: document.querySelectorAll('.house').length,
    route: !!document.querySelector('.route line'),
  }));
  // click a household
  await page.click('.house-dot');
  await page.waitForTimeout(400);
  const s1 = await page.evaluate(() => ({ route: !!document.querySelector('.route line'), pin: !!document.querySelector('.route-pin') }));
  console.log('map:', JSON.stringify(s0));
  console.log('after click:', JSON.stringify(s1));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/map.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
