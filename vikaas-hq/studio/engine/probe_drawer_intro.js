const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('P:' + e.message.slice(0, 140)));
  await page.goto('http://localhost:5173/drawer', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  const intro = await page.evaluate(() => ({
    lines: document.querySelectorAll('.dt-line').length,
    line1op: getComputedStyle(document.querySelector('.dt-line[data-line="the"]')).opacity,
    line2op: getComputedStyle(document.querySelector('.dt-line[data-line="drawer"]')).opacity,
    sub: getComputedStyle(document.querySelector('#dintroSub')).opacity,
    rail: !!document.querySelector('.story-rail i'),
  }));
  console.log('intro:', JSON.stringify(intro));
  // story scrub: scroll to mid-story, check rail fills + lines visible
  await page.evaluate(() => { document.querySelector('.story-wrap').scrollIntoView({ behavior: 'instant', block: 'start' }); });
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollBy(0, 1400));
  await page.waitForTimeout(800);
  const story = await page.evaluate(() => ({
    railH: document.querySelector('.story-rail i').style.height,
    l1: getComputedStyle(document.querySelector('.story-copy .l1')).opacity,
    big: getComputedStyle(document.querySelector('.story-copy .big')).opacity,
  }));
  console.log('story mid:', JSON.stringify(story));
  await page.screenshot({ path: '/tmp/qa_gate/drawer-story-mid.png' });
  console.log('errs:', errs.length ? errs.join(' | ') : 'none');
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 150)); process.exit(1); });
