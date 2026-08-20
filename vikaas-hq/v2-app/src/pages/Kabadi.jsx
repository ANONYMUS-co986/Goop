import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './kabadi.css';

const CAST = [
  {
    no: '01', title: 'THE KABADIWALA', tag: 'THE STREET KING',
    line: 'Knows every street, every building, every guard. Cash in hand, trust earned over decades, a scale older than the phone he collects.',
    get: 'VIKAAS routes doorstep requests to him, shows him live rates, and receipts every kilo — he stops waiting at gates and starts getting called to them.',
    stamp: 'THE NETWORK', cls: 'st-green',
  },
  {
    no: '02', title: 'THE COLLECTION HUB', tag: 'THE TONNAGE MOVER',
    line: 'The middle of the chain: trucks, sorting yards, the muscle that moves 500-kg minimums and full loads.',
    get: 'The app consolidates a street of tiny drawers into his full loads — the small lots he never saw become his margin.',
    stamp: 'THE VOLUME', cls: 'st-violet',
  },
  {
    no: '03', title: 'THE AUTHORISED RECYCLER', tag: 'THE LICENSED END',
    line: 'HSPCB-licensed, audited, accountable. 15 of them in Gurugram alone — waiting at 500 kg while homes hold 1.4.',
    get: 'VIKAAS feeds him documented, receipted inflow — and the chain of custody proof that keeps his licence clean.',
    stamp: '15 · SOURCED', cls: 'st-gold',
  },
];

const WHY = [
  ['01', 'WORK COMES TO YOU', 'No more waiting at the gate for bulk. The app routes requests to your area, your slot, your rate — the doorstep comes to you.'],
  ['02', 'CASH + TRUST', 'Weigh-and-pay at the door, receipt auto-generated. Households see your rate before booking — no haggling, no distrust, no "kabhi kaam aayega".'],
  ['03', 'PRICE TRANSPARENCY', 'Live rate cards: ₹8/kg and everyone knows it. You set the rate; the app brings the volume that makes it worth your trip.'],
  ['04', 'LEGITIMACY', 'Registered centres get listed publicly on the roster — HSPCB-verified recyclers get the badge, the traffic, and the documented chain.'],
];

export default function Kabadi() {
  return (
    <main className="kb-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="kb-hero">
        <p className="eyebrow cmd shiny">the network room · the moat</p>
        <h1 className="anton kb-title">THE KABADI<br /><span>UNIVERSE</span></h1>
        <p className="kb-sub">Before the app, there was the network: the kabadiwala who knows every street, the hub that moves the tonnes, the licensed recycler at the end of the chain. They already exist. <b>What's missing is the doorstep</b> — and the app that pays them for reaching it.</p>
        <div className="kb-stats">
          <div className="kb-stat"><b className="anton">15</b><span>HSPCB recyclers</span><span className="stamp st-green">SOURCED</span></div>
          <div className="kb-stat"><b className="anton">8</b><span>centres on the roster</span><span className="stamp st-green">REGISTERED</span></div>
          <div className="kb-stat"><b className="anton">1.4 KG</b><span>the pilot lot</span><span className="stamp st-gold">WEIGHED</span></div>
          <div className="kb-stat"><b className="anton">₹40</b><span>paid at the door</span><span className="stamp st-gold">RECEIPT #0001</span></div>
        </div>
      </section>

      <section className="kb-cast-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the cast · three links, one chain</p>
          <h2 className="section-title">THE NETWORK<br /><span>THAT ALREADY EXISTS</span></h2>
          <div className="kb-cast">
            {CAST.map((c, i) => (
              <motion.article key={c.no} className="kb-card"
                initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.25 }} transition={{ duration: 0.7, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}>
                <span className="kb-cast-no anton">{c.no}</span>
                <span className="kb-tag cmd">{c.tag}</span>
                <h3 className="anton">{c.title}</h3>
                <p className="kb-line">{c.line}</p>
                <div className="kb-get">
                  <span className="cmd">WITH VIKAAS</span>
                  <p>{c.get}</p>
                </div>
                <span className={`stamp ${c.cls}`}>{c.stamp}</span>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      <section className="kb-econ-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the economics · before / after</p>
          <h2 className="section-title">WAITING AT 500 KG.<br /><span>OR ROUTED AT ₹8/KG.</span></h2>
          <div className="kb-econ">
            <motion.div className="kb-econ-panel before"
              initial={{ opacity: 0, x: -36 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}>
              <span className="cmd">BEFORE</span>
              <h3 className="anton">THE WAIT</h3>
              <ul>
                <li>Recyclers demand a 500-kg minimum lot</li>
                <li>A home holds 1.4 kg — it never calls</li>
                <li>The kabadiwala waits at gates for bulk</li>
                <li>Drawers fill for years: 3.2M tonnes/yr, 22% recycled</li>
              </ul>
              <span className="stamp st-red">THE GAP</span>
            </motion.div>
            <motion.div className="kb-econ-panel after"
              initial={{ opacity: 0, x: 36 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.7, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}>
              <span className="cmd">AFTER · VIKAAS</span>
              <h3 className="anton">THE ROUTE</h3>
              <ul>
                <li>Every drawer books a doorstep pickup</li>
                <li>The centre comes, weighs, pays cash — ₹8/kg live</li>
                <li>Small lots consolidate into full loads for hubs</li>
                <li>Receipted chain: door → partner → HSPCB recycler</li>
              </ul>
              <span className="stamp st-green">ESTIMATE · MODEL</span>
            </motion.div>
          </div>
          <p className="kb-note">The before is real — we lived it: 1.4 kg, 500-kg minimum, 0 doorsteps. The after is the model the app runs on. <em>Every number in it gets receipted, live, door by door.</em></p>
        </div>
      </section>

      <section className="kb-why-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">why they join · the recruitment pitch</p>
          <h2 className="section-title">THE DEAL<br /><span>WE OFFER THE NETWORK</span></h2>
          <div className="kb-why">
            {WHY.map(([n, t, d], i) => (
              <motion.div key={n} className="kb-why-card" data-cursor={t}
                initial={{ opacity: 0, y: 34 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: i * 0.08 }}>
                <span className="kb-why-no anton">{n}</span>
                <h3 className="anton">{t}</h3>
                <p>{d}</p>
              </motion.div>
            ))}
          </div>
          <div className="kb-moat">
            <p className="kb-moat-q">Anybody can draw an app.<br /><span>We recruited the network.</span></p>
            <div className="kb-ctas">
              <Link to="/buddy" data-cursor="REBEE" data-mag className="go mag glow-hover">ASK REBEE →</Link>
              <Link to="/" data-cursor="THE GATE" data-mag className="go ghost mag glow-hover">BACK TO THE GATE</Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="kb-foot">
        <div className="foot-big anton grad-text">15 RECYCLERS.<br />0 DOORSTEPS.<span style={{ color: 'var(--acid)' }}> UNTIL NOW.</span></div>
        <div className="kb-footmeta cmd">THE KABADI UNIVERSE · VIKAAS · NO DRAWER LEFT BEHIND</div>
      </footer>
    </main>
  );
}
