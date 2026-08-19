import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './centres.css';

const CENTRES = [
  { name: 'Exigo Recycling', type: 'recycler', area: 'Manesar · Gurugram', cap: '5,000 kg/mo', rate: '₹8/kg', rating: 4.7, badge: 'CPCB · HSPCB', status: 'accepting' },
  { name: 'EcoMetals Hub', type: 'recycler', area: 'Sector 57 · Gurugram', cap: '3,000 kg/mo', rate: '₹9/kg', rating: 4.9, badge: 'ISO 14001', status: 'accepting' },
  { name: 'Kabadiwala Raju', type: 'kabadiwala', area: 'Sector 45 · Gurugram', cap: '500 kg/mo', rate: '₹10/kg', rating: 4.8, badge: 'DOORSTEP', status: 'accepting' },
  { name: 'Kabadiwala Suresh', type: 'kabadiwala', area: 'Sector 31 · Gurugram', cap: '400 kg/mo', rate: '₹9/kg', rating: 4.6, badge: 'DOORSTEP', status: 'accepting' },
  { name: 'Cerebra Integrated', type: 'recycler', area: 'HITEC City · Hyderabad', cap: '8,000 kg/mo', rate: '₹7/kg', rating: 4.8, badge: 'CPCB', status: 'onboarding' },
  { name: 'Attero Recycling', type: 'recycler', area: 'Noida · NCR', cap: '10,000 kg/mo', rate: '₹8/kg', rating: 4.9, badge: 'CPCB · NASDAQ', status: 'onboarding' },
  { name: 'E-Parisaraa', type: 'recycler', area: 'Peenya · Bengaluru', cap: '6,000 kg/mo', rate: '₹8/kg', rating: 5.0, badge: 'R2v3', status: 'onboarding' },
  { name: 'Kabadiwala Mohan', type: 'kabadiwala', area: 'Sector 22 · Gurugram', cap: '300 kg/mo', rate: '₹11/kg', rating: 4.5, badge: 'DOORSTEP', status: 'pending' },
];

const TYPE_LABEL = { recycler: 'AUTHORISED RECYCLER', kabadiwala: 'KABADIWALA' };

export default function Centres() {
  const [registered, setRegistered] = useState(false);
  const [form, setForm] = useState({ name: '', type: 'kabadiwala', area: '', phone: '' });

  return (
    <main className="centres-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div className="wrap">
        <p className="eyebrow cmd shiny">the moat · we recruit the network</p>
        <h1 className="section-title centres-title">COLLECTION<br /><span>CENTRES</span></h1>
        <p className="centres-sub">15 authorised recyclers exist on the HSPCB list. The kabadiwala network knows every street. The app routes pickups to both — doorstep, weighed, receipted.</p>

        <div className="centres-grid">
          {CENTRES.map((c, i) => (
            <motion.div key={c.name} className={`centre-card ${c.status}`} data-cursor={c.status === 'accepting' ? 'ACCEPTING' : c.status.toUpperCase()}
              initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06, duration: 0.5 }}>
              <span className="centre-type cmd">{TYPE_LABEL[c.type]}</span>
              <span className={`centre-status ${c.status}`}>{c.status === 'accepting' ? '● ACCEPTING PICKUPS' : c.status.toUpperCase()}</span>
              <h3 className="anton">{c.name}</h3>
              <p className="centre-area">{c.area}</p>
              <div className="centre-rows">
                <span>CAPACITY</span><b>{c.cap}</b>
                <span>PRICING</span><b>{c.rate}</b>
                <span>RATING</span><b>★ {c.rating}</b>
              </div>
              <span className="centre-badge">{c.badge}</span>
            </motion.div>
          ))}
        </div>

        {/* REGISTER FORM */}
        <div className="register-box">
          <p className="eyebrow cmd shiny">are you a kabadiwala or a recycler?</p>
          <h2 className="anton register-title">REGISTER YOUR CENTRE</h2>
          {!registered ? (
            <>
              <p className="centres-sub">Join the network. The app sends pickups to your door — you weigh, you pay, you recycle. We handle the households, you handle the metal.</p>
              <div className="reg-form">
                <input placeholder="Centre / shop name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
                <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                  <option value="kabadiwala">Kabadiwala</option>
                  <option value="recycler">Authorised Recycler</option>
                </select>
                <input placeholder="Area (e.g. Sector 45, Gurugram)" value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} />
                <input placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
                <button className="reg-submit" onClick={() => setRegistered(true)}>REGISTER →</button>
              </div>
            </>
          ) : (
            <div className="reg-done">
              <div className="done-check">✓</div>
              <h3 className="anton">REGISTRATION RECEIVED</h3>
              <p>{form.name || 'Your centre'} · {form.area || '—'} — we'll verify and activate you. This is the VIKAAS moat: NIRMAN has a concept, we have a network.</p>
              <Link to="/app" data-cursor="THE APP" className="go mag glow-hover">BACK TO THE APP →</Link>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
