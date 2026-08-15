/* ============================================================
   VIKAAS sound lib — WebAudio UI blips + shared context.
   Respects the zustand `muted` flag. One context, reused.
   ============================================================ */
import { useUI } from '../shell/Shell.jsx';

let AC = null;
let unlocked = false;

export function ac() {
  if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} }
  return AC;
}
export function unlockAudio() {
  if (unlocked) return;
  unlocked = true;
  ac();
}
export function isMuted() { return useUI.getState().muted; }

/** blip — a tiny UI tick (hover/click). freq 400–1600, 0.09s. */
export function blip(freq = 800 + Math.random() * 500, vol = 0.04) {
  if (isMuted()) return;
  const C = ac(); if (!C) return;
  try {
    const t0 = C.currentTime;
    const o = C.createOscillator(); const g = C.createGain();
    o.type = 'sine'; o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.09);
    o.connect(g); g.connect(C.destination); o.start(t0); o.stop(t0 + 0.1);
  } catch (e) {}
}

/** whoosh — filtered noise sweep (transitions). */
export function whoosh(dur = 0.7) {
  if (isMuted()) return;
  const C = ac(); if (!C) return;
  try {
    const len = C.sampleRate * dur, buf = C.createBuffer(1, len, C.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
    const src = C.createBufferSource(); src.buffer = buf;
    const f = C.createBiquadFilter(); f.type = 'bandpass';
    f.frequency.setValueAtTime(300, C.currentTime);
    f.frequency.exponentialRampToValueAtTime(2400, C.currentTime + dur * 0.85); f.Q.value = 1.1;
    const g = C.createGain(); g.gain.value = 0.12;
    src.connect(f); f.connect(g); g.connect(C.destination); src.start();
  } catch (e) {}
}

/** playOnce — play a public/audio file once. */
export function playOnce(path, vol = 0.8) {
  if (isMuted()) return;
  try { const a = new Audio(path); a.volume = vol; a.play().catch(() => {}); } catch (e) {}
}

/** attachHoverBlips — global hover blip listener (call once per app). */
export function attachHoverBlips() {
  if (matchMedia('(hover: none)').matches) return;
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest('a,button,[data-cursor]')) blip();
  }, { passive: true });
}
