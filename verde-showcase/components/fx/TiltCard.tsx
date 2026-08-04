"use client";

import { useRef } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

/**
 * TiltCard — 3D perspective tilt toward the cursor (React Bits "TiltedCard"
 * port). Spring-return on leave, preserved 3D for layered children.
 * Pairs well wrapped around GlowCard.
 */
export default function TiltCard({
  children,
  className = "",
  max = 7,
}: {
  children?: React.ReactNode;
  className?: string;
  max?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const rx = useMotionValue(0);
  const ry = useMotionValue(0);
  const srx = useSpring(rx, { stiffness: 210, damping: 17, mass: 0.4 });
  const sry = useSpring(ry, { stiffness: 210, damping: 17, mass: 0.4 });

  return (
    <motion.div
      ref={ref}
      style={{ rotateX: srx, rotateY: sry, transformStyle: "preserve-3d", transformPerspective: 950 }}
      className={className}
      onMouseMove={(e) => {
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        const r = ref.current?.getBoundingClientRect();
        if (!r) return;
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        rx.set(-py * max);
        ry.set(px * max);
      }}
      onMouseLeave={() => { rx.set(0); ry.set(0); }}
    >
      {children}
    </motion.div>
  );
}
