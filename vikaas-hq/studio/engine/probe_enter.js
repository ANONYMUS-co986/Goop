const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 180)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 180)); });
  await page.goto('http://localhost:5173/boot?fast=1', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  // ENTER button should be .show in fast mode
  const s1 = await page.evaluate(() => ({ show: document.querySelector('#enter').classList.contains('show'), stage: !!document.querySelector('#stage') }));
  console.log('boot state:', JSON.stringify(s1));
  await page.click('#enter');
  await page.waitForTimeout(2500);
  const s2 = await page.evaluate(() => ({
    path: location.pathname,
    bodyText: document.body.innerText.slice(0, 80),
    wipe: (() => { const w = document.querySelector('.pagewipe'); return w ? getComputedStyle(w).transform + '|' + getComputedStyle(w).display : 'gone'; })(),
    main: !!document.querySelector('main'),
    gateTitle: (document.querySelector('.gate-title') || {}).textContent || 'none',
    scrollH: document.documentElement.scrollHeight,
  }));
  console.log('after enter:', JSON.stringify(s2));
  await page.screenshot({ path: '/tmp/qa_gate/after-enter.png' });
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
