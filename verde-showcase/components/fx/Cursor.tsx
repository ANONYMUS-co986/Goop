"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Lab cursor: lime dot + lerped reticle ring.
 * Ring grows + softens glow over interactive elements (a, button, [data-hover]).
 * Disabled entirely on touch / coarse pointers and reduced-motion users.
 */
export default function Cursor() {
  const dotRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    setEnabled(fine && !reduced);
  }, []);

  useEffect(() => {
    if (!enabled) return;

    let x = -100, y = -100, rx = -100, ry = -100;
    let hovering = false;
    let raf = 0;

    const onMove = (e: MouseEvent) => {
      x = e.clientX;
      y = e.clientY;
      const target = e.target as HTMLElement | null;
      hovering = !!target?.closest("a, button, [role='button'], [data-hover]");
      if (dotRef.current) {
        dotRef.current.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
      }
    };

    const loop = () => {
      rx += (x - rx) * 0.16;
      ry += (y - ry) * 0.16;
      if (ringRef.current) {
        const s = hovering ? 2.1 : 1;
        ringRef.current.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%) scale(${s})`;
        ringRef.current.style.borderColor = hovering
          ? "rgba(166,255,63,0.9)"
          : "rgba(233,255,242,0.45)";
        ringRef.current.style.boxShadow = hovering
          ? "0 0 18px rgba(166,255,63,0.35)"
          : "0 0 0 rgba(0,0,0,0)";
      }
      raf = requestAnimationFrame(loop);
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    raf = requestAnimationFrame(loop);
    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(raf);
    };
  }, [enabled]);

  if (!enabled) return null;

  return (
    <>
      <div
        ref={dotRef}
        className="pointer-events-none fixed left-0 top-0 z-[10001] h-1.5 w-1.5 rounded-full bg-lime"
        style={{ boxShadow: "0 0 10px rgba(166,255,63,0.8)" }}
      />
      <div
        ref={ringRef}
        className="pointer-events-none fixed left-0 top-0 z-[10000] h-8 w-8 rounded-full border border-dew/45 transition-[border-color,box-shadow] duration-200"
      />
    </>
  );
}
