const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3500);
  const r = await page.evaluate(() => {
    const btn = document.querySelector('.gnav-menu');
    const b = btn.getBoundingClientRect();
    const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
    const top = document.elementFromPoint(cx, cy);
    const gnav = document.querySelector('.gnav');
    const gn = gnav.getBoundingClientRect();
    return {
      btn: { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) },
      gnavZ: getComputedStyle(gnav).zIndex,
      gnavPos: getComputedStyle(gnav).position,
      topAtBtn: top ? (top.id || top.tagName + '.' + (top.className || '').slice(0, 30)) : 'none',
      topZ: top ? getComputedStyle(top).zIndex : '?',
      canvas: (() => { const c = document.querySelector('.mono-wrap canvas'); const cr = c.getBoundingClientRect(); return { x: Math.round(cr.x), y: Math.round(cr.y), w: Math.round(cr.width), h: Math.round(cr.height), pe: getComputedStyle(c).pointerEvents, parentPe: getComputedStyle(c.parentElement).pointerEvents }; })(),
    };
  });
  console.log(JSON.stringify(r, null, 1));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
