"use client";

import { useEffect } from "react";
import { useThree } from "@react-three/fiber";

/**
 * Freezes the R3F frameloop when the canvas scrolls out of view —
 * no rendering tax for anything a pixel away from the viewport.
 */
export default function ViewportPause({ onChange }: { onChange: (visible: boolean) => void }) {
  const gl = useThree((s) => s.gl);
  useEffect(() => {
    const el = gl.domElement;
    const io = new IntersectionObserver(([e]) => onChange(e.isIntersecting), { threshold: 0.02 });
    io.observe(el);
    return () => io.disconnect();
  }, [gl, onChange]);
  return null;
}
