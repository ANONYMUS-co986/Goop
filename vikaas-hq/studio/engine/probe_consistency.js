const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
async function run(vp, label) {
  let browser;
  try {
    browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
    const page = await browser.newPage({ viewport: vp });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message.slice(0,120)));
    await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load', timeout: 45000 });
    await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
    await page.waitForTimeout(900);
    const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));
    const probes = [];
    for (const frac of [0.05, 0.3, 0.55, 0.85, 0.97]) {
      await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * frac));
      await page.waitForTimeout(350);
      const r = await page.evaluate(() => {
        const at = (x, y) => { const el = document.elementFromPoint(x, y); return el ? (el.id || el.tagName + '.' + (el.className || '').split(' ')[0]) : 'none'; };
        const box = (s) => { const el = document.querySelector(s); if (!el) return null; const b = el.getBoundingClientRect(); return { t: Math.round(b.top), b: Math.round(b.bottom), l: Math.round(b.left), r: Math.round(b.right) }; };
        return { term: box('#termbox'), stats: box('#stats'), enter: box('#enter'),
                 center: at(innerWidth/2, innerHeight/2), bottom: at(innerWidth/2, innerHeight-70),
                 enterShow: (document.querySelector('#enter')||{}).classList ? document.querySelector('#enter').classList.contains('show') : false };
      });
      probes.push({ frac, ...r });
    }
    console.log(label, JSON.stringify({ errs, extent, probes }));
    await browser.close();
  } catch (e) { console.log(label, 'FAIL', e.message.slice(0,150)); if (browser) await browser.close().catch(()=>{}); }
}
(async () => {
  await run({ width: 1440, height: 900 }, 'DESKTOP');
  await run({ width: 390, height: 844 }, 'MOBILE');
  await run({ width: 820, height: 1180 }, 'TABLET');
})();
