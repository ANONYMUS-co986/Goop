import { useEffect, useRef } from 'react';

const SCR = '!<>-_\\/[]{}—=+*^?#$%&@ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const rand = () => SCR[Math.floor(Math.random() * SCR.length)];

/** TextScramble — matrix-style char scramble that settles into the text.
 *  usage: <TextScramble text="VIKAAS" speed={34} className="..." /> */
export default function TextScramble({ text = '', speed = 34, className = '', as: Tag = 'span' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = text; return; }
    let frame = 0;
    const total = 90;
    const tick = () => {
      const p = frame / total;
      const reveal = Math.floor(p * text.length);
      let out = '';
      for (let i = 0; i < text.length; i++) out += i < reveal ? text[i] : rand();
      el.textContent = out;
      frame++;
      if (frame <= total) setTimeout(tick, speed);
      else el.textContent = text;
    };
    tick();
  }, [text, speed]);
  return <Tag ref={ref} className={className}>{text}</Tag>;
}
