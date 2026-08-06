/* VIKAAS portfolio — shared juice: burger nav, cursor, tooltips, reveal,
   page-wipe, magnets, count-ups, grain. Zero deps; self-injecting.
   Respects prefers-reduced-motion + touch devices. */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(hover: none)').matches;
  const qs = (s, r) => (r || document).querySelector(s);
  const qsa = (s, r) => Array.from((r || document).querySelectorAll(s));

  const ROOMS = [
    { n: '01', t: 'THE DRAWER', u: 'index.html#hero', s: 'room1' },
    { n: '02', t: 'PROOF LEDGER', u: 'ledger.html', s: 'room2' },
    { n: '03', t: 'FILMS', u: 'films.html', s: 'room3' },
    { n: '04', t: 'KABADI UNIVERSE', u: null, s: 'room4', ph: 3 },
    { n: '05', t: 'SYSTEM', u: null, s: 'room5', ph: 3 },
    { n: '06', t: 'THE LAB', u: null, s: 'room6', ph: 4 },
  ];
  const here = document.body.dataset.room || 'room1';

  /* ---------- NAV: topbar + burger overlay (auto-injected on every page) ---------- */
  const bar = document.createElement('nav');
  bar.className = 'vbar';
  bar.innerHTML =
    '<a class="vbar-brand anton" href="index.html">VIKAAS<span>.</span></a>' +
    '<span class="vbar-tag" id="vbarTag"></span>' +
    '<button class="vbar-menu" id="vbarMenu" aria-label="open menu">MENU<span class="dots"><i></i><i></i><i></i></span></button>';
  document.body.prepend(bar);
  const cur = ROOMS.find(r => r.s === here);
  qs('#vbarTag').textContent = cur ? ('ROOM ' + cur.n + ' · ' + cur.t) : '';

  const ov = document.createElement('div');
  ov.className = 'vnav';
  ov.innerHTML =
    '<button class="vnav-x" aria-label="close menu">✕ CLOSE</button>' +
    '<div class="vnav-hd cmd">the ledger of rooms — pick one</div>' +
    '<div class="vnav-list">' +
    ROOMS.map(r =>
      r.u
        ? `<a class="vnav-item" href="${r.u}"><span class="no">${r.n}</span><span class="tt anton">${r.t}</span><span class="st ${r.s === here ? 'now' : 'live'}">${r.s === here ? 'YOU ARE HERE' : 'ENTER →'}</span></a>`
        : `<div class="vnav-item locked"><span class="no">${r.n}</span><span class="tt anton">${r.t}</span><span class="st">PHASE ${r.ph} · LOCKED</span></div>`
    ).join('') +
    '</div><div class="vnav-ft">receipts with taste · @qwerty_aarav</div>';
  document.body.appendChild(ov);

  let navOpen = false;
  function setNav(open) {
    navOpen = open;
    ov.classList.toggle('on', open);
    document.body.classList.toggle('navlock', open);
    if (open) {
      const items = qsa('.vnav-item', ov);
      items.forEach((el, i) => {
        el.style.transition = 'none'; el.style.transform = 'translateX(-26px)'; el.style.opacity = '0';
        setTimeout(() => {
          el.style.transition = 'transform .5s cubic-bezier(.2,.9,.2,1) ' + (60 * i) + 'ms, opacity .4s ' + (60 * i) + 'ms';
          el.style.transform = 'none'; el.style.opacity = '1';
        }, 30);
      });
    }
  }
  qs('#vbarMenu').addEventListener('click', () => setNav(true));
  qs('.vnav-x', ov).addEventListener('click', () => setNav(false));
  addEventListener('keydown', e => { if (e.key === 'Escape') setNav(false); });

  /* ---------- CURSOR (desktop only) ---------- */
  if (!touch && !reduce) {
    const dot = document.createElement('div'); dot.className = 'cur-dot';
    const lab = document.createElement('div'); lab.className = 'cur-lab';
    document.body.append(dot, lab);
    document.documentElement.classList.add('has-cursor');
    let mx = innerWidth / 2, my = innerHeight / 2, cx = mx, cy = my;
    addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });
    (function loop() {
      cx += (mx - cx) * 0.18; cy += (my - cy) * 0.18;
      dot.style.transform = `translate(${mx}px,${my}px)`;
      lab.style.transform = `translate(${cx + 16}px,${cy + 12}px)`;
      requestAnimationFrame(loop);
    })();
    document.addEventListener('mouseover', e => {
      const t = e.target.closest('[data-cursor]');
      if (t) { lab.textContent = t.dataset.cursor; lab.classList.add('on'); dot.classList.add('big'); }
      else { lab.classList.remove('on'); dot.classList.remove('big'); }
    });
  }

  /* ---------- TOOLTIPS: [data-tip] ---------- */
  if (!touch) {
    const tip = document.createElement('div'); tip.className = 'vtip'; document.body.appendChild(tip);
    let tid = null;
    document.addEventListener('mouseover', e => {
      const t = e.target.closest('[data-tip]');
      if (!t) return;
      tip.innerHTML = t.dataset.tip;
      tip.classList.add('on');
      clearTimeout(tid);
    });
    document.addEventListener('mousemove', e => {
      if (!tip.classList.contains('on')) return;
      const w = tip.offsetWidth, x = Math.min(e.clientX + 18, innerWidth - w - 12);
      tip.style.left = x + 'px'; tip.style.top = (e.clientY + 18) + 'px';
    });
    document.addEventListener('mouseout', e => {
      if (e.target.closest && e.target.closest('[data-tip]')) {
        tid = setTimeout(() => tip.classList.remove('on'), 120);
      }
    });
  }

  /* ---------- REVEAL on scroll: .rv (auto-stagger) ---------- */
  const rvEls = qsa('.rv');
  if (rvEls.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.classList.add('on');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    rvEls.forEach((el, i) => {
      el.style.setProperty('--rdd', (el.dataset.rdd || (i % 4) * 0.07) + 's');
      io.observe(el);
    });
  }

  /* ---------- COUNT-UP on view: [data-count] ---------- */
  const counters = qsa('[data-count]');
  if (counters.length) {
    const cio = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        const el = en.target, target = parseFloat(el.dataset.count);
        const dec = (el.dataset.count.split('.')[1] || '').length;
        if (reduce) { el.textContent = target.toFixed(dec); return; }
        const t0 = performance.now(), D = 900;
        (function tick(t) {
          const p = Math.min((t - t0) / D, 1), e2 = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * e2).toFixed(dec);
          if (p < 1) requestAnimationFrame(tick);
        })(t0);
      });
    }, { threshold: 0.4 });
    counters.forEach(el => cio.observe(el));
  }

  /* ---------- PAGE WIPE transitions (.html links) ---------- */
  if (!reduce) {
    const wipe = document.createElement('div'); wipe.className = 'vwipe';
    wipe.innerHTML = '<span class="anton">VIKAAS<span style="color:var(--acid)">.</span></span>';
    document.body.appendChild(wipe);
    const entering = sessionStorage.getItem('vwipe') === '1';
    if (entering) {
      sessionStorage.removeItem('vwipe');
      wipe.classList.add('in');
      requestAnimationFrame(() => setTimeout(() => wipe.classList.add('out'), 60));
      setTimeout(() => wipe.remove(), 950);
    } else { wipe.remove(); }
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href || !href.endsWith('.html') || a.target === '_blank' || href.includes('#') && href.split('#')[0] === location.pathname.split('/').pop()) return;
      e.preventDefault();
      const w2 = document.createElement('div'); w2.className = 'vwipe';
      document.body.appendChild(w2);
      sessionStorage.setItem('vwipe', '1');
      requestAnimationFrame(() => w2.classList.add('in2'));
      setTimeout(() => { location.href = href; }, 380);
    });
  }

  /* ---------- MAGNETS: .mag ---------- */
  if (!touch && !reduce) qsa('.mag').forEach(el => {
    const r = 46;
    el.addEventListener('mousemove', e => {
      const b = el.getBoundingClientRect();
      const dx = e.clientX - (b.left + b.width / 2), dy = e.clientY - (b.top + b.height / 2);
      const d = Math.hypot(dx, dy);
      if (d < r + b.width / 2) el.style.transform = `translate(${dx * 0.22}px,${dy * 0.22}px)`;
    });
    el.addEventListener('mouseleave', () => { el.style.transform = ''; });
  });
})();
