import { useEffect, useRef } from 'react';
import SplitType from 'split-type';
import gsap from 'gsap';

/** SplitReveal — char-split + staggered yPercent/rotate reveal (GSAP).
 *  usage: <SplitReveal text="VIKAAS" className="anton big" stagger={0.05} /> */
export default function SplitReveal({ text = '', className = '', stagger = 0.05, ease = 'back.out(1.7)', as: Tag = 'h1' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { el.textContent = text; return; }
    el.textContent = text;
    let chars = [];
    try { const st = new SplitType(el, { types: 'chars' }); chars = st.chars || []; }
    catch (e) { chars = []; }
    if (chars.length) {
      gsap.fromTo(chars, { yPercent: 130, rotate: 10, opacity: 0 }, { yPercent: 0, rotate: 0, opacity: 1, stagger, duration: 1.0, ease });
    } else {
      gsap.fromTo(el, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: 'power4.out' });
    }
    return () => { if (window.SplitType && chars.length) { try { SplitType.revert(el); } catch (e) {} } };
  }, [text, stagger, ease]);
  return <Tag ref={ref} className={className}>{text}</Tag>;
}
