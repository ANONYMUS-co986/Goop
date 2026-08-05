"use client";

import { useEffect, useRef } from "react";
import { gsap } from "@/lib/gsap";

/**
 * Scroll-enter reveals (GSAP ScrollTrigger, fires once, transform+opacity
 * only = zero layout cost after settle).
 *
 * <Reveal>            — single element entry (up/left/right/blur/scale/fade)
 * <RevealGroup>       — staggers its direct children as a pack
 * <AssembleGroup>     — children fly in from ALTERNATING SIDES with a
 *                       rotation + back.out overshoot = parts snapping
 *                       together. The "assembly line" effect.
 */
const REDUCED = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function Reveal({
  children,
  className,
  variant = "up",
  delay = 0,
  start = "top 88%",
}: {
  children?: React.ReactNode;
  className?: string;
  variant?: "up" | "left" | "right" | "blur" | "scale" | "fade";
  delay?: number;
  start?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || REDUCED()) return;
    const from =
      variant === "up" ? { y: 46, opacity: 0 } :
      variant === "left" ? { x: -110, opacity: 0 } :
      variant === "right" ? { x: 110, opacity: 0 } :
      variant === "blur" ? { opacity: 0, filter: "blur(10px)" } :
      variant === "scale" ? { scale: 0.92, opacity: 0 } :
      { opacity: 0 };
    const anim = gsap.from(el, {
      ...from,
      duration: variant === "left" || variant === "right" ? 1.0 : 0.95,
      delay,
      ease: variant === "left" || variant === "right" ? "expo.out" : "power3.out",
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
    if (!el || REDUCED()) return;
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

/**
 * ASSEMBLY LINE — children converge from alternating sides with a slight
 * tumble and an overshoot snap. Even children from the left, odd from the
 * right (or pass `alternate={false}` to drive everything from one side).
 */
export function AssembleGroup({
  children,
  className,
  stagger = 0.09,
  delay = 0,
  start = "top 84%",
  distance = 110,
  alternate = true,
  side = "left",
}: {
  children?: React.ReactNode;
  className?: string;
  stagger?: number;
  delay?: number;
  start?: string;
  distance?: number;
  alternate?: boolean;
  side?: "left" | "right";
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || REDUCED()) return;
    const kids = Array.from(el.children) as HTMLElement[];
    const anims = kids.map((kid, i) => {
      const fromLeft = alternate ? i % 2 === 0 : side === "left";
      return gsap.from(kid, {
        x: (fromLeft ? -1 : 1) * distance,
        rotation: (fromLeft ? -1 : 1) * 3.5,
        opacity: 0,
        duration: 1.05,
        delay: delay + i * stagger,
        ease: "back.out(1.7)",
        clearProps: "transform,opacity",
        scrollTrigger: { trigger: el, start, once: true },
      });
    });
    return () => { anims.forEach((a) => { a.scrollTrigger?.kill(); a.kill(); }); };
  }, [stagger, delay, start, distance, alternate, side]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}

export default Reveal;
