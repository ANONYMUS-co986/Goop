import { useRef, useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './arsenal.css';

import v1 from '../assets/img/arsenal/VIKAAS_01_THE-DRAWER.jpg';
import v2 from '../assets/img/arsenal/VIKAAS_02_15-RECYCLERS-0-DOORSTEPS.jpg';
import v3 from '../assets/img/arsenal/VIKAAS_03_KABADI-PARADOX.jpg';
import v4 from '../assets/img/arsenal/VIKAAS_04_COMEDY-CLUB.jpg';
import v5 from '../assets/img/arsenal/VIKAAS_05_DOORSTEP-PHONK.jpg';
import v6 from '../assets/img/arsenal/VIKAAS_06_MEME-REEL.jpg';
import p1 from '../assets/img/arsenal/p1.jpg';
import p2 from '../assets/img/arsenal/p2.jpg';
import p3 from '../assets/img/arsenal/p3.jpg';
import p4 from '../assets/img/arsenal/p4.jpg';
import p5 from '../assets/img/arsenal/p5.jpg';

const REELS = [
  { file: 'VIKAAS_01_THE-DRAWER.mp4', poster: v1, title: 'THE DRAWER', tag: 'THE ORIGIN', line: '1.4 kg of “kabhi kaam aayega” — the drawer that started the universe.', stamp: 'REEL 01', cls: 'st-green' },
  { file: 'VIKAAS_02_15-RECYCLERS-0-DOORSTEPS.mp4', poster: v2, title: '15 RECYCLERS · 0 DOORSTEPS', tag: 'THE GAP', line: 'Fifteen licensed recyclers in Gurugram. Not one doorstep. Until now.', stamp: 'REEL 02', cls: 'st-red' },
  { file: 'VIKAAS_03_KABADI-PARADOX.mp4', poster: v3, title: 'THE KABADI PARADOX', tag: 'THE NETWORK', line: 'He knows every street. The recycler holds the licence. Nobody connects them.', stamp: 'REEL 03', cls: 'st-violet' },
  { file: 'VIKAAS_04_COMEDY-CLUB.mp4', poster: v4, title: 'THE COMEDY CLUB', tag: 'THE DRAWER NATION', line: 'Ten homes. Ten drawers. Zero recyclers named. Laugh, then measure.', stamp: 'REEL 04', cls: 'st-gold' },
  { file: 'VIKAAS_05_DOORSTEP-PHONK.mp4', poster: v5, title: 'DOORSTEP PHONK', tag: 'THE SOUND', line: 'The 138 BPM drift — the sound of the doorstep arriving.', stamp: 'REEL 05', cls: 'st-green' },
  { file: 'VIKAAS_06_MEME-REEL.mp4', poster: v6, title: 'THE MEME REEL', tag: 'THE REACH', line: 'When the drawer becomes a meme, the message rides along.', stamp: 'REEL 06', cls: 'st-gold' },
];

const POST_SERIES = [
  { name: 'M1–M8', label: 'THE MEMES', color: 'acid' },
  { name: 'P1–P6', label: 'THE POSTERS', color: 'green' },
  { name: 'R1–R8', label: 'THE REEL CUTS', color: 'violet' },
];

// 22 tiles: M1-M8 (typographic), P1-P6 (p1-p5 art + 1 typo), R1-R8 (typo)
const POST_TILES = [
  { id: 'M1', art: null }, { id: 'M2', art: null }, { id: 'M3', art: null }, { id: 'M4', art: null },
  { id: 'M5', art: null }, { id: 'M6', art: null }, { id: 'M7', art: null }, { id: 'M8', art: null },
  { id: 'P1', art: p1 }, { id: 'P2', art: p2 }, { id: 'P3', art: p3 }, { id: 'P4', art: p4 },
  { id: 'P5', art: p5 }, { id: 'P6', art: null },
  { id: 'R1', art: null }, { id: 'R2', art: null }, { id: 'R3', art: null }, { id: 'R4', art: null },
  { id: 'R5', art: null }, { id: 'R6', art: null }, { id: 'R7', art: null }, { id: 'R8', art: null },
];

const VO = [
  { file: 'vo1_pov.mp3', label: 'vo1 · POV', line: '“your drawer, finally seen”' },
  { file: 'vo2_mummy.mp3', label: 'vo2 · MUMMY', line: 'the voice that asked “kabhi kaam aayega?”' },
  { file: 'vo3_narrator1.mp3', label: 'vo3 · NARRATOR', line: 'the gospel of the doorstep' },
  { file: 'vo4_papa.mp3', label: 'vo4 · PAPA', line: 'the sceptic, converted by the scale' },
  { file: 'vo5_narrator2.mp3', label: 'vo5 · NARRATOR 2', line: 'the numbers, read like poetry' },
  { file: 'vo6_calc.mp3', label: 'vo6 · THE CALCULATION', line: '1.4 kg × ₹8 = the first receipt' },
  { file: 'vo7_kabadi.mp3', label: 'vo7 · THE KABADIWALA', line: 'the man who knows every street' },
  { file: 'vo8_finale.mp3', label: 'vo8 · FINALE', line: 'no drawer left behind' },
];

const vidSrc = (file) => {
  if (typeof __ARSENAL_FS__ === 'undefined' || !import.meta.env.DEV) return '';
  return '/@fs' + __ARSENAL_FS__ + '/' + file;
};

export default function Arsenal() {
  const [playing, setPlaying] = useState(null); // reel index
  const [voOn, setVoOn] = useState(null); // vo index
  const audioRef = useRef(null);
  const [durs, setDurs] = useState({});

  useEffect(() => {
    return () => { if (audioRef.current) audioRef.current.pause(); };
  }, []);

  const toggleVo = (i) => {
    if (voOn === i) {
      audioRef.current.pause();
      setVoOn(null);
      return;
    }
    if (audioRef.current) audioRef.current.pause();
    audioRef.current = new Audio('/arsenal/vo/' + VO[i].file);
    audioRef.current.play();
    audioRef.current.onended = () => setVoOn(null);
    setVoOn(i);
  };

  return (
    <main className="ar-page">
      <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

      <section className="ar-hero">
        <p className="eyebrow cmd shiny">the arsenal · made with code</p>
        <h1 className="anton ar-title">THE<br /><span>ARSENAL</span></h1>
        <p className="ar-sub">Six reels. Twenty-two posts. Eight voice clips. Every frame generated with code, every number stamped. This is the content engine of the campaign — hover the reels to play, tap the voice to hear the doorstep.</p>
        <div className="ar-stats">
          <div className="ar-stat"><b className="anton">6</b><span>reels</span><span className="stamp st-green">MADE WITH CODE</span></div>
          <div className="ar-stat"><b className="anton">22</b><span>posts</span><span className="stamp st-green">3 SERIES</span></div>
          <div className="ar-stat"><b className="anton">8</b><span>voice clips</span><span className="stamp st-violet">THE SOUND</span></div>
          <div className="ar-stat"><b className="anton">138</b><span>bpm phonk bed</span><span className="stamp st-gold">DRIFT-FORGE</span></div>
        </div>
      </section>

      <section className="ar-reels-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the films · hover to play</p>
          <h2 className="section-title">SIX REELS.<br /><span>ONE DRAWER.</span></h2>
          <div className="ar-reels">
            {REELS.map((r, i) => (
              <motion.figure key={r.title} className="ar-reel"
                initial={{ opacity: 0, y: 44 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.7, delay: (i % 3) * 0.1, ease: [0.22, 1, 0.36, 1] }}
                data-cursor={playing === i ? 'PAUSE' : 'PLAY'}
                onMouseEnter={() => setPlaying(i)}
                onMouseLeave={() => setPlaying(null)}>
                <div className="ar-screen">
                  <img src={r.poster} alt={r.title} loading="lazy" className={playing === i ? 'off' : ''} />
                  <video
                    src={vidSrc(r.file)}
                    muted loop playsInline preload="none"
                    className={playing === i ? 'on' : ''}
                    onLoadedMetadata={(e) => setDurs((d) => ({ ...d, [r.file]: e.target.duration }))}
                    onMouseEnter={(e) => { if (playing === i) e.target.play(); }}
                  />
                  <span className="ar-badge cmd">{playing === i ? '▶ PLAYING' : (durs[r.file] ? Math.round(durs[r.file]) + 's' : 'REEL')}</span>
                </div>
                <figcaption>
                  <span className="ar-tag cmd">{r.tag}</span>
                  <h3 className="anton">{r.title}</h3>
                  <p>{r.line}</p>
                  <span className={`stamp ${r.cls}`}>{r.stamp}</span>
                </figcaption>
              </motion.figure>
            ))}
          </div>
          <p className="ar-note">The reels live in the repo and stream through the dev server — no fake screenshots, no placeholder frames. <em>Hover. Play. Believe.</em></p>
        </div>
      </section>

      <section className="ar-posts-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the feed · 3 series</p>
          <h2 className="section-title">22 POSTS.<br /><span>0 TEMPLATES.</span></h2>
          <div className="ar-series">
            {POST_SERIES.map((s) => (
              <span key={s.name} className={`ar-series-chip ${s.color}`}><b className="anton">{s.name}</b>{s.label}</span>
            ))}
          </div>
          <div className="ar-tiles">
            {POST_TILES.map((t, i) => (
              <motion.div key={t.id} className={`ar-tile ${t.art ? 'has-art' : 'typo'}`} data-cursor={t.art ? 'POST' : t.id}
                initial={{ opacity: 0, scale: 0.9 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.5, delay: (i % 8) * 0.04 }}>
                {t.art ? <img src={t.art} alt={t.id} loading="lazy" /> : <span className="ar-tile-no anton">{t.id}</span>}
                <span className="ar-tile-id cmd">{t.id}</span>
              </motion.div>
            ))}
          </div>
          <p className="ar-note">Every post carries the same spine: the drawer, the scale, the receipt. <em>Made with code — every single one.</em></p>
        </div>
      </section>

      <section className="ar-vo-sec">
        <div className="wrap">
          <p className="eyebrow cmd shiny">the voice · the sound of the doorstep</p>
          <h2 className="section-title">EIGHT VOICES.<br /><span>ONE STORY.</span></h2>
          <div className="ar-vo">
            {VO.map((v, i) => (
              <motion.div key={v.label} className="ar-vo-row"
                initial={{ opacity: 0, x: -26 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.05 }}>
                <button className={`ar-vo-btn ${voOn === i ? 'on' : ''}`} onClick={() => toggleVo(i)} data-cursor={voOn === i ? 'STOP' : 'PLAY'}>
                  {voOn === i ? '■' : '▶'}
                </button>
                <div className="ar-vo-main">
                  <b className="anton">{v.label}</b>
                  <span className="cmd">{v.line}</span>
                </div>
                <span className="ar-vo-wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <footer className="ar-foot">
        <div className="foot-big anton grad-text">EVERY FRAME.<br />MADE WITH CODE<span style={{ color: 'var(--acid)' }}>.</span></div>
        <div className="ar-ctas">
          <Link to="/system" data-cursor="THE SYSTEM" data-mag className="go mag glow-hover">THE SYSTEM →</Link>
          <Link to="/" data-cursor="THE GATE" data-mag className="go ghost mag glow-hover">BACK TO THE GATE</Link>
        </div>
        <div className="ar-footmeta cmd">THE ARSENAL · 6 REELS · 22 POSTS · 8 VO · #EWasteOff</div>
      </footer>
    </main>
  );
}
