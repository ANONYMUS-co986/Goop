"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Lab cursor: lime dot + lerped reticle ring.
 * Ring grows + softens glow over interactive elements (a, button, [data-hover]).
 * Elements with [data-cursor="label"] bloom the ring into a labelled lens.
 * Disabled entirely on touch / coarse pointers and reduced-motion users.
 */
export default function Cursor() {
  const dotRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);
  const labelRef = useRef<HTMLSpanElement>(null);
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
    let labeled = false;
    let raf = 0;

    const onMove = (e: MouseEvent) => {
      x = e.clientX;
      y = e.clientY;
      const target = e.target as HTMLElement | null;
      hovering = !!target?.closest("a, button, [role='button'], [data-hover]");
      const cursorEl = target?.closest("[data-cursor]") as HTMLElement | null;
      const text = cursorEl?.dataset.cursor ?? "";
      if (text !== (labelRef.current?.dataset.prev ?? "")) {
        if (labelRef.current) {
          labelRef.current.dataset.prev = text;
          labelRef.current.textContent = text;
        }
      }
      labeled = text.length > 0;
      if (dotRef.current) {
        dotRef.current.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
        dotRef.current.style.opacity = labeled ? "0" : "1";
      }
    };

    const loop = () => {
      rx += (x - rx) * 0.16;
      ry += (y - ry) * 0.16;
      if (ringRef.current) {
        const s = labeled ? 3.2 : hovering ? 2.1 : 1;
        ringRef.current.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%) scale(${s})`;
        ringRef.current.style.borderColor = labeled || hovering
          ? "rgba(166,255,63,0.9)"
          : "rgba(233,255,242,0.45)";
        ringRef.current.style.background = labeled ? "rgba(5,13,11,0.72)" : "transparent";
        ringRef.current.style.boxShadow = labeled || hovering
          ? "0 0 18px rgba(166,255,63,0.35)"
          : "0 0 0 rgba(0,0,0,0)";
      }
      if (labelRef.current) {
        labelRef.current.style.opacity = labeled ? "1" : "0";
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
        style={{ boxShadow: "0 0 10px rgba(166,255,63,0.8)", transform: "translate(-100px, -100px)" }}
      />
      <div
        ref={ringRef}
        className="pointer-events-none fixed left-0 top-0 z-[10000] h-8 w-8 rounded-full border border-dew/45 transition-[border-color,box-shadow,background] duration-200 flex items-center justify-center"
        style={{ transform: "translate(-100px, -100px)" }}
      >
        <span
          ref={labelRef}
          className="font-mono text-[5px] font-bold uppercase tracking-[0.18em] text-lime opacity-0 transition-opacity duration-150 select-none scale-[0.31]"
          style={{ fontSize: 8, letterSpacing: "0.14em" }}
        />
      </div>
    </>
  );
}
