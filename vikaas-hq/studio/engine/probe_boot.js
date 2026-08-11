const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message.slice(0,150)));
  await page.goto('file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html', { waitUntil: 'load' });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  const s5 = await page.evaluate(() => ({
    bootOn: !!document.querySelector('#autoBoot'),
    typed: (document.querySelector('#abTerm')||{}).textContent ? document.querySelector('#abTerm').textContent.length : 0,
    bar: (document.querySelector('#abBar')||{}).style ? document.querySelector('#abBar').style.width : '',
    status: (document.querySelector('#abStatus')||{}).textContent || '',
    webgl: !!document.querySelector('canvas#three').width,
  }));
  console.log('T+1s', JSON.stringify(s5));
  await page.waitForTimeout(6000);
  const s6 = await page.evaluate(() => ({
    typed: document.querySelector('#abTerm').textContent.length,
    bar: document.querySelector('#abBar').style.width,
    status: document.querySelector('#abStatus').textContent,
    word: document.querySelector('#abWord').textContent,
  }));
  console.log('T+7s', JSON.stringify(s6));
  await page.waitForTimeout(5000);
  const s7 = await page.evaluate(() => ({
    bootGone: !document.querySelector('#autoBoot'),
    cue: getComputedStyle(document.querySelector('#cue')).opacity,
    stEnabled: window.ScrollTrigger ? ScrollTrigger.getAll().map(t=>t.enabled) : [],
  }));
  console.log('T+12s', JSON.stringify(s7));
  console.log('ERRS:', errs.length ? errs.join('|') : 'none');
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
