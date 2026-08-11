/* ============================================================
   VIKAAS v2 — LOADER v3 "THE BOOT · FINALE"
   Timeline (460vh pinned, scrub):
     0.00–0.02  HUD + cue in · rail live
     0.02–0.10  terminal lines reveal (scroll-linked)
     0.08–0.20  camera push-in (object-tween pattern) · lid creaks
     0.20–0.38  lid swings open · LIGHT SPILL ignites · e-waste floats + orbits
     0.38–0.52  VIKAAS scramble-assembles · glitch · pulse glow starts
     0.52–0.64  stats slam (scanline sweep) + stamps rotate in
     0.64–0.78  ReBee arcs across (fixed aspect) · विकास in
     0.78–0.90  big line char-stagger reveal (SplitType)
     0.88–1.00  ENTER pill (wide reliable window) · click → acid exit
   ?fast=1 / reduced-motion → final state. Mobile-safe layout.
   ============================================================ */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fast = new URLSearchParams(location.search).has('fast');
  const $ = (s) => document.querySelector(s);
  const stage = $('#stage'), wordEl = $('#word'), devEl = $('#dev'), termEl = $('#term'),
        cueEl = $('#cue'), railFill = $('#railFill'), enterBtn = $('#enter'),
        rebee = $('#rebeeFly'), bigline = $('#bigline h2'), hudTime = $('#hudTime');
  const stats = Array.from(document.querySelectorAll('.stat'));
  const stamps = Array.from(document.querySelectorAll('.stamp'));

  /* ---------- HUD clock ---------- */
  const pad = (n) => String(n).padStart(2, '0');
  const tick = () => { const d = new Date(); hudTime.textContent = pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds()) + ' IST'; };
  tick(); setInterval(tick, 1000);

  /* ---------- word chars + big line chars ---------- */
  const FULL = 'VIKAAS';
  wordEl.innerHTML = FULL.split('').map((c) => '<span class="ch">' + c + '</span>').join('');
  const chars = Array.from(wordEl.querySelectorAll('.ch'));
  const SCR = '!<>-_\\/[]{}—=+*^?#$%&@ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  const rand = () => SCR[Math.floor(Math.random() * SCR.length)];
  let bigChars = [];
  if (window.SplitType && !reduce) {
    const st = new SplitType(bigline, { types: 'chars' });
    bigChars = st.chars || [];
    gsap.set(bigChars, { yPercent: 120, opacity: 0 });
  } else {
    gsap.set(bigline, { opacity: 1 });
  }

  /* ---------- terminal ---------- */
  const LINES = [
    ['scanning drawer inventory', '3 phones · 7 chargers · 1 speaker (2022)', 'dim'],
    ['weighing …', '1.4 KG — receipt logged', 'acid'],
    ['surveying 10 homes …', '10/10 have the same drawer', 'dim'],
    ['querying HSPCB registry …', '15 authorised recyclers found', 'acid'],
    ['doorsteps served …', '0', 'red'],
    ['summoning ReBee …', 'scrap-scan online', 'gold'],
    ['finalising …', 'NO DRAWER LEFT BEHIND', 'acid'],
  ];
  termEl.innerHTML = LINES.map(([t, v, c]) => `<span class="${c}" data-l>${t} ${v}</span>`).join('\n');
  const termLines = Array.from(termEl.querySelectorAll('[data-l]'));
  const cursor = document.createElement('span'); cursor.className = 'cur'; termEl.appendChild(cursor);

  /* ---------- 3D SCENE ---------- */
  let renderer = null, scene = null, camera = null, drawerGroup = null, lidPivot = null,
      items = [], particles = null, spill = null, grid = null, THREE_OK = false;
  const cam = { x: 0, y: 1.1, z: 7.6, lx: 0, ly: -0.3, lz: 0 };
  function initThree() {
    try { renderer = new THREE.WebGLRenderer({ canvas: $('#three'), antialias: true, alpha: true }); }
    catch (e) { document.body.classList.add('no3d'); return; }
    THREE_OK = true;
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 60);
    camera.position.set(cam.x, cam.y, cam.z); camera.lookAt(cam.lx, cam.ly, cam.lz);

    scene.add(new THREE.AmbientLight(0x23352a, 1.1));
    const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(4, 7, 5); scene.add(key);
    const acid = new THREE.PointLight(0xb9ff3f, 26, 18); acid.position.set(-3, 1.5, 3); scene.add(acid);
    const rim = new THREE.PointLight(0x2ede82, 14, 16); rim.position.set(3, -1, 4); scene.add(rim);
    // LIGHT SPILL inside the drawer (ignites when lid opens)
    spill = new THREE.PointLight(0xb9ff3f, 0, 12); spill.position.set(0, -0.5, 0.6); scene.add(spill);

    // ground grid
    grid = new THREE.GridHelper(14, 28, 0x1d2a22, 0x0f1a14);
    grid.position.y = -1.75; scene.add(grid);

    // ---- THE DRAWER ----
    drawerGroup = new THREE.Group();
    const metal = new THREE.MeshStandardMaterial({ color: 0x12171a, metalness: 0.82, roughness: 0.34 });
    const dark = new THREE.MeshStandardMaterial({ color: 0x0a0f0c, metalness: 0.6, roughness: 0.5 });
    const body = new THREE.Mesh(new THREE.BoxGeometry(3.1, 1.5, 2.1), metal);
    body.position.y = -0.85; drawerGroup.add(body);
    const cv = document.createElement('canvas'); cv.width = 512; cv.height = 160;
    const ctx = cv.getContext('2d');
    ctx.fillStyle = '#0d1310'; ctx.fillRect(0, 0, 512, 160);
    ctx.strokeStyle = '#1d2a22'; ctx.lineWidth = 6; ctx.strokeRect(10, 10, 492, 140);
    ctx.fillStyle = '#b9ff3f'; ctx.font = '700 72px Anton, sans-serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('VIKAAS', 256, 84);
    const tex = new THREE.CanvasTexture(cv);
    const panel = new THREE.Mesh(new THREE.PlaneGeometry(2.5, 0.78), new THREE.MeshBasicMaterial({ map: tex }));
    panel.position.set(0, -0.85, 1.06); drawerGroup.add(panel);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.1, 1.5, 2.1)), new THREE.LineBasicMaterial({ color: 0x2ede82, transparent: true, opacity: 0.5 }));
    edges.position.y = -0.85; drawerGroup.add(edges);
    lidPivot = new THREE.Group(); lidPivot.position.set(0, -0.1, -1.0);
    const lid = new THREE.Mesh(new THREE.BoxGeometry(3.35, 0.22, 2.35), metal);
    lid.position.set(0, 0, 1.0); lidPivot.add(lid);
    const lidEdge = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.35, 0.22, 2.35)), new THREE.LineBasicMaterial({ color: 0xb9ff3f, transparent: true, opacity: 0.35 }));
    lidEdge.position.set(0, 0, 1.0); lidPivot.add(lidEdge);
    drawerGroup.add(lidPivot);
    const base = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.16, 2.5), dark); base.position.y = -1.63; drawerGroup.add(base);
    scene.add(drawerGroup);

    // ---- E-WASTE ----
    const makeItem = (geo, mat, x, y, z, rot) => {
      const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); if (rot) m.rotation.set(rot[0], rot[1], rot[2]);
      drawerGroup.add(m); items.push(m); return m;
    };
    const glassMat = new THREE.MeshStandardMaterial({ color: 0x1b2420, emissive: 0x2ede82, emissiveIntensity: 0.25, metalness: 0.3, roughness: 0.4 });
    const phone = makeItem(new THREE.BoxGeometry(0.78, 1.5, 0.07), glassMat, -0.85, -0.55, 0.05, [0, 0.35, 0.12]);
    const phoneScreen = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 1.32), new THREE.MeshBasicMaterial({ color: 0x0a2a18 }));
    phoneScreen.position.set(0, 0, 0.05); phone.add(phoneScreen);
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(-0.4, -0.6, 0.1), new THREE.Vector3(0.1, -0.2, 0.3), new THREE.Vector3(0.45, -0.5, 0.05), new THREE.Vector3(0.8, -0.2, 0.25)]);
    const cable = new THREE.Mesh(new THREE.TubeGeometry(curve, 24, 0.045, 8), new THREE.MeshStandardMaterial({ color: 0x151a1d, metalness: 0.4, roughness: 0.6 }));
    drawerGroup.add(cable); items.push(cable);
    const cable2 = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(1.0, -0.7, 0.0), new THREE.Vector3(1.3, -0.3, 0.2), new THREE.Vector3(1.55, -0.6, -0.05)]), 20, 0.035, 8), new THREE.MeshStandardMaterial({ color: 0x20262a, metalness: 0.35, roughness: 0.6 }));
    drawerGroup.add(cable2); items.push(cable2);
    const battery = makeItem(new THREE.BoxGeometry(0.62, 0.3, 0.95), new THREE.MeshStandardMaterial({ color: 0x2a2f33, metalness: 0.5, roughness: 0.5 }), 0.35, -0.7, 0.3, [0.1, -0.3, 0.2]);
    const charger = makeItem(new THREE.BoxGeometry(0.5, 0.5, 0.14), new THREE.MeshStandardMaterial({ color: 0x1c2125, metalness: 0.6, roughness: 0.45 }), -0.2, -0.75, -0.4, [0.2, 0.5, -0.1]);
    const prong = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.3, 8), new THREE.MeshStandardMaterial({ color: 0x8a939b, metalness: 0.9, roughness: 0.25 }));
    prong.position.set(0.14, -0.36, 0); charger.add(prong);
    const pcb = makeItem(new THREE.BoxGeometry(1.3, 0.05, 0.9), new THREE.MeshStandardMaterial({ color: 0x0f3d22, roughness: 0.6 }), 0.6, -0.55, -0.55, [0.1, 0.2, 0.05]);
    const pcbLine = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1.3, 0.05, 0.9)), new THREE.LineBasicMaterial({ color: 0xb9ff3f, transparent: true, opacity: 0.6 }));
    pcbLine.position.copy(pcb.position); pcbLine.rotation.copy(pcb.rotation); drawerGroup.add(pcbLine);

    // ---- PARTICLES ----
    const N = 420, pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
    const palette = [[0.72, 1, 0.25], [0.18, 0.87, 0.51], [1, 0.83, 0.3], [0.92, 0.94, 0.96]];
    for (let i = 0; i < N; i++) {
      const r = 2.2 + Math.random() * 5.5, a = Math.random() * Math.PI * 2, y = (Math.random() - 0.5) * 6;
      pos[i * 3] = Math.cos(a) * r; pos[i * 3 + 1] = y; pos[i * 3 + 2] = Math.sin(a) * r;
      const c = palette[i % 4]; col[i * 3] = c[0]; col[i * 3 + 1] = c[1]; col[i * 3 + 2] = c[2];
    }
    const pg = new THREE.BufferGeometry();
    pg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    pg.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const pm = new THREE.PointsMaterial({ size: 0.05, vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false });
    particles = new THREE.Points(pg, pm); scene.add(particles);

    addEventListener('resize', () => { renderer.setSize(innerWidth, innerHeight); camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); });
  }
  initThree();

  /* ---------- render loop: apply cam object + bob + parallax ---------- */
  let mx = 0, my = 0;
  addEventListener('pointermove', (e) => { mx = (e.clientX / innerWidth - 0.5); my = (e.clientY / innerHeight - 0.5); }, { passive: true });
  (function loop() {
    if (THREE_OK) {
      // smooth camera toward the tweened cam object
      camera.position.x += ((cam.x + mx * 0.35) - camera.position.x) * 0.06;
      camera.position.y += ((cam.y + my * 0.18) - camera.position.y) * 0.06;
      camera.position.z += (cam.z - camera.position.z) * 0.06;
      camera.lookAt(cam.lx, cam.ly, cam.lz);
      if (particles) particles.rotation.y += 0.0006;
      items.forEach((it, i) => {
        if (it.userData.bob) it.position.y = it.userData.baseY + Math.sin(performance.now() * 0.0012 + i * 1.7) * 0.05;
        if (it.userData.spin) it.rotation.y += 0.004 * (i % 2 ? 1 : -1);
      });
      renderer.render(scene, camera);
    }
    requestAnimationFrame(loop);
  })();

  /* ---------- AUDIO ---------- */
  let unlocked = false;
  const unlock = () => { if (unlocked) return; unlocked = true; const a = new Audio('assets/audio/boot.wav'); a.volume = 0.7; a.play().catch(() => {}); };
  ['wheel', 'touchstart', 'pointerdown'].forEach((ev) => addEventListener(ev, unlock, { passive: true, once: true }));
  const whoosh = () => {
    if (!unlocked) return;
    try {
      const C = new (window.AudioContext || window.webkitAudioContext)();
      const len = C.sampleRate * 0.7, buf = C.createBuffer(1, len, C.sampleRate), d = buf.getChannelData(0);
      for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
      const src = C.createBufferSource(); src.buffer = buf;
      const f = C.createBiquadFilter(); f.type = 'bandpass'; f.frequency.setValueAtTime(300, C.currentTime); f.frequency.exponentialRampToValueAtTime(2400, C.currentTime + 0.6); f.Q.value = 1.1;
      const g = C.createGain(); g.gain.value = 0.12;
      src.connect(f); f.connect(g); g.connect(C.destination); src.start();
    } catch (e) {}
  };

  /* ---------- MASTER TIMELINE ---------- */
  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: { trigger: '#stage', start: 'top top', end: '+=4600', pin: true, scrub: 0.6 },
    onUpdate: function () {
      const p = this.progress;
      railFill.style.height = (p * 100) + '%';
      if (p > 0.38 && p < 0.52) {
        const n = Math.min(FULL.length, Math.floor((p - 0.38) / 0.14 * FULL.length));
        chars.forEach((ch, i) => { ch.textContent = i < n ? FULL[i] : rand(); });
      }
      const lineIdx = Math.min(LINES.length - 1, Math.floor(p / 0.14));
      cursor.style.display = p < 0.1 && lineIdx < LINES.length ? 'inline-block' : 'none';
    },
  });

  tl.to('.hud', { opacity: 1, duration: 0.02 }, 0.005);
  tl.to('#cue', { opacity: 1, duration: 0.02 }, 0.01);

  termLines.forEach((ln, i) => {
    tl.fromTo(ln, { opacity: 0.12 }, { opacity: 1, duration: 0.02 }, 0.02 + i * 0.014);
  });

  if (THREE_OK) {
    // camera object tweens (codrops pattern)
    tl.to(cam, { z: 6.6, duration: 0.12 }, 0.08);
    tl.to(lidPivot.rotation, { x: 0.05, duration: 0.06 }, 0.12);
    tl.to(lidPivot.rotation, { x: 1.28, duration: 0.18, ease: 'power2.inOut' }, 0.20);
    tl.to(spill, { intensity: 9, duration: 0.14, ease: 'power1.out' }, 0.22);
    tl.to(drawerGroup.position, { y: -0.25, duration: 0.12 }, 0.20);
    tl.to(drawerGroup.scale, { x: 0.9, y: 0.9, z: 0.9, duration: 0.14 }, 0.20);
    items.forEach((it, i) => {
      const dir = (i % 2 ? 1 : -1) * (0.5 + (i % 3) * 0.25);
      it.userData.baseY = it.position.y;
      it.userData.bob = true;
      it.userData.spin = true;
      tl.to(it.position, { y: it.position.y + 1.5 + (i % 3) * 0.4, duration: 0.1, ease: 'power1.out' }, 0.21 + i * 0.012);
      tl.to(it.rotation, { y: it.rotation.y + 1.2 * dir, duration: 0.1 }, 0.21 + i * 0.012);
    });
    tl.to(cam, { z: 5.2, y: 0.75, duration: 0.16, ease: 'power1.inOut' }, 0.44);
  }

  // wordmark
  chars.forEach((ch, i) => {
    tl.fromTo(ch, { yPercent: 130, rotate: 12, scale: 0.7 }, { yPercent: 0, rotate: 0, scale: 1, opacity: 1, duration: 0.035, ease: 'back.out(2)' }, 0.385 + i * 0.012);
  });
  tl.call(function () { wordEl.classList.add('glitching'); }, [], 0.40);
  tl.call(function () { wordEl.classList.remove('glitching'); }, [], 0.403);
  tl.call(function () { wordEl.classList.add('glitching'); }, [], 0.465);
  tl.call(function () { wordEl.classList.remove('glitching'); }, [], 0.468);
  tl.call(function () { wordEl.classList.add('pulse'); }, [], 0.50);
  tl.call(whoosh, [], 0.52);

  // stats
  stats.forEach((s, i) => {
    tl.fromTo(s, { scale: 0.4, y: 60, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.045, ease: 'back.out(2.2)' }, 0.535 + i * 0.02);
  });
  stamps.forEach((s, i) => {
    tl.fromTo(s, { scale: 2.2, rotate: (i % 2 ? 12 : -12), opacity: 0 }, { scale: 1, rotate: 7, opacity: 1, duration: 0.03, ease: 'back.out(2)' }, 0.60 + i * 0.01);
  });

  // ReBee arc
  tl.to(rebee, { opacity: 1, duration: 0.01 }, 0.64);
  tl.fromTo(rebee, { left: '-22vw', top: '20%' }, { left: '108vw', top: '12%', duration: 0.14, ease: 'power1.in' }, 0.64);
  tl.to(rebee, { opacity: 0, duration: 0.02 }, 0.78);
  tl.to(devEl, { opacity: 1, duration: 0.03 }, 0.68);
  tl.call(whoosh, [], 0.78);

  // big line char reveal
  tl.to(bigline, { clipPath: 'inset(0 0% 0 0)', duration: 0.05, ease: 'power2.inOut' }, 0.78);
  if (bigChars.length) {
    tl.fromTo(bigChars, { yPercent: 120, opacity: 0 }, { yPercent: 0, opacity: 1, stagger: 0.012, duration: 0.045, ease: 'back.out(1.8)' }, 0.80);
  }
  tl.to(cueEl, { opacity: 0, duration: 0.02 }, 0.85);

  // ENTER — wide reliable window
  tl.to(enterBtn, { opacity: 1, y: 0, scale: 1, duration: 0.06, ease: 'back.out(2)' }, 0.88)
    .add(function () { enterBtn.classList.add('show'); }, 0.90);

  /* ---------- ENTER ---------- */
  enterBtn.addEventListener('click', () => {
    if (unlocked) { const a = new Audio('assets/audio/enter.wav'); a.volume = 0.9; a.play().catch(() => {}); }
    stage.classList.add('leaving');
    setTimeout(() => { location.href = 'index.html'; }, 1100);
  });
  addEventListener('keydown', (e) => { if (e.key === 'Enter' && enterBtn.classList.contains('show')) enterBtn.click(); });

  /* ---------- fast / reduced-motion ---------- */
  if (fast || reduce) {
    gsap.set('.hud', { opacity: 1 });
    gsap.set(termLines, { opacity: 1 });
    gsap.set(chars, { opacity: 1, yPercent: 0, rotate: 0, scale: 1 });
    gsap.set(stats, { opacity: 1, scale: 1, y: 0 });
    gsap.set(stamps, { opacity: 1, scale: 1, rotate: 7 });
    gsap.set(devEl, { opacity: 1 });
    gsap.set(bigline, { clipPath: 'inset(0 0% 0 0)' });
    if (bigChars.length) gsap.set(bigChars, { yPercent: 0, opacity: 1 });
    gsap.set(rebee, { opacity: 0 });
    gsap.set(cueEl, { opacity: 0 });
    railFill.style.height = '100%';
    enterBtn.classList.add('show');
    if (reduce) ScrollTrigger.getAll().forEach((st) => st.disable());
  }
})();
