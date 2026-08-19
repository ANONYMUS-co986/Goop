import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import drawerImg from '../assets/img/drawer_real.jpg';
import '../assets/css/drawer.css';

gsap.registerPlugin(ScrollTrigger);

const ITEMS = {
  phone:   { name: '3 DEAD PHONES',     line: 'cracked screens, swollen battery — weighed', value: '≈ ₹12 · copper + board', recycler: 'Exigo Recycling · Manesar', stamp: 'WEIGHED' },
  charger: { name: '7 CHARGERS',        line: '2014–forever — “kabhi kaam aayega”', value: '≈ ₹9 · copper wire + plugs', recycler: 'EcoMetals · Gurugram', stamp: 'RECEIPT #1' },
  cable:   { name: 'TANGLED CABLES',    line: 'the drawer’s own ecosystem', value: '≈ ₹4 · mixed metals', recycler: 'Cerebra · HITEC City', stamp: 'SOURCED' },
  battery: { name: 'SWOLLEN POWER BANK', line: 'the one that scared us', value: '≈ ₹3 · lithium — respect it', recycler: 'Attero · Noida', stamp: 'HANDLE CAREFULLY' },
  speaker: { name: '1 SPEAKER',         line: 'died 2022 — the only one that said goodbye', value: '≈ ₹12 · magnet + board', recycler: 'E-Parisaraa · Peenya', stamp: 'WEIGHED' },
};

export default function Drawer() {
  const toyRef = useRef(null);
  const frontRef = useRef(null);
  const readoutRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [readout, setReadout] = useState('CLICK THE DRAWER');
  const [spec, setSpec] = useState(null);

  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

    // drawer intro hero (visible on load) — line-stagger + glow
    const t = document.querySelector('#dintroTitle');
    const sub = document.querySelector('#dintroSub');
    const cue = document.querySelector('#dintroCue');
    if (!reduce && t) {
      gsap.timeline({ defaults: { ease: 'power4.out' } })
        .fromTo('#dintroTitle .dt-line[data-line="the"]', { yPercent: 120, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.9, ease: 'back.out(1.6)' }, 0.15)
        .fromTo('#dintroTitle .dt-line[data-line="drawer"]', { yPercent: 120, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1.0, ease: 'back.out(1.6)' }, 0.35)
        .fromTo(sub, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7 }, 0.8)
        .fromTo(cue, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.1);
    } else {
      gsap.set([t, sub, cue], { opacity: 1, y: 0 });
      gsap.set('#dintroTitle .dt-line', { opacity: 1, y: 0 });
    }
    // pinned story
    if (!reduce) {
      const tl = gsap.timeline({
        scrollTrigger: { trigger: '#story', start: 'top top', end: '+=2200', pin: true, scrub: 0.6 },
      });
      tl.fromTo('#storyPhoto', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1.0, ease: 'power2.inOut' }, 0)
        .fromTo('#storyPhoto img', { scale: 1.15 }, { scale: 1.0, duration: 1.0, ease: 'power1.out' }, 0)
        .fromTo('.story-copy .l1', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.0)
        .fromTo('.story-copy .l2', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.4)
        .fromTo('.story-copy .l3', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 1.8)
        .fromTo('.story-copy .l4', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, 2.2)
        .fromTo('.story-copy .big', { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'power2.out' }, 2.7)
        .fromTo('.story-copy .kicker', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.45 }, 3.1);
    } else {
      gsap.set('#storyPhoto', { clipPath: 'inset(0 0% 0 0)' });
      gsap.set('.story-copy .line, .story-copy .big, .story-copy .kicker', { opacity: 1, y: 0 });
    }

    // scale sequence (scroll-scrubbed)
    if (!reduce) {
      const stScale = ScrollTrigger.create({
        trigger: '#scaleRig', start: 'top 80%', end: 'bottom 60%', scrub: 0.5,
      });
      gsap.timeline({
        scrollTrigger: stScale,
        onUpdate: function () {
          let p = stScale.progress;
          if (!isFinite(p)) p = 0;
          p = Math.max(0, Math.min(1, p));
          const needle = document.querySelector('#needle');
          const read = document.querySelector('#scaleReadout b');
          const status = document.querySelector('#scaleReadout span');
          if (needle) needle.setAttribute('x2', String(100 + Math.sin(p * Math.PI) * 60));
          if (read) read.textContent = (1.4 * p).toFixed(2) + ' KG';
          if (status) status.textContent = p >= 0.98 ? 'SETTLED · 1.4 KG' : (p > 0.05 ? 'WEIGHING…' : 'READY');
        },
      })
        .fromTo('#sLine1', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25 }, 0.1)
        .fromTo('#sLine2', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25 }, 0.3)
        .fromTo('#sLine3', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25 }, 0.55)
        .fromTo('#sLine4', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25 }, 0.72)
        .fromTo('#sReceipt', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(1.8)' }, 0.85);
    } else {
      gsap.set('.scale-line, #sReceipt', { opacity: 1, y: 0 });
    }

    // list cards
    document.querySelectorAll('.lcard').forEach((c, i) => {
      if (reduce) { gsap.set(c, { opacity: 1, y: 0 }); return; }
      gsap.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: i * 0.12, scrollTrigger: { trigger: c, start: 'top 90%', once: true } });
    });
    // footer
    if (reduce) gsap.set('.foot-big', { opacity: 1, y: 0 });
    else gsap.fromTo('.foot-big', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out', scrollTrigger: { trigger: '#geneva', start: 'top 88%', once: true } });

    // 3D tilt on the toy
    const toyEl = toyRef.current;
    if (toyEl) {
      toyEl.addEventListener('pointermove', (e) => {
        const b = toyEl.getBoundingClientRect();
        const rx = ((e.clientY - b.top) / b.height - 0.5) * -5;
        const ry = ((e.clientX - b.left) / b.width - 0.5) * 7;
        toyEl.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg)`;
      });
      toyEl.addEventListener('pointerleave', () => { toyEl.style.transform = ''; });
    }
    return () => { ScrollTrigger.getAll().forEach((st) => st.kill()); };
  }, []);

  const toggleToy = (e) => {
    if (e.target.closest('.toy-item')) return;
    setOpen((v) => !v);
    setReadout(!open ? 'THE DRAWER IS OPEN — TAP AN ITEM' : 'CLICK THE DRAWER');
  };
  const tapItem = (e, key) => {
    e.stopPropagation();
    const item = e.currentTarget;
    setReadout(ITEMS[key].name + ' — ' + ITEMS[key].line);
    item.classList.add('popped');
    setTimeout(() => item.classList.remove('popped'), 400);
    setSpec(ITEMS[key]);
  };

  return (
    <main>
      <section id="dintro">
        <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
        <div className="dintro-inner">
          <p className="eyebrow cmd shiny">room 02 · the origin</p>
          <h1 className="anton dintro-title" id="dintroTitle"><span className="dt-line" data-line="the">THE</span><span className="dt-line" data-line="drawer">DRAWER</span></h1>
          <p className="dintro-sub" id="dintroSub">Four years of “kuch kaam ka cheez”, weighed at last. Scroll to open the story.</p>
          <div className="cue" id="dintroCue">SCROLL<span></span></div>
        </div>
      </section>

      <div className="story-wrap">
      <div className="story-rail" aria-hidden="true"><i></i></div>
      <section id="story">
        <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
        <div className="story-stage" id="storyStage">
          <div className="story-photo" id="storyPhoto">
            <img src={drawerImg} alt="the drawer — real photo, our kitchen" />
            <div className="photo-glow"></div>
          </div>
          <div className="story-copy">
            <p className="eyebrow cmd shiny">the origin · 1.4 kg</p>
            <p className="line l1">The drawer had been waiting four years.</p>
            <p className="line l2">Inside — 1.4 kg of <em>“kuch kaam ka cheez”.</em></p>
            <p className="line l3">Ten homes asked. Ten drawers found.</p>
            <p className="line l4">Not one could name a single authorised recycler.</p>
            <h2 className="big"><span className="n15">15 RECYCLERS.</span> <span className="n0">0 DOORSTEPS.</span></h2>
            <p className="kicker">The infrastructure isn’t missing. The doorstep is.</p>
          </div>
        </div>
      </section>
      </div>

      <section id="toy">
        <div className="wrap">
          <p className="eyebrow cmd shiny">interactive · open it yourself</p>
          <h2 className="section-title">OPEN THE<br /><span>DRAWER</span></h2>
          <div className="toy-wrap">
            <div>
              <div className={`drawer-toy ${open ? 'open' : ''}`} ref={toyRef} onClick={toggleToy} data-cursor="OPEN / CLOSE">
                <div className="toy-front" ref={frontRef}>
                  <span className="toy-label anton">VIKAAS</span>
                  <div className="toy-handle"></div>
                </div>
                <div className="toy-inside" id="toyInside">
                  <div className="toy-item ph" data-item="phone" onClick={(e) => tapItem(e, 'phone')}>📱</div>
                  <div className="toy-item ch" data-item="charger" onClick={(e) => tapItem(e, 'charger')}>🔌</div>
                  <div className="toy-item cb" data-item="cable" onClick={(e) => tapItem(e, 'cable')}>🔗</div>
                  <div className="toy-item bt" data-item="battery" onClick={(e) => tapItem(e, 'battery')}>🔋</div>
                  <div className="toy-item sp" data-item="speaker" onClick={(e) => tapItem(e, 'speaker')}>🔊</div>
                </div>
              </div>
              <div className="toy-readout" ref={readoutRef}>{readout}</div>
              {spec && (
                <div className="holo-card" key={spec.name} data-cursor="SPEC">
                  <div className="holo-scan" aria-hidden="true"></div>
                  <span className="holo-tag cmd">SCRAP-SCAN · LIVE</span>
                  <h4 className="anton holo-name">{spec.name}</h4>
                  <p className="holo-line">{spec.line}</p>
                  <div className="holo-rows">
                    <div className="holo-row"><span className="cmd">VALUE</span><b className="anton">{spec.value}</b></div>
                    <div className="holo-row"><span className="cmd">RECYCLER</span><b className="anton">{spec.recycler}</b></div>
                  </div>
                  <span className="stamp st-green">{spec.stamp}</span>
                </div>
              )}
            </div>
            <div className="toy-info">
              <p>Every item was real. Every item was weighed. Click the drawer, click the items — this is the audit, playable.</p>
              <div className="toy-stats">
                <div className="ts"><b className="anton">3</b><span>dead phones</span></div>
                <div className="ts"><b className="anton">7</b><span>chargers (2014–forever)</span></div>
                <div className="ts"><b className="anton">1</b><span>speaker, died 2022</span></div>
                <div className="ts"><b className="anton">10</b><span>homes surveyed</span></div>
              </div>
              <span className="stamp st-green">WEIGHED · 1.4 KG</span>
            </div>
          </div>
        </div>
      </section>

      <section id="scale-seq">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the moment · weighed, not guessed</p>
          <h2 className="section-title">THE WEIGH<br /><span>IN</span></h2>
          <div className="scale-rig" id="scaleRig">
            <div className="scale-dial">
              <svg viewBox="0 0 200 140" className="scale-svg">
                <path d="M20 120 A80 80 0 0 1 180 120" fill="none" stroke="rgba(255,255,255,.12)" strokeWidth="3"/>
                <path d="M40 120 A60 60 0 0 1 160 120" fill="none" stroke="rgba(255,255,255,.08)" strokeWidth="2"/>
                <g className="ticks">
                  {[0,15,30,45,60,75,90,105,120,135,150,165,180].map(a => (
                    <line key={a} x1={100 + 78*Math.cos((a-90)*Math.PI/180)} y1={120 + 78*Math.sin((a-90)*Math.PI/180)} x2={100 + 84*Math.cos((a-90)*Math.PI/180)} y2={120 + 84*Math.sin((a-90)*Math.PI/180)} stroke="rgba(185,255,63,.5)" strokeWidth="2"/>
                  ))}
                </g>
                <text x="100" y="105" textAnchor="middle" className="scale-unit cmd">0–2 KG</text>
                <g id="needleG" className="needle">
                  <line id="needle" x1="100" y1="120" x2="100" y2="44" stroke="#B9FF3F" strokeWidth="3" strokeLinecap="round"/>
                  <circle cx="100" cy="120" r="7" fill="#B9FF3F"/>
                </g>
              </svg>
              <div className="scale-readout" id="scaleReadout"><b className="anton">0.00 KG</b><span className="cmd">WEIGHING…</span></div>
            </div>
            <div className="scale-copy">
              <p className="scale-line" id="sLine1">The drawer, on the scale.</p>
              <p className="scale-line" id="sLine2">The needle swings… settles.</p>
              <p className="scale-line" id="sLine3"><b className="anton">1.4 KG.</b> Weighed. Photographed. Logged.</p>
              <p className="scale-line" id="sLine4">Not guessed. Not “about this much”. <em>Weighed.</em></p>
              <div className="scale-receipt" id="sReceipt"><span className="cmd">RECEIPT #0001</span><b className="anton">1.4 KG · ₹40</b><span className="stamp st-green">WEIGHED</span></div>
            </div>
          </div>
        </div>
      </section>

      <section id="list">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the public list · sourced</p>
          <h2 className="section-title">15 RECYCLERS<br /><span>0 DOORSTEPS</span></h2>
          <p className="list-sub">Gurugram has 15 government-authorised e-waste recyclers — on the Haryana Pollution Control Board's own list. We called. The first question is always the same: “how many kilos?”</p>
          <div className="list-cards" id="listCards">
            <div className="lcard" data-cursor="BULK-ONLY"><b className="anton">500 KG</b><span>minimum lot, said the recycler</span><span className="stamp st-red">BULK-ONLY</span></div>
            <div className="lcard" data-cursor="WE HAD"><b className="anton">1.4 KG</b><span>what our drawer weighed</span><span className="stamp st-green">WEIGHED</span></div>
            <div className="lcard" data-cursor="THE GAP"><b className="anton">498.6 KG</b><span>the distance between them</span><span className="stamp st-gold">THE GAP</span></div>
          </div>
          <Link className="go mag glow-hover" to="/proof" data-cursor="THE PROOF" data-mag>SEE THE FULL EVIDENCE →</Link>
        </div>
      </section>

      <footer id="geneva">
        <div className="foot-big anton grad-text">NO DRAWER<br />LEFT BEHIND<span style={{ color: 'var(--acid)' }}>.</span></div>
        <div className="foot-links">
          <Link to="/" data-cursor="THE GATE" data-mag className="glow-hover">BACK TO THE GATE →</Link>
          <Link to="/boot" data-cursor="REPLAY" data-mag className="glow-hover">REPLAY THE BOOT →</Link>
        </div>
        <div className="foot-meta cmd">vikaas · gurugram · receipts with taste</div>
      </footer>
    </main>
  );
}
