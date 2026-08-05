"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

/**
 * RotatingText — cycles words with a rise-and-deblur swap
 * (React Bits "RotatingText" port).
 */
export default function RotatingText({
  words,
  interval = 2200,
  className = "",
}: {
  words: string[];
  interval?: number;
  className?: string;
}) {
  const [i, setI] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const t = setInterval(() => setI((v) => (v + 1) % words.length), interval);
    return () => clearInterval(t);
  }, [words.length, interval]);

  return (
    <span className={`inline-block ${className}`}>
      <AnimatePresence mode="wait" initial={false}>
        <motion.span
          key={words[i]}
          initial={{ opacity: 0, y: 14, filter: "blur(4px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          exit={{ opacity: 0, y: -14, filter: "blur(4px)" }}
          transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
          className="inline-block"
        >
          {words[i]}
        </motion.span>
      </AnimatePresence>
    </span>
  );
}
