#!/usr/bin/env node
/* ============================================================
   VIKAAS FINALE POWER SUITE — suite.js
   One CLI for the whole self-review loop:
     node suite.js qa <url> [outDir] [--mobile] [--beats a,b,c]
       - walks scroll progress beats, screenshots, reports console/page errors,
         overlap probes (elementFromPoint at center/bottom), enter-button check
     node suite.js verify <url>          -> exits 1 if ANY error/overlap found
   Usage: cd vikaas-hq/studio && node engine/suite.js qa <url>
   ============================================================ */
const path = require('path');
const fs = require('fs');
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

const URL = process.argv[3];
if (!URL) { console.error('usage: node suite.js qa|verify <url> [outDir] [--mobile] [--beats=0.05,0.3,0.55,0.85,0.97]'); process.exit(2); }
const MODE = process.argv[2];
const ARGS = process.argv.slice(4);
const OUT = ARGS.find((a) => !a.startsWith('--')) || '/tmp/suite';
const MOBILE = ARGS.includes('--mobile');
const beatsArg = ARGS.find((a) => a.startsWith('--beats='));
const BEATS = beatsArg ? beatsArg.split('=')[1].split(',').map(Number) : [0.05, 0.3, 0.55, 0.85, 0.97];
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const vp = MOBILE ? { width: 390, height: 844 } : { width: 1440, height: 900 };
  const page = await browser.newPage({ viewport: vp });
  const errors = [];
  page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message.slice(0, 200)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 200)); });

  await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(900);

  const extent = await page.evaluate(() => Math.max(document.documentElement.scrollHeight - innerHeight, 1));
  const report = { viewport: vp, extent, beats: [] };

  for (const frac of BEATS) {
    await page.evaluate((y) => window.scrollTo(0, y), Math.floor(extent * frac));
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const at = (x, y) => { const el = document.elementFromPoint(x, y); return el ? (el.id || el.tagName + '.' + String(el.className || '').split(' ')[0]) : 'none'; };
      const box = (s) => { const el = document.querySelector(s); if (!el) return null; const b = el.getBoundingClientRect(); return { t: Math.round(b.top), b: Math.round(b.bottom), l: Math.round(b.left), r: Math.round(b.right) }; };
      const overlap = (a, b) => a && b && !(a.b < b.t || b.b < a.t || a.r < b.l || b.r < a.l);
      const term = box('#termbox'), stats = box('#stats'), ent = box('#enter');
      return {
        center: at(innerWidth / 2, innerHeight / 2),
        bottom: at(innerWidth / 2, innerHeight - 70),
        overlaps: {
          term_stats: overlap(term, stats),
          stats_enter: overlap(stats, ent),
          term_enter: overlap(term, ent),
        },
        enterShow: (document.querySelector('#enter') || {}).classList ? document.querySelector('#enter').classList.contains('show') : false,
      };
    });
    const shot = path.join(OUT, 'beat-' + String(frac).replace('.', '') + (MOBILE ? '-m' : '') + '.png');
    await page.screenshot({ path: shot });
    report.beats.push({ frac, ...r, shot });
  }

  // final enter clickability
  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  await page.waitForTimeout(1000);
  let clickable = false;
  try { await page.click('#enter', { timeout: 3000 }); clickable = true; } catch (e) { clickable = false; }
  await page.waitForTimeout(400);
  report.enterClickable = clickable;
  report.leaving = await page.evaluate(() => { const s = document.querySelector('#stage'); return s ? (s.className || '').includes('leaving') : false; }).catch(() => false);
  report.errors = errors;

  const fail = errors.length > 0 || report.beats.some((b) => b.overlaps.term_stats || b.overlaps.stats_enter || b.overlaps.term_enter) || !clickable;
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
  if (MODE === 'verify' && fail) { console.error('SUITE: FAIL'); process.exit(1); }
  console.log(fail ? 'SUITE: FAIL' : 'SUITE: PASS');
})().catch((e) => { console.error('SUITE CRASH:', e.message.slice(0, 300)); process.exit(1); });
