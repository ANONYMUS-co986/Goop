// shoot_boot.js — VIKAAS loader v2 self-review: scrolls the pinned timeline,
// screenshots each beat, reports console errors + key states.
const path = require('path');
const fs = require('fs');
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
const OUT = '/tmp/qa_boot'; fs.mkdirSync(OUT, { recursive: true });
const URL = 'file:///home/user/Goop/vikaas-hq/portfolio/v2/loader.html';
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message.slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 160)); });
  await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(700);

  // scroll extent = track height - viewport
  await page.waitForTimeout(400);
  const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));

  const beats = [
    [0.00, 'b0-start'], [0.08, 'b1-term'], [0.25, 'b2-creak'], [0.30, 'b3-lid-open'],
    [0.45, 'b4-word'], [0.58, 'b5-stats'], [0.70, 'b6-rebee'], [0.85, 'b7-bigline'], [0.97, 'b8-enter'],
  ];
  for (const [frac, name] of beats) {
    await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * frac));
    await page.waitForTimeout(650);
    await page.screenshot({ path: path.join(OUT, name + '.png') });
  }
  const states = await page.evaluate(() => {
    const vis = (sel) => { const el = document.querySelector(sel); if (!el) return 'MISS'; const cs = getComputedStyle(el); return cs.opacity !== '0' && cs.display !== 'none' && cs.visibility !== 'hidden'; };
    return {
      word: document.querySelector('#word').textContent,
      dev: getComputedStyle(document.querySelector('#dev')).opacity,
      statsOn: Array.from(document.querySelectorAll('.stat')).filter(s => getComputedStyle(s).opacity !== '0').length,
      stampsOn: Array.from(document.querySelectorAll('.stamp')).filter(s => getComputedStyle(s).opacity !== '0').length,
      enterShow: document.querySelector('#enter').classList.contains('show'),
      rebee: getComputedStyle(document.querySelector('#rebeeFly')).opacity,
      rail: document.querySelector('#railFill').style.height,
      webgl: !!document.querySelector('canvas#three'),
      threeOk: (window.THREE && document.querySelector('canvas#three').width > 0),
    };
  });
  console.log('STATES:', JSON.stringify(states));
  // click enter -> should leave
  await page.click('#enter');
  await page.waitForTimeout(1400);
  const left = await page.evaluate(() => ({ leaving: (document.querySelector('#stage') || {}).className || null, href: location.href }));
  console.log('LEAVE:', JSON.stringify(left));
  console.log('ERRORS:', errors.length ? '\n' + errors.join('\n') : 'none');
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
