const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));
  await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * 0.97));
  await page.waitForTimeout(1200);
  const info = await page.evaluate(() => {
    const b = document.querySelector('#enter');
    const r = b.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const top = document.elementFromPoint(cx, cy);
    const cs = getComputedStyle(b);
    return {
      box: { left: Math.round(r.left), top: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) },
      center: [Math.round(cx), Math.round(cy)],
      topEl: top ? (top.id || top.tagName + '.' + (top.className || '')) : 'NONE',
      show: b.classList.contains('show'),
      pe: cs.pointerEvents, z: cs.zIndex, opacity: cs.opacity,
    };
  });
  console.log(JSON.stringify(info, null, 1));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
