import HeroSection from "@/components/three/HeroSection";
import { ROUTES } from "@/components/nav/nav";
import TransitionLink from "@/components/nav/TransitionLink";
import GlowCard from "@/components/fx/GlowCard";
import ScrambleText from "@/components/fx/Scramble";
import SplitReveal from "@/components/fx/SplitReveal";
import { Reveal, RevealGroup } from "@/components/fx/Reveal";
import VelocityMarquee from "@/components/fx/VelocityMarquee";

const LEDGER = [
  "17→2 CALLS/SEC", "8 MHZ XCLK", "₹1,890 BUILD", "13/13 TESTS",
  "94% CROP.HEALTH", "5 SENSORS · 2 MCUS", "SVGA LEAF CAM",
  "60 S HEARTBEAT", "3-NETWORK FAILSAFE", "8 S WATCHDOG", "ZERO SERVERS",
];

export default function Home() {
  return (
    <main className="bg-ink">
      <HeroSection />

      {/* THE SAGA — bento route map */}
      <section id="saga" className="relative px-6 md:px-10 py-24 md:py-32 bg-ink">
        <div className="mx-auto max-w-6xl">
          <Reveal variant="fade"><p className="font-mono text-[10px] uppercase tracking-[0.3em] text-lime mb-4">the saga // choose your wing</p></Reveal>
          <h2 className="font-display font-bold uppercase tracking-tight text-4xl md:text-6xl text-dew max-w-3xl leading-[0.95]">
            <SplitReveal as="span" text="Six rooms. " className="inline" />{" "}
            <SplitReveal as="span" text="One greenhouse" className="inline text-stroke-lime" delay={0.18} />{" "}
            <SplitReveal as="span" text="operating system." className="inline" delay={0.42} />
          </h2>
          <Reveal variant="blur" delay={0.15}>
            <p className="mt-6 max-w-2xl font-sans text-sm md:text-base text-dew-dim leading-relaxed">
              Every failure and every flex of Project Verde, staged room by room.
              Doors marked with their build batch light up as fabrication
              completes — starting with the Home hologram you just met.
            </p>
          </Reveal>

          <RevealGroup className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" stagger={0.07}>
            {ROUTES.map((r, i) => (
              <TransitionLink
                key={r.href}
                href={r.href}
                label={r.label}
                data-hover
                data-cursor={r.live ? "open" : `batch ${r.batch}`}
                className={`group relative overflow-hidden rounded-2xl border p-6 min-h-[190px] flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 ${
                  r.live
                    ? "border-lime/35 bg-gradient-to-br from-lime-ghost to-transparent shadow-glow-lime"
                    : "border-white/10 bg-white/[0.03] hover:border-lime/25"
                } ${i === 0 ? "sm:col-span-2 lg:col-span-2" : ""}`}
              >
                <GlowCard className="absolute inset-0 rounded-2xl" />
                <span className="absolute -right-3 -top-6 font-display font-bold text-8xl text-stroke-ghost select-none transition-colors group-hover:text-stroke-lime">
                  {r.ghost}
                </span>
                <div className="relative">
                  <span className={`chip ${r.live ? "border-lime/40 bg-lime-ghost text-lime" : "border-white/10 bg-white/[0.04] text-dew-mute"}`}>
                    {r.live ? "● live now" : `◌ batch ${r.batch}`}
                  </span>
                  <h3 className="mt-4 font-display font-bold uppercase text-2xl text-dew group-hover:text-lime transition-colors">
                    <ScrambleText text={r.label} hover root="a" />
                  </h3>
                  <p className="mt-2 font-sans text-[13px] text-dew-dim leading-relaxed max-w-[240px]">{r.blurb}</p>
                </div>
                <div className="relative mt-5 font-mono text-[10px] uppercase tracking-[0.26em] text-dew-mute group-hover:text-lime transition-colors">
                  open door <span className="inline-block transition-transform group-hover:translate-x-1.5">→</span>
                </div>
              </TransitionLink>
            ))}
          </RevealGroup>
        </div>
      </section>

      {/* ledger marquee footer — scroll velocity reactive */}
      <footer className="border-t border-white/[0.07] bg-ink-2/80 py-4 overflow-hidden">
        <VelocityMarquee items={LEDGER} />
      </footer>
    </main>
  );
}
