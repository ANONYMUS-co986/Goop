/* ============================================================
   VIKAAS v2 — THE GATE (index.html) choreography
   Timeline (page load + scroll):
     LOAD  0.0  aurora fade · nav drop · eyebrow
           0.2  VIKAAS chars slam (SplitType, back.out)
           0.5  विकास fades · sub words blur-in (BlurText)
           0.8  chips pop + count-ups fire
           1.1  cue fades in
     SCROLL: manifesto lines blur-reveal · spotlight stats
            slam + count · room cards stagger + tilt ·
            rebee parallax/tilt · footer big line reveal
   ?fast=1 / reduced-motion → everything visible instantly.
   ============================================================ */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(hover: none)').matches;
  const fast = new URLSearchParams(location.search).has('fast');
  const $ = (s) => document.querySelector(s);
  const qsa = (s) => Array.from(document.querySelectorAll(s));
  gsap.registerPlugin(ScrollTrigger, CustomEase);
  CustomEase.create('vx', '0.76, 0, 0.24, 1');
  CustomEase.create('pop', '0.34, 1.56, 0.64, 1');

  /* ---------- count-up ---------- */
  function countUp(el) {
    const t = parseFloat(el.dataset.count);
    const dec = parseInt(el.dataset.dec || '0', 10);
    if (reduce) { el.textContent = t.toFixed(dec); return; }
    const D = 1200, t0 = performance.now();
    (function tick(now) {
      const p = Math.min((now - t0) / D, 1);
      el.textContent = (t * (1 - Math.pow(1 - p, 3))).toFixed(dec);
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }
  function fireCounts(scope) {
    qsa('[data-count]', scope).forEach(countUp);
  }

  /* ---------- HERO LOAD ---------- */
  const title = $('#gateTitle');
  const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
  if (!fast && !reduce) {
    const st = new SplitType(title, { types: 'chars' });
    const chs = (st.chars || []).filter((c) => !c.classList.contains('dev'));
    const dev = title.querySelector('.dev');
    tl.fromTo(chs, { yPercent: 130, rotate: 10, opacity: 0 }, { yPercent: 0, rotate: 0, opacity: 1, stagger: 0.05, duration: 1.0, ease: 'back.out(1.7)' }, 0.2)
      .fromTo(dev, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: 'pop' }, 0.9)
      .fromTo(qsa('#gateSub .w'), { opacity: 0, filter: 'blur(10px)', y: 12 }, { opacity: 1, filter: 'blur(0px)', y: 0, stagger: 0.018, duration: 0.7 }, 1.05)
      .fromTo(qsa('.chip'), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, stagger: 0.08, duration: 0.6, ease: 'pop' }, 1.4)
      .add(() => fireCounts('#heroChips'), 1.6)
      .fromTo('#heCue', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.9);
    gsap.fromTo('.gnav', { y: -80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'vx' }, 0.05);
    gsap.fromTo('#heEyebrow', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6 }, 0.1);
  } else {
    gsap.set([title, qsa('#gateSub .w'), qsa('.chip'), '#heCue', '#heEyebrow', '.gnav'], { opacity: 1, y: 0, filter: 'none' });
    fireCounts(document);
  }

  /* ---------- MANIFESTO blur-reveal ---------- */
  qsa('.mani-line').forEach((l, i) => {
    if (reduce) { gsap.set(l, { opacity: 1, filter: 'none', y: 0 }); return; }
    gsap.fromTo(l, { opacity: 0, filter: 'blur(14px)', y: 46 }, {
      opacity: 1, filter: 'blur(0px)', y: 0, duration: 1.1, ease: 'power3.out',
      scrollTrigger: { trigger: l, start: 'top 86%', once: true },
    });
  });

  /* ---------- SPOTLIGHT STATS ---------- */
  const spots = qsa('.spot');
  spots.forEach((s, i) => {
    if (reduce) { gsap.set(s, { opacity: 1, y: 0 }); fireCounts(s); return; }
    s.addEventListener('pointermove', (e) => {
      const b = s.getBoundingClientRect();
      s.style.setProperty('--mx', ((e.clientX - b.left) / b.width * 100) + '%');
      s.style.setProperty('--my', ((e.clientY - b.top) / b.height * 100) + '%');
    });
    gsap.fromTo(s, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: (i % 2) * 0.08,
      scrollTrigger: { trigger: s, start: 'top 88%', once: true },
      onStart: () => countUp(s),
    });
  });

  /* ---------- ROOM CARDS: stagger + tilt + magnet ---------- */
  const cards = qsa('.room-card');
  cards.forEach((c, i) => {
    if (reduce) { gsap.set(c, { opacity: 1, y: 0 }); return; }
    gsap.fromTo(c, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.65, ease: 'power3.out', delay: (i % 3) * 0.09,
      scrollTrigger: { trigger: c, start: 'top 90%', once: true },
    });
    if (!touch) {
      c.addEventListener('pointermove', (e) => {
        const b = c.getBoundingClientRect();
        const rx = ((e.clientY - b.top) / b.height - 0.5) * -7;
        const ry = ((e.clientX - b.left) / b.width - 0.5) * 9;
        c.style.transform = 'perspective(800px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateY(-4px)';
      });
      c.addEventListener('pointerleave', () => { c.style.transform = ''; });
    }
  });

  /* ---------- REBEE: parallax + tilt ---------- */
  const art = $('#rebeeArt');
  if (!reduce) {
    gsap.fromTo(art.querySelector('img'), { yPercent: 5 }, {
      yPercent: -5, ease: 'none',
      scrollTrigger: { trigger: '#rebee', start: 'top bottom', end: 'bottom top', scrub: true },
    });
  }
  if (!touch && !reduce) {
    art.addEventListener('pointermove', (e) => {
      const b = art.getBoundingClientRect();
      const rx = ((e.clientY - b.top) / b.height - 0.5) * -9;
      const ry = ((e.clientX - b.left) / b.width - 0.5) * 9;
      art.style.transform = 'perspective(900px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
    });
    art.addEventListener('pointerleave', () => { art.style.transform = ''; });
  }
  qsa('.power').forEach((p, i) => {
    if (reduce) { gsap.set(p, { opacity: 1, y: 0 }); return; }
    gsap.fromTo(p, { opacity: 0, y: 24 }, {
      opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', delay: i * 0.1,
      scrollTrigger: { trigger: p, start: 'top 90%', once: true },
    });
  });
  if (reduce) gsap.set('.mission', { opacity: 1, y: 0 });
  else gsap.fromTo('.mission', { opacity: 0, y: 24 }, {
    opacity: 1, y: 0, duration: 0.7, ease: 'vx',
    scrollTrigger: { trigger: '.mission', start: 'top 92%', once: true },
  });

  /* ---------- FOOTER ---------- */
  if (reduce) gsap.set('#footBig', { opacity: 1, y: 0 });
  else gsap.fromTo('#footBig', { opacity: 0, y: 50 }, {
    opacity: 1, y: 0, duration: 1.0, ease: 'vx',
    scrollTrigger: { trigger: '#geneva', start: 'top 88%', once: true },
  });
})();
