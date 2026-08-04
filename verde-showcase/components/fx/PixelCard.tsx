"use client";

import { useCallback, useEffect, useRef } from "react";

/**
 * PixelCard (reactbits port) — a hover-activated pixel bloom: a loose grid
 * of accent pixels pops in / breathes / dies out over the card. Canvas is
 * completely idle when not hovered (no rAF, zero cost), so it's safe to use
 * on several cards. transform/opacity discipline preserved.
 */
type Px = { x: number; y: number; life: number; speed: number; size: number };

export default function PixelCard({
  children,
  className = "",
  accent = "#A6FF3F",
  gap = 13,
  density = 0.1,
}: {
  children?: React.ReactNode;
  className?: string;
  accent?: string;
  gap?: number;
  density?: number;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const raf = useRef(0);
  const pixels = useRef<Px[]>([]);
  const hovering = useRef(false);
  const reduced = useRef(false);

  useEffect(() => {
    reduced.current = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    return () => cancelAnimationFrame(raf.current);
  }, []);

  const tick = useCallback(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.fillStyle = accent;
    let alive = 0;
    for (const p of pixels.current) {
      p.life += p.speed;
      // life: 0→1 in, hang, then >1 fades out
      const a = p.life < 1 ? p.life : Math.max(0, 2.4 - p.life);
      if (hovering.current && p.life < 1.4) alive++;
      if (a <= 0.01 && !hovering.current) continue;
      ctx.globalAlpha = a * 0.5;
      const s = p.size * (p.life < 1 ? p.life : 1);
      ctx.fillRect(p.x, p.y, s, s);
      if (p.life > 2.4) p.life = 0; // recycle while hovering
    }
    ctx.globalAlpha = 1;
    if (hovering.current || pixels.current.some((p) => p.life < 2.4 && p.life > 0)) {
      raf.current = requestAnimationFrame(tick);
    }
  }, [accent]);

  const spawn = useCallback(() => {
    const c = canvasRef.current;
    if (!c || reduced.current) return;
    const { width, height } = c.getBoundingClientRect();
    c.width = width;
    c.height = height;
    pixels.current = [];
    for (let x = gap; x < width - gap; x += gap) {
      for (let y = gap; y < height - gap; y += gap) {
        if (Math.random() < density) {
          pixels.current.push({
            x, y,
            life: -Math.random() * 1.2, // staggered birth
            speed: 0.02 + Math.random() * 0.05,
            size: 2.5 + Math.random() * 3.5,
          });
        }
      }
    }
    cancelAnimationFrame(raf.current);
    raf.current = requestAnimationFrame(tick);
  }, [density, gap, tick]);

  const onEnter = useCallback(() => { hovering.current = true; spawn(); }, [spawn]);
  const onLeave = useCallback(() => {
    hovering.current = false;
    // let existing pixels finish their fade, then the loop self-terminates
    cancelAnimationFrame(raf.current);
    raf.current = requestAnimationFrame(tick);
  }, [tick]);

  return (
    <div
      className={`group/pixel relative overflow-hidden ${className}`}
      onMouseEnter={onEnter}
      onMouseLeave={onLeave}
    >
      <canvas
        ref={canvasRef}
        aria-hidden
        className="pointer-events-none absolute inset-0 z-0 h-full w-full"
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
