const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2800);
  const before = await page.evaluate(() => ({
    nav: !!document.querySelector('.gnav'),
    mute: !!document.querySelector('.gnav-mute'),
    prog: !!document.querySelector('.scrollprog'),
    hud: !!document.querySelector('#hudTime'),
  }));
  // open the menu
  await page.click('.gnav-menu');
  await page.waitForTimeout(600);
  const after = await page.evaluate(() => ({
    overlayOn: !!document.querySelector('.gnov'),
    items: document.querySelectorAll('.gn-item').length,
    opacity: getComputedStyle(document.querySelector('.gnov')).opacity,
  }));
  await page.screenshot({ path: '/tmp/qa_gate/nav-open.png' });
  // close via esc
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  const closed = await page.evaluate(() => getComputedStyle(document.querySelector('.gnov')).opacity);
  console.log('before:', JSON.stringify(before));
  console.log('menu:', JSON.stringify(after), 'closed-opacity:', closed);
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
