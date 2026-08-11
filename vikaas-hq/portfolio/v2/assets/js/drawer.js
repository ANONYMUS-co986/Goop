/* ============================================================
   VIKAAS v2 — THE DRAWER page
   pinned story scrub · interactive drawer toy (click to open,
   click items for readout) · the list cards · footer
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

  /* ---------- PINNED STORY ---------- */
  if (!reduce && !touch) {
    const tl = gsap.timeline({
      scrollTrigger: { trigger: '#story', start: 'top top', end: '+=2200', pin: true, scrub: 0.6 },
    });
    tl.fromTo('#storyPhoto', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.0, ease: 'power2.inOut' }, 0)
      .fromTo('#storyPhoto img', { scale: 1.15 }, { scale: 1.0, duration: 1.0, ease: 'power1.out' }, 0)
      .fromTo('.story-copy .l1', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.0)
      .fromTo('.story-copy .l2', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.4)
      .fromTo('.story-copy .l3', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.8)
      .fromTo('.story-copy .l4', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 2.2)
      .fromTo('.story-copy .big', { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'vx' }, 2.7)
      .fromTo('.story-copy .kicker', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.45 }, 3.1);
  } else {
    gsap.set('#storyPhoto', { clipPath: 'inset(0 0% 0 0)' });
    gsap.set('.story-copy .line, .story-copy .big, .story-copy .kicker', { opacity: 1, y: 0 });
  }

  /* ---------- INTERACTIVE DRAWER TOY ---------- */
  const toy = $('#drawerToy'), front = $('#toyFront'), inside = $('#toyInside'),
        readout = $('#toyReadout');
  const ITEMS = {
    phone: '3 DEAD PHONES · cracked screens, swollen battery — weighed',
    charger: '7 CHARGERS · 2014–forever — “kabhi kaam aayega”',
    cable: 'TANGLED CABLES · the drawer’s own ecosystem',
    battery: 'SWOLLEN POWER BANK · the one that scared us',
    speaker: '1 SPEAKER · died 2022 — the only one that told us goodbye',
  };
  let open = false;
  function setOpen(v) {
    open = v;
    toy.classList.toggle('open', v);
    front.classList.toggle('gone', v);
    readout.textContent = v ? 'THE DRAWER IS OPEN — TAP AN ITEM' : 'CLICK THE DRAWER';
  }
  toy.addEventListener('click', (e) => {
    const item = e.target.closest('.toy-item');
    if (item) {
      readout.textContent = ITEMS[item.dataset.item] || '';
      item.classList.add('popped');
      setTimeout(() => item.classList.remove('popped'), 400);
      return;
    }
    setOpen(!open);
  });

  /* ---------- THE LIST ---------- */
  qsa('.lcard').forEach((c, i) => {
    if (reduce) { gsap.set(c, { opacity: 1, y: 0 }); return; }
    gsap.fromTo(c, { opacity: 0, y: 40 }, {
      opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: i * 0.12,
      scrollTrigger: { trigger: c, start: 'top 90%', once: true },
    });
  });
  gsap.fromTo('.go', { opacity: 0, y: 20 }, {
    opacity: 1, y: 0, duration: 0.6, delay: 0.3,
    scrollTrigger: { trigger: '.go', start: 'top 92%', once: true },
  });
  if (reduce) gsap.set('.go', { opacity: 1, y: 0 });

  /* ---------- FOOTER ---------- */
  if (reduce) gsap.set('.foot-big', { opacity: 1, y: 0 });
  else gsap.fromTo('.foot-big', { opacity: 0, y: 50 }, {
    opacity: 1, y: 0, duration: 1.0, ease: 'vx',
    scrollTrigger: { trigger: '#geneva', start: 'top 88%', once: true },
  });
})();
