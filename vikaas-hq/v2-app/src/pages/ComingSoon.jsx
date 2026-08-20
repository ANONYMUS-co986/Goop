import { Link, useLocation } from 'react-router-dom';
import SplitReveal from '../lib/fx/SplitReveal.jsx';
import './comingsoon.css';

const ROOM_META = {
  buddy:    { no: '06', name: 'THE BUDDY',    phase: 'PHASE 21 · IN BUILD', teaser: 'ReBee — 1M1B\u2019s AI buddy. SCRAP-SCAN, DOORSTEP DIAL, MATERIAL MATCH. Built from the problem.' },
  system:   { no: '07', name: 'THE SYSTEM',   phase: 'PHASE 22 · IN BUILD', teaser: 'The engine room: the pipelines, the QA gate, the receipts of the receipts.' },
  geneva:   { no: '★',  name: 'GENEVA',       phase: 'THE GOAL · 20 NOV 2026', teaser: 'Top 3 fly to the 1M1B Impact Summit at the United Nations. That\u2019s the plan — publicly.' },
};

export default function ComingSoon() {
  const { pathname } = useLocation();
  const room = pathname.replace('/', '');
  const meta = ROOM_META[room] || { no: '?', name: 'THE VOID', phase: 'UNKNOWN ROOM', teaser: 'Even the drawer doesn\u2019t know this room.' };
  return (
    <main className="cs-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div className="cs-inner">
        <p className="eyebrow cmd shiny">room {meta.no} · the universe</p>
        <SplitReveal text={meta.name} className="anton cs-title" stagger={0.04} />
        <p className="cs-phase cmd">{meta.phase}</p>
        <p className="cs-teaser">{meta.teaser}</p>
        <div className="cs-links">
          <Link to="/drawer" data-cursor="THE DRAWER" data-mag className="go mag glow-hover">← BACK TO THE DRAWER</Link>
          <Link to="/" data-cursor="THE GATE" data-mag className="go mag glow-hover">THE GATE →</Link>
        </div>
      </div>
    </main>
  );
}
