const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  // check the scale's scroll trigger state + manual scrub via window scroll
  const info = await page.evaluate(() => {
    const sts = window.ScrollTrigger.getAll().map(t => ({ trigger: t.trigger ? (t.trigger.id || t.trigger.className.slice(0,20)) : 'none', prog: +t.progress.toFixed(3), start: t.start, end: t.end }));
    const rig = document.querySelector('#scaleRig');
    const r = rig.getBoundingClientRect();
    return { sts: sts.slice(0, 8), rigTop: Math.round(r.top), rigH: Math.round(r.height), scrollY: window.scrollY, docH: document.documentElement.scrollHeight, vh: innerHeight };
  });
  console.log(JSON.stringify(info, null, 1));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
