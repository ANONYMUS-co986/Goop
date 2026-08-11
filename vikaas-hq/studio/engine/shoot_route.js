const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const route = process.argv[2] || '/';
  const out = process.argv[3] || '/tmp/suite/shot.png';
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173' + route, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3500);
  await page.screenshot({ path: out });
  console.log('shot', out);
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
