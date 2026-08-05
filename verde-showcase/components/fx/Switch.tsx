"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import gsap from "gsap";

const STRIPS = 5;

// guards against double navigation while a cover is on screen
let covering = false;

/**
 * Page-switch loader ("the door between rooms").
 * Listens for `verde:cover` events (fired by TransitionLink), slams 5 ink
 * strips up with the destination label flashing through, router.push()es at
 * blackout, then lifts the strips once the new route actually mounts.
 * Reduced-motion: instant push, no curtain.
 */
export default function Switch() {
  const router = useRouter();
  const pathname = usePathname();
  const stripsRef = useRef<HTMLDivElement>(null);
  const labelRef = useRef<HTMLSpanElement>(null);
  const subRef = useRef<HTMLSpanElement>(null);
  const targetRef = useRef<string | null>(null);
  const [visible, setVisible] = useState(false);

  const reveal = useCallback(() => {
    const strips = stripsRef.current?.children;
    if (!strips) { setVisible(false); covering = false; return; }
    const tl = gsap.timeline({
      onComplete: () => { setVisible(false); covering = false; },
    });
    tl.to(labelRef.current, { opacity: 0, y: -8, duration: 0.18 }, 0)
      .to(subRef.current, { opacity: 0, duration: 0.15 }, 0)
      .set(strips, { transformOrigin: "top" }, 0)
      .to(strips, {
        scaleY: 0,
        duration: 0.5,
        stagger: { each: 0.05, from: "end" },
        ease: "power3.inOut",
      }, 0.08);
  }, []);

  // lift the curtain when the requested route lands
  useEffect(() => {
    if (targetRef.current && pathname === targetRef.current) {
      targetRef.current = null;
      // give the new page one beat to paint under the curtain
      const t = setTimeout(reveal, 120);
      return () => clearTimeout(t);
    }
  }, [pathname, reveal]);

  useEffect(() => {
    const onCover = (e: Event) => {
      const { href, label } = (e as CustomEvent<{ href: string; label?: string }>).detail;
      if (covering || href === pathname) return;
      covering = true;

      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        covering = false;
        router.push(href);
        return;
      }

      targetRef.current = href;
      if (labelRef.current) labelRef.current.textContent = label ?? href.replace("/", "") + "";
      if (subRef.current) subRef.current.textContent = `verde://${href === "/" ? "home" : href.slice(1)} — opening door`;
      setVisible(true);

      requestAnimationFrame(() => {
        const strips = stripsRef.current?.children;
        if (!strips) { router.push(href); return; }
        gsap.set(strips, { transformOrigin: "bottom", scaleY: 0 });
        gsap.set(labelRef.current, { opacity: 0, y: 10 });
        gsap.set(subRef.current, { opacity: 0 });
        const tl = gsap.timeline({
          onComplete: () => {
            router.push(href);
            // failsafe: if the route never changes (compile stall), lift anyway
            gsap.delayedCall(2.4, () => {
              if (targetRef.current === href) {
                targetRef.current = null;
                reveal();
              }
            });
          },
        });
        tl.to(strips, {
          scaleY: 1,
          duration: 0.45,
          stagger: { each: 0.05, from: "start" },
          ease: "power3.inOut",
        }, 0)
          .to(labelRef.current, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.28)
          .to(subRef.current, { opacity: 1, duration: 0.3 }, 0.36);
      });
    };
    window.addEventListener("verde:cover", onCover);
    return () => window.removeEventListener("verde:cover", onCover);
  }, [pathname, router, reveal]);

  if (!visible) return null;

  return (
    <div className="fixed inset-0 z-[10004] pointer-events-none" aria-hidden>
      <div ref={stripsRef} className="absolute inset-0 flex">
        {Array.from({ length: STRIPS }).map((_, i) => (
          <div key={i} className="h-full flex-1 bg-ink-3 border-r border-ink-4/50 last:border-r-0" />
        ))}
      </div>
      <div className="absolute inset-0 grid place-items-center text-center px-6">
        <div>
          <span ref={labelRef} className="block font-display font-bold uppercase tracking-tight text-4xl md:text-6xl text-lime drop-shadow-[0_0_24px_rgba(166,255,63,0.35)] opacity-0" />
          <span ref={subRef} className="mt-3 block font-mono text-[10px] uppercase tracking-[0.3em] text-dew-mute opacity-0" />
        </div>
      </div>
    </div>
  );
}
