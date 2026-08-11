const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  // GATE hero
  let page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3500);
  await page.screenshot({ path: '/tmp/suite/gate-hero.png' });
  await page.close();
  // DRAWER story + toy
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  await page.evaluate(() => { document.querySelector('#story').scrollIntoView({ behavior: 'instant', block: 'start' }); });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/tmp/suite/drawer-story.png' });
  await page.evaluate(() => { document.querySelector('#toy').scrollIntoView({ behavior: 'instant', block: 'start' }); });
  await page.waitForTimeout(800);
  await page.screenshot({ path: '/tmp/suite/drawer-toy.png' });
  await page.close();
  // BOOT stage
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:5173/boot?fast=1', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/suite/boot-stage.png' });
  await browser.close();
  console.log('done');
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
