"use client";

import { useEffect, useRef } from "react";

/**
 * VelocityMarquee — infinite ticker that reacts to scroll: Lenis velocity
 * feeds both speed and skewX, so flicking the page whips the marquee and
 * it relaxes back to cruise. (React Bits "ScrollVelocity" port, Lenis-fed.)
 */
export default function VelocityMarquee({
  items,
  separator = "//",
  className = "",
}: {
  items: string[];
  separator?: string;
  className?: string;
}) {
  const trackRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const track = trackRef.current;
    if (!track) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let offset = 0;
    let vel = 0;
    let skew = 0;
    let raf = 0;
    let half = track.scrollWidth / 2;

    type LenisLike = { on: (ev: string, cb: (e: { velocity: number }) => void) => void; off?: (ev: string, cb: unknown) => void };
    const lenis = (window as unknown as { __lenis?: LenisLike }).__lenis;
    const onScroll = (e: { velocity: number }) => { vel = e.velocity; };
    lenis?.on("scroll", onScroll);

    const onResize = () => { half = track.scrollWidth / 2; };
    window.addEventListener("resize", onResize);

    const loop = () => {
      raf = requestAnimationFrame(loop);
      vel *= 0.92; // relax toward cruise
      const speed = 0.7 + Math.min(Math.abs(vel) * 0.045, 16);
      offset -= speed;
      if (half > 0) {
        const wrapped = ((offset % half) + half) % half;
        skew += (Math.max(-12, Math.min(12, vel * 0.45)) - skew) * 0.12;
        track.style.transform = `translateX(${-wrapped}px) skewX(${skew.toFixed(2)}deg)`;
      }
    };
    raf = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
      lenis?.off?.("scroll", onScroll);
    };
  }, []);

  const Row = ({ hidden }: { hidden?: boolean }) => (
    <div aria-hidden={hidden} className="flex shrink-0 items-center">
      {items.map((t, i) => (
        <span key={i} className="mx-6 font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute">
          {t} <span className="text-lime/60 ml-6">{separator}</span>
        </span>
      ))}
    </div>
  );

  return (
    <div className={`overflow-hidden ${className}`}>
      <div ref={trackRef} className="flex w-max will-change-transform">
        <Row />
        <Row hidden />
      </div>
    </div>
  );
}
