const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  // scroll to scale
  await page.evaluate(() => document.querySelector('#scale-seq').scrollIntoView({ behavior: 'instant', block: 'start' }));
  await page.waitForTimeout(700);
  // scrub through
  await page.evaluate(() => window.scrollBy(0, 600));
  await page.waitForTimeout(900);
  const mid = await page.evaluate(() => ({
    needle: document.querySelector('#needle').getAttribute('x2'),
    read: document.querySelector('#scaleReadout b').textContent,
    status: document.querySelector('#scaleReadout span').textContent,
    line3: getComputedStyle(document.querySelector('#sLine3')).opacity,
  }));
  await page.evaluate(() => window.scrollBy(0, 900));
  await page.waitForTimeout(900);
  const end = await page.evaluate(() => ({
    read: document.querySelector('#scaleReadout b').textContent,
    status: document.querySelector('#scaleReadout span').textContent,
    receipt: getComputedStyle(document.querySelector('#sReceipt')).opacity,
  }));
  console.log('mid:', JSON.stringify(mid));
  console.log('end:', JSON.stringify(end));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/scale-end.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
