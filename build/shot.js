// shot.js <url> <out.png> [waitMs] [scrollY]
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
  const url = process.argv[2] || 'http://localhost:3000';
  const out = process.argv[3] || 'shot.png';
  const waitMs = parseInt(process.argv[4] || '4500', 10);
  const scrollY = parseInt(process.argv[5] || '0', 10);
  ensureAl2023Libs();

  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
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
  await page.waitForTimeout(waitMs);
  if (scrollY > 0) {
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), scrollY);
    await page.waitForTimeout(1200);
  }
  await page.screenshot({ path: out });
  console.log('HTTP', status, '| errors:', errors.length ? errors.slice(0, 6) : 'none');
  console.log('shot ->', path.resolve(out));
  await browser.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
