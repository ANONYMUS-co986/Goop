import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './receipts.css';

const CHAIN = ['YOUR DRAWER', 'THE DOORSTEP', 'COLLECTION PARTNER', 'HSPCB RECYCLER', 'THE REFINER'];

const FUTURE = [
  ['#0003', 'SECTOR 56 · HOME B'],
  ['#0004', 'SECTOR 45 · FLAT 12'],
  ['#0005', 'GURUGRAM · YOUR DRAWER?'],
  ['#0006', 'THE NEXT 20 …'],
];

const STAMP_LEGEND = [
  ['WEIGHED', 'st-green', 'measured on a real scale'],
  ['SOURCED', 'st-green', 'from the HSPCB list / CWC'],
  ['RECEIPT #N', 'st-gold', 'a document, not a screenshot'],
  ['ESTIMATE', 'st-violet', 'live app estimate, ₹8/kg'],
  ['THE GAP', 'st-red', '15 recyclers · 0 doorsteps'],
  ['DRAMATISED', 'st-mute', 'stylised, never faked'],
];

export default function Receipts() {
  return (
    <main className="rx-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="rx-hero">
        <p className="eyebrow cmd shiny">the proof library · the receipts room</p>
        <h1 className="anton rx-title">RECEIPTS WITH<br /><span>TASTE</span></h1>
        <p className="rx-sub">Every claim in this portfolio carries a stamp. This is where the stamps live — the documents behind the drama. Weighed. Paid. Receipted.</p>
      </section>

      <section className="rx-manifesto">
        <div className="wrap">
          <p className="rx-quote">Some portfolios show screenshots of apps that <em>don't exist</em>.<br /><b>This one shows a receipt from a drawer that did.</b></p>
          <div className="rx-stamps">
            {STAMP_LEGEND.map(([t, c, d]) => (
              <div key={t} className="rx-stamp-cell"><span className={`stamp ${c}`}>{t}</span><p>{d}</p></div>
            ))}
          </div>
        </div>
      </section>

      <section className="rx-list">
        <div className="wrap">

          {/* RECEIPT #0001 — THE REAL PILOT */}
          <motion.article className="rx-card rx-real"
            initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }} transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}>
            <div className="rx-card-head">
              <div>
                <p className="eyebrow cmd shiny">receipt #0001 · the pilot</p>
                <h2 className="anton">THE DRAWER<br />THAT STARTED IT</h2>
              </div>
              <span className="stamp st-green rx-big-stamp">WEIGHED</span>
            </div>
            <div className="rx-paper">
              <div className="rx-paper-top cmd">
                <span>VIKAAS · GURUGRAM</span><span>DATE: 2026 · CASH</span>
              </div>
              <div className="rx-items">
                <div className="rx-item"><span>3 phones (dead, 2014–19)</span><b>0.8 KG</b></div>
                <div className="rx-item"><span>7 chargers (“kabhi kaam aayega”)</span><b>0.3 KG</b></div>
                <div className="rx-item"><span>1 speaker (died 2022)</span><b>0.2 KG</b></div>
                <div className="rx-item"><span>cable bundle + odds</span><b>0.1 KG</b></div>
              </div>
              <div className="rx-total">
                <span>GROSS WEIGHT</span><b className="anton">1.4 KG</b>
              </div>
              <div className="rx-total gold">
                <span>PAID · CASH AT THE DOOR</span><b className="anton">₹40</b>
              </div>
              <div className="rx-paper-foot cmd">weighed on a kitchen scale · photographed · logged · 0 words used</div>
            </div>
            <div className="rx-chain">
              {CHAIN.map((c, i) => (
                <div key={c} className="rx-chain-node">
                  <span className="rx-dot">{i + 1}</span>
                  <b>{c}</b>
                  {i < CHAIN.length - 1 && <i className="rx-arrow">→</i>}
                </div>
              ))}
            </div>
            <p className="rx-note">The chain of custody is the point: the receipt doesn't end at the door. It ends at a verified recycler. <b>That's what the app digitises.</b></p>
          </motion.article>

          {/* RECEIPT #0002 — THE APP (live) */}
          <motion.article className="rx-card"
            initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }} transition={{ duration: 0.7, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}>
            <div className="rx-card-head">
              <div>
                <p className="eyebrow cmd shiny">receipt #0002 · the app</p>
                <h2 className="anton">BOOKED ON THE<br />WIZARD, LIVE</h2>
              </div>
              <span className="stamp st-violet">ESTIMATE</span>
            </div>
            <div className="rx-paper slim">
              <div className="rx-paper-top cmd"><span>VIKAAS APP · PICKUP #0002</span><span>SLOT: TOMORROW</span></div>
              <div className="rx-total"><span>WEIGHT ENTERED</span><b className="anton">2.3 KG</b></div>
              <div className="rx-total gold"><span>LIVE ESTIMATE · ₹8/KG</span><b className="anton">₹18</b></div>
              <div className="rx-paper-foot cmd">generated by the wizard on /app/book — every booking stamps its own receipt</div>
            </div>
            <p className="rx-note">Receipt #0001 was made by hand. Receipt #0002 is made by the app you just used. <Link to="/app/book" className="rx-link glow-hover" data-cursor="BOOK">Book one yourself →</Link></p>
          </motion.article>

          {/* FUTURE RECEIPTS */}
          <motion.section className="rx-future"
            initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3 }} transition={{ duration: 0.7, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}>
            <div className="rx-future-head">
              <div>
                <p className="eyebrow cmd shiny">the next 23 · mission 2 target</p>
                <h2 className="anton">YOUR DRAWER<br />IS #0003</h2>
              </div>
              <span className="stamp st-red">THE GAP</span>
            </div>
            <div className="rx-slot-grid">
              {FUTURE.map(([no, who]) => (
                <div key={no} className="rx-slot" data-cursor="OPEN">
                  <span className="cmd">{no}</span>
                  <b className="anton">{who}</b>
                </div>
              ))}
            </div>
            <p className="rx-note">Mission 2 is <b>25 households</b> — every drawer weighed, every handover receipted, before and after numbers, photographed. The receipts above are the evidence trail we're building, one door at a time.</p>
            <div className="rx-ctas">
              <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">START YOUR PICKUP →</Link>
              <Link to="/app" data-cursor="THE APP" data-mag className="go ghost mag glow-hover">BACK TO THE APP</Link>
            </div>
          </motion.section>

        </div>
      </section>
    </main>
  );
}
