"use client";

import { useCallback, useState } from "react";
import { motion } from "framer-motion";
import StormCanvas, { type StormMode } from "@/components/fx/StormCanvas";
import TransitionLink from "@/components/nav/TransitionLink";
import GlowCard from "@/components/fx/GlowCard";
import ScrambleText from "@/components/fx/Scramble";
import CountUp from "@/components/fx/CountUp";
import Magnetic from "@/components/fx/Magnetic";

const CASEFILE = [
  { n: "01", t: "THE SYMPTOM", c: "danger", body: "Every ~10 seconds the dashboard froze for a beat. Scroll, buttons, charts — everything hiccupped on schedule, like the app had a pacemaker with a loose wire." },
  { n: "02", t: "THE SUSPECT", c: "amber", body: "AUTO mode refreshes telemetry on a 10s heartbeat. The stutter landed exactly on that beat — too regular to be chance, too rhythmic to be hardware." },
  { n: "03", t: "THE EVIDENCE", c: "amber", body: "Serial logs + network tab: each refresh fired SEVENTEEN separate REST reads — one per sensor field, one per control flag — each blocking parse, re-render, paint." },
  { n: "04", t: "THE VERDICT", c: "danger", body: "Not Firebase. Not WiFi. Death by a thousand GETs: the JSON schema was flat, so the dashboard fetched node by node and choked its own main thread." },
  { n: "05", t: "THE SURGERY", c: "lime", body: "Firmware now bundles everything into ONE /sensors JSON push. Dashboard does one read for the bundle + one for /actuators transitions. 17 calls → 2. Stutter: extinct." },
  { n: "06", t: "THE DISCHARGE", c: "lime", body: "13/13 checklist passes, 60s cloud heartbeat, 8s watchdog never fired since. The scar stays in the commit log so we remember the lesson." },
];

const PIPELINE = [
  { k: "SENSE", d: "5 sensors, 1 eye", tip: "soil · temp/humidity · light · tank sonar + the SVGA leaf cam" },
  { k: "FILTER", d: "10-pt rings + 5-pt tank", tip: "ring-buffer medians — a splash or a sunbeam can't fake a reading" },
  { k: "DECIDE", d: "35% ± 2 hysteresis", tip: "waters below 35% moisture, stops above 37% — the 2% band kills pump chatter at the threshold" },
  { k: "ACT", d: "pump + UV, boot-safe", tip: "relay is active-LOW, UV gated after boot — GPIO floats can't fire anything mid-boot" },
  { k: "REPORT", d: "one bundle / 60s", tip: "the fix born from the 10s stutter — one JSON push, not seventeen" },
];

const TERMINAL_LINES = [
  { t: "// --- Code_1_Main_Brain.ino · v3.0.7-FINAL (593 lines) ---", c: "text-dew-mute" },
  { t: "const uint8_t PUMP_RELAY   = 5;   // ACTIVE-LOW, boot-safe", c: "text-dew-dim" },
  { t: "const uint8_t MOISTURE_PWR = 23;  // probe powered 30ms/read only", c: "text-dew-dim" },
  { t: "#define MOISTURE_THRESHOLD 35", c: "text-lime" },
  { t: "#define HYSTERESIS          2     // anti-chatter band", c: "text-lime" },
  { t: "esp_task_wdt_init(8, true);       // 8s watchdog — bite, never hang", c: "text-hydro" },
  { t: "WiFiMulti wifiMulti;  // Airtel → Oppo A17K → CCA SCHOOL", c: "text-hydro" },
  { t: "preferences.begin(\"verde\", false); // NVS — survives power cuts", c: "text-dew-dim" },
  { t: "// v2.0.0-fix: bundle ALL telemetry into ONE json push — 17 calls → 2", c: "text-amber" },
  { t: "// the stutter died here.", c: "text-amber" },
];

export default function BrainPage() {
  const [mode, setMode] = useState<StormMode>("storm");
  const [cycles, setCycles] = useState(0);
  const [calls, setCalls] = useState(0);
  const onCycle = useCallback((n: number) => {
    setCycles((c) => c + 1);
    setCalls((c) => c + n);
  }, []);
  const storm = mode === "storm";

  return (
    <main className="relative">
      {/* ————— header ————— */}
      <section className="relative min-h-[66vh] flex flex-col justify-end px-6 md:px-16 pb-14 pt-36 overflow-hidden">
        <div className="absolute inset-0 bg-grid-thin bg-grid-44 opacity-60" aria-hidden />
        <span className="chip border-lime/40 bg-lime-ghost text-lime w-fit mb-6">● live · batch B3</span>
        <h1 className="font-display font-extrabold leading-[0.92] tracking-tight text-[13vw] md:text-[7.5rem]">
          THE BRAIN<span className="text-lime">.</span>
        </h1>
        <p className="mt-5 max-w-xl text-dew-dim text-base md:text-lg leading-relaxed">
          593 lines of C++ that nearly lost to{" "}
          <span className="text-danger">seventeen HTTP calls</span> — and the
          one-line-idea surgery that saved it. Firmware v3.0.7-FINAL, running
          reboot-free to this day.
        </p>
        <div className="mt-8 flex flex-wrap gap-3 font-mono text-[10px] uppercase tracking-[0.22em] text-dew-mute">
          <span className="chip">8s watchdog</span>
          <span className="chip">3-network failsafe</span>
          <span className="chip">nvs persistence</span>
          <span className="chip text-lime border-lime/30">17 → 2 calls</span>
        </div>
      </section>

      {/* ————— THE STORM (interactive) ————— */}
      <section className="px-6 md:px-16 py-16 md:py-24">
        <div className="flex items-end justify-between flex-wrap gap-6 mb-8">
          <div>
            <h2 className="font-display font-extrabold text-4xl md:text-6xl leading-none">
              THE STORM<span className="text-uv">.</span>
            </h2>
            <p className="mt-3 max-w-lg text-dew-dim text-sm md:text-base">
              Flip the switch. Left: the bug as diagnosed — watch for the red
              10s stutter. Right: the shipped fix.
            </p>
          </div>

          {/* before/after toggle */}
          <Magnetic strength={0.25}>
            <div className="relative flex rounded-full border border-white/12 bg-ink-2/80 p-1 font-mono text-[10px] uppercase tracking-[0.2em]">
              <motion.span
                layout
                className={`absolute top-1 bottom-1 w-[calc(50%-4px)] rounded-full ${storm ? "bg-danger/20 border border-danger/40" : "bg-lime/15 border border-lime/40"}`}
                animate={{ left: storm ? 4 : "calc(50% + 0px)" }}
                transition={{ type: "spring", stiffness: 320, damping: 28 }}
              />
              <button
                onClick={() => setMode("storm")}
                className={`relative z-10 px-4 md:px-5 py-2.5 rounded-full whitespace-nowrap transition-colors ${storm ? "text-danger" : "text-dew-mute hover:text-dew"}`}
                aria-pressed={storm}
              >
                <ScrambleText text="before · 17 calls" hover />
              </button>
              <button
                onClick={() => setMode("fixed")}
                className={`relative z-10 px-4 md:px-5 py-2.5 rounded-full whitespace-nowrap transition-colors ${!storm ? "text-lime" : "text-dew-mute hover:text-dew"}`}
                aria-pressed={!storm}
              >
                <ScrambleText text="after · 2 calls" hover />
              </button>
            </div>
          </Magnetic>
        </div>

        <div className="relative h-[62vh] min-h-[380px] rounded-2xl border border-white/10 bg-ink-2/60 overflow-hidden glass">
          <StormCanvas mode={mode} onCycle={onCycle} />
          {/* HUD */}
          <div className="absolute top-4 left-4 flex gap-3 font-mono text-[10px] uppercase tracking-[0.2em]">
            <span className={`chip ${storm ? "border-danger/40 text-danger" : "border-lime/40 text-lime"}`}>
              {storm ? "anomaly live" : "nominal"}
            </span>
            <span className="chip border-white/10 text-dew-mute hidden sm:inline">c dbg feed · simulated on real constants</span>
          </div>
          <div className="absolute bottom-4 left-4 right-4 flex flex-wrap gap-x-8 gap-y-2 font-mono text-[10px] uppercase tracking-[0.2em] text-dew-mute">
            <span>cycles <span className="text-dew"><CountUp to={cycles} duration={0.4} /></span></span>
            <span>api calls <span className={storm ? "text-danger" : "text-lime"}><CountUp to={calls} duration={0.4} /></span></span>
            <span className="ml-auto hidden md:inline">{storm ? "ui: blocked every 10s" : "ui: 60fps, unbothered"}</span>
          </div>
        </div>
      </section>

      {/* ————— CASE FILE ————— */}
      <section className="px-6 md:px-16 py-16 md:py-24">
        <h2 className="font-display font-extrabold text-4xl md:text-6xl leading-none mb-3">
          CASE FILE: THE 10s STUTTER<span className="text-uv">.</span>
        </h2>
        <p className="text-dew-dim max-w-xl mb-10">
          The bug that nearly killed Project Verde, written down as it
          actually happened. Hover a card — it glows where your cursor lands.
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {CASEFILE.map((c) => (
            <GlowCard
              key={c.n}
              color={c.c === "lime" ? "166,255,63" : c.c === "danger" ? "255,92,108" : "255,194,75"}
              className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 min-h-[210px] flex flex-col"
            >
              <span className={`relative font-mono text-[10px] tracking-[0.3em] ${c.c === "lime" ? "text-lime" : c.c === "danger" ? "text-danger" : "text-amber"}`}>
                {c.n} · <ScrambleText text={c.t} hover root="div" />
              </span>
              <p className="relative mt-4 text-dew-dim text-sm leading-relaxed">{c.body}</p>
            </GlowCard>
          ))}
        </div>
      </section>

      {/* ————— PIPELINE ————— */}
      <section className="px-6 md:px-16 py-16 md:py-24">
        <h2 className="font-display font-extrabold text-4xl md:text-6xl leading-none mb-3">
          THE LOOP THAT NEVER SLEEPS<span className="text-lime">.</span>
        </h2>
        <p className="text-dew-dim max-w-xl mb-10">
          Every 10 seconds, forever. Hover a stage for the engineering notes.
        </p>
        <div className="grid md:grid-cols-5 gap-3">
          {PIPELINE.map((s, i) => (
            <div key={s.k} className="relative" data-tip={s.tip}>
              <GlowCard className="rounded-xl border border-white/10 bg-ink-2/70 px-5 py-6 h-full hover:border-lime/50 transition-colors">
                <div className="relative font-mono text-[9px] tracking-[0.3em] text-dew-mute">0{i + 1}</div>
                <div className="relative font-display font-extrabold text-xl md:text-2xl text-lime mt-1">
                  <ScrambleText text={s.k} hover root="div" />
                </div>
                <div className="relative mt-2 font-mono text-[10px] text-dew-dim leading-relaxed">{s.d}</div>
              </GlowCard>
              {i < PIPELINE.length - 1 && (
                <span className="hidden md:block absolute top-1/2 -right-3 -translate-y-1/2 font-mono text-lime/60 text-sm z-10">→</span>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ————— TERMINAL ————— */}
      <section className="px-6 md:px-16 py-16 md:pb-28">
        <div className="rounded-2xl border border-white/10 bg-ink-2/80 overflow-hidden">
          <div className="flex items-center gap-2 px-5 py-3 border-b border-white/[0.07]">
            <span className="h-2 w-2 rounded-full bg-danger/80" />
            <span className="h-2 w-2 rounded-full bg-amber/80" />
            <span className="h-2 w-2 rounded-full bg-lime/80" />
            <span className="ml-3 font-mono text-[10px] uppercase tracking-[0.24em] text-dew-mute">verde@esp32: ~/firmware — cat main.ino</span>
          </div>
          <div className="px-5 md:px-7 py-6 font-mono text-[11px] md:text-xs leading-[1.9] overflow-x-auto">
            {TERMINAL_LINES.map((l, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -10 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-12% 0px" }}
                transition={{ delay: i * 0.09, duration: 0.4 }}
                className={`whitespace-pre ${l.c}`}
              >
                <span className="text-dew-mute/60 select-none mr-4 inline-block w-6 text-right">{i + 1}</span>
                {l.t}
              </motion.div>
            ))}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: TERMINAL_LINES.length * 0.09 + 0.2 }}
              className="mt-2 text-lime"
            >
              <span className="text-dew-mute/60 select-none mr-4 inline-block w-6 text-right">$</span>
              <span className="animate-blinker">▊</span> uptime: still zero reboots
            </motion.div>
          </div>
        </div>
      </section>

      {/* ————— next door ————— */}
      <section className="px-6 md:px-16 pb-24">
        <TransitionLink href="/doctor" label="AI Doctor" data-cursor="enter" className="group relative block overflow-hidden border border-uv/30 rounded-2xl px-8 py-10 glass hover:border-uv/70 transition-colors">
          <GlowCard className="absolute inset-0 rounded-2xl" color="167,139,250" size={300} />
          <div className="relative font-mono text-[10px] tracking-[0.3em] text-uv uppercase mb-3">next room · batch b4</div>
          <div className="relative font-display font-extrabold text-3xl md:text-5xl group-hover:text-uv transition-colors">
            AI DOCTOR — the leaf gets a diagnosis <span className="inline-block transition-transform group-hover:translate-x-2">→</span>
          </div>
        </TransitionLink>
      </section>
    </main>
  );
}
