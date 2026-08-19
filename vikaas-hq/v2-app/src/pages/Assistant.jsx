import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import './assistant.css';

const SCRIPT = {
  '💸 What\'s my drawer worth?': {
    reply: 'Snap a photo or tell me what\'s inside 📸 A dead phone ≈ ₹25–40, 7 chargers ≈ ₹12, a 2022 speaker ≈ ₹8. Your drawer ≈ ₹40–60 — but only the scale decides. Book a pickup and the centre weighs it in front of you.',
    stamp: ['ESTIMATE', 'st-violet'],
  },
  '📅 Book a pickup': {
    reply: 'Done. 15 collection centres within 10 km of you. Nearest: Sharma E-Waste Hub · 1.2 km · ₹8/kg · 4.6★. Pick a slot on the book page — the app routes your door to them, not the other way round.',
    stamp: ['BOOKED', 'st-green'],
  },
  '🔗 Where does it actually go?': {
    reply: 'Your e-waste travels: drawer → doorstep → collection partner → HSPCB-verified recycler → refiner. Receipt #0001 proved that chain end-to-end — 1.4 kg, ₹40, every hand stamped. No landfill, no backyard burning.',
    stamp: ['CHAIN', 'st-gold'],
  },
  '♻️ What can I recycle?': {
    reply: 'If it has a plug or a battery, it\'s VIKAAS. Phones, chargers, cables, speakers, laptops, batteries, PCBs, CPU fans, that keyboard with the missing key. No drawer left behind.',
    stamp: ['NO DRAWER LEFT BEHIND', 'st-red'],
  },
};

const CHIP_ORDER = Object.keys(SCRIPT);

export default function Assistant() {
  const [msgs, setMsgs] = useState([
    { who: 'bee', text: 'Hi! I\'m ReBee — the AI inside VIKAAS 🐝 Tell me what\'s in your drawer and I\'ll tell you what it\'s worth, where it goes, and when it gets picked up.' },
  ]);
  const [typing, setTyping] = useState(false);
  const [sent, setSent] = useState({});
  const boxRef = useRef(null);

  useEffect(() => {
    const b = boxRef.current;
    if (b) b.scrollTop = b.scrollHeight;
  }, [msgs, typing]);

  const ask = (chip) => {
    if (sent[chip] || typing) return;
    setSent((s) => ({ ...s, [chip]: true }));
    setMsgs((m) => [...m, { who: 'you', text: chip }]);
    setTyping(true);
    setTimeout(() => {
      const a = SCRIPT[chip];
      setMsgs((m) => [...m, { who: 'bee', text: a.reply, stamp: a.stamp }]);
      setTyping(false);
    }, 900);
  };

  return (
    <main className="as-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="as-hero">
        <p className="eyebrow cmd shiny">the ai inside · the buddy</p>
        <h1 className="anton as-title">MEET<br /><span>REBEE</span></h1>
        <p className="as-sub">1M1B's AI buddy, born from a Gurugram drawer — now the brain of the app. Capacitor body, phone-glass wings, charger-LED eyes, weighing-scale chest. Ask him what your junk is worth.</p>
      </section>

      <section className="as-chat-sec">
        <div className="wrap">
          <div className="as-chat" data-cursor="REBEE">
            <div className="as-chat-head">
              <span className="as-bee">🐝</span>
              <div>
                <b>ReBee · री-बी</b>
                <span className="cmd">ONLINE · SCRAP-SCAN READY</span>
              </div>
              <i className="as-live" />
            </div>
            <div className="as-box" ref={boxRef}>
              <AnimatePresence initial={false}>
                {msgs.map((m, i) => (
                  <motion.div key={i} className={`as-msg ${m.who}`}
                    initial={{ opacity: 0, y: 14, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} transition={{ duration: 0.3 }}>
                    <p>{m.text}</p>
                    {m.stamp && <span className={`stamp ${m.stamp[1]}`}>{m.stamp[0]}</span>}
                  </motion.div>
                ))}
                {typing && (
                  <motion.div key="typing" className="as-msg bee as-typing"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <i></i><i></i><i></i>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
            <div className="as-chips">
              {CHIP_ORDER.map((c) => (
                <button key={c} className={`as-chip ${sent[c] ? 'done' : ''}`} onClick={() => ask(c)} disabled={!!sent[c] || typing}>
                  {sent[c] ? '✓ ' : ''}{c}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="as-powers">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the three powers</p>
          <h2 className="section-title">WHY THE APP<br /><span>HAS A BRAIN</span></h2>
          <div className="as-power-grid">
            <div className="as-power" data-cursor="SCRAP-SCAN">
              <span className="as-pno anton">01</span>
              <h3 className="anton">SCRAP-SCAN</h3>
              <p>Snap a photo of your pile. ReBee reads the devices, estimates weight and value before the centre even leaves — no guessing, no bargaining in the dark.</p>
              <span className="stamp st-violet">ESTIMATE</span>
            </div>
            <div className="as-power" data-cursor="DOORSTEP DIAL">
              <span className="as-pno anton">02</span>
              <h3 className="anton">DOORSTEP DIAL</h3>
              <p>Finds the nearest collection centre, checks their live rate, books the slot. 15 HSPCB recyclers + recruited kabadiwalas — routed to your door.</p>
              <span className="stamp st-green">BOOKED</span>
            </div>
            <div className="as-power" data-cursor="MATERIAL MATCH">
              <span className="as-pno anton">03</span>
              <h3 className="anton">MATERIAL MATCH</h3>
              <p>Each material goes to the recycler that's licensed for it — batteries to battery recyclers, PCBs to PCB refiners. The chain of custody, automated.</p>
              <span className="stamp st-gold">CHAIN</span>
            </div>
          </div>
          <p className="as-note">ReBee won 1M1B's Flash Challenge — the AI buddy built from the problem he solves. Now he runs the app. <em>That's the AI feature scrap apps don't have.</em></p>
          <div className="as-ctas">
            <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">BOOK A PICKUP →</Link>
            <Link to="/app" data-cursor="THE APP" data-mag className="go ghost mag glow-hover">BACK TO THE APP</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
