"use client";

import { useEffect } from "react";
import Lenis from "lenis";

/**
 * Unified kinetic scroll — one Lenis instance for the whole lab.
 * autoRaf: Lenis drives its own rAF loop (v1.1+).
 * Reduced-motion users keep native scrolling.
 */
export default function SmoothScroll() {
  useEffect(() => {
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
    };
  }, []);

  return null;
}
