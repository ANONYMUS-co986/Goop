"use client";

import { useEffect, useRef, useState } from "react";
import gsap from "gsap";

const BOOT_LINES = [
  { tag: "[ok]", text: "verde://showcase kernel v0.1 — cold start" },
  { tag: "[ok]", text: "mounting /dev/nightlab  (ink #050D0B)" },
  { tag: "[ok]", text: "spore particle field ......... seeded" },
  { tag: "[ok]", text: "fresnel shader pipeline ...... online" },
  { tag: "[ok]", text: "gsap timeline bus ............ synced" },
  { tag: "[ok]", text: "lenis kinetic scroll ......... armed" },
  { tag: "[ok]", text: "hologram lattice ............. charged" },
  { tag: "[ok]", text: "telemetry uplink ............. standby" },
  { tag: "[..]", text: "access request → class-x builders" },
  { tag: "[ok]", text: "ACCESS GRANTED — welcome to the lab" },
];

const STRIPS = 5;

/**
 * Multi-stage boot preloader.
 * Stage 1: kernel log streams in. Stage 2: % counter + rail fill.
 * Stage 3: sprout path draws. Stage 4: column-strip explosion exit.
 * Shows a fast version if the session already booted. Click to skip.
 */
export default function Preloader() {
  const overlayRef = useRef<HTMLDivElement>(null);
  const logRef = useRef<HTMLUListElement>(null);
  const pctRef = useRef<HTMLSpanElement>(null);
  const barRef = useRef<HTMLDivElement>(null);
  const sproutRef = useRef<SVGPathElement>(null);
  const stripsRef = useRef<HTMLDivElement>(null);
  const [gone, setGone] = useState(false);

  useEffect(() => {
    const overlay = overlayRef.current;
    if (!overlay) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setGone(true);
      return;
    }

    const seen = sessionStorage.getItem("verde-booted") === "1";
    sessionStorage.setItem("verde-booted", "1");

    const pct = { v: 0 };
    const lines = logRef.current?.querySelectorAll("li") ?? [];
    const strips = stripsRef.current?.children ?? [];

    const tl = gsap.timeline({
      defaults: { ease: "power2.out" },
      onComplete: () => setGone(true),
    });

    if (seen) {
      // fast re-check for returning visitors
      tl.fromTo(logRef.current!.children[9], { opacity: 0 }, { opacity: 1, duration: 0.2 })
        .to(pct, {
          v: 100, duration: 0.5, ease: "power2.inOut",
          onUpdate: () => { if (pctRef.current) pctRef.current.textContent = String(Math.round(pct.v)); },
        }, 0);
    } else {
      tl.fromTo(
        lines,
        { opacity: 0, y: 8, filter: "blur(4px)" },
        { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.22, stagger: 0.09 }
      );
      tl.to(pct, {
        v: 100, duration: 2.1, ease: "power2.inOut",
        onUpdate: () => { if (pctRef.current) pctRef.current.textContent = String(Math.round(pct.v)); },
      }, 0.15);
      if (sproutRef.current) {
        const len = sproutRef.current.getTotalLength();
        tl.fromTo(sproutRef.current,
          { strokeDasharray: len, strokeDashoffset: len },
          { strokeDashoffset: 0, duration: 1.3, ease: "power2.inOut" }, 0.5);
      }
      tl.to(barRef.current, { scaleX: 1, duration: 2.1, ease: "power2.inOut" }, 0.15);
      tl.to({}, { duration: 0.25 }); // savour "ACCESS GRANTED"
    }

    // strip explosion exit
    tl.to(strips, {
      scaleY: 0, transformOrigin: "top", duration: 0.55,
      stagger: { each: 0.06, from: "center" }, ease: "power3.inOut",
    });
    tl.to(overlay, { opacity: 0, duration: 0.3 }, "<0.25");
    tl.set(overlay, { display: "none" });

    const skip = () => tl.progress(1);
    overlay.addEventListener("click", skip);
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape" || e.key === "Enter") tl.progress(1); };
    window.addEventListener("keydown", onKey);
    return () => {
      overlay.removeEventListener("click", skip);
      window.removeEventListener("keydown", onKey);
      tl.kill();
    };
  }, []);

  if (gone) return null;

  return (
    <div ref={overlayRef} className="fixed inset-0 z-[10005] bg-ink" role="dialog" aria-label="Loading Verde Showcase">
      {/* exit strips */}
      <div ref={stripsRef} className="absolute inset-0 flex">
        {Array.from({ length: STRIPS }).map((_, i) => (
          <div key={i} className="h-full flex-1 bg-ink-2 border-r border-ink-4/40 last:border-r-0" />
        ))}
      </div>

      {/* boot console */}
      <div className="absolute inset-0 flex items-center justify-center px-6 pointer-events-none">
        <div className="w-full max-w-xl">
          <div className="flex items-center gap-3 mb-5">
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden>
              <path
                ref={sproutRef}
                d="M13 23 V13 C13 8 9 6 4 6 C4 12 8 14 13 13 M13 13 C13 7 17 3 22 3 C22 10 18 13 13 13"
                stroke="#A6FF3F" strokeWidth="1.6" strokeLinecap="round"
              />
            </svg>
            <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute">verde bios — night lab</span>
          </div>
          <ul ref={logRef} className="space-y-1.5 font-mono text-[11px] leading-relaxed">
            {BOOT_LINES.map((l, i) => (
              <li key={i} className="opacity-0">
                <span className={i === BOOT_LINES.length - 1 ? "text-lime" : l.tag === "[..]" ? "text-amber" : "text-hydro"}>{l.tag}</span>{" "}
                <span className={i === BOOT_LINES.length - 1 ? "text-lime" : "text-dew-dim"}>{l.text}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* rail + % */}
      <div className="absolute inset-x-0 bottom-0 p-6 md:p-10">
        <div className="flex items-end justify-between mb-3">
          <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute">tapping / clicking skips</span>
          <span className="font-display font-bold text-5xl md:text-7xl text-lime leading-none tabular-nums drop-shadow-[0_0_24px_rgba(166,255,63,0.35)]">
            <span ref={pctRef}>0</span><span className="text-dew-mute text-2xl md:text-3xl">%</span>
          </span>
        </div>
        <div className="h-px w-full bg-white/10">
          <div ref={barRef} className="h-px bg-lime origin-left scale-x-0 shadow-glow-lime" />
        </div>
      </div>
    </div>
  );
}
