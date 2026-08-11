const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
async function launch() {
  for (let i = 0; i < 3; i++) {
    try { return await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  throw new Error('launch failed');
}
(async () => {
  const url = process.argv[2];
  const browser = await launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'load', timeout: 45000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(1500);
  const d = await page.evaluate(() => {
    const sections = Array.from(document.querySelectorAll('section')).map(s => ({ id: s.id, h: Math.round(s.getBoundingClientRect().height) }));
    return { scrollHeight: document.documentElement.scrollHeight, vh: innerHeight, scrolls: Math.round(document.documentElement.scrollHeight / innerHeight), sections };
  });
  console.log(JSON.stringify(d));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0,120)); process.exit(1); });
