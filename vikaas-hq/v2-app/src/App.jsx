import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Shell from './shell/Shell.jsx';
import Scape from './components/Scape.jsx';
import SafeNet from './lib/SafeNet.jsx';
import { unlockAudio, attachHoverBlips } from './lib/sound.js';
import useLenis from './lib/hooks/useLenis.js';
import Boot from './pages/Boot.jsx';
import Gate from './pages/Gate.jsx';
import Drawer from './pages/Drawer.jsx';
import Type from './pages/Type.jsx';
import ComingSoon from './pages/ComingSoon.jsx';
import Proof from './pages/Proof.jsx';
import Kabadi from './pages/Kabadi.jsx';
import Assistant from './pages/Assistant.jsx';

gsap.registerPlugin(ScrollTrigger);

const ROOM_NAMES = { '/': 'THE GATE', '/boot': 'THE BOOT', '/drawer': 'THE DRAWER', '/proof': 'THE PROOF', '/kabadi': 'THE KABADI', '/buddy': 'THE BUDDY', '/type': 'THE TYPE' };

/* ---------- PAGE WIPE (route transition curtain) ---------- */
function PageWipe({ pathname }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div className="pagewipe" key={'wipe-' + pathname}
        initial={{ scaleY: 1, transformOrigin: 'top' }}
        animate={{ scaleY: 0, transformOrigin: 'top', transition: { duration: 0.75, ease: [0.76, 0, 0.24, 1] } }}
        exit={{ scaleY: 0 }}
        style={{ position: 'fixed', inset: 0, zIndex: 9996, background: 'var(--acid)', pointerEvents: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ fontFamily: 'var(--f-display)', fontSize: 'clamp(30px,6vw,60px)', color: 'var(--ink)', letterSpacing: '.04em' }}>
          {ROOM_NAMES[pathname] || 'VIKAAS'}
        </span>
      </motion.div>
    </AnimatePresence>
  );
}

export default function App() {
  const location = useLocation();
  const pathname = location.pathname;

  // audio unlock + hover blips (once)
  useEffect(() => {
    const u = () => unlockAudio();
    ['pointerdown', 'wheel', 'touchstart'].forEach((ev) => addEventListener(ev, u, { once: true, passive: true }));
    attachHoverBlips();
    return () => ['pointerdown', 'wheel', 'touchstart'].forEach((ev) => removeEventListener(ev, u));
  }, []);

  // per-route Lenis (disabled on boot — it has its own scroll universe)
  useLenis({ enabled: pathname !== '/boot' });

  // scroll to top on route change (not boot) + refresh triggers
  useEffect(() => {
    if (pathname !== '/boot') window.scrollTo(0, 0);
    const t = setTimeout(() => ScrollTrigger.refresh(), 200);
    return () => clearTimeout(t);
  }, [pathname]);

  // scape (fixed 3D bg): ON in real browsers, OFF in automation (headless
  // SwiftShader can stall the GPU process — breaks the QA gate), force on
  // via ?scape=1 for the dedicated Scape probe.
  const scapeOn = pathname !== '/boot' && (new URLSearchParams(location.search).has('scape') || !navigator.webdriver);

  return (
    <SafeNet>
      {scapeOn && <Scape />}
      <Shell pathname={pathname} />
      <PageWipe pathname={pathname} />
      <Routes location={location}>
        <Route path="/" element={<Gate />} />
        <Route path="/boot" element={<Boot />} />
        <Route path="/drawer" element={<Drawer />} />
        <Route path="/type" element={<Type />} />
        <Route path="/proof" element={<Proof />} />
        <Route path="/kabadi" element={<Kabadi />} />
        <Route path="/buddy" element={<Assistant />} />
        <Route path="/system" element={<ComingSoon />} />
        <Route path="/geneva" element={<ComingSoon />} />
        <Route path="/arsenal" element={<Gate />} />
        <Route path="/app" element={<Gate />} />
        <Route path="/app/*" element={<Gate />} />
        <Route path="*" element={<Gate />} />
      </Routes>
    </SafeNet>
  );
}
