const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/app', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  const s1 = await page.evaluate(() => ({
    phone: !!document.querySelector('.phone'),
    title: (document.querySelector('.app-title')||{}).textContent ? document.querySelector('.app-title').textContent.slice(0, 40) : 'none',
    step: (document.querySelector('.ps-tag')||{}).textContent || 'none',
    impact: document.querySelectorAll('.impact-cell').length,
    how: document.querySelectorAll('.how-card').length,
    ctas: document.querySelectorAll('.app-ctas a').length,
  }));
  console.log('t0:', JSON.stringify(s1));
  await page.waitForTimeout(3000);
  const s2 = await page.evaluate(() => ({ step: document.querySelector('.ps-tag').textContent, title: document.querySelector('.ps-step h3').textContent }));
  console.log('t3s:', JSON.stringify(s2));
  await page.screenshot({ path: '/tmp/qa_gate/app-page.png' });
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
