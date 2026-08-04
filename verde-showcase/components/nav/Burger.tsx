"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ROUTES } from "./nav";
import TransitionLink from "./TransitionLink";
import ScrambleText from "@/components/fx/Scramble";

/**
 * Burger command deck — full-viewport navigation overlay.
 * Circle-wipe reveal, staggered route rows, live/fabrication status chips,
 * syscon footer. Esc closes; Lenis pauses while open.
 */
export default function Burger() {
  const [open, setOpen] = useState(false);
  const [uptime, setUptime] = useState(0);
  const pathname = usePathname();
  const startRef = useRef(Date.now());

  useEffect(() => {
    const t = setInterval(() => setUptime(Math.floor((Date.now() - startRef.current) / 1000)), 1000);
    return () => clearInterval(t);
  }, []);

  const setLenis = useCallback((running: boolean) => {
    const lenis = (window as unknown as { __lenis?: { stop: () => void; start: () => void } }).__lenis;
    if (!lenis) return;
    if (running) lenis.start(); else lenis.stop();
  }, []);

  useEffect(() => {
    document.documentElement.style.overflow = open ? "hidden" : "";
    setLenis(!open);
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("keydown", onKey);
      document.documentElement.style.overflow = "";
      setLenis(true);
    };
  }, [open, setLenis]);

  const mm = String(Math.floor(uptime / 60)).padStart(2, "0");
  const ss = String(uptime % 60).padStart(2, "0");

  return (
    <>
      {/* burger trigger */}
      <button
        onClick={() => setOpen(!open)}
        aria-label={open ? "Close menu" : "Open menu"}
        className="fixed top-5 right-5 md:top-6 md:right-8 z-[10003] group flex h-11 w-11 items-center justify-center rounded-full border border-white/10 bg-ink-2/80 backdrop-blur-md transition-colors hover:border-lime/50"
      >
        <span className="relative block h-3 w-5">
          <span className={`absolute left-0 top-0 h-px w-full bg-dew transition-all duration-300 group-hover:bg-lime ${open ? "top-1/2 -translate-y-1/2 rotate-45" : ""}`} />
          <span className={`absolute left-0 top-1/2 h-px w-full -translate-y-1/2 bg-dew transition-all duration-200 ${open ? "opacity-0" : "group-hover:w-3 group-hover:bg-lime"}`} />
          <span className={`absolute left-0 bottom-0 h-px w-full bg-dew transition-all duration-300 group-hover:bg-lime ${open ? "bottom-1/2 translate-y-1/2 -rotate-45" : ""}`} />
        </span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ clipPath: "circle(0% at 94% 4%)" }}
            animate={{ clipPath: "circle(150% at 94% 4%)" }}
            exit={{ clipPath: "circle(0% at 94% 4%)" }}
            transition={{ duration: 0.65, ease: [0.76, 0, 0.24, 1] }}
            className="fixed inset-0 z-[10002] bg-ink-2/95 backdrop-blur-xl flex flex-col"
            aria-label="Site navigation"
          >
            <div className="flex-1 overflow-y-auto px-6 md:px-16 pt-24 md:pt-28 pb-6">
              <p className="font-mono text-[10px] uppercase tracking-[0.32em] text-dew-mute mb-8">navigation // command deck</p>
              <ul className="space-y-1 md:space-y-2">
                {ROUTES.map((r, i) => {
                  const active = pathname === r.href;
                  return (
                    <motion.li
                      key={r.href}
                      initial={{ opacity: 0, x: -28 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.18 + i * 0.06, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                    >
                      <TransitionLink
                        href={r.href}
                        label={r.label}
                        onNavigate={() => setOpen(false)}
                        data-cursor={active ? "here" : "go"}
                        className="group flex items-baseline gap-4 md:gap-6 py-2.5 md:py-3 border-b border-white/[0.06] hover:border-lime/30 transition-colors"
                      >
                        <span className="font-mono text-[11px] text-lime/70 w-7 shrink-0">{r.ghost}</span>
                        <ScrambleText
                          text={r.label}
                          hover
                          root="a"
                          className={`font-display font-bold uppercase tracking-tight text-3xl sm:text-4xl md:text-5xl transition-all duration-300 ${
                            active ? "text-lime drop-shadow-[0_0_18px_rgba(166,255,63,0.4)]" : "text-dew group-hover:text-lime group-hover:translate-x-3"
                          }`}
                        />
                        <span className="hidden md:inline font-sans text-xs text-dew-mute max-w-[220px] leading-snug">
                          {r.blurb}
                        </span>
                        <span className={`ml-auto chip shrink-0 ${
                          r.live
                            ? "border-lime/40 bg-lime-ghost text-lime"
                            : "border-white/10 bg-white/[0.03] text-dew-mute"
                        }`}>
                          {r.live ? "● live" : `◌ ${r.batch}`}
                        </span>
                      </TransitionLink>
                    </motion.li>
                  );
                })}
              </ul>
            </div>

            {/* syscon footer */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="pl-[4.5rem] pr-6 md:px-16 py-5 border-t border-white/[0.07] flex flex-wrap items-center gap-x-8 gap-y-2 font-mono text-[10px] uppercase tracking-[0.24em] text-dew-mute"
            >
              <span>session t+{mm}:{ss}</span>
              <span className="text-lime/70">aarav × anuj</span>
              <span>kern: night-lab 0.1</span>
              <span className="ml-auto hidden sm:inline">esc to close</span>
            </motion.div>
          </motion.nav>
        )}
      </AnimatePresence>
    </>
  );
}
