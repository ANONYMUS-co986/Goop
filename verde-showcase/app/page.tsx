/**
 * B0 — toolchain proof shell.
 * This page exists to prove the Night Lab system end-to-end:
 * fonts, tokens, grain, cursor, smooth scroll, keyframes.
 * It is REPLACED by the real hero in Batch 1.
 */

const TICKER = [
  "17→2 CALLS/SEC",
  "8 MHZ XCLK",
  "₹1,890 BUILD",
  "13/13 TESTS",
  "94% CROP.HEALTH",
  "5 SENSORS · 2 MCUS",
  "SVGA LEAF CAM",
  "60 S HEARTBEAT",
  "3-NETWORK FAILSAFE",
  "8 S WATCHDOG",
];

export default function Page() {
  return (
    <main className="relative min-h-screen bg-ink bg-grid-thin bg-grid-44 overflow-hidden">
      {/* scanline sweep */}
      <div className="pointer-events-none absolute inset-x-0 h-24 top-0 animate-scanline bg-gradient-to-b from-transparent via-lime/[0.06] to-transparent" />

      {/* top console strip */}
      <header className="absolute inset-x-0 top-0 flex items-center justify-between px-6 md:px-10 py-5 font-mono text-[10px] uppercase tracking-[0.28em] text-dew-mute">
        <span className="text-lime">VERDE://SHOWCASE</span>
        <span className="hidden sm:inline">NIGHT LAB · B0 ONLINE</span>
        <span className="text-hydro">DAV ACON 5 · ROUND 2</span>
      </header>

      {/* center proof stack */}
      <section className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6 text-center">
        <div className="chip border-lime/30 bg-lime-ghost text-lime mb-8">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-lime animate-pingring" />
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-lime" />
          </span>
          BOOT SEQUENCE COMPLETE
        </div>

        <h1 className="font-display font-bold uppercase leading-[0.92] tracking-tight text-[13vw] sm:text-[11vw] lg:text-[8.5rem]">
          <span className="block text-dew">The plant that</span>
          <span className="block text-stroke-lime">waters</span>
          <span className="block text-lime drop-shadow-[0_0_28px_rgba(166,255,63,0.35)]">
            itself.
          </span>
        </h1>

        <p className="mt-8 max-w-xl font-sans text-sm md:text-base text-dew-dim leading-relaxed">
          Toolchain proof: Night Lab tokens, Syne display, custom cursor,
          Lenis smooth scroll, film grain — all live. Phase B1 swaps this
          shell for the holographic hero.
        </p>

        <div className="mt-10 flex items-center gap-4">
          <span className="rounded-full border border-lime/40 bg-lime-ghost px-6 py-3 font-mono text-[11px] uppercase tracking-[0.24em] text-lime shadow-glow-lime">
            System nominal
          </span>
          <span className="rounded-full border border-hydro/30 bg-hydro-ghost px-6 py-3 font-mono text-[11px] uppercase tracking-[0.24em] text-hydro">
            B1 → hero next
          </span>
        </div>
      </section>

      {/* bottom ledger marquee */}
      <footer className="absolute inset-x-0 bottom-0 border-t border-white/[0.07] bg-ink-2/80 backdrop-blur-sm overflow-hidden py-3.5">
        <div className="flex w-max animate-marquee gap-0 whitespace-nowrap">
          {[0, 1].map((rep) => (
            <div key={rep} className="flex shrink-0">
              {TICKER.map((t, i) => (
                <span
                  key={`${rep}-${i}`}
                  className="mx-6 font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute"
                >
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
