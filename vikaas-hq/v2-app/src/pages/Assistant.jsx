import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { askReBee, REBEE_INTRO } from '../lib/rebee.js';
import './assistant.css';

const QUICK = [
  '💸 What\'s my drawer worth?',
  '📅 Book a pickup',
  '🔗 Where does it actually go?',
  '🎯 Mission 2 — what do I do?',
  '🏆 Forbes 30 under 30?',
  '🇨🇭 Geneva trip?',
];

export default function Assistant() {
  const [msgs, setMsgs] = useState([{ who: 'bee', text: REBEE_INTRO }]);
  const [typing, setTyping] = useState(false);
  const [input, setInput] = useState('');
  const [online, setOnline] = useState(null); // null = unknown, true = LLM, false = script
  const boxRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const b = boxRef.current;
    if (b) b.scrollTop = b.scrollHeight;
  }, [msgs, typing]);

  const send = async (textRaw) => {
    const text = (textRaw || input).trim();
    if (!text || typing) return;
    setInput('');
    setMsgs((m) => [...m, { who: 'you', text }]);
    setTyping(true);
    const history = msgs
      .filter((m) => m.who === 'you' || m.who === 'bee')
      .map((m) => ({ role: m.who === 'you' ? 'user' : 'assistant', content: m.text }));
    const res = await askReBee([...history, { role: 'user', content: text }]);
    setTyping(false);
    setOnline(res.offline ? false : true);
    setMsgs((m) => [...m, { who: 'bee', text: res.reply }]);
  };

  const onKey = (e) => { if (e.key === 'Enter') send(); };

  return (
    <main className="as-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="as-hero">
        <p className="eyebrow cmd shiny">the ai inside · the buddy · real llm</p>
        <h1 className="anton as-title">MEET<br /><span>REBEE</span></h1>
        <p className="as-sub">1M1B's AI buddy, born from a Gurugram drawer — now the brain of the app, powered by a real language model. <b>He's portfolio-aware:</b> ask him about the 1.4-kg drawer, the 15 recyclers, Mission 2, Flash 3, or what your junk is worth.</p>
      </section>

      <section className="as-chat-sec">
        <div className="wrap">
          <div className="as-chat" data-cursor="REBEE">
            <div className="as-chat-head">
              <span className="as-bee">🐝</span>
              <div>
                <b>ReBee · री-बी</b>
                <span className="cmd">PORTFOLIO-AWARE · {online === null ? 'AI BRAIN' : online ? 'AI ONLINE' : 'SCRIPT MODE'}</span>
              </div>
              <i className={`as-live ${online === false ? 'off' : ''}`} />
            </div>
            <div className="as-box" ref={boxRef}>
              <AnimatePresence initial={false}>
                {msgs.map((m, i) => (
                  <motion.div key={i} className={`as-msg ${m.who}`}
                    initial={{ opacity: 0, y: 14, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} transition={{ duration: 0.3 }}>
                    <p>{m.text}</p>
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
            <div className="as-quick">
              {QUICK.map((c) => (
                <button key={c} className="as-chip" onClick={() => send(c)} disabled={typing}>{c}</button>
              ))}
            </div>
            <div className="as-inputrow">
              <input
                ref={inputRef}
                className="as-input"
                placeholder="Ask ReBee anything about VIKAAS…"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={onKey}
                maxLength={300}
              />
              <button className="as-send" onClick={() => send()} disabled={typing || !input.trim()}>SEND →</button>
            </div>
          </div>
          <p className="as-legal cmd">REBEE · BRAIN: {online === false ? 'SCRIPT MODE (AI unreachable — check internet)' : 'OPENROUTER LLM · portfolio-aware'}</p>
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
          <p className="as-note">ReBee won 1M1B's Flash Challenge — the AI buddy built from the problem he solves. Now he runs the app, powered by a real LLM that knows the whole VIKAAS story. <em>That's the AI feature scrap apps don't have.</em></p>
          <div className="as-ctas">
            <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">BOOK A PICKUP →</Link>
            <Link to="/app" data-cursor="THE APP" data-mag className="go ghost mag glow-hover">BACK TO THE APP</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
