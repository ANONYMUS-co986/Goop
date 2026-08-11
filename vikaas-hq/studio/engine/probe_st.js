const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE: ' + e.message.slice(0, 200)));
  page.on('console', m => { if (m.type() === 'error') errs.push('CON: ' + m.text().slice(0, 200)); });
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(600);
  const d = await page.evaluate(() => ({
    three: typeof THREE !== 'undefined' ? 'loaded' : 'MISSING',
    st: typeof ScrollTrigger !== 'undefined' ? 'loaded' : 'MISSING',
    stCount: window.ScrollTrigger ? ScrollTrigger.getAll().length : -1,
    pinSpacers: document.querySelectorAll('.pin-spacer').length,
    scrollHeight: document.documentElement.scrollHeight,
    stageRect: (() => { const r = document.querySelector('#stage').getBoundingClientRect(); return { top: Math.round(r.top), h: Math.round(r.height) }; })(),
    trackH: document.querySelector('#track').getBoundingClientRect().height,
  }));
  console.log(JSON.stringify(d, null, 1));
  console.log('ERRS:', errs.length ? errs.join('\n') : 'none');
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
