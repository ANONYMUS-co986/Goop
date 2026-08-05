// Vikaas Studio — static post shooter. 1080x1350 @2x PNG.
// Usage: node engine/shot.js <htmlPath> <outPng> [w] [h]
const path = require('path');
const fs = require('fs');
const zlib = require('zlib');
const cp = require('child_process');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');

function ensureAl2023Libs() {
  if (fs.existsSync('/tmp/al2023/lib/libnspr4.so')) return;
  let dir = path.dirname(require.resolve('@sparticuz/chromium'));
  for (let i = 0; i < 8 && !fs.existsSync(path.join(dir, 'bin', 'al2023.tar.br')); i++) dir = path.dirname(dir);
  const br = path.join(dir, 'bin', 'al2023.tar.br');
  fs.mkdirSync('/tmp/al2023', { recursive: true });
  fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(br)));
  cp.execSync('tar -xf /tmp/al2023.tar -C /tmp/al2023');
  fs.rmSync('/tmp/al2023.tar', { force: true });
}

const _cr = require('@sparticuz/chromium');
const chromium = _cr.default || _cr;
const { chromium: pw } = require('playwright-core');

(async () => {
  const html = process.argv[2];
  const out = process.argv[3];
  const W = parseInt(process.argv[4] || '1080', 10);
  const H = parseInt(process.argv[5] || '1350', 10);
  ensureAl2023Libs();
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.error('PAGEERROR:', e.message.slice(0, 300)));
  await page.goto('file://' + path.resolve(html), { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(500);
  await page.screenshot({ path: out, type: 'png' });
  await browser.close();
  console.log('[shot]', out);
})();
