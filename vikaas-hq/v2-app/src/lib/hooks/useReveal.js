import { useEffect, useRef } from 'react';

/** useReveal — scroll-reveal via IntersectionObserver (Framer-free, cheap).
 *  usage: const ref = useReveal({ y: 30, delay: 0.1 }); <div ref={ref} class="rv"> */
export default function useReveal({ y = 30, delay = 0, once = true } = {}) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.style.opacity = '1'; el.style.transform = 'none'; return; }
    el.style.opacity = '0';
    el.style.transform = `translateY(${y}px)`;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          el.style.transition = `opacity .8s cubic-bezier(.2,.8,.2,1) ${delay}s, transform .8s cubic-bezier(.2,.8,.2,1) ${delay}s`;
          el.style.opacity = '1';
          el.style.transform = 'none';
          if (once) io.unobserve(el);
        } else if (!once) {
          el.style.opacity = '0';
          el.style.transform = `translateY(${y}px)`;
        }
      });
    }, { threshold: 0.12 });
    io.observe(el);
    return () => io.disconnect();
  }, [y, delay, once]);
  return ref;
}
