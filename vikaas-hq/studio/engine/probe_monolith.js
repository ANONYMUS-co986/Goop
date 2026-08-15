const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 180)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 180)); });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000); // let R3F mount + render
  const r = await page.evaluate(() => {
    const c = document.querySelector('.mono-wrap canvas');
    return {
      canvas: !!c,
      canvasW: c ? c.width : 0,
      gl: !!window.WebGLRenderingContext,
      heroText: (document.querySelector('.gate-title')||{}).textContent || 'none',
      chips: document.querySelectorAll('.chip').length,
      scrollH: document.documentElement.scrollHeight,
    };
  });
  console.log(JSON.stringify(r));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await page.screenshot({ path: '/tmp/qa_gate/monolith.png' });
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 180)); process.exit(1); });
