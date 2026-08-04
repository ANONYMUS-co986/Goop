"use client";

import { useEffect, useRef } from "react";
import { gsap } from "@/lib/gsap";

/**
 * Scroll-enter reveals (GSAP ScrollTrigger, fires once, transform+opacity
 * only = zero layout cost after settle).
 *
 * <Reveal>            — single element rise/blur/scale
 * <RevealGroup>       — staggers its direct children as a pack
 */
export function Reveal({
  children,
  className,
  variant = "up",
  delay = 0,
  start = "top 88%",
}: {
  children?: React.ReactNode;
  className?: string;
  variant?: "up" | "blur" | "scale" | "fade";
  delay?: number;
  start?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const from =
      variant === "up" ? { y: 46, opacity: 0 } :
      variant === "blur" ? { opacity: 0, filter: "blur(10px)" } :
      variant === "scale" ? { scale: 0.92, opacity: 0 } :
      { opacity: 0 };
    const anim = gsap.from(el, {
      ...from,
      duration: 0.95,
      delay,
      ease: "power3.out",
      clearProps: "all",
      scrollTrigger: { trigger: el, start, once: true },
    });
    return () => { anim.scrollTrigger?.kill(); anim.kill(); };
  }, [variant, delay, start]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}

export function RevealGroup({
  children,
  className,
  stagger = 0.08,
  delay = 0,
  start = "top 86%",
}: {
  children?: React.ReactNode;
  className?: string;
  stagger?: number;
  delay?: number;
  start?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const anim = gsap.from(el.children, {
      y: 42,
      opacity: 0,
      duration: 0.85,
      delay,
      stagger,
      ease: "power3.out",
      clearProps: "transform,opacity",
      scrollTrigger: { trigger: el, start, once: true },
    });
    return () => { anim.scrollTrigger?.kill(); anim.kill(); };
  }, [stagger, delay, start]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}

export default Reveal;
