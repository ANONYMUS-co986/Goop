const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  // scroll to toy
  await page.evaluate(() => document.querySelector('#toy').scrollIntoView({ behavior: 'instant', block: 'start' }));
  await page.waitForTimeout(800);
  // open drawer
  await page.click('.drawer-toy');
  await page.waitForTimeout(900);
  const openState = await page.evaluate(() => ({ open: document.querySelector('.drawer-toy').classList.contains('open'), items: document.querySelectorAll('.toy-item').length }));
  // tap phone item
  await page.click('.toy-item.ph');
  await page.waitForTimeout(700);
  const spec = await page.evaluate(() => {
    const c = document.querySelector('.holo-card');
    return c ? { name: c.querySelector('.holo-name').textContent, value: c.querySelector('.holo-row b').textContent, stamp: c.querySelector('.stamp').textContent, tag: c.querySelector('.holo-tag').textContent } : 'NO-CARD';
  });
  console.log('open:', JSON.stringify(openState));
  console.log('spec:', JSON.stringify(spec));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/toy2-holo.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
