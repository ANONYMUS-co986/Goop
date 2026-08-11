const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 120)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 120)); });
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  await page.evaluate(() => { document.querySelector('#toy').scrollIntoView({ behavior: 'instant', block: 'start' }); });
  await page.waitForTimeout(900);
  const before = await page.evaluate(() => getComputedStyle(document.querySelector('.toy-front')).transform);
  await page.click('.drawer-toy');
  await page.waitForTimeout(1100);
  const after = await page.evaluate(() => ({
    cls: document.querySelector('.drawer-toy').className,
    front: getComputedStyle(document.querySelector('.toy-front')).transform,
    readout: document.querySelector('.toy-readout').textContent,
    items: document.querySelectorAll('.toy-item').length,
  }));
  console.log('before:', before);
  console.log('after:', JSON.stringify(after));
  console.log('errs:', errs.length ? errs.join(' || ') : 'none');
  await page.screenshot({ path: '/tmp/suite/drawer-open.png' });
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0, 200)); process.exit(1); });
