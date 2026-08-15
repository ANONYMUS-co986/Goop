const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGEERROR:', e.message.slice(0, 120)));
  page.on('console', m => { const t = m.text(); if (m.type() === 'error' || t.includes('above error') || t.includes('component')) console.log('CONSOLE:', t.slice(0, 600)); });
  await page.goto('http://localhost:5173/boot?fast=1', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2200);
  // check how many chars/words are in #word now (did innerHTML init run?)
  const pre = await page.evaluate(() => ({ wordChildren: document.querySelector('#word').children.length, wordHTML: document.querySelector('#word').innerHTML.slice(0, 60) }));
  console.log('pre-enter word:', JSON.stringify(pre));
  await page.click('#enter');
  await page.waitForTimeout(2500);
  const post = await page.evaluate(() => ({ root: document.getElementById('root').innerHTML.length, bodyText: document.body.innerText.slice(0, 40) }));
  console.log('post:', JSON.stringify(post));
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
