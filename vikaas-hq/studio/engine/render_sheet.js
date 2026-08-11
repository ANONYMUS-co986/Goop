// render_sheet.js — render a local HTML file to PNG with the in-sandbox Chromium.
// Usage: node render_sheet.js <htmlPath> <outPng> [width] [height]
// QA: asserts fonts loaded (SpaceGrotesk/Anton/NotoDev) + every element inside viewport.
const path = require('path');
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

const htmlPath = path.resolve(process.argv[2]);
const outPng = process.argv[3];
const W = parseInt(process.argv[4] || '1080', 10);
const H = parseInt(process.argv[5] || '1920', 10);

(async () => {
  const browser = await pw.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath(),
    headless: true,
    ignoreHTTPSErrors: true,
  });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.goto('file://' + htmlPath, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const qa = await page.evaluate(async () => {
    const fonts = [];
    for (const f of ['SpaceGrotesk', 'Anton', 'NotoDev']) {
      await document.fonts.load(`16px "${f}"`);
      const loaded = document.fonts.check(`16px "${f}"`);
      const dev = f === 'NotoDev' ? document.fonts.check('16px "NotoDev"', 'री-बी') : true;
      fonts.push({ f, loaded, dev });
    }
    const clipped = [];
    document.querySelectorAll('body *').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0 && (r.bottom > window.innerHeight + 1 || r.right > window.innerWidth + 1)) {
        clipped.push(el.className || el.tagName);
      }
    });
    return { fonts, clipped: clipped.slice(0, 10), docH: document.documentElement.scrollHeight, vpH: window.innerHeight };
  });
  console.log('QA fonts:', JSON.stringify(qa.fonts));
  console.log('QA clipped:', qa.clipped.length ? qa.clipped : 'none', '| docH:', qa.docH, 'vp:', qa.vpH);

  await page.screenshot({ path: outPng, fullPage: false });
  console.log('rendered:', outPng);
  await browser.close();
  if (qa.fonts.some((f) => !f.loaded)) { console.error('FAIL: a font did not load'); process.exit(1); }
  if (qa.clipped.length) { console.error('FAIL: clipped elements present'); process.exit(1); }
})().catch((e) => { console.error('FAIL:', e.message); process.exit(1); });
