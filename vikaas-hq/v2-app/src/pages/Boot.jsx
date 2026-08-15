import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import * as THREE from 'three';
import rebeeImg from '../assets/img/rebee.png';
import './boot.css';

gsap.registerPlugin(ScrollTrigger);

const FULL = 'VIKAAS';
const SCR = '!<>-_\\/[]{}—=+*^?#$%&@ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const rand = () => SCR[Math.floor(Math.random() * SCR.length)];

const BOOT_LINES = [
  ['scanning drawer inventory', '3 phones · 7 chargers · 1 speaker (2022)', 'dim'],
  ['weighing …', '1.4 KG — receipt logged', 'acid'],
  ['surveying 10 homes …', '10/10 have the same drawer', 'dim'],
  ['querying HSPCB registry …', '15 authorised recyclers found', 'acid'],
  ['doorsteps served …', '0', 'red'],
  ['summoning ReBee …', 'scrap-scan online', 'gold'],
  ['mounting universe …', 'NO DRAWER LEFT BEHIND', 'acid'],
];
const STATUS = ['INITIALISING…', 'SCANNING…', 'WEIGHING…', 'VERIFYING…', 'SUMMONING…', 'READY.'];
const CHAPTERS = [['00', 'IGNITION'], ['01', 'THE OPEN'], ['02', 'THE WORD'], ['03', 'THE PROOF'], ['04', 'THE FLIGHT'], ['05', 'THE LINE'], ['06', 'THE DOOR']];
const esc = (s) => s.replace(/[<>&]/g, (m) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[m]));

export default function Boot() {
  const nav = useNavigate();
  const stageRef = useRef(null);
  const canvasRef = useRef(null);
  const wordRef = useRef(null);
  const devRef = useRef(null);
  const rebeeRef = useRef(null);
  const biglineRef = useRef(null);
  const railFillRef = useRef(null);
  const chapterRef = useRef(null);
  const railPctRef = useRef(null);
  const enterRef = useRef(null);
  const abRef = useRef(null);
  const abTermRef = useRef(null);
  const abBarRef = useRef(null);
  const abStatusRef = useRef(null);
  const abPctRef = useRef(null);
  const abWordRef = useRef(null);
  const [skipHidden, setSkipHidden] = useState(false);
  const [bootGone, setBootGone] = useState(false);

  useEffect(() => {
    const fast = new URLSearchParams(location.search).has('fast');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const wordEl = wordRef.current;
    wordEl.innerHTML = FULL.split('').map((c) => `<span class="ch">${c}</span>`).join('');
    const chars = Array.from(wordEl.querySelectorAll('.ch'));
    let bigChars = [];

    /* ===== 3D SCENE ===== */
    let renderer, scene, camera, drawerGroup, lidPivot, items = [], particles, spill;
    const cam = { x: 0, y: 1.1, z: 7.6, lx: 0, ly: -0.3, lz: 0 };
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current, antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.setSize(innerWidth, innerHeight);
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 60);
      camera.position.set(cam.x, cam.y, cam.z); camera.lookAt(cam.lx, cam.ly, cam.lz);
      scene.add(new THREE.AmbientLight(0x23352a, 1.1));
      const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(4, 7, 5); scene.add(key);
      const acid = new THREE.PointLight(0xb9ff3f, 26, 18); acid.position.set(-3, 1.5, 3); scene.add(acid);
      const rim = new THREE.PointLight(0x2ede82, 14, 16); rim.position.set(3, -1, 4); scene.add(rim);
      spill = new THREE.PointLight(0xb9ff3f, 0, 12); spill.position.set(0, -0.5, 0.6); scene.add(spill);
      const grid = new THREE.GridHelper(14, 28, 0x1d2a22, 0x0f1a14); grid.position.y = -1.75; scene.add(grid);

      drawerGroup = new THREE.Group();
      const metal = new THREE.MeshStandardMaterial({ color: 0x12171a, metalness: 0.82, roughness: 0.34 });
      const dark = new THREE.MeshStandardMaterial({ color: 0x0a0f0c, metalness: 0.6, roughness: 0.5 });
      const body = new THREE.Mesh(new THREE.BoxGeometry(3.1, 1.5, 2.1), metal); body.position.y = -0.85; drawerGroup.add(body);
      const cv = document.createElement('canvas'); cv.width = 512; cv.height = 160;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = '#0d1310'; ctx.fillRect(0, 0, 512, 160);
      ctx.strokeStyle = '#1d2a22'; ctx.lineWidth = 6; ctx.strokeRect(10, 10, 492, 140);
      ctx.fillStyle = '#b9ff3f'; ctx.font = '700 72px Anton, sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('VIKAAS', 256, 84);
      const panel = new THREE.Mesh(new THREE.PlaneGeometry(2.5, 0.78), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cv) }));
      panel.position.set(0, -0.85, 1.06); drawerGroup.add(panel);
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.1, 1.5, 2.1)), new THREE.LineBasicMaterial({ color: 0x2ede82, transparent: true, opacity: 0.5 }));
      edges.position.y = -0.85; drawerGroup.add(edges);
      lidPivot = new THREE.Group(); lidPivot.position.set(0, -0.1, -1.0);
      const lid = new THREE.Mesh(new THREE.BoxGeometry(3.35, 0.22, 2.35), metal); lid.position.set(0, 0, 1.0); lidPivot.add(lid);
      const lidEdge = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.35, 0.22, 2.35)), new THREE.LineBasicMaterial({ color: 0xb9ff3f, transparent: true, opacity: 0.35 }));
      lidEdge.position.set(0, 0, 1.0); lidPivot.add(lidEdge);
      drawerGroup.add(lidPivot);
      const base = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.16, 2.5), dark); base.position.y = -1.63; drawerGroup.add(base);
      scene.add(drawerGroup);

      const makeItem = (geo, mat, x, y, z, rot) => {
        const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); if (rot) m.rotation.set(rot[0], rot[1], rot[2]);
        drawerGroup.add(m); items.push(m); return m;
      };
      const glassMat = new THREE.MeshStandardMaterial({ color: 0x1b2420, emissive: 0x2ede82, emissiveIntensity: 0.25, metalness: 0.3, roughness: 0.4 });
      const phone = makeItem(new THREE.BoxGeometry(0.78, 1.5, 0.07), glassMat, -0.85, -0.55, 0.05, [0, 0.35, 0.12]);
      const phoneScreen = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 1.32), new THREE.MeshBasicMaterial({ color: 0x0a2a18 }));
      phoneScreen.position.set(0, 0, 0.05); phone.add(phoneScreen);
      const cable = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(-0.4, -0.6, 0.1), new THREE.Vector3(0.1, -0.2, 0.3), new THREE.Vector3(0.45, -0.5, 0.05), new THREE.Vector3(0.8, -0.2, 0.25)]), 24, 0.045, 8), new THREE.MeshStandardMaterial({ color: 0x151a1d, metalness: 0.4, roughness: 0.6 }));
      drawerGroup.add(cable); items.push(cable);
      const battery = makeItem(new THREE.BoxGeometry(0.62, 0.3, 0.95), new THREE.MeshStandardMaterial({ color: 0x2a2f33, metalness: 0.5, roughness: 0.5 }), 0.35, -0.7, 0.3, [0.1, -0.3, 0.2]);
      const charger = makeItem(new THREE.BoxGeometry(0.5, 0.5, 0.14), new THREE.MeshStandardMaterial({ color: 0x1c2125, metalness: 0.6, roughness: 0.45 }), -0.2, -0.75, -0.4, [0.2, 0.5, -0.1]);
      const pcb = makeItem(new THREE.BoxGeometry(1.3, 0.05, 0.9), new THREE.MeshStandardMaterial({ color: 0x0f3d22, roughness: 0.6 }), 0.6, -0.55, -0.55, [0.1, 0.2, 0.05]);

      const N = 520, pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
      const palette = [[0.72, 1, 0.25], [0.18, 0.87, 0.51], [1, 0.83, 0.3], [0.65, 0.55, 0.98], [0.92, 0.94, 0.96]];
      for (let i = 0; i < N; i++) {
        const r = 2.0 + Math.random() * 6, a = Math.random() * Math.PI * 2, y = (Math.random() - 0.5) * 6.5;
        pos[i * 3] = Math.cos(a) * r; pos[i * 3 + 1] = y; pos[i * 3 + 2] = Math.sin(a) * r;
        const c = palette[i % 5]; col[i * 3] = c[0]; col[i * 3 + 1] = c[1]; col[i * 3 + 2] = c[2];
      }
      const pg = new THREE.BufferGeometry();
      pg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      pg.setAttribute('color', new THREE.BufferAttribute(col, 3));
      particles = new THREE.Points(pg, new THREE.PointsMaterial({ size: 0.055, vertexColors: true, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending, depthWrite: false }));
      scene.add(particles);
    } catch (e) { /* no3d */ }

    let mx = 0, my = 0;
    const pm = (e) => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; };
    addEventListener('pointermove', pm, { passive: true });
    const loop = () => {
      if (renderer) {
        camera.position.x += ((cam.x + mx * 0.35) - camera.position.x) * 0.06;
        camera.position.y += ((cam.y + my * 0.18) - camera.position.y) * 0.06;
        camera.position.z += (cam.z - camera.position.z) * 0.06;
        camera.lookAt(cam.lx, cam.ly, cam.lz);
        if (particles) particles.rotation.y += 0.0006;
        items.forEach((it, i) => { if (it.userData.bob) it.position.y = it.userData.baseY + Math.sin(performance.now() * 0.0012 + i * 1.7) * 0.05; });
        renderer.render(scene, camera);
      }
      requestAnimationFrame(loop);
    };
    loop();

    /* ===== AUDIO ===== */
    let unlocked = false;
    const unlock = () => {
      if (unlocked) return; unlocked = true;
      try { new Audio('/audio/boot.wav').play().catch(() => {}); } catch (e) {}
      try {
        const amb = new Audio('/audio/boot_ambient.wav');
        amb.loop = true; amb.volume = 0.5;
        amb.play().catch(() => {});
        window.__amb = amb;
      } catch (e) {}
    };
    ['wheel', 'touchstart', 'pointerdown'].forEach((ev) => addEventListener(ev, unlock, { passive: true, once: true }));

    /* ===== AUTO BOOT ===== */
    const getBootEls = () => ({
      abTerm: document.querySelector('#abTerm'),
      abBar: document.querySelector('.ab-bar i'),
      abStatus: document.querySelector('.ab-status'),
      abWord: document.querySelector('.ab-word span'),
    });
    let { abTerm, abBar, abStatus, abWord } = getBootEls();

    const bootTimers = [];
    const T = (fn, ms) => { const id = setTimeout(fn, ms); bootTimers.push(id); return id; };

    const bootDone = () => {
      const ab = abRef.current; if (!ab) return;
      ab.classList.add('leaving');
      T(() => { setBootGone(true); enableScroll(); }, 1000);
    };
    const enableScroll = () => {
      ScrollTrigger.getAll().forEach((st) => st.enable());
      ScrollTrigger.refresh();
      gsap.to('#cue', { opacity: 1, duration: 0.8, delay: 0.3 });
      gsap.to('.hud', { opacity: 1, duration: 0.6, delay: 0.5 });
      if (chapterRef.current) gsap.to(chapterRef.current, { opacity: 1, duration: 0.6, delay: 0.5 });
    };
    if (!fast && !reduce) {
      ScrollTrigger.getAll().forEach((st) => st.disable());
      window.scrollTo(0, 0);
      abWord.innerHTML = FULL.split('').map((c) => `<span class="ch">${c}</span>`).join('');
      const abChars = Array.from(abWord.querySelectorAll('.ch'));
      const done = [];
      let li = 0, ci = 0, totalChars = BOOT_LINES.reduce((a, l) => a + l[0].length, 0), typed = 0;
      const render = () => {
        const els = getBootEls(); if (!els.abTerm || !els.abBar) return;
        const out = done.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`);
        const cur = BOOT_LINES[li];
        out.push(`<span class="${cur[2]}">${esc(cur[0].slice(0, ci))}</span><span class="cur"></span>`);
        els.abTerm.innerHTML = out.join('\n');
        const pct = Math.round((typed + ci) / totalChars * 100);
        els.abBar.style.width = pct + '%';
        const pctEl = document.querySelector('.ab-status span');
        if (pctEl) pctEl.textContent = pct + '%';
      };
      const type = () => {
        if (ci < BOOT_LINES[li][0].length) { ci++; typed++; render(); T(type, 18); }
        else {
          done.push(BOOT_LINES[li]); li++;
          if (li < BOOT_LINES.length) { ci = 0; abStatus.textContent = STATUS[Math.min(li, STATUS.length - 1)]; render(); T(type, 180); }
          else {
            abTerm.innerHTML = done.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`).join('\n') + '\n<span class="acid">> READY — awaiting command</span>';
            abBar.style.width = '100%'; abStatus.textContent = 'READY.';
            if (abPctRef.current) abPctRef.current.textContent = '100%';
            let frame = 0;
            (function tick() {
              const p = frame / 55;
              abChars.forEach((ch, i) => { ch.textContent = i < Math.floor(p * FULL.length) ? FULL[i] : rand(); });
              frame++;
              if (frame <= 55) T(tick, 26);
              else { abChars.forEach((ch, i) => { ch.textContent = FULL[i]; }); T(bootDone, 650); }
            })();
          }
        }
      };
      type();
    } else {
      setBootGone(true);
      gsap.set(['.hud', '#chapter', '#cue'], { opacity: 1 });
      enableScroll();
    }

    /* ===== SCROLL TIMELINE ===== */
    const railFill = railFillRef.current, chapterEl = chapterRef.current, railPct = railPctRef.current;
    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { trigger: '#track', start: 'top top', end: 'bottom bottom', scrub: 0.6 },
      onUpdate: function () {
        const p = this.progress;
        if (!isFinite(p)) return;
        if (railFill) railFill.style.height = (p * 100) + '%';
        if (railPct) railPct.textContent = Math.round(p * 100) + '%';
        if (chapterEl) {
          const ci = Math.min(CHAPTERS.length - 1, Math.max(0, Math.floor(p * CHAPTERS.length)));
          chapterEl.textContent = CHAPTERS[ci][0] + ' · ' + CHAPTERS[ci][1];
        }
        if (p > 0.38 && p < 0.52) {
          const n = Math.min(FULL.length, Math.floor((p - 0.38) / 0.14 * FULL.length));
          chars.forEach((ch, i) => { ch.textContent = i < n ? FULL[i] : rand(); });
        }
      },
    });
    tl.to('#cue', { opacity: 0, duration: 0.02 }, 0.02);
    if (renderer) {
      tl.to(cam, { z: 6.6, duration: 0.12 }, 0.05);
      tl.to(lidPivot.rotation, { x: 0.05, duration: 0.06 }, 0.10);
      tl.to(lidPivot.rotation, { x: -1.95, duration: 0.18, ease: 'power2.inOut' }, 0.18);
      tl.to(spill, { intensity: 9, duration: 0.14, ease: 'power1.out' }, 0.20);
      tl.to(drawerGroup.position, { y: -0.25, duration: 0.12 }, 0.18);
      tl.to(drawerGroup.scale, { x: 0.9, y: 0.9, z: 0.9, duration: 0.14 }, 0.18);
      items.forEach((it, i) => {
        it.userData.baseY = it.position.y; it.userData.bob = true;
        tl.to(it.position, { y: it.position.y + 1.5 + (i % 3) * 0.4, duration: 0.1, ease: 'power1.out' }, 0.19 + i * 0.012);
        tl.to(it.rotation, { y: it.rotation.y + 1.2 * (i % 2 ? 1 : -1) * (0.5 + (i % 3) * 0.25), duration: 0.1 }, 0.19 + i * 0.012);
      });
      tl.to(cam, { z: 5.2, y: 0.75, duration: 0.16, ease: 'power1.inOut' }, 0.44);
    }
    chars.forEach((ch, i) => {
      tl.fromTo(ch, { yPercent: 130, rotate: 12, scale: 0.7 }, { yPercent: 0, rotate: 0, scale: 1, opacity: 1, duration: 0.035, ease: 'back.out(2)' }, 0.385 + i * 0.012);
    });
    tl.call(() => { wordEl.classList.add('glitching'); }, [], 0.40);
    tl.call(() => { wordEl.classList.remove('glitching'); }, [], 0.403);
    tl.call(() => { wordEl.classList.add('pulse'); }, [], 0.50);
    const statsEls = Array.from(document.querySelectorAll('.stat'));
    statsEls.forEach((s, i) => {
      tl.fromTo(s, { scale: 0.4, y: 60, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.045, ease: 'back.out(2.2)' }, 0.535 + i * 0.02);
    });
    Array.from(document.querySelectorAll('.stamp')).forEach((s, i) => {
      tl.fromTo(s, { scale: 2.2, rotate: (i % 2 ? 12 : -12), opacity: 0 }, { scale: 1, rotate: 7, opacity: 1, duration: 0.03, ease: 'back.out(2)' }, 0.60 + i * 0.01);
    });
    const rebeeEl = rebeeRef.current;
    tl.to(rebeeEl, { opacity: 1, duration: 0.01 }, 0.64);
    tl.fromTo(rebeeEl, { left: '-22vw', top: '20%' }, { left: '108vw', top: '12%', duration: 0.14, ease: 'power1.in' }, 0.64);
    tl.to(rebeeEl, { opacity: 0, duration: 0.02 }, 0.78);
    tl.to(devRef.current, { opacity: 1, duration: 0.03 }, 0.68);
    const bl = biglineRef.current;
    tl.to(bl, { clipPath: 'inset(0 0% 0 0)', duration: 0.05, ease: 'power2.inOut' }, 0.78);
    const enterEl = enterRef.current;
    tl.to(enterEl, { opacity: 1, y: 0, scale: 1, duration: 0.06, ease: 'back.out(2)' }, 0.88)
      .add(() => enterEl.classList.add('show'), 0.90);

    if (fast || reduce) {
      gsap.set('.hud', { opacity: 1 });
      gsap.set(chars, { opacity: 1, yPercent: 0, rotate: 0, scale: 1 });
      gsap.set(statsEls, { opacity: 1, scale: 1, y: 0 });
      gsap.set('.stamp', { opacity: 1, scale: 1, rotate: 7 });
      gsap.set(devRef.current, { opacity: 1 });
      gsap.set(bl, { clipPath: 'inset(0 0% 0 0)' });
      gsap.set(rebeeEl, { opacity: 0 });
      enterEl.classList.add('show');
    }

    // (type loop uses T so cleanup can cancel)
    return () => {
      bootTimers.forEach(clearTimeout);
      removeEventListener('pointermove', pm);
      ScrollTrigger.getAll().forEach((st) => st.kill());
      if (renderer) { renderer.dispose(); }
      if (window.__amb) { try { window.__amb.pause(); } catch (e) {} window.__amb = null; }
    };
  }, [nav]);

  const enter = () => {
    const a = new Audio('/audio/enter.wav'); a.volume = 0.9; a.play().catch(() => {});
    if (stageRef.current) stageRef.current.classList.add('leaving');
    setTimeout(() => nav('/'), 1100);
  };

  return (
    <>
      <div id="track" style={{ height: '460vh' }}>
        <div id="stage" ref={stageRef}>
          <div className="nebula" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
          <canvas id="three" ref={canvasRef}></canvas>
          <div className="glow"></div>
          <div id="wordzone">
            <div id="word" ref={wordRef}></div>
            <div id="dev" ref={devRef}>विकास</div>
          </div>
          <div id="stats">
            <div className="stat"><b>1.4 KG</b><span>weighed on a kitchen scale</span><span className="stamp st-green">WEIGHED</span></div>
            <div className="stat"><b>₹40</b><span>cash at the gate</span><span className="stamp st-gold">RECEIPT #1</span></div>
            <div className="stat"><b>15</b><span>govt-authorised recyclers</span><span className="stamp st-green">SOURCED</span></div>
            <div className="stat"><b>0</b><span>doorsteps served</span><span className="stamp st-red">THE GAP</span></div>
          </div>
          <img id="rebeeFly" ref={rebeeRef} src={rebeeImg} alt="ReBee" />
          <div id="bigline"><h2 ref={biglineRef}>NO DRAWER LEFT BEHIND<span style={{ color: 'var(--acid)' }}>.</span></h2></div>
          <div id="chapter" className="cmd" ref={chapterRef}>00 · IGNITION</div>
          <div id="rail"><i ref={railFillRef}></i></div>
          <div id="railPct" ref={railPctRef}>0%</div>
          <div id="cue">SCROLL TO ENTER THE UNIVERSE</div>
          <button id="enter" ref={enterRef} onClick={enter}>ENTER THE DRAWER <span>→</span></button>
          <div className="scan"></div>
          <div className="scanlines"></div>
          <div className="vignette"></div>
          <div className="grain"></div>
        </div>
      </div>

      {!bootGone && <div id="autoBoot" ref={abRef} aria-hidden="true">
        <div className="nebula"><i></i><i></i><i></i><i></i></div>
        <div className="glow"></div>
        <div className="ab-box">
          <div className="ab-top cmd"><span>VIKAAS <b>OS</b></span><span>BOOT SEQUENCE <b>v5.0</b></span><span>GURUGRAM · <b>2026</b></span></div>
          <div className="ab-word"><span id="abWord" ref={abWordRef}></span></div>
          <pre id="abTerm" ref={abTermRef}></pre>
          <div className="ab-bar"><i ref={abBarRef}></i></div>
          <div className="ab-status cmd" ref={abStatusRef}>INITIALISING…</div>
        </div>
        <button id="abSkip" className="cmd" style={skipHidden ? { display: 'none' } : {}} onClick={() => {
          setSkipHidden(true);
          const ab = abRef.current; if (!ab || ab.classList.contains('leaving')) return;
          const term = abTermRef.current;
          term.innerHTML = BOOT_LINES.map(([t, v, c]) => `<span class="${c}">${esc(t)} ${esc(v)}</span>`).join('\n') + '\n<span class="acid">> READY — awaiting command</span>';
          abBarRef.current.style.width = '100%'; abStatusRef.current.textContent = 'READY.';
          ab.classList.add('leaving');
          T(() => { setBootGone(true); ScrollTrigger.getAll().forEach((st) => st.enable()); ScrollTrigger.refresh(); }, 1000);
        }}>SKIP BOOT →</button>
        <div className="scanlines"></div>
        <div className="vignette"></div>
        <div className="grain"></div>
      </div>}
    </>
  );
}
