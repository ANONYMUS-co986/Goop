const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  await page.click('.gnav-menu');
  await page.waitForTimeout(600);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => {
    const btn = document.querySelector('.gnav-menu');
    const b = btn.getBoundingClientRect();
    const top = document.elementFromPoint(b.x + b.width/2, b.y + b.height/2);
    const ov = document.querySelector('.gnov');
    return {
      btnVisible: getComputedStyle(btn).display !== 'none' && b.width > 0,
      btnPe: getComputedStyle(btn).pointerEvents,
      btnRect: { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) },
      topEl: top ? (top.id || top.tagName + '.' + (top.className||'').slice(0,20)) : 'none',
      overlayStillThere: !!ov,
      overlayDisplay: ov ? getComputedStyle(ov).display : 'gone',
      overlayPe: ov ? getComputedStyle(ov).pointerEvents : 'gone',
    };
  });
  console.log(JSON.stringify(r, null, 1));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
