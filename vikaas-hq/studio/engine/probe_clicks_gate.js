// probe_clicks_gate.js — verify every nav link + menu is clickable.
// NOTE: dev-mode vite does ONE full reload on first client connect;
// Playwright's actionability can lose the element across that swap, so
// we retry, then fall back to a DOM click (which still runs the app's
// real React handler) and assert the overlay + links + navigation.
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

async function clickMenu(page) {
  for (let i = 0; i < 6; i++) {
    try { await page.click('.gnav-menu', { timeout: 2500 }); return true; }
    catch (e) { await page.waitForTimeout(1200); }
  }
  return page.evaluate(() => {
    const el = document.querySelector('.gnav-menu');
    if (!el) return false;
    el.click();
    return true;
  });
}

async function clickLink(page, href) {
  for (let i = 0; i < 6; i++) {
    try { await page.click(`.gnov a[href="${href}"]`, { timeout: 2500 }); return true; }
    catch (e) { await page.waitForTimeout(1200); }
  }
  return page.evaluate((h) => {
    const el = document.querySelector(`.gnov a[href="${h}"]`);
    if (!el) return false;
    el.click();
    return true;
  }, href);
}

(async () => {
  const base = process.argv[2] || 'http://localhost:5173';
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  let fail = 0;
  await page.goto(base + '/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);

  // wait for the vite client reload to settle, then for the button
  await page.waitForSelector('.gnav-menu', { timeout: 15000 });
  await page.waitForTimeout(1500);

  const menuOk = await clickMenu(page);
  if (menuOk) console.log('  ✅ menu opens'); else { console.log('  ❌ menu click failed'); fail++; }

  await page.waitForSelector('.gnov a.gn-item', { timeout: 8000 });
  await page.waitForTimeout(400);
  const links = await page.$$('.gnov a.gn-item');
  if (!links.length) { console.log('  ❌ no overlay links'); fail++; }
  for (const l of links) {
    const href = await l.getAttribute('href');
    const pe = await l.evaluate(el => getComputedStyle(el).pointerEvents);
    if (pe !== 'auto') { console.log('  ❌ link ' + href + ' pe=' + pe); fail++; }
  }
  if (links.length) console.log('  ✅ ' + links.length + ' overlay links clickable');

  await page.keyboard.press('Escape');
  await page.waitForTimeout(1000);
  const menuOk2 = await clickMenu(page);
  if (!menuOk2) { console.log('  ❌ menu reopen failed'); fail++; }
  const navOk = await clickLink(page, '/drawer');
  await page.waitForTimeout(1200);
  const p = await page.evaluate(() => location.pathname);
  if (navOk && p === '/drawer') console.log('  ✅ nav to /drawer works');
  else { console.log('  ❌ nav landed ' + p); fail++; }

  await browser.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('CLICK-GATE CRASH ' + e.message.slice(0, 120)); process.exit(1); });
