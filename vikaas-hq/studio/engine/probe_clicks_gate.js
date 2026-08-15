// probe_clicks_gate.js — verify every nav link + menu is clickable.
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const base = process.argv[2] || 'http://localhost:5173';
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  let fail = 0;
  await page.goto(base + '/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  let menuOk = false;
  for (let i = 0; i < 3 && !menuOk; i++) {
    try { await page.click('.gnav-menu', { timeout: 3000 }); menuOk = true; }
    catch (e) { await page.waitForTimeout(1000); }
  }
  if (menuOk) console.log('  ✅ menu opens'); else { console.log('  ❌ menu click failed'); fail++; }
  await page.waitForSelector('.gnov a.gn-item', { timeout: 5000 });
  await page.waitForTimeout(300);
  const links = await page.$$('.gnov a.gn-item');
  if (!links.length) { console.log('  ❌ no overlay links'); fail++; }
  for (const l of links) {
    const href = await l.getAttribute('href');
    const pe = await l.evaluate(el => getComputedStyle(el).pointerEvents);
    if (pe !== 'auto') { console.log('  ❌ link ' + href + ' pe=' + pe); fail++; }
  }
  if (links.length) console.log('  ✅ ' + links.length + ' overlay links clickable');
  await page.keyboard.press('Escape');
  await page.waitForTimeout(800); // let exit animation fully finish + unmount
  try {
    await page.click('.gnav-menu', { timeout: 5000 });
    await page.waitForTimeout(500);
    await page.click('.gnov a[href="/drawer"]', { timeout: 3000 });
    await page.waitForTimeout(1000);
    const p = await page.evaluate(() => location.pathname);
    if (p === '/drawer') console.log('  ✅ nav to /drawer works');
    else { console.log('  ❌ nav landed ' + p); fail++; }
  } catch (e) { console.log('  ❌ nav: ' + e.message.slice(0, 80)); fail++; }
  await browser.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('CLICK-GATE CRASH ' + e.message.slice(0, 120)); process.exit(1); });
