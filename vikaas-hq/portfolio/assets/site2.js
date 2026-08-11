/* ============================================================
   VIKAAS HUB v2 — site2.js · the choreography layer
   GSAP + ScrollTrigger + CustomEase + Lenis + SplitType
   Boot sequence → hero intro → story pin → receipt print →
   scale → arsenal pin → rebee → plan → footer. Self-review ready:
   ?fast=1 skips the boot for headless QA.
   ============================================================ */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(hover: none)').matches;
  const qs = (s) => document.querySelector(s);
  const fast = new URLSearchParams(location.search).has('fast') || new URLSearchParams(location.search).has('skipboot');
  const isHub = !!qs('#heroTitle');

  if (!isHub) return; // this layer only runs on the hub page

  gsap.registerPlugin(ScrollTrigger, CustomEase);
  CustomEase.create('vx', '0.76, 0, 0.24, 1');
  CustomEase.create('pop', '0.34, 1.56, 0.64, 1');

  /* ============ BOOT SEQUENCE ============ */
  const BOOT = [
    ['> vikaas_portfolio v2.3 — boot', 'dim'],
    ['> scanning drawer inventory … 3 phones · 7 chargers · 1 speaker (2022)', ''],
    ['> weighing … 1.4 KG — receipt logged', 'acid'],
    ['> surveying 10 homes … 10/10 have the same drawer', ''],
    ['> querying HSPCB registry … 15 authorised recyclers found', 'acid'],
    ['> doorsteps served … 0', 'red'],
    ['> mission: NO DRAWER LEFT BEHIND', 'acid'],
  ];
  const logEl = qs('#bootlog');
  const barEl = qs('#bootbar i');

  function bootDone() {
    document.body.classList.add('booted');
    setTimeout(startHero, 650);
  }

  function esc(s) { return s.replace(/[<>&]/g, (m) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[m])); }

  function runBoot() {
    if (fast || reduce) { bootDone(); return; }
    let li = 0, ci = 0;
    const done = [];
    const render = () => {
      const out = done.map(([t, cls]) => (cls ? `<span class="${cls}">${esc(t)}</span>` : esc(t)));
      const cur = BOOT[li];
      const partial = esc(cur[0].slice(0, ci));
      out.push(cur[1] ? `<span class="${cur[1]}">${partial}</span>` : partial);
      logEl.innerHTML = out.join('\n');
    };
    const tick = () => {
      if (ci < BOOT[li][0].length) {
        ci++;
        render();
        setTimeout(tick, 9);
      } else {
        done.push([BOOT[li][0], BOOT[li][1]]);
        li++;
        if (li < BOOT.length) { ci = 0; render(); setTimeout(tick, 150); }
        else finish();
      }
    };
    function finish() {
      gsap.to(barEl, { width: '100%', duration: 0.7, ease: 'power2.inOut', onComplete: bootDone });
    }
    render();
    tick();
  }
  qs('#skip').addEventListener('click', () => { if (!document.body.classList.contains('booted')) bootDone(); });

  /* ============ HERO INTRO ============ */
  function startHero() {
    const title = qs('#heroTitle');
    const chars = window.SplitType ? new SplitType(title, { types: 'chars' }) : null;
    const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
    if (chars && chars.chars && !reduce) {
      tl.fromTo(chars.chars,
        { yPercent: 120, rotate: 8, opacity: 0 },
        { yPercent: 0, rotate: 0, opacity: 1, stagger: 0.045, duration: 1.05, ease: 'power4.out' }, 0.15);
    } else {
      tl.fromTo(title, { opacity: 0, y: 46 }, { opacity: 1, y: 0, duration: 0.9 }, 0.15);
    }
    tl.fromTo('#heroEyebrow', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6 }, 0.3)
      .fromTo('#heroSub', { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.7 }, 0.55)
      .fromTo('.chip', { opacity: 0, y: 26, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, stagger: 0.08, duration: 0.6, ease: 'pop' }, 0.75)
      .fromTo('#heroCue', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.1);
  }

  /* ============ LENIS SMOOTH SCROLL ============ */
  if (window.Lenis && !reduce && !touch) {
    const lenis = new Lenis({ lerp: 0.1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  /* ============ STORY — pinned scrub ============ */
  if (!reduce && !touch) {
    const tl = gsap.timeline({
      scrollTrigger: { trigger: '#story', start: 'top top', end: '+=1900', pin: true, scrub: 0.6 },
    });
    tl.fromTo('#storyPhoto', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.1, ease: 'power2.inOut' }, 0)
      .fromTo('.story-copy .l1', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.1)
      .fromTo('.story-copy .l2', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.5)
      .fromTo('.story-copy .l3', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.9)
      .fromTo('.story-copy .l4', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 2.3)
      .fromTo('.story-copy .big', { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'vx' }, 2.8)
      .fromTo('.story-copy .kicker', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.45 }, 3.2);
  } else {
    gsap.set('.story-copy .line, .story-copy .big, .story-copy .kicker', { opacity: 1, y: 0 });
    gsap.set('#storyPhoto', { clipPath: 'inset(0 0% 0 0)' });
  }

  /* ============ RECEIPT — print + stamps ============ */
  const paper = qs('#receiptPaper');
  if (!reduce) {
    gsap.fromTo(paper, { clipPath: 'inset(100% 0 0 0)' }, {
      clipPath: 'inset(0% 0 0 0)', ease: 'none',
      scrollTrigger: { trigger: paper, start: 'top 80%', end: 'top 30%', scrub: true },
    });
  }
  const stamps = gsap.timeline({
    scrollTrigger: { trigger: paper, start: 'top 55%', once: true },
    defaults: { ease: 'pop' },
  });
  if (reduce) { gsap.set('.stamp', { opacity: 1 }); }
  else {
    stamps.fromTo('.stamp', { opacity: 0, scale: 1.9, rotate: (i) => (i % 2 ? 8 : -8) }, {
      opacity: 1, scale: 1, rotate: (i) => (i % 2 ? 3 : -4), stagger: 0.14, duration: 0.5,
    });
  }

  /* ============ SCALE ============ */
  if (!reduce) {
    gsap.fromTo('.bar .fill.big', { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: 'power3.inOut', scrollTrigger: { trigger: '#scale', start: 'top 70%', once: true } });
    gsap.fromTo('.bar .fill.small', { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: 'power3.inOut', delay: 0.25, scrollTrigger: { trigger: '#scale', start: 'top 70%', once: true } });
    gsap.fromTo('#scalePunch', { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.6, delay: 0.6, scrollTrigger: { trigger: '#scalePunch', start: 'top 85%', once: true } });
  } else {
    gsap.set('.bar .fill', { scaleX: 1 });
    gsap.set('#scalePunch', { opacity: 1, y: 0 });
  }

  /* ============ ARSENAL — horizontal pin (desktop) ============ */
  const track = qs('#reelTrack');
  if (!reduce && !touch && innerWidth >= 900) {
    const dist = () => Math.max(track.scrollWidth - innerWidth, 0);
    gsap.to(track, {
      x: () => -dist(), ease: 'none',
      scrollTrigger: {
        trigger: '#pinArs', start: 'top top', end: () => '+=' + (dist() + innerHeight * 0.6),
        pin: true, scrub: 1, invalidateOnRefresh: true,
      },
    });
  }

  /* reel hover-play */
  qsa('.reel-card').forEach((card) => {
    const v = card.querySelector('video');
    if (!v) return;
    if (!touch && !reduce) {
      card.addEventListener('mouseenter', () => { v.currentTime = 0; v.play().catch(() => {}); });
      card.addEventListener('mouseleave', () => { v.pause(); });
    } else {
      card.addEventListener('click', () => { v.paused ? v.play().catch(() => {}) : v.pause(); });
    }
  });

  /* ============ REBEE — parallax + reveals + tilt ============ */
  if (!reduce) {
    gsap.fromTo('.rebee-art img', { yPercent: 4 }, {
      yPercent: -4, ease: 'none',
      scrollTrigger: { trigger: '#rebee', start: 'top bottom', end: 'bottom top', scrub: true },
    });
  }
  gsap.fromTo('.power', { opacity: 0, y: 26 }, {
    opacity: 1, y: 0, stagger: 0.12, duration: 0.6, ease: 'power3.out',
    scrollTrigger: { trigger: '.powers', start: 'top 78%', once: true },
  });
  if (!touch && !reduce) {
    const art = qs('#rebeeArt');
    art.addEventListener('pointermove', (e) => {
      const b = art.getBoundingClientRect();
      const rx = ((e.clientY - b.top) / b.height - 0.5) * -10;
      const ry = ((e.clientX - b.left) / b.width - 0.5) * 10;
      art.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    });
    art.addEventListener('pointerleave', () => { art.style.transform = ''; });
  }

  /* ============ PLAN — road fill + stops ============ */
  const fill = document.createElement('i');
  fill.style.cssText = 'position:absolute;inset:0;background:linear-gradient(var(--acid),var(--green));transform:scaleY(0);transform-origin:top';
  qs('#roadLine').appendChild(fill);
  const roadTl = gsap.timeline({
    scrollTrigger: { trigger: '#plan', start: 'top 65%', end: 'bottom 55%', scrub: 0.5 },
  });
  roadTl.to(fill, { scaleY: 1, ease: 'none', duration: 1 }, 0);
  if (!reduce) {
    gsap.utils.toArray('.stop').forEach((s, i) => {
      roadTl.to(s, { opacity: 1, duration: 0.12, ease: 'none' }, 0.18 * i + 0.05);
    });
  }

  /* ============ FOOTER ============ */
  if (!reduce) {
    gsap.fromTo('.foot-big', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.9, ease: 'vx', scrollTrigger: { trigger: '#foot', start: 'top 85%', once: true } });
    gsap.fromTo('.foot-links a', { opacity: 0, y: 18 }, { opacity: 1, y: 0, stagger: 0.07, duration: 0.5, scrollTrigger: { trigger: '.foot-links', start: 'top 90%', once: true } });
  }
  qs('#reboot').addEventListener('click', () => location.reload());

  /* helper for querySelectorAll (used by hover-play) */
  function qsa(s) { return Array.from(document.querySelectorAll(s)); }

  /* kick off */
  runBoot();
})();
