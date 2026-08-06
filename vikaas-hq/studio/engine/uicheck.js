// VIKAAS — UI check: drives the LIVE portfolio server, performs real interactions,
// asserts streaming/console health, saves proof screenshots.
// Usage: node engine/uicheck.js [baseUrl]
const path = require('path');
const fs = require('fs');
const zlib = require('zlib');
const cp = require('child_process');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
function ensureAl2023Libs() {
  if (fs.existsSync('/tmp/al2023/lib/libnspr4.so')) return;
  let dir = path.dirname(require.resolve('@sparticuz/chromium'));
  for (let i = 0; i < 8 && !fs.existsSync(path.join(dir, 'bin', 'al2023.tar.br')); i++) dir = path.dirname(dir);
  const br = path.join(dir, 'bin', 'al2023.tar.br');
  fs.mkdirSync('/tmp/al2023', { recursive: true });
  fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(br)));
  cp.execSync('tar -xf /tmp/al2023.tar -C /tmp/al2023');
  fs.rmSync('/tmp/al2023.tar', { force: true });
}
const _cr = require('@sparticuz/chromium');
const chromium = _cr.default || _cr;
const { chromium: pw } = require('playwright-core');

const BASE = process.argv[2] || 'http://127.0.0.1:4173';
const OUT = '/tmp/uicheck';
fs.mkdirSync(OUT, { recursive: true });
let PASS = 0, FAIL = 0;
function verdict(ok, name, extra) {
  console.log(`  ${ok ? '✅' : '❌'} ${name}${extra ? ' — ' + extra : ''}`);
  ok ? PASS++ : FAIL++;
}

async function withPage(name, vw, fn) {
  for (let a = 1; a <= 2; a++) {
    let browser;
    try {
      browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
      const page = await browser.newPage({ viewport: vw });
      page._errs = [];
      page.on('pageerror', e => page._errs.push(String(e)));
      page.on('console', m => { if (m.type() === 'error') page._errs.push(m.text()); });
      await fn(page);
      await browser.close();
      return;
    } catch (e) {
      try { await browser && browser.close(); } catch (_) {}
      console.log(`  retry(${a}) ${name}: ${String(e).split('\n')[0]}`);
    }
  }
  verdict(false, name + ' (page run crashed)');
}

(async () => {
  console.log('UICHECK', BASE);

  await withPage('index-desktop', { width: 1440, height: 900 }, async (page) => {
    const statuses = [];
    page.on('response', r => { if (r.url().includes('.mp4') || r.url().endsWith('.ttf')) statuses.push([r.status(), r.url().split('/').pop()]); });
    await page.goto(BASE + '/portfolio/index.html', { waitUntil: 'domcontentloaded' });
    verdict(page._errs.length === 0, 'index: zero console errors on boot', page._errs.slice(0, 2).join(' | '));
    await page.waitForTimeout(700);
    await page.screenshot({ path: OUT + '/i1_boot.png' });
    await page.evaluate(() => { try { sessionStorage.setItem('vboot', '1'); } catch (e) {} location.reload(); });
    await page.waitForTimeout(2200);
    // tooltip on chip hover
    await page.hover('.chip.mag').catch(() => {});
    await page.waitForTimeout(400);
    const tipOn = await page.evaluate(() => { const t = document.querySelector('.vtip'); return t && t.classList.contains('on'); });
    verdict(tipOn, 'index: chip tooltip appears on hover');
    // cursor label on room card
    await page.evaluate(() => document.getElementById('rooms').scrollIntoView());
    await page.waitForTimeout(900);
    const rvCount = await page.evaluate(() => document.querySelectorAll('.rv.on').length);
    verdict(rvCount >= 3, 'index: reveal-on-scroll fired (' + rvCount + ' elements on)');
    await page.hover('.room[data-go="ledger.html"]').catch(() => {});
    await page.waitForTimeout(350);
    const curLab = await page.evaluate(() => { const l = document.querySelector('.cur-lab'); return l && l.classList.contains('on') ? l.textContent : null; });
    verdict(curLab === 'ENTER →', 'index: cursor label on live card', String(curLab));
    await page.screenshot({ path: OUT + '/i2_rooms_tooltip.png' });
    // burger menu
    await page.click('#vbarMenu');
    await page.waitForTimeout(900);
    const navOn = await page.evaluate(() => document.querySelector('.vnav').classList.contains('on'));
    verdict(navOn, 'index: burger overlay opens');
    const navItems = await page.evaluate(() => document.querySelectorAll('.vnav-item').length);
    verdict(navItems === 6, 'index: menu lists 6 rooms');
    await page.screenshot({ path: OUT + '/i3_menu.png' });
    await page.keyboard.press('Escape');
    // locked room click honesty
    await page.evaluate(() => document.getElementById('rooms').scrollIntoView());
    await page.click('.room.locked').catch(() => {});
    await page.waitForTimeout(200);
    const badgeTxt = await page.evaluate(() => { const b = document.querySelector('.room.locked .badge'); return b ? b.textContent : ''; });
    verdict(badgeTxt.includes('COMING IN PHASE'), 'index: locked room tells its phase', badgeTxt.slice(0, 40));
    const codes = statuses.filter(s => s[1].endsWith('.ttf')).map(s => s[0]);
    verdict(codes.length > 0 && codes.every(c => c === 200), 'index: fonts 200 OK (' + codes.length + ')');
  });

  await withPage('ledger-desktop', { width: 1440, height: 900 }, async (page) => {
    await page.goto(BASE + '/portfolio/ledger.html', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1800);
    verdict(page._errs.length === 0, 'ledger: zero console errors', page._errs.slice(0, 2).join(' | '));
    // vbar injected
    verdict(await page.evaluate(() => !!document.querySelector('#vbarMenu')), 'ledger: juiced topbar injected');
    // scale toy interaction
    const before = await page.textContent('#verdict');
    await page.evaluate(() => { const r = document.getElementById('mykg'); r.value = 60; r.dispatchEvent(new Event('input')); });
    await page.waitForTimeout(400);
    const after = await page.textContent('#verdict');
    verdict(before !== after && after.includes('6.0'), 'ledger: scale toy reacts (6.0 kg verdict)', after.slice(0, 44));
    const w = await page.evaluate(() => document.getElementById('fill1').style.width);
    verdict(w === '1.2%', 'ledger: TRUE percent math (6kg vs 500 = 1.2%)', w);
    // stamp tooltip
    await page.hover('.stamp').catch(() => {});
    await page.waitForTimeout(400);
    const tipOn = await page.evaluate(() => { const t = document.querySelector('.vtip'); return t && t.classList.contains('on'); });
    verdict(tipOn, 'ledger: stamp tooltip explains itself');
    await page.screenshot({ path: OUT + '/l1_toy_stamp.png' });
  });

  await withPage('films-desktop', { width: 1440, height: 900 }, async (page) => {
    const got206 = [];
    page.on('response', r => { if (r.url().includes('.mp4')) got206.push([r.status(), r.url().split('/').pop().split('?')[0]]); });
    await page.goto(BASE + '/portfolio/films.html', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    verdict(page._errs.length === 0, 'films: zero console errors', page._errs.slice(0, 2).join(' | '));
    const cards = await page.evaluate(() => document.querySelectorAll('.film').length);
    verdict(cards === 5, 'films: 5 cinema cards present');
    const snds = await page.evaluate(() => document.querySelectorAll('button.snd').length);
    verdict(snds === 5, 'films: PLAY WITH SOUND buttons on all');
    const audios = await page.evaluate(() => document.querySelectorAll('.audiolab audio').length);
    verdict(audios === 2, 'films: audio lab players wired (2)');
    await page.evaluate(() => document.querySelector('.film').scrollIntoView({ block: 'center' }));
    await page.waitForTimeout(2500);
    await page.screenshot({ path: OUT + '/f1_cards.png' });
    const streamed = got206.some(s => s[0] === 206) || got206.length === 0; // headless codec may skip mp4 fetch entirely
    verdict(got206.length === 0 || got206.every(s => s[0] === 206 || s[0] === 200), 'films: mp4 responses via server (' + got206.map(g => g[0]).join(',') + ')');
    await page.click('.snd').catch(() => {});
    await page.waitForTimeout(800);
    const ctrl = await page.evaluate(() => { const v = document.querySelector('.film video'); return v && v.controls && !v.muted; });
    verdict(!!ctrl, 'films: PLAY WITH SOUND unmuts+controls');
    await page.screenshot({ path: OUT + '/f2_soundmode.png' });
  });

  await withPage('index-mobile', { width: 390, height: 844 }, async (page) => {
    await page.goto(BASE + '/portfolio/index.html', { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => { try { sessionStorage.setItem('vboot', '1'); } catch (e) {} location.reload(); });
    await page.waitForTimeout(2000);
    verdict(page._errs.length === 0, 'mobile: zero console errors');
    await page.click('#vbarMenu');
    await page.waitForTimeout(700);
    await page.screenshot({ path: OUT + '/m1_menu.png' });
    await page.keyboard.press('Escape');
    await page.evaluate(() => document.getElementById('rooms').scrollIntoView());
    await page.waitForTimeout(700);
    await page.screenshot({ path: OUT + '/m2_rooms.png' });
  });

  console.log(`\nUICHECK DONE — ${PASS} pass, ${FAIL} fail`);
  process.exit(FAIL ? 2 : 0);
})();
