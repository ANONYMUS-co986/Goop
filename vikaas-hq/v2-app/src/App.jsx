import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useRef, useState } from 'react';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Shell from './components/Shell.jsx';
import Boot from './pages/Boot.jsx';
import Gate from './pages/Gate.jsx';
import Drawer from './pages/Drawer.jsx';

gsap.registerPlugin(ScrollTrigger);

const ROOM_NAMES = { '/': 'THE GATE', '/boot': 'THE BOOT', '/drawer': 'THE DRAWER' };

function PageWipe({ pathname }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const name = ROOM_NAMES[pathname] || 'VIKAAS';
    el.querySelector('span').textContent = name;
    el.style.transition = 'none';
    el.style.transform = 'scaleY(1)';
    el.style.transformOrigin = 'top';
    el.style.display = 'flex';
    void el.offsetWidth;
    el.style.transition = 'transform .75s cubic-bezier(.76,0,.24,1)';
    el.style.transform = 'scaleY(0)';
    const t = setTimeout(() => { el.style.display = 'none'; }, 850);
    return () => clearTimeout(t);
  }, [pathname]);
  return <div className="pagewipe" ref={ref}><span></span></div>;
}

export default function App() {
  const location = useLocation();
  const lenisRef = useRef(null);

  // global smooth scroll
  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const touch = matchMedia('(hover: none)').matches;
    if (reduce || touch || location.pathname === '/boot') return;
    const lenis = new Lenis({ lerp: 0.1 });
    lenisRef.current = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    const raf = (t) => lenis.raf(t * 1000);
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);
    return () => { gsap.ticker.remove(raf); lenis.destroy(); };
  }, [location.pathname]);

  // scroll to top on route change (not for boot)
  useEffect(() => {
    if (location.pathname !== '/boot') window.scrollTo(0, 0);
    ScrollTrigger.refresh();
  }, [location.pathname]);

  return (
    <>
      <Shell pathname={location.pathname} />
      <PageWipe pathname={location.pathname} />
      <Routes>
        <Route path="/" element={<Gate />} />
        <Route path="/boot" element={<Boot />} />
        <Route path="/drawer" element={<Drawer />} />
        <Route path="*" element={<Gate />} />
      </Routes>
    </>
  );
}
