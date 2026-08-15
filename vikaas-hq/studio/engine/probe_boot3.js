const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE: ' + e.message.slice(0, 250)));
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text().slice(0, 250)); });
  await page.goto('http://localhost:5173/boot', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  const s = await page.evaluate(() => ({
    abTerm: (document.querySelector('#abTerm')||{}).textContent ? document.querySelector('#abTerm').textContent.length : 'NO-EL',
    abWord: (document.querySelector('#abWord')||{}).textContent || 'NO-EL',
    abStatus: (document.querySelector('.ab-status')||{}).textContent || 'NO-EL',
    autoBoot: !!document.querySelector('#autoBoot'),
    stage: !!document.querySelector('#stage'),
  }));
  console.log(JSON.stringify(s));
  console.log('errs:', errs.length ? errs.join('\n') : 'NONE');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
