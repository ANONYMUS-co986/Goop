const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');
async function launch() {
  for (let i = 0; i < 3; i++) {
    try { return await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  throw new Error('launch failed');
}
(async () => {
  const browser = await launch();
  for (const route of ['/', '/drawer', '/boot', '/boot?fast=1']) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = [];
    page.on('pageerror', e => errs.push('PAGE: ' + e.message.slice(0, 300)));
    page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type().toUpperCase() + ': ' + m.text().slice(0, 300)); });
    page.on('requestfailed', r => errs.push('REQFAIL: ' + r.url().slice(0, 150) + ' ' + (r.failure() ? r.failure().errorText : '')));
    const resp = await page.goto('http://localhost:5173' + route, { waitUntil: 'networkidle', timeout: 45000 }).catch(e => 'NAVFAIL: ' + e.message.slice(0, 150));
    await page.waitForTimeout(3500);
    const state = await page.evaluate(() => ({
      title: document.title,
      bodyKids: document.body.children.length,
      rootKids: (document.getElementById('root') || {}).children ? document.getElementById('root').children.length : -1,
      hasMain: !!document.querySelector('main'),
      scrollH: document.documentElement.scrollHeight,
      text: (document.body.innerText || '').slice(0, 80),
    })).catch(e => ({ evalfail: e.message.slice(0, 120) }));
    console.log('==== ' + route + ' ====');
    console.log('state:', JSON.stringify(state));
    console.log('errs:', errs.length ? '\n  ' + errs.join('\n  ') : 'NONE');
    await page.screenshot({ path: '/tmp/suite/all-' + route.replace(/[^a-z0-9]/gi, '_') + '.png' }).catch(() => {});
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e.message.slice(0, 200)); process.exit(1); });
