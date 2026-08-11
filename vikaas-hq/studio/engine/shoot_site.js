// shoot_site.js — VIKAAS portfolio self-review harness.
// Opens the hub in-sandbox, walks every section, saves screenshots to /tmp/qa/.
// Usage: node engine/shoot_site.js [outDir]
const path = require('path');
const fs = require('fs');
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

const OUT = process.argv[2] || '/tmp/qa';
fs.mkdirSync(OUT, { recursive: true });
const URL = 'file:///home/user/Goop/vikaas-hq/portfolio/index.html?fast=1';

(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message.slice(0, 200)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 200)); });

  await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(2600); // hero intro
  await page.screenshot({ path: path.join(OUT, '01-hero.png') });

  const sections = [
    ['02-story', '#story', 800],
    ['03-receipt', '#receipt', 300],
    ['04-scale', '#scale', 300],
    ['05-arsenal', '#pinArs', 700],
    ['06-rebee', '#rebee', 300],
    ['07-plan', '#plan', 400],
    ['08-foot', '#foot', 0],
  ];
  for (const [name, sel, extra] of sections) {
    try {
      await page.evaluate((s) => { document.querySelector(s).scrollIntoView({ behavior: 'instant', block: 'start' }); }, sel);
      await page.waitForTimeout(350);
      if (extra) await page.evaluate((y) => window.scrollBy(0, y), extra);
      await page.waitForTimeout(1300);
      await page.screenshot({ path: path.join(OUT, name + '.png') });
    } catch (e) { errors.push('SHOTFAIL ' + name + ': ' + e.message.slice(0, 120)); }
  }

  await browser.close();
  console.log('ERRORS:' + (errors.length ? '\n' + errors.join('\n') : ' none'));
  const files = fs.readdirSync(OUT).filter((f) => f.endsWith('.png')).sort();
  console.log('SHOTS:', files.join(', '));
})().catch((e) => { console.error('FAIL', e.message); process.exit(1); });
