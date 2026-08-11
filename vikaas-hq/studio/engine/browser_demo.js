// CAPABILITY PROOF: in-sandbox headless Chromium via @sparticuz/chromium (npm-bundled binary)
// Demonstrates: launch -> render local HTML -> screenshot -> close. All egress-free.
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

(async () => {
  const execPath = await chromium.executablePath();
  console.log('executablePath:', execPath);
  const browser = await pw.launch({
    args: chromium.args,
    executablePath: execPath,
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.setContent(`<!doctype html><html><head><style>
    body{margin:0;background:#0e1116;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh}
    h1{font-size:64px} p{font-size:28px;color:#9aa4b2}
  </style></head><body><div><h1>🐝 ReBee browser online</h1><p>headless chromium via @sparticuz/chromium · npm-only workaround</p></div></body></html>`);
  await page.screenshot({ path: '/tmp/browser_demo.png' });
  console.log('screenshot written: /tmp/browser_demo.png');
  const ua = await page.evaluate(() => navigator.userAgent);
  console.log('userAgent:', ua);
  await browser.close();
  console.log('OK: browser launched, rendered, screenshotted, closed.');
})().catch((e) => { console.error('FAIL:', e.message); process.exit(1); });
