/* ============================================================
   VIKAAS v2 — LOADER (Phase 1)
   Terminal typing + scramble wordmark + ring progress + glitch
   + dust canvas + synth audio on ENTER. ?fast=1 for QA.
   ============================================================ */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fast = new URLSearchParams(location.search).has('fast');
  const $ = (s) => document.querySelector(s);
  const wordEl = $('#word'), devEl = $('#dev'), termEl = $('#term'),
        pctEl = $('#pct'), ringFg = $('#ringFg'), barFill = $('#barFill'),
        enterBtn = $('#enter'), loaderEl = $('#loader');

  const RING = 578.05; // 2*pi*92? (r=92 in viewBox 200) — here r=55: 2*pi*55=345.6
  const RING_LEN = 2 * Math.PI * 55;
  ringFg.style.strokeDasharray = RING_LEN;

  /* ---------- HUD clock ---------- */
  const hudTime = $('#hudTime');
  const tickClock = () => {
    const d = new Date();
    const p = (n) => String(n).padStart(2, '0');
    hudTime.textContent = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds()) + ' IST';
  };
  tickClock(); setInterval(tickClock, 1000);

  /* ---------- terminal ---------- */
  const STEPS = [
    ['scanning drawer inventory', '3 phones · 7 chargers · 1 speaker (2022)', 'dim'],
    ['weighing …', '1.4 KG — receipt logged', 'acid'],
    ['surveying 10 homes …', '10/10 have the same drawer', 'dim'],
    ['querying HSPCB registry …', '15 authorised recyclers found', 'acid'],
    ['doorsteps served …', '0', 'red'],
    ['summoning ReBee …', 'scrap-scan online', 'gold'],
    ['finalising …', 'NO DRAWER LEFT BEHIND', 'acid'],
  ];
  const esc = (s) => s.replace(/[<>&]/g, (m) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[m]));

  function runTerminal(onDone) {
    if (fast || reduce) { termEl.innerHTML = STEPS.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`).join('\n'); onDone(); return; }
    let si = 0, ci = 0;
    const done = [];
    const cursor = '<span class="cur"></span>';
    const render = () => {
      const lines = done.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`);
      const cur = STEPS[si];
      const partial = esc(cur[0].slice(0, ci));
      lines.push(`<span class="${cur[2]}">${partial}</span>${cursor}`);
      termEl.innerHTML = lines.join('\n');
    };
    const step = () => {
      if (ci < STEPS[si][0].length) { ci++; render(); setTimeout(step, 11); }
      else {
        done.push(STEPS[si]); si++;
        if (si < STEPS.length) { ci = 0; render(); setTimeout(step, 160); }
        else { termEl.innerHTML = done.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`).join('\n') + '\n<span class="acid">' + esc('> READY — awaiting command') + '</span>'; onDone(); }
      }
    };
    render(); step();
  }

  /* ---------- wordmark scramble ---------- */
  const FULL = 'VIKAAS';
  const CHARS = '!<>-_\\/[]{}—=+*^?#ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let scrambleTimer = null;

  function runScramble() {
    if (fast || reduce) { wordEl.textContent = FULL; return; }
    let frame = 0;
    const total = 90;
    const tick = () => {
      const p = frame / total;
      const reveal = Math.floor(p * FULL.length);
      let out = '';
      for (let i = 0; i < FULL.length; i++) {
        out += i < reveal ? FULL[i] : CHARS[Math.floor(Math.random() * CHARS.length)];
      }
      wordEl.textContent = out;
      if (Math.random() < 0.05) { wordEl.classList.add('glitching'); setTimeout(() => wordEl.classList.remove('glitching'), 300); }
      frame++;
      if (frame <= total) scrambleTimer = setTimeout(tick, 34);
      else wordEl.textContent = FULL;
    };
    tick();
  }

  /* ---------- progress ---------- */
  const DUR = reduce || fast ? 50 : 5200;
  let p = 0, done = false;

  function progressLoop() {
    if (done) return;
    p += 100 / DUR * (1000 / 60) * (fast || reduce ? 0.35 : 1);
    if (p >= 100) { p = 100; done = true; }
    const eased = 1 - Math.pow(1 - p / 100, 3);
    pctEl.innerHTML = String(Math.round(p)).padStart(3, '0') + '<small>%</small>';
    ringFg.style.strokeDashoffset = RING_LEN * (1 - eased);
    barFill.style.width = eased * 100 + '%';
    if (!done) requestAnimationFrame(progressLoop);
  }

  /* ---------- dust canvas ---------- */
  const cv = $('#dust'), cx = cv.getContext('2d');
  let W, H, parts = [];
  function sizeCanvas() { W = cv.width = innerWidth; H = cv.height = innerHeight; }
  sizeCanvas(); addEventListener('resize', sizeCanvas);
  const COLORS = ['185,255,63', '46,222,130', '255,211,77', '234,255,244'];
  for (let i = 0; i < 70; i++) parts.push({
    x: Math.random() * innerWidth, y: Math.random() * innerHeight,
    r: 0.6 + Math.random() * 1.8, vy: 0.08 + Math.random() * 0.35,
    vx: (Math.random() - 0.5) * 0.12, c: COLORS[i % 4], tw: Math.random() * 6.28,
  });
  let dustOn = true;
  (function dustLoop() {
    if (!dustOn) return;
    cx.clearRect(0, 0, W, H);
    for (const q of parts) {
      q.y -= q.vy; q.x += q.vx + Math.sin(q.tw) * 0.05; q.tw += 0.02;
      if (q.y < -4) { q.y = H + 4; q.x = Math.random() * W; }
      if (q.x < -4) q.x = W + 4; if (q.x > W + 4) q.x = -4;
      const a = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(q.tw * 2));
      cx.beginPath(); cx.arc(q.x, q.y, q.r, 0, 6.283);
      cx.fillStyle = 'rgba(' + q.c + ',' + a + ')'; cx.fill();
    }
    requestAnimationFrame(dustLoop);
  })();

  /* ---------- audio ---------- */
  const SOUNDS = { boot: null, enter: null };
  function loadAudio() {
    const base = 'assets/audio/';
    const mk = (name) => { const a = new Audio(base + name + '.wav'); a.volume = 0.8; return a; };
    SOUNDS.boot = mk('boot'); SOUNDS.enter = mk('enter');
  }

  function finish() {
    done = true; p = 100;
    pctEl.innerHTML = '100<small>%</small>';
    ringFg.style.strokeDashoffset = 0;
    barFill.style.width = '100%';
    devEl.classList.add('on');
    enterBtn.classList.add('show');
    if (SOUNDS.boot) SOUNDS.boot.play().catch(() => {});
  }

  enterBtn.addEventListener('click', () => {
    if (SOUNDS.enter) SOUNDS.enter.play().catch(() => {});
    loaderEl.classList.add('leaving');
    setTimeout(() => { location.href = '../index.html'; }, 1050);
  });
  addEventListener('keydown', (e) => { if (e.key === 'Enter' && enterBtn.classList.contains('show')) enterBtn.click(); });

  /* ---------- boot ---------- */
  loadAudio();
  runScramble();
  runTerminal(() => { if (fast || reduce) finish(); });
  progressLoop();
  if (!fast && !reduce) setTimeout(() => { if (!done) finish(); }, DUR + 900);
})();
