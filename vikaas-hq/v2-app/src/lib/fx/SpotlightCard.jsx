import { useRef } from 'react';

/** SpotlightCard — cursor-following radial spotlight (reactbits-style).
 *  usage: <SpotlightCard className="..." >content</SpotlightCard> */
export default function SpotlightCard({ children, className = '', color = 'rgba(185,255,63,.13)' }) {
  const ref = useRef(null);
  const onMove = (e) => {
    const el = ref.current;
    if (!el) return;
    const b = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - b.left) / b.width * 100) + '%');
    el.style.setProperty('--my', ((e.clientY - b.top) / b.height * 100) + '%');
  };
  return (
    <div ref={ref} className={'spot-card ' + className} onPointerMove={onMove} style={{ '--spot': color }}>
      <div className="spot-glow" aria-hidden="true" />
      {children}
    </div>
  );
}
