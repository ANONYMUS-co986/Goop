// Render build/index.html -> Project_Verde_Documentation.pdf via bundled Chromium
const path = require('path');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
const chromium = require('@sparticuz/chromium').default;
const { chromium: pw } = require('playwright-core');

(async () => {
  const browser = await pw.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath(),
    headless: true,
  });
  const page = await browser.newPage();
  const file = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(file, { waitUntil: 'load' });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
  await page.waitForTimeout(600);

  // --- DOM overflow audit: any page whose content exceeds the A4 box? ---
  const audit = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const dh = pg.scrollHeight - pg.clientHeight;
      const dw = pg.scrollWidth - pg.clientWidth;
      if (dh > 2 || dw > 2) bad.push({ page: i + 1, overH: dh, overW: dw });
      // also flag content elements spilling past the page bounds
      pg.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        const pr = pg.getBoundingClientRect();
        if (r.bottom > pr.bottom + 3 || r.right > pr.right + 3) {
          const tag = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : '');
          bad.push({ page: i + 1, el: tag.slice(0, 80), bottomOver: Math.round(r.bottom - pr.bottom), rightOver: Math.round(r.right - pr.right) });
        }
      });
    });
    return bad;
  });
  if (audit.length) {
    console.log('OVERFLOW AUDIT:');
    audit.slice(0, 40).forEach(a => console.log(' ', JSON.stringify(a)));
  } else {
    console.log('OVERFLOW AUDIT: clean — no clipped pages or elements');
  }

  await page.pdf({
    path: path.resolve(__dirname, '..', 'Project_Verde_Documentation.pdf'),
    width: '210mm', height: '297mm',
    printBackground: true,
    preferCSSPageSize: true,
    outline: true,
    tagged: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });
  await browser.close();
  console.log('PDF written');
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
