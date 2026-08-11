/* ============================================================
   VIKAAS v2 — SHELL.js (shared across every page)
   cursor v2 (blob+ring+splash+labels) · glass nav overlay ·
   wipe transitions · Lenis smooth scroll · hover audio blips ·
   HUD clock. Self-injecting, guarded per page.
   ============================================================ */
(function () {
  'use strict';
  const touch = matchMedia('(hover: none)').matches;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s) => document.querySelector(s);
  const qsa = (s) => Array.from(document.querySelectorAll(s));

  /* ---------- hide native scrollbar on loader (rail is the indicator) ---------- */
  if (location.pathname.includes('loader')) document.documentElement.classList.add('no-bar');

  /* ---------- HUD clock ---------- */
  const ht = $('#hudTime');
  if (ht) {
    const p = (n) => String(n).padStart(2, '0');
    const t = () => { const d = new Date(); ht.textContent = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds()) + ' IST'; };
    t(); setInterval(t, 1000);
  }

  /* ---------- CURSOR v2 ---------- */
  if (!touch) {
    const blob = document.createElement('div'); blob.className = 'cur-blob';
    const ring = document.createElement('div'); ring.className = 'cur-ring';
    const lab = document.createElement('div'); lab.className = 'cur-lab';
    const cv = document.createElement('canvas'); cv.className = 'cur-splash';
    document.body.append(blob, ring, lab, cv);
    document.documentElement.classList.add('has-cur');
    const ctx = cv.getContext('2d');
    let W, H;
    const fit = () => { W = cv.width = innerWidth; H = cv.height = innerHeight; };
    fit(); addEventListener('resize', fit);
    const parts = [];
    const COLS = ['185,255,63', '46,222,130', '255,211,77', '234,255,244'];
    let mx = innerWidth / 2, my = innerHeight / 2, bx = mx, by = my, rx = mx, ry = my, px = mx, py = my, hover = false;
    addEventListener('mousemove', (e) => {
      px = mx; py = my; mx = e.clientX; my = e.clientY;
      const sp = Math.hypot(mx - px, my - py);
      if (sp > 22 && Math.random() < 0.6) {
        parts.push({ x: mx, y: my, vx: (Math.random() - .5) * 2.4, vy: (Math.random() - .5) * 2.4 - .5, life: 1, decay: 0.04 + Math.random() * 0.035, size: 1 + Math.random() * 2.4, c: COLS[Math.floor(Math.random() * 4)] });
      }
    }, { passive: true });
    document.addEventListener('mouseover', (e) => {
      const t = e.target.closest('[data-cursor], a, button, .spot, .gn-item, .room-card');
      if (t) {
        hover = true;
        const l = t.getAttribute && t.getAttribute('data-cursor');
        if (l) { lab.textContent = l; lab.classList.add('on'); } else lab.classList.remove('on');
      } else { hover = false; lab.classList.remove('on'); }
    });
    (function loop() {
      bx += (mx - bx) * 0.16; by += (my - by) * 0.16; rx += (mx - rx) * 0.07; ry += (my - ry) * 0.07;
      blob.style.transform = 'translate(' + bx + 'px,' + by + 'px) translate(-50%,-50%)';
      ring.style.transform = 'translate(' + rx + 'px,' + ry + 'px) translate(-50%,-50%)';
      const s = hover ? 2.1 : 1;
      blob.style.width = (10 * s) + 'px'; blob.style.height = (10 * s) + 'px';
      ring.style.width = (hover ? 62 : 36) + 'px'; ring.style.height = (hover ? 62 : 36) + 'px';
      ring.style.borderColor = hover ? 'rgba(185,255,63,.9)' : 'rgba(185,255,63,.45)';
      ctx.clearRect(0, 0, W, H);
      for (let i = parts.length - 1; i >= 0; i--) {
        const p = parts[i];
        p.x += p.vx; p.y += p.vy; p.vy += 0.05; p.life -= p.decay;
        if (p.life <= 0) { parts.splice(i, 1); continue; }
        ctx.globalAlpha = Math.max(p.life, 0);
        ctx.fillStyle = 'rgba(' + p.c + ',' + Math.max(p.life, 0) + ')';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- GLASS NAV ---------- */
  const menu = $('#gnMenu'), ov = $('#gnOverlay');
  if (menu && ov) {
    menu.addEventListener('click', () => {
      ov.classList.add('on'); document.body.classList.add('navlock');
      qsa('.gn-item', ov).forEach((el, i) => {
        el.style.transition = 'none'; el.style.opacity = '0'; el.style.transform = 'translateY(24px)';
        setTimeout(() => {
          el.style.transition = 'opacity .5s,transform .5s cubic-bezier(.2,.9,.2,1) ' + (70 * i) + 'ms';
          el.style.opacity = '1'; el.style.transform = 'none';
        }, 40);
      });
    });
    const close = () => { ov.classList.remove('on'); document.body.classList.remove('navlock'); };
    const x = $('#gnX'); if (x) x.addEventListener('click', close);
    addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    ov.addEventListener('click', (e) => { if (e.target === ov) close(); });
  }

  /* ---------- WIPE transitions ---------- */
  if (!reduce) {
    const entering = sessionStorage.getItem('vwipe') === '1';
    const w = document.createElement('div'); w.className = 'vwipe';
    w.innerHTML = '<span class="anton">VIKAAS<span style="color:var(--acid)">.</span></span>';
    document.body.appendChild(w);
    if (entering) {
      sessionStorage.removeItem('vwipe');
      requestAnimationFrame(() => setTimeout(() => w.classList.add('out'), 80));
      setTimeout(() => w.remove(), 1000);
    } else w.remove();
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href]');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#') || a.target === '_blank' || !href.endsWith('.html')) return;
      e.preventDefault();
      const w2 = document.createElement('div'); w2.className = 'vwipe'; w2.classList.add('in2');
      document.body.appendChild(w2);
      sessionStorage.setItem('vwipe', '1');
      setTimeout(() => { location.href = href; }, 420);
    });
  }

  /* ---------- LENIS ---------- */
  if (window.Lenis && !touch && !reduce && document.documentElement.dataset.lenis !== 'off') {
    const lenis = new Lenis({ lerp: 0.1 });
    if (window.ScrollTrigger) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
  }

  /* ---------- MAGNETIC [data-mag] ---------- */
  if (!touch) qsa('[data-mag]').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const b = el.getBoundingClientRect();
      const dx = e.clientX - (b.left + b.width / 2), dy = e.clientY - (b.top + b.height / 2);
      const d = Math.hypot(dx, dy);
      if (d < 90 + b.width / 2) el.style.transform = 'translate(' + dx * 0.22 + 'px,' + dy * 0.22 + 'px)';
    });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });

  /* ---------- AUDIO: hover blips (reused AudioContext) ---------- */
  let AC = null;
  const ac = () => { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} } return AC; };
  let unlocked = false;
  const unlock = () => { if (unlocked) return; unlocked = true; ac(); };
  ['pointerdown', 'wheel', 'touchstart'].forEach((ev) => addEventListener(ev, unlock, { once: true, passive: true }));
  if (!touch) {
    document.addEventListener('mouseover', (e) => {
      if (!unlocked) return;
      const t = e.target.closest('a, button, [data-cursor]');
      if (!t) return;
      const C = ac(); if (!C) return;
      try {
        const t0 = C.currentTime;
        const o = C.createOscillator(); const g = C.createGain();
        o.type = 'sine'; o.frequency.value = 800 + Math.random() * 500;
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.exponentialRampToValueAtTime(0.04, t0 + 0.012);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.09);
        o.connect(g); g.connect(C.destination); o.start(t0); o.stop(t0 + 0.1);
      } catch (err) {}
    }, { passive: true });
  }
})();
