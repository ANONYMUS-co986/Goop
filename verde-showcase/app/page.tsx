import Link from "next/link";
import HeroSection from "@/components/three/HeroSection";
import { ROUTES } from "@/components/nav/nav";

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
          <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-lime mb-4">the saga // choose your wing</p>
          <h2 className="font-display font-bold uppercase tracking-tight text-4xl md:text-6xl text-dew max-w-3xl leading-[0.95]">
            Six rooms. <span className="text-stroke-lime">One greenhouse</span> operating system.
          </h2>
          <p className="mt-6 max-w-2xl font-sans text-sm md:text-base text-dew-dim leading-relaxed">
            Every failure and every flex of Project Verde, staged room by room.
            Doors marked with their build batch light up as fabrication
            completes — starting with the Home hologram you just met.
          </p>

          <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {ROUTES.map((r, i) => (
              <Link
                key={r.href}
                href={r.href}
                data-hover
                className={`group relative overflow-hidden rounded-2xl border p-6 min-h-[190px] flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 ${
                  r.live
                    ? "border-lime/35 bg-gradient-to-br from-lime-ghost to-transparent shadow-glow-lime"
                    : "border-white/10 bg-white/[0.03] hover:border-lime/25"
                } ${i === 0 ? "sm:col-span-2 lg:col-span-2" : ""}`}
              >
                <span className="absolute -right-3 -top-6 font-display font-bold text-8xl text-stroke-ghost select-none transition-colors group-hover:text-stroke-lime">
                  {r.ghost}
                </span>
                <div>
                  <span className={`chip ${r.live ? "border-lime/40 bg-lime-ghost text-lime" : "border-white/10 bg-white/[0.04] text-dew-mute"}`}>
                    {r.live ? "● live now" : `◌ batch ${r.batch}`}
                  </span>
                  <h3 className="mt-4 font-display font-bold uppercase text-2xl text-dew group-hover:text-lime transition-colors">
                    {r.label}
                  </h3>
                  <p className="mt-2 font-sans text-[13px] text-dew-dim leading-relaxed max-w-[240px]">{r.blurb}</p>
                </div>
                <div className="mt-5 font-mono text-[10px] uppercase tracking-[0.26em] text-dew-mute group-hover:text-lime transition-colors">
                  open door <span className="inline-block transition-transform group-hover:translate-x-1.5">→</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ledger marquee footer */}
      <footer className="border-t border-white/[0.07] bg-ink-2/80 py-4 overflow-hidden">
        <div className="flex w-max animate-marquee whitespace-nowrap">
          {[0, 1].map((rep) => (
            <div key={rep} className="flex shrink-0">
              {LEDGER.map((t, i) => (
                <span key={`${rep}-${i}`} className="mx-6 font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute">
                  {t} <span className="text-lime/60 ml-6">//</span>
                </span>
              ))}
            </div>
          ))}
        </div>
      </footer>
    </main>
  );
}
