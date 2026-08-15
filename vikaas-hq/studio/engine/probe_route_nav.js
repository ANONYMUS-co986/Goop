const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  // navigate to drawer via the menu
  await page.click('.gnav-menu');
  await page.waitForTimeout(500);
  await page.click('.gnov a[href="/drawer"]');
  await page.waitForTimeout(1200);
  const afterNav = await page.evaluate(() => ({
    path: location.pathname,
    wipe: !!document.querySelector('.pagewipe'),
    drawerIntro: !!document.querySelector('#dintro'),
    scrollH: document.documentElement.scrollHeight,
  }));
  await page.screenshot({ path: '/tmp/qa_gate/after-nav.png' });
  console.log('after nav:', JSON.stringify(afterNav));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
