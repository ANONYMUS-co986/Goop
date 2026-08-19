import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Shell from './shell/Shell.jsx';
import { unlockAudio, attachHoverBlips } from './lib/sound.js';
import useLenis from './lib/hooks/useLenis.js';
import Boot from './pages/Boot.jsx';
import Gate from './pages/Gate.jsx';
import Drawer from './pages/Drawer.jsx';
import Type from './pages/Type.jsx';
import ComingSoon from './pages/ComingSoon.jsx';
import AppHome from './pages/AppHome.jsx';
import Book from './pages/Book.jsx';
import Centres from './pages/Centres.jsx';
import MapPage from './pages/MapPage.jsx';
import Receipts from './pages/Receipts.jsx';
import Assistant from './pages/Assistant.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Login from './pages/Login.jsx';
import Admin from './pages/Admin.jsx';

gsap.registerPlugin(ScrollTrigger);

const ROOM_NAMES = { '/': 'THE GATE', '/boot': 'THE BOOT', '/drawer': 'THE DRAWER', '/type': 'THE TYPE', '/app/receipts': 'THE RECEIPTS', '/app/assistant': 'REBEE', '/app/dashboard': 'THE LEDGER', '/app/login': 'THE DOOR', '/app/admin': 'CENTRE OPS' };

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

  return (
    <>
      <Shell pathname={pathname} />
      <PageWipe pathname={pathname} />
      <Routes location={location}>
        <Route path="/" element={<Gate />} />
        <Route path="/boot" element={<Boot />} />
        <Route path="/drawer" element={<Drawer />} />
        <Route path="/type" element={<Type />} />
        <Route path="/proof" element={<ComingSoon />} />
        <Route path="/kabadi" element={<ComingSoon />} />
        <Route path="/arsenal" element={<ComingSoon />} />
        <Route path="/buddy" element={<ComingSoon />} />
        <Route path="/system" element={<ComingSoon />} />
        <Route path="/geneva" element={<ComingSoon />} />
        <Route path="/app" element={<AppHome />} />
        <Route path="/app/book" element={<Book />} />
        <Route path="/app/centres" element={<Centres />} />
        <Route path="/app/map" element={<MapPage />} />
        <Route path="/app/receipts" element={<Receipts />} />
        <Route path="/app/assistant" element={<Assistant />} />
        <Route path="/app/dashboard" element={<Dashboard />} />
        <Route path="/app/login" element={<Login />} />
        <Route path="/app/admin" element={<Admin />} />
        <Route path="*" element={<Gate />} />
      </Routes>
    </>
  );
}
