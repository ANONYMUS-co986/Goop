const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('console', m => { if (m.type() === 'error') console.log('CON:', m.text().slice(0, 200)); });
  page.on('pageerror', e => console.log('PAGE:', e.message.slice(0, 200)));
  await page.goto('http://localhost:5173/boot', { waitUntil: 'networkidle', timeout: 45000 });
  const env = await page.evaluate(() => ({ reduce: matchMedia('(prefers-reduced-motion: reduce)').matches, fast: new URLSearchParams(location.search).has('fast'), url: location.href }));
  console.log('ENV:', JSON.stringify(env));
  await page.waitForTimeout(3000);
  const s = await page.evaluate(() => ({
    abTermLen: (document.querySelector('#abTerm')||{}).textContent ? document.querySelector('#abTerm').textContent.length : 'NO-EL',
    abWord: (document.querySelector('#abWord')||{}).textContent || 'NO-EL',
    bootChildren: document.querySelector('#autoBoot') ? document.querySelector('#autoBoot').children.length : -1,
  }));
  console.log('STATE:', JSON.stringify(s));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
