const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
async function launch() {
  for (let i = 0; i < 3; i++) {
    try { return await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  throw new Error('launch failed');
}
(async () => {
  const browser = await launch();
  for (const [label, url] of [['GATE', 'http://localhost:5173/'], ['DRAWER', 'http://localhost:5173/drawer']]) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push('PAGE: ' + e.message.slice(0, 160)));
    page.on('console', m => { if (m.type() === 'error') errs.push('CON: ' + m.text().slice(0, 160)); });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    await page.waitForTimeout(2500);
    const d = await page.evaluate(() => {
      const r = {};
      const title = document.querySelector('.gate-title');
      r.titleExists = !!title;
      if (title) {
        r.titleOpacity = getComputedStyle(title).opacity;
        r.chars = Array.from(title.querySelectorAll('.ch')).slice(0, 8).map(c => getComputedStyle(c).opacity);
        r.devOpacity = title.querySelector('.dev') ? getComputedStyle(title.querySelector('.dev')).opacity : 'no-dev';
      }
      const toy = document.querySelector('.drawer-toy');
      r.toy = toy ? { cls: toy.className, front: toy.querySelector('.toy-front') ? getComputedStyle(toy.querySelector('.toy-front')).transform : 'no-front' } : 'no-toy';
      const hero = document.querySelector('#hero');
      r.hero = hero ? { h: Math.round(hero.getBoundingClientRect().height), top: Math.round(hero.getBoundingClientRect().top) } : 'none';
      const nav = document.querySelector('.gnav');
      r.navOverlap = nav ? (nav.getBoundingClientRect().bottom) : 'no-nav';
      r.scrollH = document.documentElement.scrollHeight;
      r.mainTop = document.querySelector('main') ? Math.round(document.querySelector('main').getBoundingClientRect().top) : 'no-main';
      return r;
    });
    console.log('== ' + label + ' ==');
    console.log(JSON.stringify(d, null, 1));
    console.log('errors:', errs.length ? errs.join(' | ') : 'none');
    await page.screenshot({ path: '/tmp/suite/' + label.toLowerCase() + '-deep.png' });
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0, 200)); process.exit(1); });
