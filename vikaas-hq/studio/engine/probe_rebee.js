// probe_rebee.js — THE REBEE CHAT TEST: opens /buddy, clicks a quick
// chip, waits for the reply, verifies a ReBee message appears + console clean.
// Sandbox can't reach OpenRouter → exercises the script-fallback path.
// Usage: node probe_rebee.js [baseUrl]
const chromium = require('@sparticuz/chromium');
const { chromium: pw } = require('playwright-core');

(async () => {
  const base = process.argv[2] || 'http://localhost:5173';
  let browser;
  for (let i = 0; i < 3; i++) {
    try { browser = await pw.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true }); break; }
    catch (e) { await new Promise(r => setTimeout(r, 1500)); }
  }
  if (!browser) { console.log('FAIL browser'); process.exit(1); }
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGE:' + e.message.slice(0, 140)));
  page.on('console', m => { if (m.type() === 'error') errs.push('CON:' + m.text().slice(0, 140)); });
  await page.goto(base + '/buddy', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2500);

  const chips = await page.$$('.as-chip');
  console.log('chips found:', chips.length);
  if (chips.length < 4) { console.log('FAIL chips'); process.exit(1); }

  // click the "what's my drawer worth" chip
  await chips[0].click();
  await page.waitForTimeout(400);
  const typing = await page.$('.as-typing');
  console.log('typing indicator:', !!typing);

  // fallback reply arrives after ~0.9s (no network) or real LLM up to 15s
  let got = false;
  for (let i = 0; i < 20; i++) {
    await page.waitForTimeout(700);
    const msgs = await page.$$eval('.as-msg.bee', els => els.map(e => e.textContent || ''));
    if (msgs.length >= 2 && msgs[msgs.length - 1].length > 10) { got = true; break; }
  }
  const last = await page.$$eval('.as-msg.bee', els => (els[els.length - 1] || {}).textContent || '');
  console.log('replied:', got, '| tail:', last.slice(0, 90).replace(/\n/g, ' '));

  // free-text input path
  await page.fill('.as-input', 'book a pickup please');
  await page.click('.as-send');
  await page.waitForTimeout(2500);
  const msgs2 = await page.$$eval('.as-msg.bee', els => els.map(e => e.textContent || ''));
  console.log('free-text reply len:', (msgs2[msgs2.length - 1] || '').length);

  const status = await page.$eval('.as-chat-head .cmd', e => e.textContent);
  console.log('brain status:', status.trim());
  await page.screenshot({ path: '/tmp/qa_gate/_assistant_chat.png' });
  await browser.close();

  const clean = errs.filter(e => !e.includes('openrouter') && !e.includes('Failed to load resource'));
  if (!got) { console.log('FAIL no reply'); process.exit(1); }
  if (clean.length) { console.log('FAIL console:', clean.join(' | ')); process.exit(1); }
  console.log('REBEE PROBE: PASS');
})();
