import type { CSSProperties } from "react";

/**
 * ShinyText — a light sweep keeps gliding across the text (React Bits
 * "ShinyText" port). Two stacked spans: base color below, gradient-clipped
 * sweep above, so it works over any background without transparency hacks.
 */
export default function ShinyText({
  text,
  className = "",
  speed = 3.4,
}: {
  text: string;
  className?: string;
  speed?: number;
}) {
  const style: CSSProperties = { animationDuration: `${speed}s` };
  return (
    <span className={`relative inline-block ${className}`}>
      <span>{text}</span>
      <span aria-hidden className="shiny-sweep absolute inset-0" style={style}>
        {text}
      </span>
    </span>
  );
}
