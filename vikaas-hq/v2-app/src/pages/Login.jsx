import { useState } from 'react';
import { Link } from 'react-router-dom';
import './op.css';

const ROLES = [
  { id: 'home', icon: '🏠', title: 'HOUSEHOLD', desc: 'Book pickups, see receipts', to: '/app/dashboard' },
  { id: 'centre', icon: '🏭', title: 'COLLECTION CENTRE', desc: 'Accept pickups, weigh, pay', to: '/app/admin' },
  { id: 'admin', icon: '🛰️', title: 'VIKAAS ADMIN', desc: 'The whole network, one screen', to: '/app/admin' },
];

export default function Login() {
  const [phone, setPhone] = useState('');
  const [sent, setSent] = useState(false);
  const [otp, setOtp] = useState('');
  const [logged, setLogged] = useState(false);
  const [role, setRole] = useState('home');

  const sendOtp = () => { if (phone.trim().length >= 10) setSent(true); };
  const verify = () => { if (otp.trim().length >= 4) setLogged(true); };

  return (
    <main className="op-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="op-hero slim">
        <p className="eyebrow cmd shiny">the app · one account, three doors</p>
        <h1 className="anton op-title">ENTER THE<br /><span>VIKAAS</span></h1>
        <p className="op-sub">Household, collection centre or network admin — one login, three doors. (Demo auth: any 10-digit phone, any 4-digit OTP.)</p>

        <div className="op-login">
          {!logged ? (
            <>
              <div className="op-roles">
                {ROLES.map((r) => (
                  <button key={r.id} className={`op-role ${role === r.id ? 'on' : ''}`} onClick={() => setRole(r.id)}>
                    <span className="op-role-icon">{r.icon}</span>
                    <b className="anton">{r.title}</b>
                    <p>{r.desc}</p>
                  </button>
                ))}
              </div>
              <div className="op-phone-row">
                <input className="op-input" placeholder="+91 · 10-digit mobile" maxLength={10} value={phone}
                  onChange={(e) => setPhone(e.target.value.replace(/\D/g, ''))} />
                {!sent
                  ? <button className="op-btn" onClick={sendOtp} disabled={phone.length < 10}>SEND OTP →</button>
                  : <>
                      <input className="op-input otp" placeholder="OTP (any 4 digits)" maxLength={4} value={otp}
                        onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))} />
                      <button className="op-btn" onClick={verify} disabled={otp.length < 4}>VERIFY →</button>
                    </>}
              </div>
            </>
          ) : (
            <div className="op-logged">
              <span className="op-bigcheck">✓</span>
              <h3 className="anton">WELCOME TO THE {ROLES.find((r) => r.id === role).title}</h3>
              <p className="op-note">Demo session · {phone || '+91 98XXXXXXXX'} · role: {role}</p>
              <div className="op-ctas center">
                <Link to={ROLES.find((r) => r.id === role).to} data-cursor="ENTER" data-mag className="go mag glow-hover">ENTER →</Link>
              </div>
            </div>
          )}
        </div>

        <p className="op-foot cmd">AUTH IS THE THIN END — THE REAL DEMO IS WHAT'S BEHIND THE DOOR: DASHBOARD LEDGERS + CENTRE OPS</p>
      </section>
    </main>
  );
}
