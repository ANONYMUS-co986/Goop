import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import './op.css';

const QUEUE = [
  { no: '#0003', kg: '0.9 KG', items: '2 phones + 4 chargers', addr: 'Sector 56, House 21', slot: 'Today 6–8 PM', val: '₹20' },
  { no: '#0004', kg: '3.1 KG', items: '1 laptop + battery pack', addr: 'Sector 45, Flat 12', slot: 'Today 6–8 PM', val: '₹185' },
  { no: '#0005', kg: '1.8 KG', items: 'speaker + cables + PCB', addr: 'Sector 43, Tower C', slot: 'Tomorrow 10 AM', val: '₹40' },
];

export default function Admin() {
  const [accepted, setAccepted] = useState({});

  const accept = (no) => setAccepted((s) => ({ ...s, [no]: true }));

  return (
    <main className="op-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="op-hero slim">
        <p className="eyebrow cmd shiny">the app · centre ops</p>
        <h1 className="anton op-title">SHARMA E-WASTE HUB<br /><span>OPS BOARD</span></h1>
        <p className="op-sub">The collection centre's side of the app: pickup requests routed to your door, weigh-and-pay at the doorstep, receipt auto-generated. No more 500-kg minimums — every drawer is a customer.</p>
        <div className="op-stats">
          <div className="op-stat"><b className="anton">3</b><span>requests today</span></div>
          <div className="op-stat"><b className="anton">₹8/KG</b><span>your live rate</span></div>
          <div className="op-stat"><b className="anton">4.6★</b><span>rating · 12 pickups</span></div>
          <div className="op-stat"><b className="anton">HSPCB</b><span>authorised · listed</span></div>
        </div>
      </section>

      <section className="op-list-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">pickup queue · routed to you</p>
          <h2 className="section-title">THE REQUESTS<br /><span>KNOCKING</span></h2>

          <div className="op-queue">
            <AnimatePresence initial={false}>
              {QUEUE.map((q, i) => (
                <motion.div key={q.no} className={`op-req ${accepted[q.no] ? 'accepted' : ''}`}
                  initial={{ opacity: 0, y: 26 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: i * 0.09 }}
                  exit={{ opacity: 0, x: 40 }}>
                  <span className="op-no cmd">{q.no}</span>
                  <div className="op-req-main">
                    <b className="anton">{q.kg} · {q.val}</b>
                    <span className="cmd">{q.items}</span>
                    <span className="cmd dim">{q.addr} · {q.slot}</span>
                  </div>
                  {accepted[q.no]
                    ? <span className="op-status ok">ACCEPTED · ROUTED</span>
                    : <button className="op-btn sm" onClick={() => accept(q.no)}>ACCEPT →</button>}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <div className="op-upcoming">
            <div>
              <p className="eyebrow cmd shiny">why this works</p>
              <h3 className="anton">THE DOORSTEP, DIGITISED</h3>
              <p className="op-note">Before VIKAAS: recyclers waited for 500 kg, homes sat on 1.4 kg, and the drawer collected dust for four years. Now the request finds you — you accept, drive 1.2 km, weigh in front of the family, pay cash, and the receipt travels with the lot to the HSPCB recycler. <b>Every accept = one drawer emptied, one receipt generated.</b></p>
            </div>
            <div className="op-ctas">
              <Link to="/app/receipts" data-cursor="RECEIPTS" data-mag className="go mag glow-hover">SEE THE RECEIPTS →</Link>
              <Link to="/app/centres" data-cursor="CENTRES" data-mag className="go ghost mag glow-hover">CENTRE ROSTER</Link>
            </div>
          </div>

          <p className="op-foot cmd">ADMIN VIEW · 15 HSPCB RECYCLERS + RECRUITED KABADIWALAS · ONE NETWORK, ONE LEDGER</p>
        </div>
      </section>
    </main>
  );
}
