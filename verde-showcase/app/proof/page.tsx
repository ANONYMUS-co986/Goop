"use client";

import { useEffect, useState } from "react";
import {
  ArrowDown,
  ArrowRight,
  Bug,
  CheckCircle2,
  FlaskConical,
  ShieldCheck,
  Timer,
  Wrench,
  Zap,
} from "lucide-react";
import SplitReveal from "@/components/fx/SplitReveal";
import { Reveal, AssembleGroup } from "@/components/fx/Reveal";
import CountUp from "@/components/fx/CountUp";
import GlowCard from "@/components/fx/GlowCard";
import ShinyText from "@/components/fx/ShinyText";
import VelocityMarquee from "@/components/fx/VelocityMarquee";
import Parallax from "@/components/fx/Parallax";
import ScrambleText from "@/components/fx/Scramble";
import StarBorder from "@/components/fx/StarBorder";
import PixelCard from "@/components/fx/PixelCard";
import ScrollStack from "@/components/fx/ScrollStack";
import Magnetic from "@/components/fx/Magnetic";
import TransitionLink from "@/components/nav/TransitionLink";

/* ————— THE THIRTEEN — every test had a trigger + pass condition written
   down BEFORE we ran it. (source: the project logbook, page 21-22) ————— */
const TESTS = [
  { id: "T01", name: "WiFi / boot", desc: "Joins the saved network cleanly from cold power.", tag: "hardware" },
  { id: "T02", name: "Watchdog soak — 10+ min", desc: "Continuous uptime under full load. Reboots: zero.", tag: "firmware" },
  { id: "T03", name: "Rain override", desc: "Forced the flag; AUTO held even with parched soil.", tag: "firmware" },
  { id: "T04", name: "DHT11 breathe test", desc: "One sigh on the sensor; humidity tile climbs, then settles.", tag: "sensor" },
  { id: "T05", name: "Moisture water-dunk", desc: "Probe dunked; reading sweeps, filtered, no wild spikes.", tag: "sensor" },
  { id: "T06", name: "LDR cover test", desc: "A thumb over the sensor = dark; grow light glides on.", tag: "sensor" },
  { id: "T07", name: "Ultrasonic hand test", desc: "Hand moved in the tank; distance tracks, splash junk rejected.", tag: "sensor" },
  { id: "T08", name: "Pump AUTO — 120s soak", desc: "Two minutes of continuous watering. No glitch, no stutter.", tag: "actuator" },
  { id: "T09", name: "OFF exactly at threshold", desc: "Moisture crossed 35% mid-run; pump stopped on the line.", tag: "actuator" },
  { id: "T10", name: "Tank lock", desc: "Emptied the tank; AUTO and manual both refused. Pump saved.", tag: "actuator" },
  { id: "T11", name: "CAM capture ≤ 2s", desc: "Button to base64 photo on screen. Timed. Twice.", tag: "ai" },
  { id: "T12", name: "Plant Doctor diagnosis", desc: "Test scan identified at 94% with a treatment plan.", tag: "ai" },
  { id: "T13", name: "AI chats + fallbacks", desc: "Both assistants answered; killing model 1 promoted model 2. Silently.", tag: "ai" },
];

/* ————— THE TOMBSTONES — ten bugs, zero hidden (logbook, page 23) ————— */
type Tomb = {
  id: string;
  sev: "ELECTRICAL" | "SOFTWARE + CLOUD";
  title: string;
  cause: string;
  fix: string;
};
const TOMBS: Tomb[] = [
  { id: "01", sev: "SOFTWARE + CLOUD", title: "AUTO pump clicks every ~10s", cause: "17 blocking Firebase calls/sec → watchdog loop", fix: "JSON bundling → 2 calls/sec" },
  { id: "02", sev: "ELECTRICAL", title: "Camera probe error 0x106", cause: "FPC ribbon unseated", fix: "Reseat gold-side down + full power cycle" },
  { id: "03", sev: "ELECTRICAL", title: "\"PSRAM not found\" at boot", cause: "Weak power, not missing RAM", fix: "Dumb 5V / 2A adapter" },
  { id: "04", sev: "ELECTRICAL", title: "Boot crash 0x20002", cause: "Camera + WiFi power surge at boot", fix: "Sequential boot: camera first, WiFi after 500ms" },
  { id: "05", sev: "ELECTRICAL", title: "WiFi dies when camera runs", cause: "20MHz XCLK radio interference", fix: "Throttle XCLK to 8MHz" },
  { id: "06", sev: "ELECTRICAL", title: "67W USB-PD brick starves board", cause: "PD needs a handshake chip we lack", fix: "Same 5V / 2A phone adapter" },
  { id: "07", sev: "ELECTRICAL", title: "Relay dead on arrival… not", cause: "Split breadboard rails", fix: "Bridge rails: + to +, − to −" },
  { id: "08", sev: "ELECTRICAL", title: "Temperature reads 0°C", cause: "DHT on the wrong pin, floating ground", fix: "GPIO 4 + shared GND" },
  { id: "09", sev: "SOFTWARE + CLOUD", title: "Firebase updates in spurts", cause: "13 calls/sec of tiny writes", fix: "One bundled call per second" },
  { id: "10", sev: "SOFTWARE + CLOUD", title: "Mystery compile error", cause: "Whitespace corrupted in a copy-paste", fix: "Re-download the source; stop hand-copying" },
];

function SessionClock() {
  const [s, setS] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setS((v) => v + 1), 1000);
    return () => clearInterval(t);
  }, []);
  const hh = String(Math.floor(s / 3600)).padStart(2, "0");
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  return (
    <span className="tabular-nums text-dew" data-tip="live: seconds since you opened this wall. the rig's own uptime story is better — scroll up.">
      {hh}:{mm}:{ss}
    </span>
  );
}

function scrollToId(id: string) {
  const lenis = (window as unknown as { __lenis?: { scrollTo: (t: string, o?: object) => void } }).__lenis;
  if (lenis) lenis.scrollTo(id, { offset: -70, duration: 1.6 });
  else document.querySelector(id)?.scrollIntoView({ behavior: "smooth" });
}

export default function ProofPage() {
  return (
    <main className="relative min-h-[100svh] bg-ink bg-grid-thin bg-grid-44 overflow-x-clip">
      {/* ghost numeral */}
      <Parallax speed={0.4} className="pointer-events-none absolute -top-6 right-0 z-0">
        <span className="font-display font-bold text-[42vw] md:text-[24rem] leading-none text-stroke-ghost select-none">04</span>
      </Parallax>

      {/* ————— HERO — the receipts counter ————— */}
      <header className="relative z-10 px-6 md:px-16 pt-28 md:pt-36 pb-10 md:pb-14">
        <div className="chip border-amber/40 bg-amber/10 text-amber mb-7">
          <FlaskConical size={12} strokeWidth={2.2} />
          wing 04 · the proof wall
        </div>
        <SplitReveal
          as="h1"
          text="RECEIPTS."
          className="font-display font-extrabold uppercase tracking-tight leading-[0.9] text-[2.4rem] sm:text-[11vw] lg:text-[8.5rem] text-dew"
        />
        <p className="mt-6 max-w-xl text-dew-dim text-sm md:text-base leading-relaxed">
          &quot;It worked once&quot; is an anecdote. This wall is the other
          thing: <span className="text-amber">13/13 tests</span> with written
          pass conditions, <span className="text-amber">10 bugs</span> buried
          in public, and <span className="text-amber">zero reboots</span> when
          we tried to kill it.
        </p>
        <div className="mt-8 flex flex-wrap gap-2">
          <span className="chip text-lime border-lime/30">13/13 tests pass</span>
          <span className="chip text-amber border-amber/30">0 reboots · 10-min soak</span>
          <span className="chip text-dew-dim border-white/12">10 bugs, zero hidden</span>
          <span className="chip text-uv border-uv/30 hidden sm:inline-flex">6/10 were power</span>
        </div>

        {/* stat trio */}
        <AssembleGroup className="mt-12 grid md:grid-cols-3 gap-4" stagger={0.12} distance={140}>
          <PixelCard accent="#FFC24B" className="glass-deep rounded-3xl">
            <div className="p-7" data-cursor="tests">
              <div className="font-display font-extrabold text-5xl md:text-6xl text-dew">
                <CountUp to={13} duration={1.2} /><span className="text-dew-mute text-3xl md:text-4xl">/13</span>
              </div>
              <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.24em] text-amber">system tests passing</p>
              <p className="mt-2 text-xs text-dew-dim leading-relaxed">Every test had a trigger and a pass condition written down before we ran it.</p>
            </div>
          </PixelCard>

          <StarBorder color="#FFC24B" speed="4.5s" className="glass-deep" innerClassName="bg-ink-2/60">
            <div className="p-7" data-cursor="soak">
              <div className="font-display font-extrabold text-5xl md:text-6xl text-dew">
                <CountUp to={0} duration={0.8} />
              </div>
              <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.24em] text-amber">reboots in a 10-min torture soak</p>
              <p className="mt-2 text-xs text-dew-dim leading-relaxed">The 8-second hardware watchdog held the line while we threw everything at it.</p>
            </div>
          </StarBorder>

          <PixelCard accent="#A6FF3F" className="glass-deep rounded-3xl">
            <div className="p-7" data-cursor="bugs">
              <div className="font-display font-extrabold text-5xl md:text-6xl text-dew">
                <CountUp to={10} duration={1.4} />
              </div>
              <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.24em] text-lime">bugs buried in public</p>
              <p className="mt-2 text-xs text-dew-dim leading-relaxed">Half our engineering education arrived wearing a bug costume. Published for the next team.</p>
            </div>
          </PixelCard>
        </AssembleGroup>

        <div className="mt-10 flex flex-wrap gap-3">
          <Magnetic strength={0.35}>
            <button
              onClick={() => scrollToId("#thirteen")}
              data-cursor="scan"
              className="rounded-full border border-lime/50 bg-lime-ghost text-lime px-7 py-3 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:bg-lime/20"
            >
              <ScrambleText text="scan the thirteen" hover /> <ArrowDown className="inline -mt-0.5" size={12} />
            </button>
          </Magnetic>
          <Magnetic strength={0.35}>
            <button
              onClick={() => scrollToId("#tombstones")}
              data-cursor="dig"
              className="rounded-full border border-white/12 bg-white/[0.03] text-dew px-7 py-3 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:border-amber/40 hover:text-amber"
            >
              <ScrambleText text="open the tombstones" hover /> <Bug className="inline -mt-0.5" size={12} />
            </button>
          </Magnetic>
        </div>
      </header>

      {/* ————— THE THIRTEEN — scan list ————— */}
      <section id="thirteen" className="relative z-10 px-6 md:px-16 py-16 md:py-24">
        <SplitReveal as="h2" text="THE THIRTEEN." className="font-display font-extrabold text-4xl md:text-6xl leading-none" />
        <Reveal variant="blur" delay={0.1}>
          <p className="mt-3 max-w-lg text-dew-dim text-sm md:text-base">
            Thirteen tests, thirteen written pass conditions. Hover any row —
            the wall keeps the receipts.
          </p>
        </Reveal>

        <AssembleGroup className="mt-10 flex flex-col gap-2.5" stagger={0.06} distance={120}>
          {TESTS.map((t) => (
            <div
              key={t.id}
              data-cursor="PASS"
              data-tip={`${t.id} · tag: ${t.tag}. pass condition was written before the run.`}
              className="group flex items-center gap-4 md:gap-6 rounded-xl border border-white/[0.08] bg-ink-2/60 px-4 md:px-6 py-3.5 transition-all duration-300 hover:border-lime/40 hover:bg-ink-2 hover:translate-x-1.5 hover:shadow-[0_0_28px_-8px_rgba(166,255,63,0.35)]"
            >
              <span className="font-mono text-[11px] text-amber w-9 shrink-0">{t.id}</span>
              <span className="hidden sm:block w-1.5 h-1.5 rounded-full bg-lime/70 animate-blinker shrink-0" />
              <div className="min-w-0 flex-1">
                <div className="font-sans font-medium text-dew text-sm md:text-[15px] truncate">{t.name}</div>
                <div className="text-xs text-dew-dim leading-snug">{t.desc}</div>
              </div>
              <span className="chip border-lime/30 text-lime shrink-0 !py-1 !px-2.5">
                <CheckCircle2 size={11} /> PASS
              </span>
            </div>
          ))}
        </AssembleGroup>
      </section>

      {/* ————— TOMBSTONES — ScrollStack ————— */}
      <section id="tombstones" className="relative z-10 px-6 md:px-16 py-16 md:py-24">
        <div className="flex items-end justify-between flex-wrap gap-6 mb-10">
          <div>
            <SplitReveal as="h2" text="TEN TOMBSTONES." className="font-display font-extrabold text-4xl md:text-6xl leading-none" />
            <Reveal variant="blur" delay={0.1}>
              <p className="mt-3 max-w-lg text-dew-dim text-sm md:text-base">
                Ten bugs, zero hidden. They stack up as you scroll — each one
                reads: what died, why it died, what brought it back.
              </p>
            </Reveal>
          </div>
          <span className="chip border-danger/35 text-danger">
            <Bug size={12} /> all fixed · all documented
          </span>
        </div>

        <ScrollStack className="max-w-4xl mx-auto" topOffset={110} gap={15}>
          {TOMBS.map((b) => {
            const electrical = b.sev === "ELECTRICAL";
            return (
              <div
                key={b.id}
                className="rounded-3xl border border-white/10 bg-[#0A1612] p-6 md:p-9 mb-6 shadow-[0_-18px_60px_-30px_rgba(0,0,0,0.9)]"
                data-cursor="RIP"
                data-tip={`bug ${b.id}/10 · ${electrical ? "power or connection" : "code"} — fixed in the shipped firmware`}
              >
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <span className="font-display font-extrabold text-4xl md:text-6xl text-stroke-ghost leading-none select-none">{b.id}</span>
                    <div>
                      <div className={`chip ${electrical ? "border-amber/40 text-amber bg-amber/10" : "border-uv/40 text-uv bg-uv/10"}`}>
                        {electrical ? <Zap size={11} /> : <Bug size={11} />} {b.sev}
                      </div>
                      <h3 className="mt-2.5 font-display font-bold text-xl md:text-3xl text-dew leading-tight">{b.title}</h3>
                    </div>
                  </div>
                  <span className="chip border-lime/40 text-lime bg-lime/10 rotate-6 mt-1" >
                    <ShieldCheck size={11} /> fixed
                  </span>
                </div>
                <div className="mt-6 grid sm:grid-cols-[1fr_auto_1fr] items-center gap-4">
                  <div className="rounded-xl border border-danger/25 bg-danger/[0.06] px-4 py-3.5">
                    <div className="font-mono text-[9px] uppercase tracking-[0.26em] text-danger mb-1.5">cause of death</div>
                    <p className="text-[13px] text-dew-dim leading-snug">{b.cause}</p>
                  </div>
                  <ArrowRight className="hidden sm:block text-dew-mute" size={18} />
                  <div className="rounded-xl border border-lime/25 bg-lime/[0.06] px-4 py-3.5">
                    <div className="font-mono text-[9px] uppercase tracking-[0.26em] text-lime mb-1.5">the resurrection</div>
                    <p className="text-[13px] text-dew leading-snug">{b.fix}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </ScrollStack>

        {/* the pattern */}
        <Reveal variant="up" className="max-w-4xl mx-auto mt-6">
          <GlowCard color="255,194,75" className="rounded-3xl p-8 md:p-10 glass">
            <div className="flex items-start gap-4">
              <Wrench className="text-amber shrink-0 mt-1" size={22} />
              <div>
                <h3 className="font-display font-bold text-2xl md:text-3xl text-dew leading-tight">
                  <ShinyText text="six of ten bugs were power or connection, not code." speed={4.5} />
                </h3>
                <p className="mt-3 text-sm md:text-[15px] text-dew-dim leading-relaxed max-w-2xl">
                  That&apos;s why wiring discipline is firmware reliability.
                  The multimeter found more bugs than the compiler ever did —
                  hardware hygiene <span className="text-amber">is</span> debugging.
                </p>
              </div>
            </div>
          </GlowCard>
        </Reveal>
      </section>

      {/* ————— METHOD — zero-reboot wall ————— */}
      <section className="relative z-10 px-6 md:px-16 py-16 md:py-24">
        <div className="grid lg:grid-cols-2 gap-8 lg:gap-14 items-center">
          <div>
            <SplitReveal as="h2" text="THE METHOD." className="font-display font-extrabold text-4xl md:text-6xl leading-none" />
            <Reveal variant="blur" delay={0.1}>
              <p className="mt-5 max-w-md text-dew-dim text-sm md:text-base leading-relaxed">
                Every test had a trigger and a pass condition written down
                <span className="text-dew"> before</span> we ran it.
              </p>
            </Reveal>
            <Reveal variant="up" delay={0.15}>
              <blockquote className="mt-8 border-l-2 border-amber/60 pl-6 max-w-md">
                <p className="font-display font-bold text-2xl md:text-[2rem] leading-tight text-dew">
                  <ShinyText text="&quot;It worked once&quot; is an anecdote; &quot;13/13&quot; is a result." speed={5} />
                </p>
              </blockquote>
            </Reveal>
            <AssembleGroup className="mt-10 flex flex-col gap-2.5 max-w-md" stagger={0.08} distance={90} side="left" alternate={false}>
              {[
                "write the pass condition first",
                "run it twice, film it once",
                "publish the failures too",
              ].map((line) => (
                <div key={line} className="flex items-center gap-3 text-sm text-dew-dim rounded-lg border border-white/[0.07] bg-ink-2/60 px-4 py-2.5 transition-colors hover:border-amber/35">
                  <CheckCircle2 size={14} className="text-amber shrink-0" />
                  <span className="font-mono text-[11px] uppercase tracking-[0.18em]">{line}</span>
                </div>
              ))}
            </AssembleGroup>
          </div>

          <Reveal variant="scale">
            <div className="relative rounded-3xl border border-white/10 bg-ink-2/70 crt-scan p-8 md:p-12 overflow-hidden" data-cursor="soak">
              <StarBorder color="#A6FF3F" speed="6s" className="mx-auto w-fit" innerClassName="px-10 py-8 bg-ink/70">
                <div className="text-center">
                  <div className="font-display font-extrabold text-8xl md:text-9xl text-lime leading-none">
                    <CountUp to={0} duration={0.6} />
                  </div>
                  <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.3em] text-lime/80">reboots · 10-min soak</p>
                </div>
              </StarBorder>
              <div className="mt-10 grid grid-cols-2 gap-4 font-mono text-[10px] uppercase tracking-[0.2em] text-dew-mute">
                <div className="rounded-xl border border-white/[0.08] bg-ink/60 px-4 py-3">
                  watchdog <span className="block text-dew mt-1">8s window</span>
                </div>
                <div className="rounded-xl border border-white/[0.08] bg-ink/60 px-4 py-3">
                  firmware <span className="block text-dew mt-1">v3.0.7-final</span>
                </div>
                <div className="rounded-xl border border-white/[0.08] bg-ink/60 px-4 py-3">
                  soak <span className="block text-dew mt-1">600s @ full load</span>
                </div>
                <div className="rounded-xl border border-white/[0.08] bg-ink/60 px-4 py-3">
                  <Timer size={11} className="inline mr-1 -mt-0.5" />you on this wall
                  <span className="block mt-1"><SessionClock /></span>
                </div>
              </div>
              <p className="mt-8 text-center font-mono text-[9px] uppercase tracking-[0.32em] text-dew-mute">
                tried to kill it · it just stood there photosynthesizing
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ————— next wing gate ————— */}
      <section className="relative z-10 px-6 md:px-16 pb-20 md:pb-28">
        <Reveal variant="up">
          <GlowCard color="167,139,250" className="glass-deep rounded-3xl p-8 md:p-12 text-center">
            <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-uv mb-4">next wing · batch b6</p>
            <h3 className="font-display font-extrabold text-3xl md:text-5xl text-dew uppercase tracking-tight">
              <ScrambleText text="meet team verde" onMount />
            </h3>
            <p className="mt-4 max-w-lg mx-auto text-sm text-dew-dim leading-relaxed">
              Two builders, one greenhouse OS — the lit-fest wins, the
              two-AI-war anecdote, and who soldered what.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Magnetic strength={0.4}>
                <TransitionLink
                  href="/team"
                  label="Team Verde"
                  data-cursor="enter"
                  className="block rounded-full border border-uv/50 bg-uv/10 text-uv px-8 py-3.5 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:bg-uv/20"
                >
                  <ScrambleText text="enter the team wing" hover root="a" />
                </TransitionLink>
              </Magnetic>
              <TransitionLink
                href="/brain"
                label="The Brain"
                data-cursor="back"
                className="rounded-full border border-white/12 bg-white/[0.03] text-dew-mute px-8 py-3.5 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:text-dew hover:border-white/25"
              >
                ← revisit the brain
              </TransitionLink>
            </div>
          </GlowCard>
        </Reveal>
      </section>

      <footer className="relative z-10 border-t border-white/[0.07] bg-ink-2/80 py-3.5 overflow-hidden">
        <VelocityMarquee
          items={Array.from({ length: 4 }).flatMap(() => ["13/13 tests", "zero reboots", "10 bugs buried", "receipts kept"])}
        />
      </footer>
    </main>
  );
}
