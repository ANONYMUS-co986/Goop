const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/app/book', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  // check for ANY react errors in the module + whether the component mounted twice
  const r = await page.evaluate(() => {
    // count how many times the root re-rendered via a marker
    const btns = Array.from(document.querySelectorAll('.bk-next'));
    return { nextBtns: btns.length, pageText: document.body.innerText.slice(0, 60) };
  });
  console.log(JSON.stringify(r));
  // try clicking with playwright's real click (not evaluate)
  await page.click('.dev-card .dev-count button:last-child');
  await page.waitForTimeout(300);
  await page.click('.bk-next', { force: true });
  await page.waitForTimeout(600);
  const after = await page.evaluate(() => ({ h: document.querySelector('.bk-h2').textContent }));
  console.log('real click after:', JSON.stringify(after));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
