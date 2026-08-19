import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import './apphome.css';

const STEPS = [
  { id: 'book', tag: '01 · BOOK', icon: '📱', title: 'Open the app', line: 'List your dead devices — phone, charger, cable, speaker.' },
  { id: 'weigh', tag: '02 · WEIGH', icon: '⚖️', title: 'Weigh it', line: '1.4 kg? Enter it. Live ₹ estimate appears — ≈ ₹40.' },
  { id: 'value', tag: '03 · VALUE', icon: '💰', title: 'Get the value', line: '₹40 at the gate. Cash. Real. Stamped.' },
  { id: 'receipt', tag: '04 · RECEIPT', icon: '🧾', title: 'Receipt printed', line: 'Weighed. Not guessed. No returns on evidence.' },
];

const IMPACT = [
  ['1.4 KG', 'diverted · real'], ['₹40', 'paid at the gate'], ['15', 'collection centres'], ['0', 'doorsteps — until now'],
];

export default function AppHome() {
  const [step, setStep] = useState(0);
  const [auto, setAuto] = useState(true);
  const [booked, setBooked] = useState(false);

  useEffect(() => {
    if (!auto) return;
    const t = setInterval(() => setStep((s) => (s + 1) % STEPS.length), 2600);
    return () => clearInterval(t);
  }, [auto]);

  return (
    <main className="app-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      {/* HERO */}
      <section className="app-hero">
        <p className="eyebrow cmd shiny">the product · swiggy for e-waste</p>
        <h1 className="anton app-title">BOOK A PICKUP.<br /><span>WEIGH. EARN. RECYCLE.</span></h1>
        <p className="app-sub">VIKAAS is the app that connects your drawer to a collection centre — doorstep pickup, cash at the gate, a receipt that proves it went to a verified recycler. This is the app. Try it.</p>

        <div className="app-stage">
          {/* PHONE MOCK */}
          <div className="phone" data-cursor="THE APP">
            <div className="phone-notch" />
            <div className="phone-screen">
              <div className="ps-top cmd"><span>VIKAAS</span><span>• • •</span></div>
              <div className="ps-body">
                <AnimatePresence mode="wait">
                  <motion.div key={step} className="ps-step"
                    initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.4 }}>
                    <div className="ps-icon">{STEPS[step].icon}</div>
                    <div className="ps-tag cmd">{STEPS[step].tag}</div>
                    <h3 className="anton">{STEPS[step].title}</h3>
                    <p>{STEPS[step].line}</p>
                    <div className="ps-fake">
                      {step === 0 && <div className="fake-row"><span>📱 3 phones</span><b>+</b></div>}
                      {step === 1 && <div className="fake-row"><span>weight</span><b>1.4 KG</b></div>}
                      {step === 2 && <div className="fake-row gold"><span>value</span><b>₹40</b></div>}
                      {step === 3 && <div className="fake-receipt">RECEIPT #0001<br />1.4 KG · ₹40 · WEIGHED</div>}
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>
              <div className="ps-dots">
                {STEPS.map((_, i) => <i key={i} className={i === step ? 'on' : ''} />)}
              </div>
              <div className="ps-cta" onClick={() => { setBooked(true); setTimeout(() => setBooked(false), 2000); }}>
                {booked ? '✓ PICKUP BOOKED — CENTRE ASSIGNED' : 'BOOK THIS PICKUP →'}
              </div>
            </div>
          </div>

          {/* SIDE */}
          <div className="app-side">
            <div className="impact-strip">
              {IMPACT.map(([n, l]) => (
                <div key={n} className="impact-cell"><b className="anton">{n}</b><span>{l}</span></div>
              ))}
            </div>
            <p className="app-note">Every number above is real — weighed on a kitchen scale, paid at the gate, listed by the HSPCB. The app makes this flow one tap away.</p>
            <div className="app-ctas">
              <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">START A PICKUP →</Link>
              <Link to="/app/centres" data-cursor="CENTRES" data-mag className="go ghost mag glow-hover">SEE THE CENTRES</Link>
            </div>
            <div className="app-roomnav cmd">
              <Link to="/app/map" data-cursor="MAP" className="glow-hover">NETWORK MAP</Link>
              <Link to="/app/receipts" data-cursor="RECEIPTS" className="glow-hover">RECEIPTS</Link>
              <Link to="/app/assistant" data-cursor="REBEE" className="glow-hover">REBEE AI</Link>
              <Link to="/app/login" data-cursor="LOGIN" className="glow-hover">LOGIN</Link>
              <Link to="/app/admin" data-cursor="OPS" className="glow-hover">CENTRE OPS</Link>
            </div>
            <button className="auto-toggle cmd" onClick={() => setAuto(!auto)}>{auto ? '⏸ PAUSE DEMO' : '▶ PLAY DEMO'}</button>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS (the 4 taps, static mirror) */}
      <section className="app-how">
        <div className="wrap">
          <p className="eyebrow cmd shiny">how it works</p>
          <h2 className="section-title">FOUR TAPS.<br /><span>ONE CLEAN DRAWER.</span></h2>
          <div className="how-grid">
            {STEPS.map((s, i) => (
              <div key={s.id} className="how-card" data-cursor={s.title}>
                <span className="how-no anton">{i + 1}</span>
                <span className="how-icon">{s.icon}</span>
                <h3 className="anton">{s.title}</h3>
                <p>{s.line}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* THE MOAT */}
      <section className="app-moat">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the moat · we recruit the network</p>
          <h2 className="section-title">COLLECTION<br /><span>CENTRES, RECRUITED</span></h2>
          <p className="app-sub">The app isn't just for households — kabadiwalas and authorised recyclers register, set their pricing and area, and the app routes pickups to them. 15 HSPCB recyclers exist in Gurugram. We're giving them the doorstep.</p>
          <div className="moat-ctas">
            <Link to="/app/centres" data-cursor="CENTRES" data-mag className="go mag glow-hover">REGISTER YOUR CENTRE →</Link>
            <Link to="/app/map" data-cursor="MAP" data-mag className="go ghost mag glow-hover">SEE THE NETWORK MAP</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
