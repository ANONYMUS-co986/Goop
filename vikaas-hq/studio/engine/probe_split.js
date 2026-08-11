const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
(async () => {
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message.slice(0, 200)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(3000);
  const r = await page.evaluate(async () => {
    const out = {};
    const mod = await import('/node_modules/.vite/deps/split-type.js?v=' + Date.now()).catch(e => 'IMPORT_FAIL: ' + e.message);
    out.modType = typeof mod;
    if (mod && mod.default) out.defaultType = typeof mod.default;
    const en = document.querySelector('.gate-title .en');
    out.enHTML = en ? en.innerHTML.slice(0, 120) : 'no-en';
    try {
      const SplitTypeCtor = (mod && mod.default) || (mod && mod.default && mod.default.default);
      out.ctorType = typeof SplitTypeCtor;
      const s = new SplitType(en, { types: 'chars' });
      out.chars = s.chars ? s.chars.length : 'no-chars-arr';
      out.afterHTML = en.innerHTML.slice(0, 200);
    } catch (e) { out.splitErr = e.message.slice(0, 200); }
    return out;
  });
  console.log(JSON.stringify(r, null, 1));
  console.log('ERR:', errs.join(' | '));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message.slice(0, 200)); process.exit(1); });
