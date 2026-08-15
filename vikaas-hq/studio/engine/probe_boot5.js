const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE:', e.message.slice(0, 200)));
  page.on('console', m => { if (m.type() === 'error') console.log('CON:', m.text().slice(0, 200)); });
  await page.goto('http://localhost:5173/boot', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  const r = await page.evaluate(() => {
    const ab = document.querySelector('#autoBoot');
    return {
      abExists: !!ab,
      abHTML: ab ? ab.innerHTML.slice(0, 200) : 'none',
      abClass: ab ? ab.className : 'none',
      bodyHasWord: !!document.querySelector('.ab-word'),
      allSpans: Array.from(document.querySelectorAll('#autoBoot span')).slice(0, 3).map(s => s.className),
      rootKids: document.getElementById('root') ? document.getElementById('root').children.length : -1,
      bodyText: document.body.innerText.slice(0, 120),
    };
  });
  console.log(JSON.stringify(r, null, 1));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
