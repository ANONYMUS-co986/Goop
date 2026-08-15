const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 120)));
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  // scroll through narrative sections, capture each
  const sections = ['#directive', '#nation', '#gap', '#flow', '#founders', '#idea'];
  for (const sel of sections) {
    await page.evaluate((s) => document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'start' }), sel);
    await page.waitForTimeout(700);
    const r = await page.evaluate((s) => {
      const el = document.querySelector(s);
      const b = el.getBoundingClientRect();
      return { top: Math.round(b.top), h: Math.round(b.height), text: (el.innerText || '').slice(0, 60) };
    }, sel);
    console.log(sel, JSON.stringify(r));
    await page.screenshot({ path: '/tmp/qa_gate/' + sel.replace('#', '') + '.png' });
  }
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
