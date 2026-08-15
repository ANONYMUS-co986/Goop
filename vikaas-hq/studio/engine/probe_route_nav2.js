const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('C:' + m.text().slice(0, 140)); });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2800);
  // SPA nav: click the drawer room-card link (in-page)
  const cardLink = await page.$('.room-card[href="/drawer"]');
  if (cardLink) {
    await cardLink.click();
  } else {
    // fallback: history push
    await page.evaluate(() => history.pushState({}, '', '/drawer'));
    await page.evaluate(() => window.dispatchEvent(new PopStateEvent('popstate')));
  }
  await page.waitForTimeout(1400);
  const r = await page.evaluate(() => ({
    path: location.pathname,
    wipeVisible: (() => { const w = document.querySelector('.pagewipe'); return w ? getComputedStyle(w).transform : 'none'; })(),
    drawerIntro: !!document.querySelector('#dintro'),
    scrollH: document.documentElement.scrollHeight,
  }));
  await page.screenshot({ path: '/tmp/qa_gate/nav-drawer.png' });
  console.log(JSON.stringify(r));
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
