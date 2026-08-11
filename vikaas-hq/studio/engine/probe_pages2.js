const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
async function launch() {
  for (let i = 0; i < 3; i++) {
    try { return await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  throw new Error('launch failed');
}
(async () => {
  const browser = await launch();
  // GATE deep check
  let page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const gerrs = [];
  page.on('pageerror', e => gerrs.push(e.message.slice(0,140)));
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  const g = await page.evaluate(() => ({
    chars: document.querySelectorAll('.gate-title .ch').length,
    ticker: !!document.querySelector('.ticker'),
    wipe: !!document.querySelector('.pagewipe'),
    prog: !!document.querySelector('.scrollprog'),
    scrollH: document.documentElement.scrollHeight,
  }));
  console.log('GATE:', JSON.stringify(g), 'errs:', gerrs.length ? gerrs.join('|') : 'none');
  await page.screenshot({ path: '/tmp/suite/gate-fixed.png' });
  await page.close();

  // DRAWER deep check + toy click
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const derrs = [];
  page.on('pageerror', e => derrs.push(e.message.slice(0,140)));
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  // scroll to toy
  await page.evaluate(() => { document.querySelector('#toy').scrollIntoView({ behavior: 'instant', block: 'start' }); });
  await page.waitForTimeout(800);
  const before = await page.evaluate(() => getComputedStyle(document.querySelector('.toy-front')).transform);
  await page.click('.drawer-toy');
  await page.waitForTimeout(900);
  const after = await page.evaluate(() => ({
    cls: document.querySelector('.drawer-toy').className,
    front: getComputedStyle(document.querySelector('.toy-front')).transform,
    readout: document.querySelector('.toy-readout').textContent,
  }));
  console.log('DRAWER toy before:', before);
  console.log('DRAWER toy after:', JSON.stringify(after), 'errs:', derrs.length ? derrs.join('|') : 'none');
  await page.screenshot({ path: '/tmp/suite/drawer-open.png' });
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0,200)); process.exit(1); });
