import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './op.css';

const PICKUPS = [
  { no: '#0001', status: 'DONE', kg: '1.4 KG', value: '₹40', date: 'THE PILOT · HAND-RUN', stamp: 'st-green', tag: 'WEIGHED' },
  { no: '#0002', status: 'BOOKED', kg: '2.3 KG', value: '₹18 est', date: 'TOMORROW · 4–6 PM', stamp: 'st-violet', tag: 'ESTIMATE' },
  { no: '#0003', status: 'YOUR DRAWER', kg: '? KG', value: '?', date: 'BOOK IT →', stamp: 'st-red', tag: 'THE GAP' },
];

const STATS = [
  ['1', 'pickup completed'], ['1.4 KG', 'diverted — real'], ['₹40', 'earned at the door'], ['1', 'drawer left behind: 0'],
];

export default function Dashboard() {
  return (
    <main className="op-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="op-hero">
        <p className="eyebrow cmd shiny">the app · your dashboard</p>
        <h1 className="anton op-title">YOUR E-WASTE.<br /><span>IN RECEIPTS.</span></h1>
        <p className="op-sub">Every pickup, every weigh, every rupee — one ledger. This is the household side of the app: what you booked, what was weighed, what the receipt says.</p>
        <div className="op-stats">
          {STATS.map(([n, l]) => (
            <div key={l} className="op-stat"><b className="anton">{n}</b><span>{l}</span></div>
          ))}
        </div>
      </section>

      <section className="op-list-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">pickup history</p>
          <h2 className="section-title">THE LEDGER<br /><span>OF YOUR DRAWER</span></h2>
          <div className="op-ledger">
            {PICKUPS.map((p, i) => (
              <motion.div key={p.no} className="op-row"
                initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.55, delay: i * 0.08 }}>
                <span className="op-no cmd">{p.no}</span>
                <div className="op-row-main">
                  <b className="anton">{p.kg}</b>
                  <span className="cmd">{p.date}</span>
                </div>
                <div className="op-row-val">
                  <b className="anton">{p.value}</b>
                  <span className={`stamp ${p.stamp}`}>{p.tag}</span>
                </div>
                <span className={`op-status ${p.status === 'DONE' ? 'ok' : p.status === 'BOOKED' ? 'soon' : 'gap'}`}>{p.status}</span>
              </motion.div>
            ))}
          </div>

          <div className="op-upcoming">
            <div>
              <p className="eyebrow cmd shiny">next pickup</p>
              <h3 className="anton">#0002 · TOMORROW 4–6 PM</h3>
              <p className="op-note">Centre assigned: <b>Sharma E-Waste Hub</b> · 1.2 km · ₹8/kg. The centre will weigh in front of you, pay cash, and the receipt will track the lot to the HSPCB recycler.</p>
            </div>
            <div className="op-ctas">
              <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">BOOK ANOTHER →</Link>
              <Link to="/app/receipts" data-cursor="RECEIPTS" data-mag className="go ghost mag glow-hover">SEE THE RECEIPTS</Link>
            </div>
          </div>

          <p className="op-foot cmd">DASHBOARD · HOUSEHOLD VIEW · SAME DATA THE CENTRE AND ADMIN SEE — ONE LEDGER, THREE DOORS</p>
        </div>
      </section>
    </main>
  );
}
