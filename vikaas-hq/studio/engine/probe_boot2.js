const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/boot', { waitUntil: 'networkidle', timeout: 45000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(1200);
  // first gesture unlock
  await page.mouse.move(400, 400); await page.mouse.down(); await page.mouse.up();
  const s1 = await page.evaluate(() => ({
    bootOn: !!document.querySelector('#autoBoot'),
    typed: (document.querySelector('#abTerm')||{}).textContent ? document.querySelector('#abTerm').textContent.length : 0,
    pct: (document.querySelector('.ab-status span')||{}).textContent || '',
    webgl: !!document.querySelector('canvas#three').width,
  }));
  console.log('T+1.2s:', JSON.stringify(s1));
  await page.waitForTimeout(7000);
  const s2 = await page.evaluate(() => ({
    typed: document.querySelector('#abTerm').textContent.length,
    pct: (document.querySelector('.ab-status span')||{}).textContent || '',
    status: document.querySelector('.ab-status').textContent,
    word: document.querySelector('#abWord').textContent,
  }));
  console.log('T+8s:', JSON.stringify(s2));
  await page.waitForTimeout(5000);
  const s3 = await page.evaluate(() => ({
    bootGone: !document.querySelector('#autoBoot'),
    cue: getComputedStyle(document.querySelector('#cue')).opacity,
    amb: !!window.__amb,
  }));
  console.log('T+13s:', JSON.stringify(s3));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
