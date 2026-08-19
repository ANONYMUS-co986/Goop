import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './book.css';

const DEVICES = [
  { id: 'phone', icon: '📱', name: 'Phone', per: 12 },
  { id: 'charger', icon: '🔌', name: 'Charger', per: 2 },
  { id: 'cable', icon: '🔗', name: 'Cable', per: 1 },
  { id: 'battery', icon: '🔋', name: 'Battery', per: 4 },
  { id: 'speaker', icon: '🔊', name: 'Speaker', per: 10 },
  { id: 'laptop', icon: '💻', name: 'Laptop', per: 60 },
  { id: 'other', icon: '📦', name: 'Other', per: 8 },
];

const SLOTS = ['Today 6–8 PM', 'Tomorrow 10 AM–12 PM', 'Tomorrow 4–6 PM', 'Sunday 11 AM–1 PM'];

export default function Book() {
  const [step, setStep] = useState(0);
  const [items, setItems] = useState({});
  const [kg, setKg] = useState('');
  const [manual, setManual] = useState(true);
  const [addr, setAddr] = useState('');
  const [slot, setSlot] = useState('');
  const [done, setDone] = useState(false);

  const estValue = (kg ? parseFloat(kg) : 0) * 8; // ₹8/kg mixed
  const inc = (id) => setItems((s) => ({ ...s, [id]: (s[id] || 0) + 1 }));
  const dec = (id) => setItems((s) => ({ ...s, [id]: Math.max(0, (s[id] || 0) - 1) }));
  const totalItems = Object.values(items).reduce((a, b) => a + b, 0);
  const canNext = step === 0 ? totalItems > 0 : step === 1 ? kg !== '' : step === 2 ? addr.trim() && slot : true;

  const next = () => { console.log('NEXT clicked, step=', step, 'canNext=', canNext); if (canNext) { if (step === 3) setDone(true); else setStep((s) => { console.log('setStep->', s + 1); return s + 1; }); } };
  const back = () => setStep((s) => Math.max(0, s - 1));

  return (
    <main className="book-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div className="wrap">
        <p className="eyebrow cmd shiny">the app · book a pickup</p>
        <h1 className="section-title book-title">BOOK A<br /><span>PICKUP</span></h1>

        {/* progress rail */}
        <div className="bk-progress">
          {['ITEMS', 'WEIGHT', 'SLOT', 'CONFIRM'].map((l, i) => (
            <div key={l} className={`bk-prog ${i === step ? 'on' : ''} ${i < step ? 'done' : ''}`}>
              <span className="bk-prog-dot" /><span className="cmd">{l}</span>
            </div>
          ))}
        </div>

        <div className="bk-stage">
          {!done ? (
              <motion.div key={step} className="bk-pane"
                initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.35 }}>

                {step === 0 && (
                  <>
                    <h2 className="anton bk-h2">WHAT'S IN YOUR DRAWER?</h2>
                    <div className="dev-grid">
                      {DEVICES.map((d) => (
                        <div key={d.id} className={`dev-card ${items[d.id] ? 'sel' : ''}`}>
                          <span className="dev-icon">{d.icon}</span>
                          <span className="dev-name">{d.name}</span>
                          <span className="dev-per">≈₹{d.per}/item</span>
                          <div className="dev-count">
                            <button onClick={() => dec(d.id)}>−</button>
                            <b>{items[d.id] || 0}</b>
                            <button onClick={() => inc(d.id)}>+</button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </>
                )}

                {step === 1 && (
                  <>
                    <h2 className="anton bk-h2">WEIGH IT — OR ESTIMATE</h2>
                    <div className="weight-row">
                      <button className={`wmode ${manual ? 'on' : ''}`} onClick={() => setManual(true)}>ENTER KG</button>
                      <button className={`wmode ${!manual ? 'on' : ''}`} onClick={() => setManual(false)}>AUTO-ESTIMATE</button>
                    </div>
                    {manual ? (
                      <input className="kg-input" type="number" placeholder="e.g. 1.4" value={kg} onChange={(e) => setKg(e.target.value)} />
                    ) : (
                      <div className="auto-est">Based on your {totalItems} items: <b className="anton">≈ {Math.max(0.5, (totalItems * 0.3)).toFixed(1)} KG</b>
                        <button className="use-auto" onClick={() => setKg(Math.max(0.5, (totalItems * 0.3)).toFixed(1))}>USE THIS</button>
                      </div>
                    )}
                    {kg !== '' && (
                      <div className="value-live">
                        <span className="cmd">LIVE VALUE</span>
                        <b className="anton">₹{estValue.toFixed(0)}</b>
                        <span className="stamp st-green">ESTIMATE</span>
                      </div>
                    )}
                  </>
                )}

                {step === 2 && (
                  <>
                    <h2 className="anton bk-h2">WHERE + WHEN</h2>
                    <input className="addr-input" placeholder="Your address (Gurugram)" value={addr} onChange={(e) => setAddr(e.target.value)} />
                    <div className="slot-grid">
                      {SLOTS.map((s) => (
                        <button key={s} className={`slot ${slot === s ? 'on' : ''}`} onClick={() => setSlot(s)}>{s}</button>
                      ))}
                    </div>
                  </>
                )}

                {step === 3 && (
                  <>
                    <h2 className="anton bk-h2">CONFIRM</h2>
                    <div className="summary">
                      <div className="sum-row"><span>ITEMS</span><b>{totalItems}</b></div>
                      <div className="sum-row"><span>WEIGHT</span><b>{kg} KG</b></div>
                      <div className="sum-row gold"><span>EST. VALUE</span><b>₹{estValue.toFixed(0)}</b></div>
                      <div className="sum-row"><span>SLOT</span><b>{slot}</b></div>
                      <div className="sum-row"><span>ADDRESS</span><b>{addr}</b></div>
                    </div>
                    <p className="sum-note">A collection centre near you will be assigned on confirm. Cash at the gate. Receipt generated.</p>
                  </>
                )}

                <div className="bk-nav">
                  {step > 0 && <button className="bk-back" onClick={back}>← BACK</button>}
                  <button className={`bk-next ${canNext ? '' : 'dim'}`} onClick={next}>{step === 3 ? 'CONFIRM PICKUP →' : 'NEXT →'}</button>
                </div>
              </motion.div>
            ) : (
              <motion.div key="done" className="bk-done"
                initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }}>
                <div className="done-check">✓</div>
                <h2 className="anton">PICKUP BOOKED</h2>
                <p>Centre assigned · {slot}</p>
                <div className="done-receipt">
                  <span className="cmd">RECEIPT #0002</span>
                  <b className="anton">{kg} KG · ₹{estValue.toFixed(0)}</b>
                  <span className="stamp st-green">WEIGHED</span>
                </div>
                <p className="sum-note">This is the VIKAAS flow — the same one we did by hand: 1.4 kg, ₹40, receipt kept.</p>
                <div className="bk-nav">
                  <Link to="/app" data-cursor="THE APP" className="bk-next">BACK TO THE APP →</Link>
                </div>
              </motion.div>
            )}
        </div>
        <p className="bk-foot cmd">VIKAAS · THE SAME FLOW WE RAN BY HAND — 1.4 KG · ₹40 · RECEIPTED · <Link to="/app/receipts" className="glow-hover">SEE THE RECEIPTS →</Link></p>
      </div>
    </main>
  );
}
