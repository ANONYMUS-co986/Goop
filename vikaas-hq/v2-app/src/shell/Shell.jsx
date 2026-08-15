import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import gsap from 'gsap';

const ROOMS = [
  ['00', 'THE BOOT', '/boot', 'live', 'REPLAY →'],
  ['01', 'THE GATE', '/', 'live', 'ENTER →'],
  ['02', 'THE DRAWER', '/drawer', 'live', 'ENTER →'],
  ['03', 'THE PROOF', null, 'locked', 'PHASE 4'],
  ['04', 'THE ARSENAL', null, 'locked', 'PHASE 6'],
  ['05', 'THE BUDDY', null, 'locked', 'PHASE 7'],
  ['06', 'THE SYSTEM', null, 'locked', 'PHASE 8'],
  ['★', 'GENEVA', null, 'locked', 'THE GOAL'],
  ['§', 'THE TYPE', '/type', 'live', 'STYLEGUIDE →'],
];

export default function Shell({ pathname }) {
  const cursorRef = useRef(null);
  const [prog, setProg] = useState(0);
  const hideNav = pathname === '/boot';

  // scroll progress bar
  useEffect(() => {
    if (hideNav) return;
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - innerHeight;
      setProg(max > 0 ? Math.min(1, h.scrollTop / max) : 0);
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => removeEventListener('scroll', onScroll);
  }, [hideNav]);

  // cursor v2 (blob + ring + splash)
  useEffect(() => {
    const touch = matchMedia('(hover: none)').matches;
    if (touch || hideNav) return;
    const blob = document.createElement('div'); blob.className = 'cur-blob';
    const ring = document.createElement('div'); ring.className = 'cur-ring';
    document.body.append(blob, ring);
    document.documentElement.classList.add('has-cur');
    let mx = innerWidth / 2, my = innerHeight / 2, bx = mx, by = my, rx = mx, ry = my, hover = false;
    const mv = (e) => { mx = e.clientX; my = e.clientY; };
    const ov = (e) => { hover = !!e.target.closest('a,button,[data-cursor],.room-card,.spot'); };
    addEventListener('mousemove', mv, { passive: true });
    document.addEventListener('mouseover', ov);
    const loop = () => {
      bx += (mx - bx) * 0.16; by += (my - by) * 0.16;
      rx += (mx - rx) * 0.07; ry += (my - ry) * 0.07;
      const s = hover ? 2.1 : 1;
      blob.style.transform = `translate(${bx}px,${by}px) translate(-50%,-50%)`;
      blob.style.width = (10 * s) + 'px'; blob.style.height = (10 * s) + 'px';
      ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
      ring.style.width = (hover ? 62 : 36) + 'px'; ring.style.height = (hover ? 62 : 36) + 'px';
      ring.style.borderColor = hover ? 'rgba(185,255,63,.9)' : 'rgba(185,255,63,.45)';
      requestAnimationFrame(loop);
    };
    loop();
    return () => { removeEventListener('mousemove', mv); document.removeEventListener('mouseover', ov); blob.remove(); ring.remove(); document.documentElement.classList.remove('has-cur'); };
  }, [hideNav]);

  // HUD clock
  useEffect(() => {
    const el = document.getElementById('hudTime');
    if (!el) return;
    const p = (n) => String(n).padStart(2, '0');
    const t = () => { const d = new Date(); el.textContent = `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())} IST`; };
    t(); const iv = setInterval(t, 1000);
    return () => clearInterval(iv);
  }, []);

  // overlay open/close + stagger
  const openNav = () => {
    const ov = document.getElementById('gnOverlay');
    if (!ov) return;
    ov.classList.add('on'); document.body.classList.add('navlock');
    ov.querySelectorAll('.gn-item').forEach((el, i) => {
      el.style.transition = 'none'; el.style.opacity = '0'; el.style.transform = 'translateY(24px)';
      setTimeout(() => {
        el.style.transition = 'opacity .5s,transform .5s cubic-bezier(.2,.9,.2,1) ' + (70 * i) + 'ms';
        el.style.opacity = '1'; el.style.transform = 'none';
      }, 40);
    });
  };
  const closeNav = () => {
    const ov = document.getElementById('gnOverlay');
    if (ov) { ov.classList.remove('on'); document.body.classList.remove('navlock'); }
  };

  if (hideNav) return <div className="vig" />;

  const progressBar = (
    <div className="scrollprog" aria-hidden="true"><i style={{ width: (prog * 100) + '%' }}></i></div>
  );

  const here = pathname === '/' ? '/boot' : pathname === '/boot' ? '/boot' : pathname;

  return (
    <>
      <nav className="gnav">
        <Link className="gnav-brand anton" to="/" data-cursor="HOME">VIKAAS<span>.</span></Link>
        <span className="gnav-tag cmd">{ROOMS.find(r => r[2] === pathname) ? ROOMS.find(r => r[2] === pathname)[1] : 'THE UNIVERSE'}</span>
        <button className="gnav-menu cmd" onClick={openNav}>MENU <i></i><i></i><i></i></button>
      </nav>

      <div className="gnov" id="gnOverlay">
        <button className="gnov-x cmd" onClick={closeNav}>✕ CLOSE</button>
        <div className="gnov-hd cmd">the universe — pick a room</div>
        <div className="gnov-list">
          {ROOMS.map(([no, tt, to, st, label]) => (
            to
              ? <Link key={no} className="gn-item" to={to} onClick={closeNav}><span className="no">{no}</span><span className="tt anton">{tt}</span><span className={`st ${pathname === to ? 'now' : 'live'}`}>{pathname === to ? 'YOU ARE HERE' : label}</span></Link>
              : <div key={no} className="gn-item locked"><span className="no">{no}</span><span className="tt anton">{tt}</span><span className="st">{label}</span></div>
          ))}
        </div>
        <div className="gnov-ft cmd">receipts with taste · @qwerty_aarav</div>
      </div>

      <div className="hud hud-tl cmd">@qwerty_aarav <b>·</b> receipts with taste</div>
      <div className="hud hud-tr cmd" id="hudTime">--:--:-- <b>IST</b></div>
      <div className="hud hud-bl cmd">#EWasteOff <b>·</b> #ChangemakersWorldCup</div>
      <div className="hud hud-br cmd">GURUGRAM <b>·</b> 28.45°N 77.02°E</div>
      {progressBar}
      <div className="vig" />
    </>
  );
}
