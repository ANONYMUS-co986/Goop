// shot.js <url> <out.png> [waitMs] [scrollY] [waitForSelector] [clickSelector] [hoverSelector]
// Headless QA capture for the showcase site — waits for compile, fonts, idle.
const path = require('path');
const fs = require('fs');
const zlib = require('zlib');
const cp = require('child_process');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');

// self-heal: @sparticuz/chromium needs its AL2023 system libs under /tmp/al2023/lib;
// /tmp gets wiped between sessions, so inflate from the package's .br archive on demand.
function ensureAl2023Libs() {
  if (fs.existsSync('/tmp/al2023/lib/libnspr4.so')) return;
  // locate the package root by climbing from its entry point (exports map blocks package.json)
  let dir = path.dirname(require.resolve('@sparticuz/chromium'));
  for (let i = 0; i < 8 && !fs.existsSync(path.join(dir, 'bin', 'al2023.tar.br')); i++) {
    dir = path.dirname(dir);
  }
  const br = path.join(dir, 'bin', 'al2023.tar.br');
  fs.mkdirSync('/tmp/al2023', { recursive: true });
  fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(br)));
  cp.execSync('tar -xf /tmp/al2023.tar -C /tmp/al2023');
  fs.rmSync('/tmp/al2023.tar', { force: true });
  console.log('[shot] inflated al2023 libs ->', fs.readdirSync('/tmp/al2023/lib').length, 'files');
}

const _cr = require('@sparticuz/chromium');
const chromium = _cr.default || _cr;
const { chromium: pw } = require('playwright-core');

(async () => {
  // args: url out [waitMs] [scrollY] [waitForSelector] [clickSelector]
  const url = process.argv[2] || 'http://localhost:3000';
  const out = process.argv[3] || 'shot.png';
  const waitMs = parseInt(process.argv[4] || '4500', 10);
  const scrollY = parseInt(process.argv[5] || '0', 10);
  const waitFor = process.argv[6] || '';
  const clickSel = process.argv[7] || '';
  const hoverSel = process.argv[8] || '';
  // optional mobile emulation: QA_VW=390 QA_VH=844 node build/shot.js ...
  const vw = parseInt(process.env.QA_VW || '1440', 10);
  const vh = parseInt(process.env.QA_VH || '900', 10);
  const mobile = vw < 700;
  ensureAl2023Libs();

  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({
    viewport: { width: vw, height: vh },
    deviceScaleFactor: 1,
    isMobile: mobile,
    hasTouch: mobile,
  });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 200)); });

  let status = 0;
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
      status = resp ? resp.status() : 0;
      if (status === 200) break;
    } catch (e) {
      errors.push('NAV ' + attempt + ': ' + e.message.slice(0, 120));
    }
    await page.waitForTimeout(3000);
  }
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; }).catch(() => {});
  // universal ritual:
  // 1. wait for the app's QA bridge, then disable GSAP lag smoothing so every
  //    timeline tracks wall-clock even at 1-2fps SwiftShader (true end states)
  // 2. skip the preloader via keyboard Escape (a real supported feature),
  //    retrying until hydration definitely happened; fall back to force-click
  await page.waitForFunction(() => typeof window.__qaNoLag === 'function', null, { timeout: 45000 }).catch(() => errors.push('qa bridge missing (hydration?)'));
  await page.evaluate(() => window.__qaNoLag && window.__qaNoLag()).catch(() => {});
  let skipped = false;
  if (process.env.QA_NOSKIP !== '1') {
    for (let i = 0; i < 15 && !skipped; i++) {
      await page.keyboard.press('Escape').catch(() => {});
      skipped = await page.waitForSelector('[role=dialog]', { state: 'detached', timeout: 1500 }).then(() => true).catch(() => false);
    }
    if (!skipped) {
      await page.click('[role=dialog]', { force: true, timeout: 4000 }).catch(() => {});
      skipped = await page.waitForSelector('[role=dialog]', { state: 'detached', timeout: 10000 }).then(() => true).catch(() => false);
    }
    if (!skipped) errors.push('preloader never detached');
  }
  if (clickSel) {
    await page.waitForSelector(clickSel, { timeout: 30000 }).catch(() => errors.push('clickSel missing: ' + clickSel));
    await page.click(clickSel).catch(e => errors.push('clickSel click: ' + e.message.slice(0, 80)));
    await page.waitForTimeout(1400);
  }
  if (waitFor) {
    await page.waitForSelector(waitFor, { timeout: 45000 }).catch(() => errors.push('waitFor timeout: ' + waitFor));
  }
  await page.waitForTimeout(waitMs);
  if (scrollY > 0) {
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), scrollY);
    await page.waitForTimeout(1200);
  }
  if (hoverSel) {
    await page.hover(hoverSel).catch(e => errors.push('hoverSel: ' + e.message.slice(0, 80)));
    await page.waitForTimeout(1100);
  }
  await page.screenshot({ path: out });
  console.log('HTTP', status, '| errors:', errors.length ? errors.slice(0, 6) : 'none');
  console.log('shot ->', path.resolve(out));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
