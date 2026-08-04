"use client";

import { useEffect, useRef } from "react";
import { gsap } from "@/lib/gsap";

/**
 * Parallax — scrub-linked depth drift. speed > 0 drifts the element up
 * slower than the page (background ghosts), < 0 races ahead.
 */
export default function Parallax({
  children,
  className,
  speed = 0.5,
}: {
  children?: React.ReactNode;
  className?: string;
  speed?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const tween = gsap.to(el, {
      yPercent: -34 * speed,
      ease: "none",
      scrollTrigger: {
        trigger: el.parentElement ?? el,
        start: "top bottom",
        end: "bottom top",
        scrub: 0.6,
      },
    });
    return () => { tween.scrollTrigger?.kill(); tween.kill(); };
  }, [speed]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}
