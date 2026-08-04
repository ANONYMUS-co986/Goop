"use client";

import { useEffect } from "react";
import Lenis from "lenis";
import gsap from "gsap";

/**
 * Unified kinetic scroll — one Lenis instance for the whole lab.
 * autoRaf: Lenis drives its own rAF loop (v1.1+).
 * Reduced-motion users keep native scrolling.
 */
export default function SmoothScroll() {
  useEffect(() => {
    // QA bridge — the headless screenshot harness renders at 1-2fps under
    // SwiftShader, where GSAP's default lag smoothing (clamp >500ms frames to
    // 33ms) makes every timeline crawl. Disabling smoothing makes GSAP track
    // wall-clock, so screenshots land on true end states regardless of fps.
    (window as unknown as { __qaNoLag?: () => void }).__qaNoLag = () => gsap.ticker.lagSmoothing(0);

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const lenis = new Lenis({
      autoRaf: true,
      lerp: 0.092,
      smoothWheel: true,
      wheelMultiplier: 1.0,
      touchMultiplier: 1.4,
    });

    (window as unknown as { __lenis?: Lenis }).__lenis = lenis;

    return () => {
      lenis.destroy();
      delete (window as unknown as { __lenis?: Lenis }).__lenis;
      delete (window as unknown as { __qaNoLag?: () => void }).__qaNoLag;
    };
  }, []);

  return null;
}
