"use client";

import type { CSSProperties } from "react";

/**
 * StarBorder (reactbits port) — two comet-glows running laps around the
 * inside of a pill. Pure CSS keyframes, zero JS runtime.
 */
export default function StarBorder({
  children,
  className = "",
  color = "#FFC24B",
  speed = "5s",
  innerClassName = "",
}: {
  children?: React.ReactNode;
  className?: string;
  color?: string;
  speed?: string;
  innerClassName?: string;
}) {
  return (
    <div
      className={`star-border rounded-full ${className}`}
      style={{ "--sb-color": color, "--sb-speed": speed } as CSSProperties}
    >
      <span aria-hidden className="sb-glow sb-glow-bottom" />
      <span aria-hidden className="sb-glow sb-glow-top" />
      <span className={`relative z-10 block rounded-full ${innerClassName}`}>
        {children}
      </span>
    </div>
  );
}
