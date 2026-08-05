"use client";

import { useMemo, useRef, useState, useCallback } from "react";
import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { Sparkles, Grid } from "@react-three/drei";
import { EffectComposer, Bloom, ChromaticAberration, Noise, Vignette } from "@react-three/postprocessing";
import ViewportPause from "./ViewportPause";

/**
 * The holographic digital-twin plant.
 * Fully procedural (no external GLB): tapered pot, tube stems, ribbon leaves —
 * everything shaded by one shared fresnel shader with a looping scan-band
 * that "rebuilds" the plant from the soil up every few seconds.
 */

const VERT = /* glsl */ `
  varying vec3 vNormal;
  varying vec3 vView;
  varying float vWy;
  void main() {
    vec4 world = modelMatrix * vec4(position, 1.0);
    vWy = world.y;
    vec4 mv = viewMatrix * world;
    vNormal = normalize(normalMatrix * normal);
    vView = normalize(-mv.xyz);
    gl_Position = projectionMatrix * mv;
  }
`;

const FRAG = /* glsl */ `
  uniform vec3 uColor;
  uniform vec3 uScanColor;
  uniform float uTime;
  uniform float uScanY;
  uniform float uScanGlow;
  uniform float uFlicker;
  uniform float uBase;
  varying vec3 vNormal;
  varying vec3 vView;
  varying float vWy;
  void main() {
    float fresnel = pow(1.0 - abs(dot(normalize(vNormal), normalize(vView))), 2.1);
    float band = exp(-pow((vWy - uScanY) * 14.0, 2.0)) * uScanGlow;
    float shimmer = 0.04 * sin(uTime * 2.3 + vWy * 9.0);
    vec3 col = uColor * (uBase + fresnel * 1.9 + shimmer) + uScanColor * band * 2.4;
    float alpha = (0.16 + fresnel * 0.75 + band * 0.65) * (1.0 - uFlicker * 0.35);
    gl_FragColor = vec4(col, alpha);
  }
`;

function useHoloMaterial(color = "#A6FF3F", scanColor = "#67E8F9") {
  return useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: VERT,
      fragmentShader: FRAG,
      uniforms: {
        uColor: { value: new THREE.Color(color) },
        uScanColor: { value: new THREE.Color(scanColor) },
        uTime: { value: 0 },
        uScanY: { value: -0.5 },
        uScanGlow: { value: 1 },
        uFlicker: { value: 0 },
        uBase: { value: 0.12 },
      },
      transparent: true,
      depthWrite: false,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
    });
  }, [color, scanColor]);
}

function Stem({ mat, points, radius = 0.022 }: { mat: THREE.ShaderMaterial; points: THREE.Vector3[]; radius?: number }) {
  const geo = useMemo(
    () => new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points), 28, radius, 6, false),
    [points, radius]
  );
  return <mesh geometry={geo} material={mat} />;
}

function Leaf({ mat, pos, rotY, scale = 1 }: { mat: THREE.ShaderMaterial; pos: THREE.Vector3; rotY: number; scale?: number }) {
  return (
    <mesh
      material={mat}
      position={[pos.x, pos.y, pos.z]}
      rotation={[0.35, rotY, 0.35]}
      scale={[0.30 * scale, 0.055 * scale, 0.15 * scale]}
    >
      <icosahedronGeometry args={[1, 1]} />
    </mesh>
  );
}

function HoloPlant() {
  const limeMat = useHoloMaterial();
  const hydroMat = useHoloMaterial("#67E8F9", "#A6FF3F");

  const stems = useMemo(() => {
    const defs: { pts: THREE.Vector3[]; lean: number }[] = [
      { pts: [new THREE.Vector3(0, 0.25, 0), new THREE.Vector3(0.05, 0.7, 0.02), new THREE.Vector3(-0.04, 1.2, -0.03), new THREE.Vector3(0.02, 1.55, 0)], lean: 0 },
      { pts: [new THREE.Vector3(0.06, 0.25, 0.03), new THREE.Vector3(0.32, 0.55, 0.1), new THREE.Vector3(0.5, 0.95, 0.14), new THREE.Vector3(0.62, 1.18, 0.1)], lean: 1 },
      { pts: [new THREE.Vector3(-0.06, 0.25, -0.02), new THREE.Vector3(-0.3, 0.6, -0.1), new THREE.Vector3(-0.46, 0.9, -0.16), new THREE.Vector3(-0.55, 1.05, -0.12)], lean: -1 },
    ];
    return defs.map((d) => ({ ...d, curve: new THREE.CatmullRomCurve3(d.pts) }));
  }, []);

  const group = useRef<THREE.Group>(null);
  const scanT = useRef(0);

  useFrame((state, delta) => {
    const t = state.clock.elapsedTime;
    for (const m of [limeMat, hydroMat]) m.uniforms.uTime.value = t;

    // scan band loops soil -> crown -> reset (fade at reset so it never pops)
    scanT.current += delta;
    const period = 6.5;
    const p = (scanT.current % period) / period;
    const y = -0.1 + p * 2.3;
    const glow = p > 0.9 ? Math.max(0, 1 - (p - 0.9) * 10) : 1;
    limeMat.uniforms.uScanY.value = y;
    hydroMat.uniforms.uScanY.value = y;
    limeMat.uniforms.uScanGlow.value = glow;
    hydroMat.uniforms.uScanGlow.value = glow;

    // occasional holo flicker
    const f = limeMat.uniforms.uFlicker.value;
    const next = f * 0.88 + (Math.random() < 0.012 ? 0.9 : 0);
    limeMat.uniforms.uFlicker.value = next;
    hydroMat.uniforms.uFlicker.value = next;

    // slow spin + pointer parallax
    if (group.current) {
      group.current.rotation.y += delta * 0.14;
      group.current.rotation.x += ((state.pointer.y * -0.06) - group.current.rotation.x) * 0.04;
    }
  });

  return (
    <group ref={group} position={[0, -0.55, 0]}>
      {/* pot */}
      <mesh material={hydroMat} position={[0, 0.24, 0]}>
        <cylinderGeometry args={[0.52, 0.38, 0.48, 22, 1, true]} />
      </mesh>
      <mesh material={hydroMat} position={[0, 0.485, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.1, 0.47, 22]} />
      </mesh>
      {/* soil glow disc */}
      <mesh material={limeMat} position={[0, 0.47, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.42, 22]} />
      </mesh>
      {/* stems */}
      {stems.map((s, i) => (
        <Stem key={i} mat={limeMat} points={s.pts} />
      ))}
      {/* leaves from curve points */}
      {stems.flatMap((s, si) =>
        [0.55, 0.8, 0.99].map((tt, li) => {
          const p = s.curve.getPoint(tt);
          return (
            <Leaf
              key={`${si}-${li}`}
              mat={limeMat}
              pos={p}
              rotY={si * 2.1 + li * 1.35}
              scale={0.75 + tt * 0.6 - si * 0.08}
            />
          );
        })
      )}
    </group>
  );
}

function Rig() {
  const ref = useRef<THREE.Group>(null);
  useFrame((state) => {
    if (!ref.current) return;
    // narrow/portrait screens: dolly the plant back + down so the headline
    // keeps clear air — feet stay planted on the grid (z-depth, not scale)
    const narrow = state.size.width / state.size.height < 0.78;
    const targetZ = narrow ? -2.1 : 0;
    const targetY = narrow ? -0.42 : 0;
    ref.current.position.z += (targetZ - ref.current.position.z) * 0.06;
    ref.current.position.y += (targetY - ref.current.position.y) * 0.06;
    ref.current.position.x += (state.pointer.x * 0.35 - ref.current.position.x) * 0.05;
  });
  return (
    <group ref={ref}>
      <HoloPlant />
    </group>
  );
}

export default function HeroCanvas() {
  const [visible, setVisible] = useState(true);
  const onChange = useCallback((v: boolean) => setVisible(v), []);
  return (
    <Canvas
      frameloop={visible ? "always" : "never"}
      dpr={[1, 1.75]}
      camera={{ position: [0, 1.05, 4.4], fov: 42 }}
      gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
      onCreated={({ gl }) => {
        gl.toneMapping = THREE.NoToneMapping;
      }}
    >
      <ViewportPause onChange={onChange} />
      <Rig />
      <Sparkles count={85} scale={[5, 3.4, 5]} size={2.2} speed={0.35} color="#A6FF3F" opacity={0.5} position={[0, 1, 0]} />
      <Sparkles count={28} scale={[4, 2.6, 4]} size={3.4} speed={0.25} color="#67E8F9" opacity={0.4} position={[0, 0.6, 0]} />
      <Grid
        position={[0, -0.58, 0]}
        args={[14, 14]}
        cellSize={0.42}
        cellThickness={0.7}
        cellColor="#0f2a1e"
        sectionSize={2.1}
        sectionThickness={1.1}
        sectionColor="#1c5c3a"
        fadeDistance={9}
        fadeStrength={2.6}
      />
      <EffectComposer>
        <Bloom mipmapBlur intensity={1.05} luminanceThreshold={0.12} luminanceSmoothing={0.24} />
        <ChromaticAberration offset={[0.00045, 0.00045]} />
        <Noise opacity={0.05} />
        <Vignette eskil={false} offset={0.2} darkness={0.82} />
      </EffectComposer>
    </Canvas>
  );
}
