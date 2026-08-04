"use client";

import { useEffect } from "react";

const SPARKS = 8;

/**
 * ClickSpark — a burst of lime tracer lines radiates from every click /
 * tap. Pure WAAPI, self-cleaning DOM, skipped for reduced-motion.
 */
export default function ClickSpark() {
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const onDown = (e: PointerEvent) => {
      const { clientX: cx, clientY: cy } = e;
      const holder = document.createElement("div");
      holder.style.cssText = `position:fixed;left:${cx}px;top:${cy}px;z-index:9999;pointer-events:none;`;
      for (let i = 0; i < SPARKS; i++) {
        const line = document.createElement("div");
        const angle = (360 / SPARKS) * i + (Math.random() * 18 - 9);
        const len = 10 + Math.random() * 8;
        line.style.cssText = `position:absolute;width:${len}px;height:2px;background:#A6FF3F;left:0;top:0;border-radius:2px;box-shadow:0 0 6px rgba(166,255,63,0.8);transform:rotate(${angle}deg);transform-origin:left center;`;
        holder.appendChild(line);
        line.animate(
          [
            { opacity: 1, transform: `rotate(${angle}deg) translateX(4px) scaleX(1)` },
            { opacity: 0, transform: `rotate(${angle}deg) translateX(${26 + Math.random() * 14}px) scaleX(0.2)` },
          ],
          { duration: 420 + Math.random() * 180, easing: "cubic-bezier(0.22,1,0.36,1)", fill: "forwards" }
        );
      }
      document.body.appendChild(holder);
      setTimeout(() => holder.remove(), 700);
    };

    window.addEventListener("pointerdown", onDown, { passive: true });
    return () => window.removeEventListener("pointerdown", onDown);
  }, []);

  return null;
}
