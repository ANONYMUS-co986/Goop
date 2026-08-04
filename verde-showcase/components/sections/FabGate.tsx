import Link from "next/link";
import type { VerdeRoute } from "@/components/nav/nav";

/**
 * Fabrication gate — a styled interstitial for routes whose content batch
 * is still being engineered. Replaced by the real page in its batch (B2-B6).
 */
export default function FabGate({ route }: { route: VerdeRoute }) {
  return (
    <main className="relative min-h-[100svh] bg-ink bg-grid-thin bg-grid-44 overflow-hidden">
      <span className="pointer-events-none absolute -top-10 right-0 font-display font-bold text-[42vw] md:text-[26rem] leading-none text-stroke-ghost select-none">
        {route.ghost}
      </span>

      <section className="relative z-10 flex min-h-[100svh] flex-col items-center justify-center px-6 text-center">
        <div className="chip border-amber/40 bg-amber/10 text-amber mb-8">
          <span className="h-1.5 w-1.5 rounded-full bg-amber animate-blinker" />
          in fabrication — batch {route.batch}
        </div>
        <h1 className="font-display font-bold uppercase tracking-tight leading-[0.9] text-[13vw] sm:text-[10vw] lg:text-[7.5rem] text-dew">
          {route.label}
        </h1>
        <p className="mt-6 max-w-lg font-sans text-sm md:text-base text-dew-dim leading-relaxed">
          {route.blurb} This wing of the lab is being soldered together as we
          speak — every page gets its own batch, its own QA pass, its own
          screenshot review. Watch this space.
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/"
            className="rounded-full border border-lime/50 bg-lime-ghost text-lime px-7 py-3 font-mono text-[11px] uppercase tracking-[0.22em] transition-colors hover:bg-lime/20"
          >
            ← back to the hologram
          </Link>
          <span className="rounded-full border border-white/10 bg-white/[0.03] px-7 py-3 font-mono text-[11px] uppercase tracking-[0.22em] text-dew-mute">
            eta: batch {route.batch}
          </span>
        </div>
      </section>

      <footer className="absolute bottom-0 inset-x-0 border-t border-white/[0.07] bg-ink-2/80 py-3.5 overflow-hidden">
        <div className="flex w-max animate-marquee whitespace-nowrap">
          {[0, 1].map((rep) => (
            <div key={rep} className="flex shrink-0">
              {Array.from({ length: 6 }).map((_, i) => (
                <span key={i} className="mx-6 font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute">
                  {route.label} <span className="text-lime/60 ml-6">//</span> under construction
                  <span className="text-lime/60 ml-6">//</span>
                </span>
              ))}
            </div>
          ))}
        </div>
      </footer>
    </main>
  );
}
