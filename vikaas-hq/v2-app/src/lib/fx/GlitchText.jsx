import { useEffect, useRef } from 'react';

/** GlitchText — rgb-split glitch burst on hover.
 *  usage: <GlitchText text="THE DRAWER" /> */
export default function GlitchText({ text = '', className = '', as: Tag = 'span' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (matchMedia('(hover: none)').matches) return;
    const onEnter = () => { el.classList.add('glitching'); setTimeout(() => el.classList.remove('glitching'), 320); };
    el.addEventListener('mouseenter', onEnter);
    return () => el.removeEventListener('mouseenter', onEnter);
  }, []);
  return <Tag ref={ref} className={'glitch-hover ' + className}>{text}</Tag>;
}
