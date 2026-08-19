import { useEffect, useRef } from 'react';
import * as THREE from 'three';

/* ============================================================
 * SCAPE — the global fixed 3D background (the "living void")
 * ------------------------------------------------------------
 * A fixed, mouse-reactive particle field behind EVERY page:
 *   - 600 soft glowing particles (acid + green + gold)
 *   - 36 instanced "e-waste chips" (boxes/rings) drifting
 *   - mouse: particles repel + camera parallax
 *   - scroll: slow vertical drift
 * Safety: try/catch WebGL (silent skip), prefers-reduced-motion
 * renders one static frame, pauses when tab hidden, full dispose
 * on unmount (React law #1 — no leaks).
 * ============================================================ */
export default function Scape() {
  const ref = useRef(null);
  const stateRef = useRef(null);

  useEffect(() => {
    const host = ref.current;
    if (!host) return;

    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let renderer, scene, camera, points, chips, raf = 0, disposed = false;
    let w = 1, h = 1, mx = 0, my = 0, tmx = 0, tmy = 0;

    try {
      renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true, powerPreference: 'low-power' });
      const gl = renderer.getContext();
      if (!gl) throw new Error('no context');
      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
      renderer.setSize(host.clientWidth || innerWidth, host.clientHeight || innerHeight);
      host.appendChild(renderer.domElement);
      renderer.domElement.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.85';
    } catch (e) {
      return; // silent skip — no console noise, CSS nebula still carries the mood
    }

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x040605, 0.055);
    camera = new THREE.PerspectiveCamera(60, 1, 0.1, 60);
    camera.position.z = 10;

    /* ---- soft particle sprite ---- */
    const cv = document.createElement('canvas');
    cv.width = cv.height = 64;
    const ctx = cv.getContext('2d');
    const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, 'rgba(255,255,255,1)');
    g.addColorStop(0.35, 'rgba(185,255,63,.9)');
    g.addColorStop(1, 'rgba(185,255,63,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(cv);

    const N = 600;
    const pos = new Float32Array(N * 3);
    const col = new Float32Array(N * 3);
    const PAL = [[185, 255, 63], [46, 222, 130], [255, 211, 77], [167, 139, 250], [234, 255, 244]];
    for (let i = 0; i < N; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 34;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 20;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 14;
      const c = PAL[(Math.random() * PAL.length) | 0];
      col[i * 3] = c[0] / 255; col[i * 3 + 1] = c[1] / 255; col[i * 3 + 2] = c[2] / 255;
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    pGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const pMat = new THREE.PointsMaterial({
      size: 0.09, map: tex, transparent: true, depthWrite: false,
      vertexColors: true, blending: THREE.AdditiveBlending, opacity: 0.55,
    });
    points = new THREE.Points(pGeo, pMat);
    scene.add(points);

    /* ---- instanced e-waste chips (boxes + rings) ---- */
    const chipGeo = new THREE.BoxGeometry(0.28, 0.42, 0.05);
    const chipMat = new THREE.MeshStandardMaterial({
      color: 0x10150f, metalness: 0.7, roughness: 0.35,
      emissive: 0x2ede82, emissiveIntensity: 0.12,
    });
    const C = 36;
    chips = new THREE.InstancedMesh(chipGeo, chipMat, C);
    const m4 = new THREE.Matrix4();
    const q = new THREE.Quaternion();
    const e = new THREE.Euler();
    const scl = new THREE.Vector3();
    const chipData = [];
    for (let i = 0; i < C; i++) {
      const p = new THREE.Vector3((Math.random() - 0.5) * 26, (Math.random() - 0.5) * 15, (Math.random() - 0.5) * 8);
      const r = new THREE.Vector3(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
      const s = 0.6 + Math.random() * 1.6;
      chipData.push({ p, r, s, sp: 0.2 + Math.random() * 0.5, ph: Math.random() * Math.PI * 2 });
      e.set(r.x, r.y, r.z); q.setFromEuler(e);
      scl.set(s, s, s);
      m4.compose(p, q, scl);
      chips.setMatrixAt(i, m4);
    }
    scene.add(chips);
    const light = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(light);
    const dlight = new THREE.DirectionalLight(0xb9ff3f, 0.9);
    dlight.position.set(4, 6, 8);
    scene.add(dlight);

    /* ---- interaction ---- */
    const onMove = (e) => { tmx = (e.clientX / innerWidth) * 2 - 1; tmy = -(e.clientY / innerHeight) * 2 + 1; };
    const onResize = () => {
      w = host.clientWidth || innerWidth; h = host.clientHeight || innerHeight;
      camera.aspect = w / h; camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    addEventListener('mousemove', onMove, { passive: true });
    addEventListener('resize', onResize);
    onResize();

    const vp = new THREE.Vector3();
    const target = new THREE.Vector3();
    const mouse3 = new THREE.Vector3();

    const tick = () => {
      if (disposed) return;
      if (document.hidden) { raf = requestAnimationFrame(tick); return; }
      mx += (tmx - mx) * 0.04;
      my += (tmy - my) * 0.04;
      const t = performance.now() * 0.001;

      // camera parallax
      camera.position.x += (mx * 1.1 - camera.position.x) * 0.03;
      camera.position.y += (my * 0.7 - camera.position.y) * 0.03;
      camera.lookAt(0, 0, 0);

      // particle repel + drift
      const arr = points.geometry.attributes.position.array;
      mouse3.set(mx * 9, my * 5.5, 0);
      for (let i = 0; i < N; i++) {
        let x = arr[i * 3], y = arr[i * 3 + 1], z = arr[i * 3 + 2];
        vp.set(x, y, z);
        const d = vp.distanceTo(mouse3);
        if (d < 2.2) {
          vp.sub(mouse3).normalize().multiplyScalar((2.2 - d) * 0.06);
          x += vp.x; y += vp.y; z += vp.z;
        }
        y += Math.sin(t * 0.4 + i * 0.05) * 0.0016;
        arr[i * 3] = x; arr[i * 3 + 1] = y; arr[i * 3 + 2] = z;
      }
      points.geometry.attributes.position.needsUpdate = true;

      // chips drift + spin
      for (let i = 0; i < C; i++) {
        const d = chipData[i];
        d.p.x += Math.sin(t * d.sp + d.ph) * 0.0018;
        d.p.y += Math.cos(t * d.sp * 0.8 + d.ph) * 0.0012;
        e.set(d.r.x + t * 0.1 * d.sp, d.r.y + t * 0.14 * d.sp, d.r.z);
        q.setFromEuler(e);
        scl.set(d.s, d.s, d.s);
        m4.compose(d.p, q, scl);
        chips.setMatrixAt(i, m4);
      }
      chips.instanceMatrix.needsUpdate = true;

      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };

    if (reduce) {
      renderer.render(scene, camera); // one static frame
    } else {
      raf = requestAnimationFrame(tick);
    }

    stateRef.current = { renderer, scene, points, chips, stop: () => { disposed = true; } };

    return () => {
      disposed = true;
      cancelAnimationFrame(raf);
      removeEventListener('mousemove', onMove);
      removeEventListener('resize', onResize);
      try {
        points.geometry.dispose(); points.material.map.dispose(); points.material.dispose();
        chips.geometry.dispose(); chips.material.dispose();
        tex.dispose();
        renderer.dispose();
        renderer.forceContextLoss();
      } catch (e) { /* noop */ }
      if (renderer.domElement && renderer.domElement.parentNode === host) {
        host.removeChild(renderer.domElement);
      }
      stateRef.current = null;
    };
  }, []);

  return <div ref={ref} aria-hidden="true" style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none' }} />;
}
