import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import drawerImg from '../assets/img/drawer_real.jpg';
import scaleImg from '../assets/img/scale_receipt.jpg';
import './proof.css';

const EVIDENCE = [
  { img: drawerImg, tag: 'EVIDENCE #1', title: 'THE DRAWER', line: 'The actual drawer, photographed — not a render. 3 phones, 7 chargers, a speaker that died in 2022, a cable bundle.', stamp: 'WEIGHED', cls: 'st-green' },
  { img: scaleImg, tag: 'EVIDENCE #2', title: 'THE SCALE + THE RECEIPT', line: '1.4 kg on a kitchen scale, ₹40 cash at the door, receipt kept. The transaction that became the app.', stamp: 'RECEIPT #0001', cls: 'st-gold' },
];

const NUMBERS = [
  ['1.4 KG', 'weighed on a kitchen scale', 'WEIGHED', 'st-green'],
  ['₹40', 'paid cash, at the door', 'RECEIPT #0001', 'st-gold'],
  ['15', 'HSPCB recyclers, sourced', 'SOURCED', 'st-green'],
  ['500 KG', 'minimum lot they demanded', 'THE GAP', 'st-red'],
  ['10/10', 'homes had a drawer; 0 could name a recycler', 'OUR SURVEY', 'st-violet'],
  ['3.2M T', 'India\u2019s e-waste, every year', 'SOURCED · CWC', 'st-green'],
];

const M2_TRACK = [
  ['BEFORE PHOTO', 'the drawer, as it was', 'CAPTURED', 'ok'],
  ['BEFORE NUMBER', '1.4 kg — same method, same scale', 'CAPTURED', 'ok'],
  ['NEIGHBOUR TALKS', '2 conversations, listen-only', 'PENDING · AARAV', 'soon'],
  ['RECYCLER CALL', 'min kg? doorstep? on speaker', 'PENDING · AARAV', 'soon'],
  ['WEIGH-DAY VIDEO', 'drawer → scale → handover, one take', 'PENDING · AARAV', 'soon'],
  ['AFTER PHOTO', 'the same drawer, emptied', 'PENDING · AARAV', 'soon'],
  ['AFTER NUMBER', 'kg diverted · ₹ paid · receipt', 'PENDING · AARAV', 'soon'],
  ['AGREEMENT', 'someone continues the change', 'PENDING · AARAV', 'soon'],
  ['MISSION PASSWORD', 'on-screen in the M2 video', 'PENDING · AARAV', 'soon'],
];

const CHAIN = ['YOUR DRAWER', 'THE DOORSTEP', 'COLLECTION PARTNER', 'HSPCB RECYCLER', 'THE REFINER'];

export default function Proof() {
  return (
    <main className="pf-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="pf-hero">
        <p className="eyebrow cmd shiny">the proof room · the evidence vault</p>
        <h1 className="anton pf-title">PROOF &gt;<br /><span>SCREENSHOTS</span></h1>
        <p className="pf-sub">Some portfolios show screenshots of apps that don't exist. <b>This one shows receipts from a drawer that did.</b> Every claim in this portfolio is stamped — here's where the stamps live, and where Mission 2's evidence lands as you capture it.</p>
      </section>

      <section className="pf-evidence-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the physical evidence · real</p>
          <h2 className="section-title">PHOTOGRAPHED.<br /><span>NOT GENERATED.</span></h2>
          <div className="pf-ev-grid">
            {EVIDENCE.map((e, i) => (
              <motion.figure key={e.tag} className="pf-ev"
                initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.25 }} transition={{ duration: 0.7, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}>
                <div className="pf-imgwrap" data-cursor="REAL">
                  <img src={e.img} alt={e.title} loading="lazy" />
                  <span className={`stamp ${e.cls} pf-bigstamp`}>{e.stamp}</span>
                </div>
                <figcaption>
                  <span className="cmd pf-tag">{e.tag}</span>
                  <h3 className="anton">{e.title}</h3>
                  <p>{e.line}</p>
                </figcaption>
              </motion.figure>
            ))}
          </div>

          <div className="pf-nums">
            {NUMBERS.map(([n, l, s, c]) => (
              <div key={n + l} className="pf-num" data-cursor={s}>
                <b className="anton">{n}</b>
                <span>{l}</span>
                <span className={`stamp ${c}`}>{s}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="pf-chain-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the chain of custody</p>
          <div className="pf-chain">
            {CHAIN.map((c, i) => (
              <div key={c} className="pf-chain-node">
                <span className="pf-dot">{i + 1}</span>
                <b>{c}</b>
                {i < CHAIN.length - 1 && <i className="pf-arrow">→</i>}
              </div>
            ))}
          </div>
          <p className="pf-chainnote">The receipt doesn't end at the door — it ends at a verified recycler. That's what the app digitises, and what Mission 2 proves, door by door.</p>
        </div>
      </section>

      <section className="pf-m2-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">mission 2 · the live evidence feed</p>
          <h2 className="section-title">MEASURE. ACT.<br /><span>MEASURE AGAIN.</span></h2>
          <p className="pf-sub">This tracker is the Mission 2 submission in real time — same method, same scale, photographed before and after. As Aarav captures each piece, it lands here. No number = incomplete. No proof = incomplete.</p>
          <div className="pf-track">
            {M2_TRACK.map(([what, how, status, cls], i) => (
              <motion.div key={what} className="pf-track-row"
                initial={{ opacity: 0, x: -26 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.05 }}>
                <span className="pf-track-no cmd">{String(i + 1).padStart(2, '0')}</span>
                <div className="pf-track-main">
                  <b className="anton">{what}</b>
                  <span className="cmd">{how}</span>
                </div>
                <span className={`pf-status ${cls}`}>{status}</span>
              </motion.div>
            ))}
          </div>
          <div className="pf-ctas">
            <Link to="/buddy" data-cursor="REBEE" data-mag className="go mag glow-hover">ASK REBEE →</Link>
            <Link to="/kabadi" data-cursor="KABADI" data-mag className="go ghost mag glow-hover">THE KABADI UNIVERSE</Link>
          </div>
        </div>
      </section>

      <footer className="pf-foot">
        <div className="foot-big anton grad-text">NO DRAWER<br />LEFT BEHIND<span style={{ color: 'var(--acid)' }}>.</span></div>
        <div className="pf-footmeta cmd">PROOF &gt; SCREENSHOTS · #EWasteOff · VIKAAS · GURUGRAM</div>
      </footer>
    </main>
  );
}
