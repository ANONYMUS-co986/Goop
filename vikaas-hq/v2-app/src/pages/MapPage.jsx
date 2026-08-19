import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import './map.css';

/* Stylized SVG network map (no external tiles — self-contained, works offline).
   Gurugram streets as paths + 15 recycler dots + 0 doorstep markers + a route. */
const CENTRES = [
  { x: 120, y: 90, name: 'Exigo · Manesar' }, { x: 210, y: 140, name: 'EcoMetals · S57' },
  { x: 300, y: 110, name: 'Cerebra · HITEC' }, { x: 380, y: 170, name: 'Attero · Noida' },
  { x: 150, y: 200, name: 'E-Parisaraa' }, { x: 260, y: 230, name: 'Kabadi Raju' },
  { x: 340, y: 250, name: 'Kabadi Suresh' }, { x: 190, y: 300, name: 'Kabadi Mohan' },
  { x: 420, y: 90, name: 'Greentek' }, { x: 100, y: 340, name: 'EcoHub' },
  { x: 450, y: 300, name: 'Metro Recycle' }, { x: 320, y: 60, name: 'GreenEarth' },
  { x: 240, y: 320, name: 'RecycleKaro' }, { x: 60, y: 250, name: 'Namo E-waste' },
  { x: 480, y: 210, name: 'Karo Sambhav' },
];
const HOUSEHOLDS = [
  { x: 200, y: 120 }, { x: 230, y: 180 }, { x: 280, y: 150 }, { x: 320, y: 200 },
  { x: 170, y: 260 }, { x: 250, y: 280 }, { x: 350, y: 130 }, { x: 300, y: 300 },
  { x: 130, y: 150 }, { x: 400, y: 240 },
];

export default function MapPage() {
  const [route, setRoute] = useState(null); // index into HOUSEHOLDS
  const [pulse, setPulse] = useState(true);

  return (
    <main className="map-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div className="wrap">
        <p className="eyebrow cmd shiny">the network · live</p>
        <h1 className="section-title map-title">15 RECYCLERS.<br /><span>0 DOORSTEPS. UNTIL NOW.</span></h1>
        <p className="map-sub">Every authorised recycler in Gurugram is on this map. Every household we surveyed is a dot. Click a household to see the route to its nearest centre — the doorstep, closing.</p>

        <div className="map-frame">
          <svg viewBox="0 0 560 400" className="netmap">
            {/* streets */}
            <g className="streets">
              <path d="M0 120 H560" /><path d="M0 240 H560" /><path d="M120 0 V400" />
              <path d="M280 0 V400" /><path d="M440 0 V400" /><path d="M0 80 H560" />
              <path d="M60 0 V400" /><path d="M200 0 V400" /><path d="M360 0 V400" />
            </g>
            {/* centre dots — 15, pulsing */}
            {CENTRES.map((c, i) => (
              <g key={i} className="centre">
                {pulse && <circle className="pulse" cx={c.x} cy={c.y} r="10" />}
                <circle cx={c.x} cy={c.y} r="6" className="centre-dot" />
                <text x={c.x + 10} y={c.y + 4} className="centre-lbl">{c.name}</text>
              </g>
            ))}
            {/* household dots */}
            {HOUSEHOLDS.map((h, i) => (
              <g key={i} className="house">
                <circle cx={h.x} cy={h.y} r="4" className="house-dot" onClick={() => setRoute(i)} data-cursor="ROUTE" />
              </g>
            ))}
            {/* route line */}
            {route !== null && (
              <g className="route">
                <line x1={HOUSEHOLDS[route].x} y1={HOUSEHOLDS[route].y} x2={CENTRES[route % CENTRES.length].x} y2={CENTRES[route % CENTRES.length].y} />
                <circle className="route-pin" cx={HOUSEHOLDS[route].x} cy={HOUSEHOLDS[route].y} r="7" />
              </g>
            )}
            <rect x="0" y="0" width="560" height="400" fill="none" className="map-border" />
          </svg>
          <div className="map-legend">
            <span><i className="lg-centre" />collection centre (15)</span>
            <span><i className="lg-house" />household (10 surveyed)</span>
            <span><i className="lg-route" />pickup route</span>
          </div>
        </div>

        <div className="map-ctas">
          <Link to="/app/book" data-cursor="BOOK" data-mag className="go mag glow-hover">BOOK A PICKUP →</Link>
          <Link to="/app/centres" data-cursor="CENTRES" data-mag className="go ghost mag glow-hover">SEE ALL CENTRES</Link>
        </div>
      </div>
    </main>
  );
}
