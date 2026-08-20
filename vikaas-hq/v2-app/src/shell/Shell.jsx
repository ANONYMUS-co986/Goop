import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { create } from 'zustand';

/* ---------- audio/ui state (zustand) ---------- */
export const useUI = create((set) => ({
  muted: false,
  toggleMute: () => set((s) => ({ muted: !s.muted })),
}));

const ROOMS = [
  ['00', 'THE BOOT', '/boot', 'live', 'REPLAY →'],
  ['01', 'THE GATE', '/', 'live', 'ENTER →'],
  ['02', 'THE DRAWER', '/drawer', 'live', 'ENTER →'],
  ['03', 'THE PROOF', '/proof', 'live', 'ENTER →'],
  ['04', 'THE KABADI UNIVERSE', '/kabadi', 'live', 'ENTER →'],
  ['05', 'THE ARSENAL', '/arsenal', 'live', 'ENTER →'],
  ['06', 'THE BUDDY', '/buddy', 'soon', 'PHASE 21 →'],
  ['07', 'THE SYSTEM', '/system', 'soon', 'PHASE 22 →'],
  ['★', 'GENEVA', '/geneva', 'soon', 'PHASE 23 →'],
  ['§', 'THE TYPE', '/type', 'live', 'STYLEGUIDE →'],
  ['📱', 'THE APP', '/app', 'live', 'TRY IT →'],
];

export default function Shell({ pathname }) {
  const hideNav = pathname === '/boot';
  const { muted, toggleMute } = useUI();
  const [prog, setProg] = useState(0);
  const [navOpen, setNavOpen] = useState(false);
  const [navMounted, setNavMounted] = useState(false);
  const cursorRef = useRef(null);
  const location = useLocation();

  /* ---------- scroll progress ---------- */
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

  /* ---------- cursor v3 (blob + ring + splash) ---------- */
  useEffect(() => {
    const touch = matchMedia('(hover: none)').matches;
    if (touch || hideNav) return;
    const blob = document.createElement('div'); blob.className = 'cur-blob';
    const ring = document.createElement('div'); ring.className = 'cur-ring';
    const cv = document.createElement('canvas'); cv.className = 'cur-splash';
    document.body.append(blob, ring, cv);
    document.documentElement.classList.add('has-cur');
    const ctx = cv.getContext('2d');
    let W, H;
    const fit = () => { W = cv.width = innerWidth; H = cv.height = innerHeight; };
    fit(); addEventListener('resize', fit);
    const parts = [];
    const COLS = ['185,255,63', '46,222,130', '255,211,77', '234,255,244'];
    let mx = innerWidth / 2, my = innerHeight / 2, bx = mx, by = my, rx = mx, ry = my, px = mx, py = my, hover = false;
    const mv = (e) => {
      px = mx; py = my; mx = e.clientX; my = e.clientY;
      const sp = Math.hypot(mx - px, my - py);
      if (sp > 22 && Math.random() < 0.6) {
        parts.push({ x: mx, y: my, vx: (Math.random() - .5) * 2.4, vy: (Math.random() - .5) * 2.4 - .5, life: 1, decay: 0.04 + Math.random() * 0.035, size: 1 + Math.random() * 2.4, c: COLS[Math.floor(Math.random() * 4)] });
      }
    };
    const ov = (e) => {
      const t = e.target.closest('a,button,[data-cursor],.room-card,.spot-card,.gn-item');
      hover = !!t;
    };
    addEventListener('mousemove', mv, { passive: true });
    document.addEventListener('mouseover', ov);
    const loop = () => {
      bx += (mx - bx) * 0.16; by += (my - by) * 0.16; rx += (mx - rx) * 0.07; ry += (my - ry) * 0.07;
      const s = hover ? 2.1 : 1;
      blob.style.transform = `translate(${bx}px,${by}px) translate(-50%,-50%)`;
      blob.style.width = (10 * s) + 'px'; blob.style.height = (10 * s) + 'px';
      ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
      ring.style.width = (hover ? 62 : 36) + 'px'; ring.style.height = (hover ? 62 : 36) + 'px';
      ring.style.borderColor = hover ? 'rgba(185,255,63,.9)' : 'rgba(185,255,63,.45)';
      ctx.clearRect(0, 0, W, H);
      for (let i = parts.length - 1; i >= 0; i--) {
        const p = parts[i];
        p.x += p.vx; p.y += p.vy; p.vy += 0.05; p.life -= p.decay;
        if (p.life <= 0) { parts.splice(i, 1); continue; }
        ctx.globalAlpha = Math.max(p.life, 0);
        ctx.fillStyle = 'rgba(' + p.c + ',' + Math.max(p.life, 0) + ')';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(loop);
    };
    loop();
    return () => {
      removeEventListener('mousemove', mv); document.removeEventListener('mouseover', ov);
      blob.remove(); ring.remove(); cv.remove();
      document.documentElement.classList.remove('has-cur');
    };
  }, [hideNav]);

  /* ---------- HUD clock ---------- */
  useEffect(() => {
    const el = document.getElementById('hudTime');
    if (!el) return;
    const p = (n) => String(n).padStart(2, '0');
    const t = () => { const d = new Date(); el.textContent = `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())} IST`; };
    t(); const iv = setInterval(t, 1000);
    return () => clearInterval(iv);
  }, [location.pathname]);

  /* ---------- body lock on nav ---------- */
  useEffect(() => {
    document.body.classList.toggle('navlock', navOpen);
    const onEsc = (e) => {
      if (e.key === 'Escape' && navOpen) {
        setNavOpen(false);
        setTimeout(() => setNavMounted(false), 400);
      }
    };
    addEventListener('keydown', onEsc);
    return () => { document.body.classList.remove('navlock'); removeEventListener('keydown', onEsc); };
  }, [navOpen]);

  /* ============================================================
     THE MOUSE-REACTIVITY ENGINE (global, delegated — every page)
     1. MAGNETIC buttons  — [data-mag] pull toward the cursor
     2. CARD SPOTLIGHT    — glass cards get a cursor-tracking glow
     3. 3D TILT           — big cards lean with the pointer
     4. VELOCITY SKEW     — hero titles skew with scroll speed
     ============================================================ */
  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;

    /* 1+2+3: pointer delegation */
    const SPOT = '.gcard,.acard,.chip,.nstat,.spot,.room-card,.impact-cell,.how-card,.kb-card,.kb-why-card,.pf-num,.pf-ev,.rx-card,.rx-stamp-cell,.as-power,.op-stat,.op-row,.op-req,.rx-slot,.ar-reel,.ar-tile,.ar-vo-row';
    const TILT = '.gcard,.acard,.impact-cell,.kb-card,.kb-why-card,.pf-num,.rx-card,.as-power,.op-stat,.op-row,.op-req,.how-card,.rx-slot,.ar-reel,.ar-tile';

    let mag = null, magTarget = null, magRAF = 0;
    const magLoop = () => {
      if (mag && magTarget) {
        const dx = magTarget.cx - magTarget.rx, dy = magTarget.cy - magTarget.ry;
        magTarget.rx += dx * 0.22; magTarget.ry += dy * 0.22;
        mag.style.transform = `translate(${magTarget.rx}px,${magTarget.ry}px)`;
        if (Math.abs(dx) > 0.3 || Math.abs(dy) > 0.3) magRAF = requestAnimationFrame(magLoop);
        else { mag.style.transform = `translate(${magTarget.rx}px,${magTarget.ry}px)`; mag = null; }
      }
    };
    const clearMag = () => {
      if (mag && magTarget) {
        magTarget.rx = 0; magTarget.ry = 0;
        mag.style.transform = '';
      }
      mag = null; magTarget = null;
      cancelAnimationFrame(magRAF);
    };

    const onOver = (e) => {
      const t = e.target.closest('[data-mag]');
      if (t && t !== magTarget) {
        clearMag();
        mag = t; magTarget = { rx: 0, ry: 0, cx: 0, cy: 0 };
        mag.style.willChange = 'transform';
        const r = t.getBoundingClientRect();
        magTarget.cx = e.clientX - (r.left + r.width / 2);
        magTarget.cy = e.clientY - (r.top + r.height / 2);
        magTarget.cx = Math.max(-9, Math.min(9, magTarget.cx * 0.28));
        magTarget.cy = Math.max(-7, Math.min(7, magTarget.cy * 0.28));
        magRAF = requestAnimationFrame(magLoop);
      }
    };

    const onMove = (e) => {
      const s = e.target.closest(SPOT);
      if (s) {
        if (!s.classList.contains('fx-spot')) s.classList.add('fx-spot');
        const r = s.getBoundingClientRect();
        s.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        s.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      }
      const t = e.target.closest(TILT);
      if (t && !t.closest('[data-mag]')) {
        const r = t.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        t.style.transform = `perspective(900px) rotateX(${(-py * 7).toFixed(2)}deg) rotateY(${(px * 9).toFixed(2)}deg) translateY(-4px)`;
        t.style.transition = 'transform .08s linear';
      }
      if (magTarget) {
        const r = mag.getBoundingClientRect();
        magTarget.cx = Math.max(-9, Math.min(9, (e.clientX - (r.left + r.width / 2)) * 0.28));
        magTarget.cy = Math.max(-7, Math.min(7, (e.clientY - (r.top + r.height / 2)) * 0.28));
      }
    };
    const onOut = (e) => {
      const t = e.target.closest(TILT);
      if (t && !t.closest('[data-mag]')) { t.style.transform = ''; t.style.transition = 'transform .4s cubic-bezier(.22,1,.36,1)'; }
      clearMag();
    };

    document.addEventListener('mouseover', onOver);
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseout', onOut);

    /* 4: velocity skew on hero titles */
    const TITLES = 'h1.anton,h2.section-title';
    let lastY = scrollY, vel = 0, velRAF = 0;
    const skewLoop = () => {
      const y = scrollY;
      vel += ((y - lastY) - vel) * 0.25;
      lastY = y;
      const v = Math.max(-2.2, Math.min(2.2, vel * 0.14));
      document.documentElement.style.setProperty('--vel', v.toFixed(3));
      velRAF = requestAnimationFrame(skewLoop);
    };
    const tagTitles = () => document.querySelectorAll(TITLES).forEach((el) => el.classList.add('vel-skew'));
    tagTitles();
    velRAF = requestAnimationFrame(skewLoop);

    return () => {
      document.removeEventListener('mouseover', onOver);
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseout', onOut);
      clearMag();
      cancelAnimationFrame(velRAF);
      document.documentElement.style.setProperty('--vel', '0');
    };
  }, []);

  if (hideNav) return <div className="vig" />;

  const here = pathname;
  const cur = ROOMS.find((r) => r[2] === here);

  return (
    <>
      <motion.nav className="gnav"
        initial={{ y: -80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7, ease: [0.76, 0, 0.24, 1] }}>
        <Link className="gnav-brand anton" to="/" data-cursor="HOME">VIKAAS<span>.</span></Link>
        <span className="gnav-tag cmd">{cur ? cur[1] : 'THE UNIVERSE'}</span>
        <div className="gnav-right">
          <button className="gnav-mute cmd" onClick={toggleMute} data-cursor={muted ? 'UNMUTE' : 'MUTE'} aria-label="toggle sound">
            {muted ? '🔇' : '🔊'}
          </button>
          <button className="gnav-menu cmd" onClick={() => { setNavOpen(true); setNavMounted(true); }}>MENU <i></i><i></i><i></i></button>
        </div>
      </motion.nav>

      <AnimatePresence>
        {navMounted && (
          <motion.div className="gnov" id="gnOverlay"
            initial={{ opacity: 0, visibility: 'hidden', pointerEvents: 'none' }}
            animate={{ opacity: 1, visibility: 'visible', pointerEvents: 'auto' }}
            exit={{ opacity: 0, visibility: 'hidden', pointerEvents: 'none' }}
            transition={{ duration: 0.3 }}>
            <button className="gnov-x cmd" onClick={() => { setNavOpen(false); setTimeout(() => setNavMounted(false), 500); }}>✕ CLOSE</button>
            <div className="gnov-hd cmd">the universe — pick a room</div>
            <div className="gnov-list">
              {ROOMS.map(([no, tt, to, st, label], i) => (
                <motion.div key={no + tt}
                  initial={{ opacity: 0, y: 24 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 + i * 0.05, duration: 0.4, ease: [0.2, 0.9, 0.2, 1] }}>
                  {to
                    ? <Link className="gn-item" to={to} onClick={() => { setNavOpen(false); setTimeout(() => setNavMounted(false), 400); }}>
                        <span className="no">{no}</span><span className="tt anton">{tt}</span>
                        <span className={`st ${pathname === to ? 'now' : 'live'}`}>{pathname === to ? 'YOU ARE HERE' : label}</span>
                      </Link>
                    : <Link className="gn-item soon" to={to} onClick={() => { setNavOpen(false); setTimeout(() => setNavMounted(false), 400); }}><span className="no">{no}</span><span className="tt anton">{tt}</span><span className="st">{label}</span></Link>}
                </motion.div>
              ))}
            </div>
            <div className="gnov-ft cmd">receipts with taste · @qwerty_aarav</div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="hud hud-tl cmd">@qwerty_aarav <b>·</b> receipts with taste</div>
      <div className="hud hud-tr cmd" id="hudTime">--:--:-- <b>IST</b></div>
      <div className="hud hud-bl cmd">#EWasteOff <b>·</b> #ChangemakersWorldCup</div>
      <div className="hud hud-br cmd">GURUGRAM <b>·</b> 28.45°N 77.02°E</div>
      <div className="scrollprog" aria-hidden="true"><i style={{ width: (prog * 100) + '%' }}></i></div>
      <div className="vig" />
    </>
  );
}
