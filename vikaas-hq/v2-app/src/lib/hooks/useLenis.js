import { useEffect } from 'react';
import gsap from 'gsap';

/** useLenis v2 — per-route smooth scroll, ScrollTrigger-synced, robust.
 *  Handles: reduced-motion off, touch off, dynamic import, cleanup, anchor
 *  scrolls (Lenis handles them if `anchors: true`). */
export default function useLenis({ enabled = true } = {}) {
  useEffect(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const touch = matchMedia('(hover: none)').matches;
    if (!enabled || reduce || touch) return;
    let lenis = null;
    let raf = null;
    let cancelled = false;
    import('lenis').then(({ default: Lenis }) => {
      if (cancelled) return;
      lenis = new Lenis({ lerp: 0.1, smoothWheel: true, anchors: true });
      lenis.on('scroll', () => { if (window.ScrollTrigger) window.ScrollTrigger.update(); });
      raf = (t) => lenis.raf(t * 1000);
      gsap.ticker.add(raf);
      gsap.ticker.lagSmoothing(0);
      window.__lenis = lenis;
    }).catch(() => {});
    return () => {
      cancelled = true;
      if (raf) gsap.ticker.remove(raf);
      if (lenis) lenis.destroy();
      window.__lenis = null;
    };
  }, [enabled]);
}
