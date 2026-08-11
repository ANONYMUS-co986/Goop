import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useRef } from 'react';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Shell from './components/Shell.jsx';
import Boot from './pages/Boot.jsx';
import Gate from './pages/Gate.jsx';
import Drawer from './pages/Drawer.jsx';

gsap.registerPlugin(ScrollTrigger);

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
      <Routes>
        <Route path="/" element={<Gate />} />
        <Route path="/boot" element={<Boot />} />
        <Route path="/drawer" element={<Drawer />} />
        <Route path="*" element={<Gate />} />
      </Routes>
    </>
  );
}
