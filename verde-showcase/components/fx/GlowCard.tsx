"use client";

import { useRef } from "react";

/**
 * GlowCard — a radial spotlight that tracks the cursor across the card,
 * plus a matching border gleam. Zero re-renders: pure CSS custom
 * properties driven by mousemove.
 */
export default function GlowCard({
  children,
  className = "",
  color = "166,255,63",
  size = 240,
  ...rest
}: {
  children?: React.ReactNode;
  className?: string;
  color?: string;
  size?: number;
} & React.HTMLAttributes<HTMLDivElement>) {
  const ref = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={ref}
      {...rest}
      onMouseMove={(e) => {
        const el = ref.current;
        if (!el) return;
        const r = el.getBoundingClientRect();
        el.style.setProperty("--mx", `${(((e.clientX - r.left) / r.width) * 100).toFixed(2)}%`);
        el.style.setProperty("--my", `${(((e.clientY - r.top) / r.height) * 100).toFixed(2)}%`);
      }}
      className={`group/glow relative ${className}`}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 rounded-[inherit] opacity-0 transition-opacity duration-300 group-hover/glow:opacity-100"
        style={{
          background: `radial-gradient(${size}px circle at var(--mx, 50%) var(--my, 50%), rgba(${color},0.12), transparent 65%)`,
        }}
      />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 rounded-[inherit] opacity-0 transition-opacity duration-300 group-hover/glow:opacity-100"
        style={{
          background: `radial-gradient(${Math.round(size * 0.7)}px circle at var(--mx, 50%) var(--my, 50%), rgba(${color},0.35), transparent 60%)`,
          mask: "linear-gradient(#000,#000) content-box, linear-gradient(#000,#000)",
          maskComposite: "exclude",
          WebkitMask: "linear-gradient(#000,#000) content-box, linear-gradient(#000,#000)",
          WebkitMaskComposite: "xor",
          padding: 1,
        }}
      />
      {children}
    </div>
  );
}
