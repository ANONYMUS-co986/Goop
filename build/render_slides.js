// Render every .page of build/index.html -> build/slides/slide-NN.png
// Same Chromium engine + entry point as render.js, so rasters are pixel-clones
// of the Project_Verde_Documentation.pdf (FX edition) pages.
// deviceScaleFactor 3.125 = 96dpi * 3.125 = exactly 300 DPI on A4 portrait.
const path = require('path');
const fs = require('fs');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');
const _cr = require('@sparticuz/chromium');
const chromium = _cr.default || _cr;
const { chromium: pw } = require('playwright-core');

(async () => {
  const outDir = path.resolve(__dirname, 'slides');
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await pw.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath(),
    headless: true,
  });
  const page = await browser.newPage({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 3.125, // 300 DPI
  });
  const file = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(file, { waitUntil: 'load' });
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await Promise.all(Array.from(document.images).map(img =>
      img.complete ? Promise.resolve()
        : new Promise(res => { img.onload = img.onerror = res; })));
    await Promise.all(Array.from(document.images).map(img =>
      img.decode ? img.decode().catch(() => {}) : Promise.resolve()));
  });
  await page.waitForTimeout(800);

  const pages = await page.$$('.page');
  console.log('pages found:', pages.length);
  if (!pages.length) throw new Error('no .page elements found');

  for (let i = 0; i < pages.length; i++) {
    const name = 'slide-' + String(i + 1).padStart(2, '0') + '.png';
    await pages[i].screenshot({ path: path.join(outDir, name) });
    console.log('captured', i + 1, '/', pages.length);
  }
  await browser.close();
  console.log('DONE', pages.length, 'slides ->', outDir);
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
