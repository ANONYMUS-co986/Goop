"use client";

import dynamic from "next/dynamic";
import { motion } from "framer-motion";

const HeroCanvas = dynamic(() => import("./HeroCanvas"), {
  ssr: false,
  loading: () => (
    <div className="absolute inset-0 flex items-center justify-center font-mono text-[10px] uppercase tracking-[0.3em] text-lime/60">
      charging hologram lattice…
    </div>
  ),
});

const STATS = [
  { k: "₹1,890", l: "total build" },
  { k: "94%", l: "leaf-id confidence" },
  { k: "2 MCU", l: "one brain + one eye" },
  { k: "60s", l: "cloud heartbeat" },
];

export default function HeroSection() {
  return (
    <section className="relative min-h-[100svh] overflow-hidden bg-ink">
      {/* the hologram lives behind the type */}
      <div className="absolute inset-0">
        <HeroCanvas />
      </div>

      {/* type layer */}
      <div className="pointer-events-none relative z-10 flex min-h-[100svh] flex-col items-center justify-center px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 18, filter: "blur(6px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ delay: 0.35, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="chip border-lime/30 bg-ink-2/70 text-lime mb-6"
        >
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute h-full w-full rounded-full bg-lime animate-pingring" />
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-lime" />
          </span>
          class x · dav acon 5 · round 2
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 26, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{ delay: 0.5, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="font-display font-bold uppercase leading-[0.88] tracking-tight"
        >
          <span className="block text-[15vw] sm:text-[12vw] lg:text-[9.2rem] text-dew drop-shadow-[0_2px_30px_rgba(5,13,11,0.9)]">
            Project
          </span>
          <span className="block text-[15vw] sm:text-[12vw] lg:text-[9.2rem] text-lime drop-shadow-[0_0_36px_rgba(166,255,63,0.45)]">
            Verde
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.72, duration: 0.6 }}
          className="mt-6 max-w-md font-sans text-sm md:text-[15px] leading-relaxed text-dew-dim bg-ink/40 backdrop-blur-[2px] rounded-xl px-4 py-2"
        >
          The plant that waters itself — and talks to AI. Built for ₹1,890,
          debugged in public, and running live off two microcontrollers,
          one cloud, and far too much stubbornness.
        </motion.p>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.95 }}
          className="pointer-events-auto mt-9 flex flex-wrap items-center justify-center gap-3"
        >
          <a
            href="#saga"
            className="rounded-full border border-lime/50 bg-lime text-ink-2 px-7 py-3 font-mono text-[11px] font-bold uppercase tracking-[0.22em] shadow-glow-lime transition-transform hover:scale-[1.04]"
          >
            Enter the lab ↓
          </a>
          <a
            href="/build"
            className="rounded-full border border-hydro/40 bg-hydro-ghost text-hydro px-7 py-3 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:bg-hydro/20"
          >
            Skip to the build
          </a>
        </motion.div>
      </div>

      {/* bottom instrument strip */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.1 }}
        className="absolute bottom-0 inset-x-0 z-10 border-t border-white/[0.07] bg-ink-2/70 backdrop-blur-md"
      >
        <div className="mx-auto max-w-6xl grid grid-cols-2 md:grid-cols-4 divide-x divide-white/[0.06]">
          {STATS.map((s) => (
            <div key={s.l} className="px-4 md:px-6 py-4 text-center">
              <div className="font-display font-bold text-xl md:text-2xl text-dew">{s.k}</div>
              <div className="font-mono text-[9px] uppercase tracking-[0.26em] text-dew-mute mt-1">{s.l}</div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* scroll cue */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4 }}
        className="absolute bottom-24 left-1/2 -translate-x-1/2 z-10 font-mono text-[9px] uppercase tracking-[0.3em] text-dew-mute hidden md:block"
      >
        scroll — the saga is long
      </motion.div>
    </section>
  );
}
