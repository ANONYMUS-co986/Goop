"use client";

import { useEffect, useRef } from "react";

/**
 * Global tooltip — any element with a data-tip attribute gets a floating
 * mono chip that follows the cursor. One DOM node, no re-renders.
 */
export default function Tip() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    const el = ref.current;
    if (!el) return;

    const onMove = (e: MouseEvent) => {
      const target = (e.target as HTMLElement | null)?.closest?.("[data-tip]") as HTMLElement | null;
      if (target && target.dataset.tip) {
        el.textContent = target.dataset.tip;
        el.style.opacity = "1";
        const w = el.offsetWidth || 180;
        const x = Math.min(e.clientX + 16, window.innerWidth - w - 12);
        const y = Math.min(e.clientY + 20, window.innerHeight - 52);
        el.style.transform = `translate(${Math.max(8, x)}px, ${Math.max(8, y)}px)`;
      } else {
        el.style.opacity = "0";
      }
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    return () => window.removeEventListener("mousemove", onMove);
  }, []);

  return (
    <div
      ref={ref}
      role="tooltip"
      className="pointer-events-none fixed left-0 top-0 z-[10006] max-w-[250px] rounded-lg border border-lime/25 bg-ink-2/95 px-3 py-2 font-mono text-[10px] leading-relaxed text-dew-dim opacity-0 shadow-glow-lime transition-opacity duration-150 backdrop-blur-md"
    />
  );
}
