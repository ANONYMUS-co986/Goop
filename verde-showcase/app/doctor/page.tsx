"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import TransitionLink from "@/components/nav/TransitionLink";
import GlowCard from "@/components/fx/GlowCard";
import ScrambleText from "@/components/fx/Scramble";
import SplitReveal from "@/components/fx/SplitReveal";
import { Reveal, RevealGroup } from "@/components/fx/Reveal";
import TiltCard from "@/components/fx/TiltCard";
import Parallax from "@/components/fx/Parallax";
import ShinyText from "@/components/fx/ShinyText";
import Magnetic from "@/components/fx/Magnetic";

const EYE_SPECS = [
  { k: "8 MHz XCLK", tip: "stock 20MHz swamped the WiFi RF front-end — photos literally killed the network. 8MHz made them coexist." },
  { k: "500ms staged boot", tip: "sensor → flash → camera init in sequence — no brownout roulette" },
  { k: "1.5s trigger poll", tip: "app drops a flag in /controls, the eye wakes, shoots, posts" },
  { k: "150ms flash pulse", tip: "onboard LED strobes just long enough for an SVGA-worthy leaf" },
  { k: "fb_return hygiene", tip: "esp_camera_fb_return after every POST — one leaked frame buffer and the heap eats itself by midnight" },
];

const PROVIDERS = [
  {
    id: "kindwise", name: "crop.kindwise", role: "primary leaf diagnostician", accent: "#A6FF3F",
    note: "pure base64 JPEG, Api-Key header, /api/v1/identification with details params — 94% match on a real tulsi leaf",
    latency: "~1.8s", vision: true,
  },
  {
    id: "gemini", name: "gemini-flash-latest", role: "backup vision + explainer", accent: "#A78BFA",
    note: "X-goog-api-key — 2.5-flash was locked for new API keys, so flash-latest carries the fall",
    latency: "~2.2s", vision: true,
  },
  {
    id: "openrouter", name: "llama-3.3-70b:free", role: "sensor chat brain", accent: "#67E8F9",
    note: "free tier via OpenRouter — answers 'is my plant okay?' from live /sensors, no eyes",
    latency: "~1.1s", vision: false,
  },
] as const;

type ProviderId = (typeof PROVIDERS)[number]["id"];

const RX_ROWS = [
  { k: "patient", v: "tulsi (ocimum tenuiflorum)" },
  { k: "scan", v: "single_leaf · SVGA 800×600" },
  { k: "diagnosis", v: "HEALTHY", c: "text-lime" },
  { k: "confidence", v: "94% — crop.kindwise", c: "text-lime" },
  { k: "note", v: "top-up light cycle nominal · moisture 41%" },
  { k: "prescription", v: "keep doing exactly this." },
];

export default function DoctorPage() {
  const [down, setDown] = useState<Record<ProviderId, boolean>>({ kindwise: false, gemini: false, openrouter: false });
  const visionChain = PROVIDERS.filter((p) => p.vision);
  const activeVision = visionChain.find((p) => !down[p.id]);
  const servedBy = activeVision ? activeVision.name : "manual mode · the 13-test checklist";
  const anyDown = PROVIDERS.some((p) => down[p.id]);

  return (
    <main className="relative">
      {/* ————— header ————— */}
      <section className="relative min-h-[66vh] flex flex-col justify-end px-6 md:px-16 pb-14 pt-36 overflow-hidden">
        <div className="absolute inset-0 bg-grid-thin bg-grid-44 opacity-60" aria-hidden />
        <Parallax speed={0.55} className="pointer-events-none absolute -right-6 top-4 select-none">
          <span className="font-display font-bold text-[38vw] md:text-[22rem] leading-none text-stroke-ghost">Rx</span>
        </Parallax>
        <span className="chip border-lime/40 bg-lime-ghost text-lime w-fit mb-6">● live · batch B4</span>
        <SplitReveal
          as="h1"
          text="AI DOCTOR."
          className="font-display font-extrabold leading-[0.92] tracking-tight text-[13vw] md:text-[7.5rem]"
          stagger={0.03}
        />
        <p className="mt-5 max-w-xl text-dew-dim text-base md:text-lg leading-relaxed">
          Point a ₹350 camera at a leaf. Ninety seconds later it has a{" "}
          <span className="text-uv">diagnosis, a confidence score and a prescription</span>{" "}
          — with two more AI brains waiting if the first one faints.
        </p>
        <div className="mt-8 flex flex-wrap gap-3 font-mono text-[10px] uppercase tracking-[0.22em] text-dew-mute">
          <span className="chip">esp32-cam · the eye</span>
          <span className="chip">3 ai providers</span>
          <span className="chip text-lime border-lime/30">94% confidence</span>
        </div>
      </section>

      {/* ————— THE EYE ————— */}
      <section className="px-6 md:px-16 py-16 md:py-24">
        <div className="grid lg:grid-cols-2 gap-10 items-center">
          <div>
            <SplitReveal as="h2" text="THE EYE." className="font-display font-extrabold text-4xl md:text-6xl leading-none" />
            <Reveal variant="blur" delay={0.1}>
              <p className="mt-4 max-w-lg text-dew-dim text-sm md:text-base leading-relaxed">
                The ESP32-CAM nearly didn't make the team — its stock clock
                jammed the WiFi radio it was supposed to upload through.
                Firmware v3.0.4-FINAL is the peace treaty. Hover the specs:
              </p>
            </Reveal>
            <RevealGroup className="mt-7 flex flex-wrap gap-2.5" stagger={0.05}>
              {EYE_SPECS.map((s) => (
                <span key={s.k} data-tip={s.tip} className="chip border-white/12 bg-white/[0.03] text-dew-dim hover:border-lime/40 hover:text-lime transition-colors cursor-help">
                  {s.k}
                </span>
              ))}
            </RevealGroup>
          </div>

          {/* cam frame mock */}
          <Reveal variant="scale">
            <TiltCard max={5}>
              <div className="relative overflow-hidden rounded-2xl border border-white/12 bg-ink-2/80 shadow-glow-uv aspect-[4/3]">
                {/* procedural leaf */}
                <svg viewBox="0 0 400 300" className="absolute inset-0 h-full w-full" aria-hidden>
                  <defs>
                    <radialGradient id="leafG" cx="50%" cy="42%" r="65%">
                      <stop offset="0%" stopColor="#1c5c3a" />
                      <stop offset="100%" stopColor="#0B1B15" />
                    </radialGradient>
                  </defs>
                  <rect width="400" height="300" fill="url(#leafG)" />
                  {[...Array(9)].map((_, i) => (
                    <path key={i} d={`M200 ${250 - i * 6} Q ${120 + i * 8} ${170 - i * 14} 200 ${40 + i * 4} Q ${280 - i * 8} ${170 - i * 14} 200 ${250 - i * 6}Z`}
                      fill="none" stroke="#2f8a54" strokeWidth="1.2" opacity={0.5 + i * 0.05} />
                  ))}
                  <path d="M200 260 V36" stroke="#A6FF3F" strokeWidth="1.4" opacity="0.7" />
                  {[...Array(7)].map((_, i) => (
                    <path key={`v${i}`} d={`M200 ${230 - i * 26} q ${46 - i * 3} -18 ${86 - i * 7} -30 M200 ${230 - i * 26} q ${-46 + i * 3} -18 ${-86 + i * 7} -30`}
                      stroke="#3aa868" strokeWidth="1" fill="none" opacity="0.65" />
                  ))}
                </svg>
                {/* scanline sweep */}
                <motion.div
                  className="absolute inset-x-0 h-14 bg-gradient-to-b from-transparent via-lime/25 to-transparent border-y border-lime/40"
                  animate={{ top: ["-15%", "105%"] }}
                  transition={{ duration: 3.2, repeat: Infinity, ease: "linear", repeatDelay: 1.5 }}
                />
                {/* HUD */}
                <div className="absolute top-3 left-3 font-mono text-[9px] tracking-[0.22em] text-lime/90 bg-ink/60 px-2 py-1 rounded">● REC · SVGA 800×600</div>
                <div className="absolute top-3 right-3 font-mono text-[9px] tracking-[0.22em] text-dew-mute bg-ink/60 px-2 py-1 rounded">flash 150ms</div>
                <div className="absolute bottom-3 left-3 font-mono text-[9px] tracking-[0.22em] text-dew-mute bg-ink/60 px-2 py-1 rounded">verde://eye — frame 0042</div>
                <div className="absolute bottom-3 right-3 font-mono text-[9px] tracking-[0.22em] text-hydro bg-ink/60 px-2 py-1 rounded">POST /api/upload-photo</div>
              </div>
            </TiltCard>
          </Reveal>
        </div>
      </section>

      {/* ————— PROVIDER CHAIN (interactive kill-switches) ————— */}
      <section className="px-6 md:px-16 py-16 md:py-24">
        <SplitReveal as="h2" text="ONE LEAF, THREE BRAINS." className="font-display font-extrabold text-4xl md:text-6xl leading-none" />
        <Reveal variant="blur" delay={0.1}>
          <p className="mt-4 max-w-xl text-dew-dim text-sm md:text-base">
            Every diagnosis races down a fallback chain.{" "}
            <span className="text-danger">Kill a provider</span> — tap its
            switch — and watch the route re-light around the corpse.
          </p>
        </Reveal>

        <RevealGroup className="mt-10 grid lg:grid-cols-3 gap-4" stagger={0.08}>
          {PROVIDERS.map((p, i) => {
            const isDown = down[p.id];
            const isServing = activeVision?.id === p.id || (p.id === "openrouter" && !isDown);
            return (
              <div key={p.id} className="relative">
                <GlowCard
                  color={isDown ? "255,92,108" : p.id === "kindwise" ? "166,255,63" : p.id === "gemini" ? "167,139,250" : "103,232,249"}
                  className={`rounded-2xl border p-6 h-full transition-colors ${isDown ? "border-danger/40 bg-danger/[0.04]" : isServing ? "border-white/20 bg-white/[0.04]" : "border-white/10 bg-white/[0.02]"}`}
                >
                  <div className="relative flex items-start justify-between gap-3">
                    <div>
                      <div className="font-mono text-[9px] tracking-[0.28em] text-dew-mute">
                        {p.vision ? (i === 0 ? "PRIMARY" : `FALLBACK ${i}`) : "CHAT ONLY"}
                      </div>
                      <div className={`font-display font-bold text-xl mt-1 ${isDown ? "line-through text-dew-mute" : "text-dew"}`}>
                        <ScrambleText text={p.name} hover root="div" />
                      </div>
                    </div>
                    {/* kill switch */}
                    <button
                      onClick={() => setDown((d) => ({ ...d, [p.id]: !d[p.id] }))}
                      aria-pressed={isDown}
                      data-tip={isDown ? `revive ${p.name}` : `kill ${p.name} — watch the chain reroute`}
                      className={`relative h-6 w-11 shrink-0 rounded-full border transition-colors ${isDown ? "bg-danger/25 border-danger/50" : "bg-lime/15 border-lime/40"}`}
                    >
                      <motion.span
                        layout
                        className={`absolute top-0.5 h-[18px] w-[18px] rounded-full ${isDown ? "bg-danger" : "bg-lime"}`}
                        animate={{ left: isDown ? 4 : 22 }}
                        transition={{ type: "spring", stiffness: 420, damping: 26 }}
                      />
                    </button>
                  </div>
                  <div className={`relative mt-2 font-mono text-[10px] ${isDown ? "text-danger" : "text-dew-mute"}`}>
                    {isDown ? "✕ DOWN — chain rerouting" : `● live · ${p.latency}`} · {p.role}
                  </div>
                  <p className="relative mt-3 text-[13px] leading-relaxed text-dew-dim">{p.note}</p>
                  {isServing && !isDown && (
                    <div className="absolute -top-px -right-px font-mono text-[8px] tracking-[0.24em] text-ink bg-lime px-2.5 py-1 rounded-bl-xl rounded-tr-2xl font-bold">
                      SERVING
                    </div>
                  )}
                </GlowCard>
                {i < PROVIDERS.length - 1 && (
                  <span className={`hidden lg:block absolute top-1/2 -right-4 -translate-y-1/2 z-10 font-mono text-sm transition-colors ${activeVision && !isDown ? "text-lime" : "text-white/20"}`}>
                    {down[p.id] ? "↷" : "→"}
                  </span>
                )}
              </div>
            );
          })}
        </RevealGroup>

        {/* served-by readout */}
        <Reveal variant="up" delay={0.1}>
          <div className="mt-6 rounded-xl border border-white/10 bg-ink-2/80 px-5 py-4 flex flex-wrap items-center gap-x-6 gap-y-2 font-mono text-[11px]">
            <span className="text-dew-mute uppercase tracking-[0.24em] text-[9px]">diagnosis served by</span>
            <motion.span
              key={servedBy}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              className={`font-bold ${activeVision ? (activeVision.id === "kindwise" ? "text-lime" : "text-uv") : "text-amber"}`}
            >
              {servedBy}
            </motion.span>
            {anyDown && (
              <Magnetic strength={0.3}>
                <button
                  onClick={() => setDown({ kindwise: false, gemini: false, openrouter: false })}
                  className="ml-auto font-mono text-[10px] uppercase tracking-[0.2em] text-hydro hover:text-lime transition-colors"
                >
                  ↺ revive the whole chain
                </button>
              </Magnetic>
            )}
          </div>
        </Reveal>
      </section>

      {/* ————— THE RX ————— */}
      <section className="px-6 md:px-16 py-16 md:pb-24">
        <div className="grid lg:grid-cols-[1fr_1.2fr] gap-10 items-center">
          <div>
            <SplitReveal as="h2" text="THE PRESCRIPTION." className="font-display font-extrabold text-[1.65rem] sm:text-4xl md:text-6xl leading-none" />
            <Reveal variant="blur" delay={0.1}>
              <p className="mt-4 max-w-md text-dew-dim text-sm md:text-base leading-relaxed">
                What ninety seconds of leaf-flirtation gets you. This is the
                actual diagnosis shape from the live pipeline — tulsi, our
                founding patient, still on record at{" "}
                <ShinyText text="94% confidence" className="text-lime" />.
              </p>
            </Reveal>
            <Reveal variant="up" delay={0.15}>
              <div className="mt-6 flex flex-wrap gap-2.5 font-mono text-[10px] uppercase tracking-[0.2em] text-dew-mute">
                <span className="chip">kindwise ?details params</span>
                <span className="chip">pure base64 — no data-url junk</span>
                <span className="chip">api-key header</span>
              </div>
            </Reveal>
          </div>

          <Reveal variant="scale">
            <TiltCard max={6}>
              <GlowCard color="167,139,250" size={320} className="rounded-2xl shadow-glow-uv">
                <div className="relative overflow-hidden rounded-2xl border border-white/12 bg-[#0d1a14]">
                  {/* pad header */}
                  <div className="border-b border-white/10 px-7 py-5 flex items-center justify-between">
                    <div>
                      <div className="font-display font-extrabold text-2xl tracking-tight text-dew">
                        ℞ <span className="text-uv">verde clinic</span>
                      </div>
                      <div className="font-mono text-[9px] tracking-[0.26em] text-dew-mute mt-1">plant-hood general · est. ₹1,890</div>
                    </div>
                    <div className="font-mono text-[9px] tracking-[0.2em] text-right text-dew-mute">
                      case #0001<br />delhi, in
                    </div>
                  </div>
                  {/* ruled rows */}
                  <div className="px-7 py-4" style={{ backgroundImage: "repeating-linear-gradient(transparent, transparent 35px, rgba(233,255,242,0.06) 36px)" }}>
                    {RX_ROWS.map((r) => (
                      <div key={r.k} className="grid grid-cols-[110px_1fr] gap-4 py-2 font-mono text-[11px] md:text-xs items-baseline">
                        <span className="text-uv/80 uppercase tracking-[0.18em] text-[9px]">{r.k}</span>
                        <span className={r.c ?? "text-dew-dim"}>{r.v}</span>
                      </div>
                    ))}
                  </div>
                  {/* signature + stamp */}
                  <div className="px-7 py-5 flex items-end justify-between border-t border-white/10">
                    <div>
                      <div className="font-mono text-[9px] tracking-[0.2em] text-dew-mute mb-1">signed,</div>
                      <div className="font-display italic font-bold text-xl text-hydro -rotate-2">dr. verde · md(flora)</div>
                    </div>
                    <div className="rotate-[-8deg] rounded-md border-2 border-lime/70 px-3 py-1.5 font-mono text-[9px] font-bold tracking-[0.22em] text-lime">
                      13/13 TESTS ✓
                    </div>
                  </div>
                </div>
              </GlowCard>
            </TiltCard>
          </Reveal>
        </div>
      </section>

      {/* ————— next door ————— */}
      <section className="px-6 md:px-16 pb-24">
        <TransitionLink href="/proof" label="Proof Wall" data-cursor="enter" className="group relative block overflow-hidden border border-amber/30 rounded-2xl px-8 py-10 glass hover:border-amber/70 transition-colors">
          <GlowCard className="absolute inset-0 rounded-2xl" color="255,194,75" size={300} />
          <div className="relative font-mono text-[10px] tracking-[0.3em] text-amber uppercase mb-3">next room · batch b5</div>
          <div className="relative font-display font-extrabold text-3xl md:text-5xl group-hover:text-amber transition-colors">
            PROOF WALL — 13/13 and the 10 bugs that died <span className="inline-block transition-transform group-hover:translate-x-2">→</span>
          </div>
        </TransitionLink>
      </section>
    </main>
  );
}
