"use client";

import { useCallback, useEffect, useRef, useState } from "react";

const GLYPHS = "!<>-_/[]{}=+*^?#—";

/**
 * Decode/scramble text — characters resolve left-to-right out of glyph noise.
 * hover: re-trigger when the pointer enters this span (or the nearest
 * ancestor matching `root`, e.g. a whole card / nav row).
 */
export default function ScrambleText({
  text,
  className,
  hover = false,
  onMount = false,
  root,
}: {
  text: string;
  className?: string;
  hover?: boolean;
  onMount?: boolean;
  root?: string;
}) {
  const [display, setDisplay] = useState(text);
  const raf = useRef(0);
  const spanRef = useRef<HTMLSpanElement>(null);

  const play = useCallback(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    cancelAnimationFrame(raf.current);
    // time-based, not frame-based — resolves in ~520ms of WALL clock at any
    // fps, so slow devices / background tabs can't leave it stuck scrambled
    const DUR = 520;
    const start = performance.now();
    const step = () => {
      const p = Math.min(1, (performance.now() - start) / DUR);
      const reveal = Math.floor(p * text.length);
      let out = "";
      for (let i = 0; i < text.length; i++) {
        out += i < reveal || text[i] === " " ? text[i] : GLYPHS[(Math.random() * GLYPHS.length) | 0];
      }
      setDisplay(out);
      if (p < 1) raf.current = requestAnimationFrame(step);
      else setDisplay(text);
    };
    raf.current = requestAnimationFrame(step);
  }, [text]);

  useEffect(() => { if (onMount) play(); }, [play, onMount]);

  useEffect(() => {
    if (!hover) return;
    const el = spanRef.current;
    const target = root ? (el?.closest(root) as HTMLElement | null) : el;
    if (!target) return;
    const enter = () => play();
    target.addEventListener("mouseenter", enter);
    return () => target.removeEventListener("mouseenter", enter);
  }, [hover, play, root]);

  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  return (
    <span ref={spanRef} className={className}>
      {display}
    </span>
  );
}
