"use client";

import { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { motion } from "framer-motion";

const BuildCanvas = dynamic(() => import("@/components/three/BuildCanvas"), {
  ssr: false,
  loading: () => (
    <div className="absolute inset-0 grid place-items-center">
      <span className="font-mono text-[11px] uppercase tracking-[0.3em] text-dew-mute animate-pulse">
        bolting the rig together…
      </span>
    </div>
  ),
});

const STAGES = [
  { id: "00", name: "CHASSIS", note: "one PCB, zero mercy — the 38-pin devboard everything hangs off" },
  { id: "01", name: "BRAIN", note: "ESP32-WROOM shield can — dual core, 240MHz, WiFi onboard" },
  { id: "02", name: "SENSES", note: "DHT11 · soil probe · sonar · LDR — four ways to feel the plant" },
  { id: "03", name: "HANDS", note: "relay → pump · UV strip — the only parts allowed to touch the world" },
  { id: "04", name: "WIRED", note: "every module tethered to its GPIO pad — slack cables and all" },
];

const BOM: { item: string; role: string; price: string }[] = [
  { item: "ESP32 DevKit v1", role: "main brain", price: "₹340" },
  { item: "DHT11", role: "temp + humidity", price: "₹120" },
  { item: "Capacitive soil probe v1.2", role: "moisture (no rust!)", price: "₹180" },
  { item: "HC-SR04 ultrasonic", role: "tank level", price: "₹110" },
  { item: "LDR module", role: "daylight sense", price: "₹50" },
  { item: "5V single relay", role: "pump switch", price: "₹90" },
  { item: "Jumper wires + headers", role: "the spaghetti", price: "₹140" },
  { item: "Breadboard + power", role: "bench supply", price: "₹130" },
  { item: "Tubing + misc hardware", role: "plumbing", price: "₹160" },
  { item: "Submersible pump", role: "the heart", price: "₹220" },
  { item: "ESP32-CAM", role: "the eye", price: "₹350" },
  { item: "Water tank", role: "upcycled from home", price: "₹0" },
];

const PINMAP: { pin: string; job: string; note: string }[] = [
  { pin: "GPIO4", job: "DHT11 DATA", note: "10k pull-up, 2s poll" },
  { pin: "GPIO5", job: "PUMP RELAY", note: "active-LOW — boot-safe" },
  { pin: "GPIO12", job: "UV LED", note: "algae patrol" },
  { pin: "GPIO18 / 19", job: "SONAR TRIG / ECHO", note: "tank level pings" },
  { pin: "GPIO23", job: "MOISTURE POWER", note: "probe gated — kills corrosion" },
  { pin: "GPIO34", job: "SOIL ADC", note: "10-pt ring filter" },
  { pin: "GPIO35", job: "LDR ADC", note: "10-pt ring filter" },
  { pin: "GPIO2", job: "BOARD LED", note: "heartbeat blink" },
];

export default function BuildPage() {
  const wrapRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef(0);
  const [stage, setStage] = useState(0);
  const [pct, setPct] = useState(0);

  useEffect(() => {
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = wrapRef.current;
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const total = el.offsetHeight - window.innerHeight;
        const p = Math.min(1, Math.max(0, -rect.top / Math.max(1, total)));
        progressRef.current = p;
        setPct(Math.round(p * 100));
        setStage(Math.min(STAGES.length - 1, Math.floor(p * STAGES.length)));
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <main className="relative">
      {/* ————— header ————— */}
      <section className="relative min-h-[72vh] flex flex-col justify-end px-6 md:px-16 pb-14 pt-36 overflow-hidden">
        <div className="absolute inset-0 bg-grid-thin bg-grid-44 opacity-60" aria-hidden />
        <span className="chip border-lime/40 bg-lime-ghost text-lime w-fit mb-6">● live · batch B2</span>
        <h1 className="font-display font-extrabold leading-[0.92] tracking-tight text-[13vw] md:text-[7.5rem]">
          THE BUILD.
        </h1>
        <p className="mt-5 max-w-xl text-dew-dim text-base md:text-lg leading-relaxed">
          <span className="text-lime">₹1,890</span> of Delhi local-market electronics, exploded in
          mid-air. Scroll — the rig takes itself apart, then wires itself back together.
        </p>
        <div className="mt-8 flex flex-wrap gap-3 font-mono text-[10px] uppercase tracking-[0.22em] text-dew-mute">
          <span className="chip">2 microcontrollers</span>
          <span className="chip">5 sensors</span>
          <span className="chip">2 actuators</span>
          <span className="chip">1 cloud</span>
        </div>
      </section>

      {/* ————— exploded rig scroller ————— */}
      <div ref={wrapRef} className="relative" style={{ height: "380vh" }}>
        <div className="sticky top-0 h-screen overflow-hidden">
          <BuildCanvas progressRef={progressRef} />

          {/* stage rail */}
          <div className="absolute left-6 md:left-16 bottom-8 md:bottom-12 max-w-md">
            <div className="font-mono text-[10px] tracking-[0.3em] text-dew-mute mb-2">
              DISASSEMBLY {String(pct).padStart(3, "0")}%
            </div>
            <div className="h-px w-40 bg-white/10 mb-4">
              <div className="h-px bg-lime origin-left shadow-glow-lime" style={{ transform: `scaleX(${pct / 100})` }} />
            </div>
            <motion.div
              key={stage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35 }}
            >
              <div className="font-display font-bold text-3xl md:text-5xl">
                <span className="text-lime/60 mr-3 text-xl md:text-3xl align-top">{STAGES[stage].id}</span>
                {STAGES[stage].name}
              </div>
              <p className="mt-2 text-dew-dim text-sm md:text-base">{STAGES[stage].note}</p>
            </motion.div>
          </div>

          {/* stage ticks */}
          <div className="absolute right-6 md:right-16 top-1/2 -translate-y-1/2 hidden md:flex flex-col gap-4">
            {STAGES.map((s, i) => (
              <div key={s.id} className="flex items-center gap-3 justify-end">
                <span className={`font-mono text-[9px] tracking-[0.25em] transition-colors ${i === stage ? "text-lime" : "text-dew-mute/50"}`}>
                  {s.name}
                </span>
                <span className={`h-px transition-all ${i === stage ? "w-8 bg-lime" : "w-4 bg-white/20"}`} />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ————— BOM ————— */}
      <section className="px-6 md:px-16 py-24 md:py-32">
        <div className="flex items-end justify-between flex-wrap gap-4 mb-10">
          <h2 className="font-display font-extrabold text-4xl md:text-6xl leading-none">
            THE RECEIPTS<span className="text-lime">.</span>
          </h2>
          <span className="font-mono text-[10px] tracking-[0.3em] text-dew-mute uppercase">
            actual market haul · no sponsors, no regrets
          </span>
        </div>
        <div className="border border-white/10 rounded-2xl overflow-hidden glass">
          {BOM.map((row, i) => (
            <div
              key={row.item}
              className="group grid grid-cols-[1fr_auto] md:grid-cols-[3rem_1fr_1fr_auto] gap-x-4 items-baseline px-5 md:px-8 py-4 border-b border-white/[0.06] last:border-b-0 hover:bg-lime-ghost/60 transition-colors"
            >
              <span className="hidden md:block font-mono text-[10px] text-dew-mute">{String(i + 1).padStart(2, "0")}</span>
              <span className="font-display font-semibold text-base md:text-lg group-hover:text-lime transition-colors">{row.item}</span>
              <span className="hidden md:block font-mono text-[11px] text-dew-mute">{row.role}</span>
              <span className="font-mono text-sm text-lime tabular-nums">{row.price}</span>
            </div>
          ))}
          <div className="grid grid-cols-[1fr_auto] md:grid-cols-[3rem_1fr_1fr_auto] gap-x-4 items-baseline px-5 md:px-8 py-5 bg-lime/10">
            <span className="hidden md:block" />
            <span className="font-display font-extrabold text-xl md:text-2xl">TOTAL DAMAGE</span>
            <span className="hidden md:block font-mono text-[11px] text-dew-dim">a pizza night, basically</span>
            <span className="font-mono text-xl md:text-2xl text-lime font-bold tabular-nums">₹1,890</span>
          </div>
        </div>
      </section>

      {/* ————— pin map ————— */}
      <section className="px-6 md:px-16 pb-28">
        <h2 className="font-display font-extrabold text-4xl md:text-6xl leading-none mb-3">
          WHERE EVERY WIRE LANDS<span className="text-lime">.</span>
        </h2>
        <p className="text-dew-dim max-w-xl mb-10">
          Straight from <span className="font-mono text-lime text-sm">Code_1_Main_Brain.ino</span>{" "}
          v3.0.7-FINAL — the firmware that never shipped a reboot.
        </p>
        <div className="grid md:grid-cols-2 gap-3">
          {PINMAP.map((row) => (
            <div
              key={row.pin}
              className="group flex items-baseline gap-4 border border-white/10 rounded-xl px-5 py-4 glass hover:border-lime/40 transition-colors"
            >
              <span className="font-mono text-lime text-sm w-28 shrink-0">{row.pin}</span>
              <span className="font-display font-semibold group-hover:text-lime transition-colors">{row.job}</span>
              <span className="ml-auto font-mono text-[10px] text-dew-mute text-right">{row.note}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ————— next door ————— */}
      <section className="px-6 md:px-16 pb-24">
        <Link href="/brain" className="group block border border-uv/30 rounded-2xl px-8 py-10 glass hover:border-uv/70 transition-colors">
          <div className="font-mono text-[10px] tracking-[0.3em] text-uv uppercase mb-3">next room · batch b3</div>
          <div className="font-display font-extrabold text-3xl md:text-5xl group-hover:text-uv transition-colors">
            THE BRAIN — how 17 API calls became 2 <span className="inline-block transition-transform group-hover:translate-x-2">→</span>
          </div>
        </Link>
      </section>
    </main>
  );
}
