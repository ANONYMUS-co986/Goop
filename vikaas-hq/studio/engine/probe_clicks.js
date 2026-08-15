const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 120)));
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);
  // open the menu
  const menuBtn = await page.$('.gnav-menu');
  const menuVisible = await page.evaluate(() => { const m = document.querySelector('.gnav-menu'); const r = m.getBoundingClientRect(); const cs = getComputedStyle(m); return { visible: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0, pe: cs.pointerEvents, z: cs.zIndex, rect: { x: r.x, y: r.y, w: r.width, h: r.height } }; });
  console.log('menu btn:', JSON.stringify(menuVisible));
  if (menuBtn) {
    try { await menuBtn.click({ timeout: 3000 }); console.log('menu click OK'); }
    catch (e) { console.log('menu click FAIL:', e.message.slice(0, 120)); }
  }
  await page.waitForTimeout(800);
  // now what's in the overlay? are the links clickable?
  const overlay = await page.evaluate(() => {
    const ov = document.querySelector('.gnov');
    if (!ov) return { open: false };
    const links = Array.from(ov.querySelectorAll('a.gn-item, .gn-item'));
    return {
      open: true,
      opacity: getComputedStyle(ov).opacity,
      pe: getComputedStyle(ov).pointerEvents,
      items: links.map(a => ({ t: a.querySelector('.tt') ? a.querySelector('.tt').textContent : a.textContent, tag: a.tagName, href: a.getAttribute('href'), pe: getComputedStyle(a).pointerEvents, cls: a.className })),
    };
  });
  console.log('overlay:', JSON.stringify(overlay, null, 1));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
