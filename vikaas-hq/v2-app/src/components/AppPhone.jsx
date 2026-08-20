import { useMemo, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sparkles } from '@react-three/drei';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import * as THREE from 'three';

/* ============================================================
 * APPPHONE — the self-made 3D model of the VIKAAS app phone.
 * ------------------------------------------------------------
 * Built from primitives (no downloaded assets): rounded-box
 * body, notch, camera dot, GLSL-shader app screen (the screen is
 * a custom ShaderMaterial — animated UI rendered in fragment
 * shader code), plus orbiting e-waste chips and a live scan
 * sweep. Mouse-reactive: the phone leans toward the cursor.
 * ============================================================ */

const SCREEN_VERT = `
varying vec2 vUv;
void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`;

const SCREEN_FRAG = `
precision highp float;
uniform float uTime;
varying vec2 vUv;

float sdRoundRect(vec2 p, vec2 b, float r){
  vec2 q = abs(p) - b + r;
  return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
}

void main(){
  vec2 uv = vUv;
  vec2 p = uv - 0.5;
  p.x *= 0.4737; // aspect-correct (1.62 / 3.42)

  // rounded screen mask
  if (sdRoundRect(p, vec2(0.5, 0.5), 0.055) > 0.0) discard;

  // base ink gradient
  vec3 col = mix(vec3(0.010, 0.026, 0.018), vec3(0.05, 0.09, 0.06), uv.y);

  // header strip
  col = mix(col, vec3(0.028, 0.05, 0.034), smoothstep(0.80, 0.86, uv.y));
  float d0 = length(p - vec2(-0.38, 0.42));
  col = mix(col, vec3(0.73, 1.0, 0.25), smoothstep(0.05, 0.02, d0));
  float d0b = length(p - vec2(-0.30, 0.42));
  col = mix(col, vec3(0.18, 0.87, 0.51), smoothstep(0.05, 0.02, d0b));

  // app rows (sliding cards with accent dots)
  for (int i = 0; i < 4; i++){
    float fi = float(i);
    float y = 0.60 - fi * 0.165;
    float slide = sin(uTime * 0.9 + fi * 1.7) * 0.015;
    vec2 c = vec2(p.x, p.y - y + slide);
    float d2 = sdRoundRect(c, vec2(0.42, 0.055), 0.03);
    float on = smoothstep(0.0, -0.02, d2);
    col = mix(col, vec3(0.09, 0.13, 0.10), on);
    float dd = length(c - vec2(-0.34, 0.0));
    col = mix(col, vec3(0.73, 1.0, 0.25), smoothstep(0.035, 0.012, dd) * on);
    float l1 = smoothstep(0.0, -0.012, sdRoundRect(c - vec2(0.02, 0.0), vec2(0.30, 0.008), 0.004));
    col = mix(col, vec3(0.36, 0.46, 0.38), l1 * on);
    float l2 = smoothstep(0.0, -0.012, sdRoundRect(c - vec2(0.02, -0.028), vec2(0.22, 0.006), 0.004));
    col = mix(col, vec3(0.22, 0.30, 0.24), l2 * on);
  }

  // scan sweep
  float sweep = fract(uTime * 0.45);
  float sw = smoothstep(0.03, 0.0, abs(uv.y - sweep));
  col += vec3(0.73, 1.0, 0.25) * sw * 0.12;

  // bottom CTA pill
  float db = sdRoundRect(vec2(p.x, p.y + 0.42), vec2(0.32, 0.05), 0.03);
  float onb = smoothstep(0.0, -0.02, db);
  col = mix(col, vec3(0.73, 1.0, 0.25), onb);
  col = mix(col, vec3(0.02, 0.03, 0.02), onb * 0.42);
  float dl = smoothstep(0.0, -0.012, sdRoundRect(vec2(p.x, p.y + 0.42), vec2(0.18, 0.012), 0.006));
  col = mix(col, vec3(0.02, 0.03, 0.02), dl * onb * 0.85);

  // vignette
  col *= 1.0 - length(p) * 0.32;

  gl_FragColor = vec4(col, 1.0);
}
`;

function Phone() {
  const group = useRef();
  const screenMat = useRef();

  // imperative geometries (reliable with three examples classes)
  const bodyGeo = useMemo(() => new RoundedBoxGeometry(1.9, 3.9, 0.2, 10, 0.14), []);
  const rimGeo = useMemo(() => new RoundedBoxGeometry(2.0, 4.0, 0.3, 10, 0.16), []);
  useEffect(() => () => { bodyGeo.dispose(); rimGeo.dispose(); }, [bodyGeo, rimGeo]);

  useFrame(({ clock, pointer }) => {
    const t = clock.getElapsedTime();
    if (screenMat.current) screenMat.current.uniforms.uTime.value = t;
    if (group.current) {
      group.current.rotation.y += (pointer.x * 0.4 - group.current.rotation.y) * 0.06;
      group.current.rotation.x += (-pointer.y * 0.22 - group.current.rotation.x) * 0.06;
    }
  });

  return (
    <group ref={group} rotation={[0.06, -0.28, 0]}>
      {/* body — self-made rounded box */}
      <mesh geometry={bodyGeo}>
        <meshStandardMaterial color="#0b1013" metalness={0.85} roughness={0.3} />
      </mesh>
      {/* acid rim halo */}
      <mesh geometry={rimGeo}>
        <meshBasicMaterial color="#2ede82" transparent opacity={0.05} />
      </mesh>
      {/* GLSL app screen */}
      <mesh position={[0, 0.05, 0.103]}>
        <planeGeometry args={[1.62, 3.42]} />
        <shaderMaterial
          ref={screenMat}
          uniforms={{ uTime: { value: 0 } }}
          vertexShader={SCREEN_VERT}
          fragmentShader={SCREEN_FRAG}
        />
      </mesh>
      {/* notch + camera */}
      <mesh position={[0, 1.72, 0.106]}>
        <boxGeometry args={[0.52, 0.13, 0.012]} />
        <meshBasicMaterial color="#000000" />
      </mesh>
      <mesh position={[0.44, 1.72, 0.108]}>
        <circleGeometry args={[0.038, 24]} />
        <meshBasicMaterial color="#16222a" />
      </mesh>
      {/* side button */}
      <mesh position={[0.96, 0.5, 0]} rotation={[0, 0, 0]}>
        <boxGeometry args={[0.03, 0.5, 0.08]} />
        <meshStandardMaterial color="#0d1215" metalness={0.8} roughness={0.4} />
      </mesh>
    </group>
  );
}

function Chips() {
  const ref = useRef();
  const N = 22;
  const data = useRef(null);
  if (!data.current) {
    data.current = Array.from({ length: N }, (_, i) => {
      const a = (i / N) * Math.PI * 2;
      return {
        pos: new THREE.Vector3(Math.cos(a) * 3.1, Math.sin(a * 1.7) * 1.9 + 0.3, Math.sin(a) * 1.4),
        rot: new THREE.Vector3(Math.random() * 3, Math.random() * 3, Math.random() * 3),
        s: 0.35 + Math.random() * 0.5,
        sp: 0.25 + Math.random() * 0.4,
        ph: Math.random() * Math.PI * 2,
      };
    });
  }
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    const m = new THREE.Matrix4();
    const q = new THREE.Quaternion();
    const e = new THREE.Euler();
    const s = new THREE.Vector3();
    data.current.forEach((d, i) => {
      d.pos.x = Math.cos((i / N) * Math.PI * 2 + t * 0.12 * d.sp) * 3.1;
      d.pos.y = Math.sin((i / N) * Math.PI * 2 * 1.7 + t * 0.1 * d.sp) * 1.9 + Math.sin(t * 0.4 + d.ph) * 0.3;
      d.pos.z = Math.sin((i / N) * Math.PI * 2 + t * 0.12 * d.sp) * 1.4;
      e.set(d.rot.x + t * d.sp * 0.3, d.rot.y + t * d.sp * 0.4, d.rot.z);
      q.setFromEuler(e);
      s.set(d.s, d.s, d.s);
      m.compose(d.pos, q, s);
      ref.current.setMatrixAt(i, m);
    });
    ref.current.instanceMatrix.needsUpdate = true;
  });
  return (
    <instancedMesh ref={ref} args={[undefined, undefined, N]}>
      <boxGeometry args={[0.34, 0.52, 0.06]} />
      <meshStandardMaterial color="#10160f" metalness={0.7} roughness={0.35} emissive="#2ede82" emissiveIntensity={0.18} />
    </instancedMesh>
  );
}

export default function AppPhone() {
  return (
    <Canvas
      dpr={[1, 1.75]}
      camera={{ position: [0, 0.3, 6.6], fov: 40 }}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      style={{ width: '100%', height: '100%' }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[4, 6, 8]} intensity={1.2} color="#b9ff3f" />
      <pointLight position={[0, 0, 2.8]} intensity={7} color="#2ede82" distance={7} />
      <Float speed={1.4} rotationIntensity={0.12} floatIntensity={0.5}>
        <Phone />
      </Float>
      <Chips />
      <Sparkles count={80} scale={[7, 7, 4]} size={1.7} speed={0.35} color="#b9ff3f" opacity={0.45} />
    </Canvas>
  );
}
