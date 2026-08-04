"use client";

import { useEffect, useRef } from "react";
import { gsap, SplitText } from "@/lib/gsap";

/**
 * SplitReveal — GSAP SplitText char explosion on scroll-enter.
 * Characters rise out of blur one by one, then the DOM is reverted back
 * to plain text (a11y + no wrapper-soup). Fires once.
 */
export default function SplitReveal({
  text,
  className,
  as = "h2",
  delay = 0,
  stagger = 0.016,
  start = "top 86%",
}: {
  text: string;
  className?: string;
  as?: "h1" | "h2" | "h3" | "span" | "p" | "div";
  delay?: number;
  stagger?: number;
  start?: string;
}) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const ctx = gsap.context(() => {
      const split = new SplitText(el, { type: "chars,words" });
      gsap.from(split.chars, {
        yPercent: 62,
        opacity: 0,
        filter: "blur(4px)",
        duration: 0.7,
        delay,
        stagger,
        ease: "power3.out",
        scrollTrigger: { trigger: el, start, once: true },
        onComplete: () => split.revert(),
      });
    }, el);

    return () => ctx.revert();
  }, [text, delay, stagger, start]);

  const Tag = as;
  return (
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    <Tag ref={ref as any} className={className}>
      {text}
    </Tag>
  );
}
