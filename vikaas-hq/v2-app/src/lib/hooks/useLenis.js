import { useEffect } from 'react';
import gsap from 'gsap';

/** useLenis — per-route Lenis smooth scroll synced with ScrollTrigger.
 *  usage: useLenis({ enabled: pathname !== '/boot' }) */
export default function useLenis({ enabled = true } = {}) {
  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const touch = matchMedia('(hover: none)').matches;
    if (!enabled || reduce || touch) return;
    import('lenis').then(({ default: Lenis }) => {
      const lenis = new Lenis({ lerp: 0.1 });
      lenis.on('scroll', () => {
        if (window.ScrollTrigger) window.ScrollTrigger.update();
      });
      const raf = (t) => lenis.raf(t * 1000);
      gsap.ticker.add(raf);
      gsap.ticker.lagSmoothing(0);
      window.__lenis = lenis;
      return () => { gsap.ticker.remove(raf); lenis.destroy(); window.__lenis = null; };
    });
  }, [enabled]);
}
