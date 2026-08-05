// Vikaas Studio v3 engine — deterministic GSAP-scrubbed HTML→MP4.
// Usage:
//   node engine/lib.js render <htmlPath> <framesDir> [fps]
//   node engine/lib.js encode <framesDir> <audioFile> <durSec> <outMp4> [fps]
//   node engine/lib.js sheet  <mp4> <outPng> [tiles]
// Design contract: the html exposes window.__reel = { duration, seek(t) }.
const path = require('path');
const fs = require('fs');
const zlib = require('zlib');
const cp = require('child_process');
process.env.LD_LIBRARY_PATH = '/tmp/al2023/lib' + (process.env.LD_LIBRARY_PATH ? ':' + process.env.LD_LIBRARY_PATH : '');

const FFMPEG = '/home/user/Goop/vikaas-hq/studio/.venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';

// @sparticuz/chromium needs AL2023 system libs under /tmp/al2023/lib; /tmp is
// wiped between sessions, so inflate from the package's own archive on demand.
function ensureAl2023Libs() {
  if (fs.existsSync('/tmp/al2023/lib/libnspr4.so')) return;
  let dir = path.dirname(require.resolve('@sparticuz/chromium'));
  for (let i = 0; i < 8 && !fs.existsSync(path.join(dir, 'bin', 'al2023.tar.br')); i++) dir = path.dirname(dir);
  const br = path.join(dir, 'bin', 'al2023.tar.br');
  fs.mkdirSync('/tmp/al2023', { recursive: true });
  fs.writeFileSync('/tmp/al2023.tar', zlib.brotliDecompressSync(fs.readFileSync(br)));
  cp.execSync('tar -xf /tmp/al2023.tar -C /tmp/al2023');
  fs.rmSync('/tmp/al2023.tar', { force: true });
  console.log('[engine] inflated al2023 libs:', fs.readdirSync('/tmp/al2023/lib').length, 'files');
}

const _cr = require('@sparticuz/chromium');
const chromium = _cr.default || _cr;
const { chromium: pw } = require('playwright-core');

async function renderFrames(htmlPath, framesDir, fps) {
  ensureAl2023Libs();
  fs.mkdirSync(framesDir, { recursive: true });
  const browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGEERROR:', e.message.slice(0, 300)));
  page.on('console', m => { if (m.type() === 'error') console.error('CONSOLE:', m.text().slice(0, 200)); });
  await page.goto('file://' + path.resolve(htmlPath), { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForFunction(() => window.__reel && typeof window.__reel.seek === 'function', null, { timeout: 30000 });
  const duration = await page.evaluate(() => window.__reel.duration);
  const total = Math.round(duration * fps);
  console.log(`[engine] ${path.basename(htmlPath)}: duration=${duration}s fps=${fps} frames=${total}`);
  // prime frame (lets timeline do first layout)
  await page.evaluate(() => window.__reel.seek(0));
  await page.waitForTimeout(400);
  const t0 = Date.now();
  for (let f = 0; f < total; f++) {
    const t = f / fps;
    await page.evaluate((tt) => window.__reel.seek(tt), t);
    await page.screenshot({ path: path.join(framesDir, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
    if (f % 100 === 0 || f === total - 1) {
      const per = (Date.now() - t0) / (f + 1);
      console.log(`[engine] frame ${f}/${total} (${(per / 1000).toFixed(2)}s/frame, eta ${(((total - f) * per) / 60000).toFixed(1)}min)`);
    }
  }
  await browser.close();
  console.log('[engine] frames done ->', framesDir);
}

function encodeReel(framesDir, audio, durSec, outMp4, fps) {
  fs.mkdirSync(path.dirname(outMp4), { recursive: true });
  const args = [
    '-y', '-framerate', String(fps), '-i', path.join(framesDir, 'f%04d.jpg'),
    '-i', audio,
    '-filter_complex',
    `[1:a]atrim=0:${durSec + 0.5},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2.2,afade=t=out:st=${(durSec - 2.6).toFixed(2)}:d=2.6,highpass=f=90,loudnorm=I=-19:TP=-1.5:LRA=11[a]`,
    '-map', '0:v', '-map', '[a]',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(fps), '-crf', '18', '-preset', 'medium',
    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', outMp4,
  ];
  const r = cp.spawnSync(FFMPEG, args, { stdio: ['ignore', 'pipe', 'pipe'] });
  if (r.status !== 0) { console.error(r.stderr.toString().slice(-1500)); throw new Error('ffmpeg encode failed'); }
  const probe = cp.spawnSync(FFMPEG.replace('ffmpeg-', 'ffprobe-').replace(/ffmpeg$/, 'ffprobe'), ['-v', 'quiet', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', outMp4]);
  console.log('[engine] encoded ->', outMp4, probe.status === 0 ? probe.stdout.toString().trim() : '');
}

function contactSheet(mp4, outPng, tiles) {
  tiles = tiles || 12;
  const cols = Math.ceil(Math.sqrt(tiles * 9 / 16));
  const rows = Math.ceil(tiles / cols);
  // sample `tiles` evenly across the clip regardless of duration
  const probeDur = parseFloat(cp.spawnSync(FFMPEG.replace(/ffmpeg$/, 'ffprobe'), ['-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4]).stdout.toString().trim()) || 27;
  const step = probeDur / (tiles + 1);
  const args = ['-y', '-i', mp4, '-vf', `fps=1/${step.toFixed(3)},scale=270:480,tile=${cols}x${rows}`, '-frames:v', '1', outPng];
  const r = cp.spawnSync(FFMPEG, args, { stdio: ['ignore', 'pipe', 'pipe'] });
  if (r.status !== 0) { console.error(r.stderr.toString().slice(-800)); throw new Error('sheet failed'); }
  console.log('[engine] contact sheet ->', outPng);
}

(async () => {
  const [, , cmd, ...a] = process.argv;
  if (cmd === 'render') await renderFrames(a[0], a[1], parseInt(a[2] || '30', 10));
  else if (cmd === 'encode') encodeReel(a[0], a[1], parseFloat(a[2]), a[3], parseInt(a[4] || '30', 10));
  else if (cmd === 'sheet') contactSheet(a[0], a[1], parseInt(a[2] || '12', 10));
  else console.log('unknown cmd');
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
