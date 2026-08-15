import { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import SplitType from 'split-type';
import '../assets/css/gate.css';
import Monolith from '../components/Monolith.jsx';

gsap.registerPlugin(ScrollTrigger);

function countUp(el) {
  const t = parseFloat(el.dataset.count);
  const dec = parseInt(el.dataset.dec || '0', 10);
  const D = 1200, t0 = performance.now();
  (function tick(now) {
    const p = Math.min((now - t0) / D, 1);
    el.textContent = (t * (1 - Math.pow(1 - p, 3))).toFixed(dec);
    if (p < 1) requestAnimationFrame(tick);
  })(t0);
}

const ROOM_CARDS = [
  { to: '/drawer', no: '02', title: 'THE DRAWER', desc: 'the origin — pinned, cinematic, interactive', badge: 'ENTER →', live: true },
  { no: '03', title: 'THE PROOF', desc: 'receipts, the scale toy, the data', badge: 'PHASE 4', more: 'Every number stamped: WEIGHED, SOURCED, ESTIMATE, DRAMATISED. The scale toy, the receipts, the data — all interactive.' },
  { no: '04', title: 'THE ARSENAL', desc: '6 reels · 22 posts · made with code', badge: 'PHASE 6', more: 'Six reels and twenty-two posts, every frame made with code. Hover to play, click to open the films room.' },
  { no: '05', title: 'THE BUDDY', desc: 'ReBee — born from a Gurugram drawer', badge: 'PHASE 7', more: "1M1B's AI buddy: SCRAP-SCAN, DOORSTEP DIAL, MATERIAL MATCH. Built from the problem he solves." },
  { no: '06', title: 'THE SYSTEM', desc: 'the engine room — how it was all built', badge: 'PHASE 8', more: 'The receipts of the receipts — the engine, the pipelines, the self-review loop. The machine behind the machine.' },
  { no: '★', title: 'GENEVA', desc: 'UN · 20 NOV 2026 · the goal', badge: 'THE GOAL', more: "Top 3 fly to the 1M1B Impact Summit at the United Nations. That's the plan — publicly. Watch us." },
];

export default function Gate() {
  const titleRef = useRef(null);
  const subRef = useRef(null);
  const chipsRef = useRef(null);
  const cueRef = useRef(null);
  const footBigRef = useRef(null);

  useEffect(() => {
    const fast = new URLSearchParams(location.search).has('fast');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const title = titleRef.current;
    const sub = subRef.current, chips = chipsRef.current, cue = cueRef.current;

    // hero load
    if (title && sub && chips && cue && !fast && !reduce) {
      const en = title.querySelector('.en');
      let chs = [];
      try {
        const st = new SplitType(en, { types: 'chars' });
        chs = st.chars || [];
      } catch (e) { /* fall back to plain fade */ }
      const dev = title.querySelector('.dev');
      gsap.timeline({ defaults: { ease: 'power4.out' } })
        .fromTo(chs.length ? chs : en, { yPercent: 130, rotate: 10, opacity: 0 }, { yPercent: 0, rotate: 0, opacity: 1, stagger: 0.05, duration: 1.0, ease: 'back.out(1.7)' }, 0.2)
        .fromTo(dev, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(2)' }, 0.9)
        .fromTo(sub.querySelectorAll('.w'), { opacity: 0, filter: 'blur(10px)', y: 12 }, { opacity: 1, filter: 'blur(0px)', y: 0, stagger: 0.018, duration: 0.7 }, 1.05)
        .fromTo(chips.querySelectorAll('.chip'), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, stagger: 0.08, duration: 0.6, ease: 'back.out(2)' }, 1.4)
        .add(() => chips.querySelectorAll('[data-count]').forEach(countUp), 1.6)
        .fromTo(cue, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.9);
    } else if (title && sub && chips && cue) {
      gsap.set([title, sub.querySelectorAll('.w'), chips.querySelectorAll('.chip'), cue], { opacity: 1, y: 0, filter: 'none' });
      title.querySelectorAll('.ch').forEach((c) => { c.style.opacity = '1'; });
      chips.querySelectorAll('[data-count]').forEach(countUp);
    }

    // manifesto lines blur-reveal
    document.querySelectorAll('.mani-line').forEach((l) => {
      if (reduce) { gsap.set(l, { opacity: 1, filter: 'none', y: 0 }); return; }
      gsap.fromTo(l, { opacity: 0, filter: 'blur(14px)', y: 46 }, { opacity: 1, filter: 'blur(0px)', y: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: l, start: 'top 86%', once: true } });
    });


    // idea blocks reveal
    document.querySelectorAll('.idea-block').forEach((b, i) => {
      if (reduce) { gsap.set(b, { opacity: 1, y: 0 }); return; }
      gsap.fromTo(b, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out', delay: (i % 2) * 0.1, scrollTrigger: { trigger: b, start: 'top 88%', once: true } });
    });

    // room cards
    document.querySelectorAll('.room-card').forEach((c, i) => {
      if (reduce) { gsap.set(c, { opacity: 1, y: 0 }); return; }
      gsap.fromTo(c, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.65, ease: 'power3.out', delay: (i % 3) * 0.09, scrollTrigger: { trigger: c, start: 'top 90%', once: true } });
    });


    // 3D tilt on room cards
    const cards = document.querySelectorAll('.room-card');
    cards.forEach((c) => {
      c.addEventListener('pointermove', (e) => {
        const b = c.getBoundingClientRect();
        const rx = ((e.clientY - b.top) / b.height - 0.5) * -6;
        const ry = ((e.clientX - b.left) / b.width - 0.5) * 8;
        c.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-3px)`;
      });
      c.addEventListener('pointerleave', () => { c.style.transform = ''; });
    });

    // footer
    if (reduce) gsap.set(footBigRef.current, { opacity: 1, y: 0 });
    else gsap.fromTo(footBigRef.current, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out', scrollTrigger: { trigger: '#geneva', start: 'top 88%', once: true } });

    return () => { ScrollTrigger.getAll().forEach((st) => st.kill()); };
  }, []);

  const toggleExpand = (e, card) => {
    if (e.target.closest('a')) return;
    const all = document.querySelectorAll('.room-card[data-expand]');
    all.forEach((o) => { if (o !== card) o.classList.remove('expanded'); });
    card.classList.toggle('expanded');
  };

  return (
    <main>
      <section id="hero">
        <div className="mono-wrap" aria-hidden="true"><Monolith /></div>
        <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
        <div className="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
        <div className="hero-inner">
          <p className="eyebrow cmd shiny" id="heEyebrow">1M1B CHANGEMAKERS WORLD CUP 2026 <span>· TRACK: KILL THE E-WASTE</span></p>
          <h1 className="anton gate-title" ref={titleRef}><span className="en">VIKAAS</span><span className="dev">विकास</span></h1>
          <p className="gate-sub" ref={subRef}>
            <span className="w">One</span> <span className="w">drawer</span> <span className="w">in</span> <span className="w">Gurugram.</span><br />
            <span className="w">1.4</span> <span className="w">kg</span> <span className="w">of</span> <span className="w">dead</span> <span className="w">electronics</span> <span className="w">—</span> <span className="w">weighed</span> <span className="w">on</span> <span className="w">a</span> <span className="w">kitchen</span> <span className="w">scale.</span>
          </p>
          <div className="stat-chips" ref={chipsRef}>
            <div className="chip"><b><span data-count="1.4" data-dec="1">0.0</span> KG</b><span>weighed on a kitchen scale</span><span className="stamp st-green">WEIGHED</span></div>
            <div className="chip"><b>₹<span data-count="40">0</span></b><span>cash at the gate</span><span className="stamp st-gold">RECEIPT #1</span></div>
            <div className="chip"><b><span data-count="15">0</span></b><span>govt-authorised recyclers</span><span className="stamp st-green">SOURCED</span></div>
            <div className="chip"><b><span data-count="0">0</span></b><span>doorsteps served by them</span><span className="stamp st-red">THE GAP</span></div>
          </div>
        </div>
        <div className="cue" ref={cueRef}>SCROLL<span></span></div>
      </section>

      <div className="ticker"><div className="lane">
        <span>NO DRAWER LEFT BEHIND <i>✦</i></span><span>WEIGH IT <i>✦</i></span><span>EARN FROM IT <i>✦</i></span><span>RECYCLE IT <i>✦</i></span><span>15 RECYCLERS · 0 DOORSTEPS <i>✦</i></span><span>1.4 KG · ₹40 · 0 WORDS <i>✦</i></span>
        <span>NO DRAWER LEFT BEHIND <i>✦</i></span><span>WEIGH IT <i>✦</i></span><span>EARN FROM IT <i>✦</i></span><span>RECYCLE IT <i>✦</i></span><span>15 RECYCLERS · 0 DOORSTEPS <i>✦</i></span><span>1.4 KG · ₹40 · 0 WORDS <i>✦</i></span>
      </div></div>

      <section id="manifesto">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the manifesto</p>
          <div className="mani-lines">
            <p className="mani-line">The drawer waited four years.</p>
            <p className="mani-line">Ten homes asked. <em>Ten drawers found.</em></p>
            <p className="mani-line big">The infrastructure isn’t missing.<br /><span>THE DOORSTEP IS.</span></p>
          </div>
        </div>
      </section>

      <section id="idea">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the idea · told in four moves</p>
          <h2 className="section-title">THE<br /><span>IDEA</span></h2>
          <div className="idea-blocks">
            <div className="idea-block" data-cursor="THE DISCOVERY">
              <span className="idea-no anton">01</span>
              <h3 className="anton">THE DISCOVERY</h3>
              <p>One drawer in Gurugram held <b>1.4 kg</b> of dead electronics — three phones, seven chargers, a speaker that died in 2022. We weighed it on a kitchen scale. That was the whole idea: <em>nobody had ever weighed the problem.</em></p>
              <span className="stamp st-green">WEIGHED · 1.4 KG</span>
            </div>
            <div className="idea-block" data-cursor="THE GAP">
              <span className="idea-no anton">02</span>
              <h3 className="anton">THE GAP</h3>
              <p>Gurugram has <b>15 government-authorised recyclers</b> — on the HSPCB’s own public list. We called. The first question is always: <em>“how many kilos?”</em> A 500-kg minimum. A home has 1.4 kg. <b>15 recyclers. 0 doorsteps.</b></p>
              <span className="stamp st-red">THE GAP · 15 / 0</span>
            </div>
            <div className="idea-block" data-cursor="THE METHOD">
              <span className="idea-no anton">03</span>
              <h3 className="anton">THE METHOD</h3>
              <p><b>Weigh it. Earn from it. Recycle it.</b> Drawer kholo → scale par rakho → list kholo → photo + drop. ₹40 cash at the gate, a receipt as proof. <em>Weighed, not guessed</em> — every number stamped, sourced or labelled.</p>
              <span className="stamp st-gold">RECEIPT #0001 · ₹40</span>
            </div>
            <div className="idea-block" data-cursor="THE GOAL">
              <span className="idea-no anton">04</span>
              <h3 className="anton">THE GOAL</h3>
              <p>25 households. Every device weighed, logged, delivered. No drawer left behind — from one drawer in Gurugram to the <b>1M1B Impact Summit at the United Nations, 20 Nov 2026.</b> That’s the plan. Publicly. Watch us.</p>
              <span className="stamp st-violet">GENEVA · 20 NOV</span>
            </div>
          </div>
        </div>
      </section>

      <section id="rooms">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the universe</p>
          <h2 className="section-title">CHOOSE YOUR<br /><span>ROOM</span></h2>
          <div className="rooms-grid" id="roomGrid">
            {ROOM_CARDS.map((c, i) => c.to
              ? <Link key={i} className="room-card" to={c.to} data-cursor="OPEN">
                  <span className="no cmd">{c.no}</span><h3 className="anton glow-hover">{c.title}</h3><p>{c.desc}</p><span className="badge live">{c.badge}</span>
                </Link>
              : <div key={i} className="room-card locked" data-expand data-cursor="OPEN" onClick={(e) => toggleExpand(e, e.currentTarget)}>
                  <span className="no cmd">{c.no}</span><h3 className="anton glow-hover">{c.title}</h3><p>{c.desc}</p><span className="badge">{c.badge}</span>
                  <div className="more"><p className="more-copy">{c.more}</p><span className="more-cta cmd">LOCKED · IN BUILD</span></div>
                  <span className="xmore anton">+</span>
                </div>
            )}
          </div>
        </div>
      </section>

      <footer id="geneva">
        <div className="foot-big anton grad-text" ref={footBigRef}>NO DRAWER<br />LEFT BEHIND<span style={{ color: 'var(--acid)' }}>.</span></div>
        <div className="foot-links">
          <Link to="/boot" data-cursor="REPLAY" data-mag className="glow-hover">REPLAY THE BOOT →</Link>
          <a href="https://instagram.com/qwerty_aarav" target="_blank" data-cursor="IG ↗" data-mag className="glow-hover">@qwerty_aarav ↗</a>
          <a href="https://instagram.com/1m1bfoundation" target="_blank" data-cursor="IG ↗" data-mag className="glow-hover">@1m1bfoundation ↗</a>
        </div>
        <div className="foot-meta cmd">#EWasteOff #ChangemakersWorldCup #1M1B<br />vikaas · gurugram · receipts with taste</div>
      </footer>
    </main>
  );
}
