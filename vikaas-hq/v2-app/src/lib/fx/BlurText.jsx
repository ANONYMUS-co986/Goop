import { useEffect, useRef } from 'react';

/** BlurText — words blur→focus (staggered), reactbits-style.
 *  usage: <BlurText text="One drawer in Gurugram." delay={0.02} /> */
export default function BlurText({ text = '', delay = 0.02, className = '', as: Tag = 'p' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.style.opacity = '1'; el.style.filter = 'none'; return; }
    const words = text.split(' ');
    el.innerHTML = words.map((w, i) => `<span class="btw" style="display:inline-block;opacity:0;filter:blur(10px);transition:opacity .6s ${i * delay}s,filter .6s ${i * delay}s">${w}&nbsp;</span>`).join('');
    el.style.opacity = '1';
    requestAnimationFrame(() => {
      el.querySelectorAll('.btw').forEach((w) => { w.style.opacity = '1'; w.style.filter = 'blur(0px)'; });
    });
  }, [text, delay]);
  return <Tag ref={ref} className={className}>{text}</Tag>;
}
