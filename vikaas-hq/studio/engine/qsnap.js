// Vikaas Studio — portfolio QA snapshots (resilient multi-launch edition).
// Usage: node engine/qsnap.js <htmlPath> <outPrefix> [--boot]
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

async function shot(desc, fn) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    let browser;
    try {
      browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
      await fn(browser);
      await browser.close();
      console.log('  ✓', desc);
      return true;
    } catch (e) {
      try { await browser && browser.close(); } catch (_) {}
      console.log(`  retry(${attempt}) ${desc}: ${e.message.split('\n')[0]}`);
    }
  }
  console.log('  ✗ FAILED', desc);
  return false;
}

(async () => {
  const html = 'file://' + path.resolve(process.argv[2]);
  const prefix = process.argv[3];
  const wantBoot = process.argv.includes('--boot');
  ensureAl2023Libs();
  if (wantBoot) await shot('boot', async (b) => {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(html); await p.waitForTimeout(900);
    await p.screenshot({ path: `${prefix}_boot.png` });
  });
  await shot('desk_hero', async (b) => {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(html);
    await p.evaluate(() => { try { sessionStorage.setItem('vboot', '1'); } catch (e) {} });
    await p.reload(); await p.waitForTimeout(1800);
    await p.screenshot({ path: `${prefix}_desk_hero.png` });
  });
  await shot('desk_rooms+hover', async (b) => {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(html);
    await p.evaluate(() => { try { sessionStorage.setItem('vboot', '1'); } catch (e) {} });
    await p.reload(); await p.waitForTimeout(1200);
    const has = await p.evaluate(() => !!document.getElementById('rooms'));
    if (!has) return;
    await p.evaluate(() => document.getElementById('rooms').scrollIntoView({ block: 'start' }));
    await p.waitForTimeout(500);
    await p.screenshot({ path: `${prefix}_desk_rooms.png` });
    await p.hover('.room:not(.locked)').catch(() => {});
    await p.waitForTimeout(350);
    await p.screenshot({ path: `${prefix}_desk_hover.png` });
  });
  await shot('mob_hero', async (b) => {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    await p.goto(html);
    await p.evaluate(() => { try { sessionStorage.setItem('vboot', '1'); } catch (e) {} });
    await p.reload(); await p.waitForTimeout(1800);
    await p.screenshot({ path: `${prefix}_mob_hero.png` });
  });
  console.log('qsnap done ->', prefix);
})().catch(e => { console.error(e.message); process.exit(1); });
