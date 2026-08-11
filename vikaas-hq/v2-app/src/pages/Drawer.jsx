import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import drawerImg from '../assets/img/drawer_real.jpg';
import '../assets/css/drawer.css';

gsap.registerPlugin(ScrollTrigger);

const ITEMS = {
  phone: '3 DEAD PHONES · cracked screens, swollen battery — weighed',
  charger: '7 CHARGERS · 2014–forever — “kabhi kaam aayega”',
  cable: 'TANGLED CABLES · the drawer’s own ecosystem',
  battery: 'SWOLLEN POWER BANK · the one that scared us',
  speaker: '1 SPEAKER · died 2022 — the only one that told us goodbye',
};

export default function Drawer() {
  const toyRef = useRef(null);
  const frontRef = useRef(null);
  const readoutRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [readout, setReadout] = useState('CLICK THE DRAWER');

  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
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
    // list cards
    document.querySelectorAll('.lcard').forEach((c, i) => {
      if (reduce) { gsap.set(c, { opacity: 1, y: 0 }); return; }
      gsap.fromTo(c, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: i * 0.12, scrollTrigger: { trigger: c, start: 'top 90%', once: true } });
    });
    // footer
    if (reduce) gsap.set('.foot-big', { opacity: 1, y: 0 });
    else gsap.fromTo('.foot-big', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.0, ease: 'power3.out', scrollTrigger: { trigger: '#geneva', start: 'top 88%', once: true } });
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
    setReadout(ITEMS[key]);
    item.classList.add('popped');
    setTimeout(() => item.classList.remove('popped'), 400);
  };

  return (
    <main>
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
          <Link className="go mag glow-hover" to="/" data-cursor="THE GATE" data-mag>BACK TO THE GATE →</Link>
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
