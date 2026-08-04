"use client";

import { useEffect, useRef } from "react";
import { gsap } from "@/lib/gsap";

/**
 * ScrollStack (reactbits port) — cards ride up and STACK on top of each
 * other while scrolling. CSS `position: sticky` does the pinning (free on
 * the compositor); GSAP only scrubs a scale-down + dim on each card as the
 * next one covers it — transform/opacity only, no layout cost.
 *
 * Children become direct sticky slots: give each child a real background
 * (no transparency) or the stack illusion breaks.
 */
export default function ScrollStack({
  children,
  className,
  topOffset = 104,
  gap = 14,
  scaleTo = 0.95,
  dimTo = 0.85,
}: {
  children?: React.ReactNode;
  className?: string;
  topOffset?: number;
  gap?: number;
  scaleTo?: number;
  dimTo?: number; // target brightness for covered cards (0-1)
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const cards = Array.from(el.children) as HTMLElement[];
    // sticky slots — each card pins slightly lower than the previous so the
    // stack edges stay visible like cards in a Rolodex
    cards.forEach((card, i) => {
      card.style.position = "sticky";
      card.style.top = `${topOffset + i * gap}px`;
      card.style.transformOrigin = "center top";
      card.style.zIndex = String(i + 1);
    });
    // scrub: as card i+1 travels to its slot, card i sinks back.
    // NOTE: dim via brightness, never opacity — opacity makes the card
    // translucent and cards below bleed through the stack illusion.
    const tweens = cards.slice(0, -1).map((card, i) =>
      gsap.to(card, {
        scale: scaleTo,
        filter: `brightness(${dimTo})`,
        ease: "none",
        scrollTrigger: {
          trigger: cards[i + 1],
          start: `top bottom`,
          end: `top top+=${topOffset + i * gap + 40}`,
          scrub: 0.5,
        },
      })
    );
    return () => tweens.forEach((t) => { t.scrollTrigger?.kill(); t.kill(); });
  }, [topOffset, gap, scaleTo, dimTo]);

  return (
    <div ref={ref} className={className}>
      {children}
      {/* tail room so the last card can reach its slot and the stack closes */}
      <div aria-hidden className="h-[22vh]" />
    </div>
  );
}
