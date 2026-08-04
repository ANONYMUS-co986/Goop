"use client";

import { useMemo, useRef } from "react";
import type { CSSProperties, MutableRefObject } from "react";
import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html, Sparkles } from "@react-three/drei";
import { EffectComposer, Bloom, Noise, Vignette } from "@react-three/postprocessing";

/**
 * THE BUILD — exploded ESP32 rig.
 * 100% procedural: PCB, shield can, headers, buttons, LED + the six external
 * modules from the real ₹1,890 bill of materials. Scroll drives the
 * explosion: board parts stair-rise, modules orbit out; slack wiring
 * (recomputed every frame) keeps every module tethered to its GPIO pad.
 *
 * progressRef.current ∈ [0,1] drives everything (scroll-scrubbed by the page).
 */

type Part = {
  id: string;
  label: string;
  color: string;
  metal?: boolean;
  glow?: string; // emissive color if the part is lit
  kind: "box" | "cyl" | "sphere";
  size: [number, number, number];
  home: [number, number, number];
  dir: [number, number, number]; // explode travel
  rot?: [number, number, number];
  tag?: string; // small caption under the label
};

const BOARD_PARTS: Part[] = [
  { id: "pcb", label: "PCB", tag: "38-pin devboard", color: "#0d2420", kind: "box", size: [2.9, 0.08, 2.0], home: [0, 0, 0], dir: [0, -0.35, 0] },
  { id: "can", label: "ESP32-WROOM", tag: "the brain · dual core 240MHz", color: "#aebab4", metal: true, kind: "box", size: [0.95, 0.14, 0.72], home: [0.62, 0.14, -0.42], dir: [0, 1.6, 0] },
  { id: "usb", label: "USB", tag: "flash + serial monitor", color: "#39443f", metal: true, kind: "box", size: [0.42, 0.16, 0.5], home: [-1.3, 0.11, -0.42], dir: [-0.35, 0.8, 0] },
  { id: "btn", label: "EN / BOOT", tag: "the two buttons we mashed", color: "#212a26", kind: "cyl", size: [0.1, 0.07, 0.1], home: [-0.62, 0.09, -0.78], dir: [0, 1.0, -0.2] },
  { id: "led", label: "GPIO2 LED", tag: "heartbeat", color: "#1c2622", glow: "#A6FF3F", kind: "box", size: [0.1, 0.07, 0.1], home: [0.16, 0.1, 0.55], dir: [0, 1.25, 0.2] },
  { id: "hdr1", label: "HEADERS", tag: "2 × 15 golden gates", color: "#c9b97a", metal: true, kind: "box", size: [2.5, 0.3, 0.08], home: [0, 0.18, 0.86], dir: [0.15, 0.65, 0.35] },
  { id: "hdr2", label: "", tag: "", color: "#c9b97a", metal: true, kind: "box", size: [2.5, 0.3, 0.08], home: [0, 0.18, -0.86], dir: [-0.15, 0.65, -0.35] },
];

const MODULES: Part[] = [
  { id: "dht", label: "DHT11", tag: "temp + humidity · GPIO4", color: "#2f5fd0", kind: "box", size: [0.42, 0.52, 0.16], home: [-2.5, 0.4, -1.15], dir: [-0.95, 1.05, -0.55] },
  { id: "soil", label: "SOIL PROBE", tag: "capacitive v1.2 · GPIO34", color: "#48555f", metal: true, kind: "box", size: [0.34, 1.05, 0.05], home: [-2.9, 0.35, 0.75], dir: [-1.35, 0.72, 0.55] },
  { id: "sonar", label: "HC-SR04", tag: "tank level · GPIO18/19", color: "#1d4ed8", kind: "box", size: [0.62, 0.28, 0.06], home: [2.55, 0.5, -1.05], dir: [1.1, 0.85, -0.5] },
  { id: "ldr", label: "LDR", tag: "daylight · GPIO35", color: "#5b2d24", kind: "box", size: [0.3, 0.4, 0.05], home: [2.9, 0.3, 0.55], dir: [1.3, 0.55, 0.45] },
  { id: "relay", label: "RELAY", tag: "pump switch · GPIO5 (active-LOW)", color: "#1e40af", kind: "box", size: [0.5, 0.42, 0.34], home: [0.2, 0.35, 2.3], dir: [0.2, 0.7, 1.15] },
  { id: "pump", label: "PUMP", tag: "₹220 heart of the hydro", color: "#d8ded9", kind: "cyl", size: [0.24, 0.55, 0.24], home: [1.9, 0.4, 2.2], dir: [0.85, 0.95, 1.0] },
  { id: "uv", label: "UV STRIP", tag: "algae patrol · GPIO12", color: "#241a3f", glow: "#A78BFA", kind: "box", size: [0.68, 0.06, 0.1], home: [-1.7, 0.3, 2.15], dir: [-0.8, 0.75, 0.95] },
];

// GPIO pads the wires tether to (x,z on the PCB top face)
const PADS: Record<string, [number, number]> = {
  dht: [-0.96, 0.86], soil: [-0.64, 0.86], sonar: [0.32, 0.86], ldr: [0.64, 0.86],
  relay: [0.96, -0.86], pump: [0.64, -0.86], uv: [-0.32, -0.86],
};

function PartMesh({ p, mat }: { p: Part; mat: THREE.Material }) {
  return (
    <mesh material={mat} position={[0, 0, 0]} rotation={p.rot ?? [0, 0, 0]}>
      {p.kind === "box" && <boxGeometry args={p.size} />}
      {p.kind === "cyl" && <cylinderGeometry args={[p.size[0], p.size[0], p.size[1], 20]} />}
      {p.kind === "sphere" && <sphereGeometry args={[p.size[0], 24, 18]} />}
    </mesh>
  );
}

function labelStyle(): CSSProperties {
  return { whiteSpace: "nowrap" };
}

const WIRE_SEGS = 14;

function Rig({ progressRef }: { progressRef: MutableRefObject<number> }) {
  const groupRefs = useRef<(THREE.Group | null)[]>([]);
  const modRefs = useRef<(THREE.Group | null)[]>([]);
  const spinRef = useRef<THREE.Group>(null);

  const mats = useMemo(() => {
    const m = new Map<string, THREE.MeshStandardMaterial>();
    for (const p of [...BOARD_PARTS, ...MODULES]) {
      m.set(
        p.id,
        new THREE.MeshStandardMaterial({
          color: p.color,
          metalness: p.metal ? 0.85 : 0.15,
          roughness: p.metal ? 0.35 : 0.6,
          emissive: new THREE.Color(p.glow ?? "#000000"),
          emissiveIntensity: p.glow ? 1.6 : 0,
          transparent: true,
        })
      );
    }
    return m;
  }, []);

  const pcbEdgeMat = useMemo(
    () => new THREE.LineBasicMaterial({ color: "#A6FF3F", transparent: true, opacity: 0.5 }),
    []
  );
  const pcbEdges = useMemo(
    () => new THREE.EdgesGeometry(new THREE.BoxGeometry(2.9, 0.08, 2.0)),
    []
  );
  const wireMat = useMemo(
    () => new THREE.LineBasicMaterial({ color: "#A6FF3F", transparent: true, opacity: 0, blending: THREE.AdditiveBlending }),
    []
  );

  // one wire line per module: [module socket .. sagging arc .. GPIO pad]
  const wires = useMemo(
    () =>
      MODULES.map(() => {
        const g = new THREE.BufferGeometry();
        g.setAttribute("position", new THREE.BufferAttribute(new Float32Array(WIRE_SEGS * 3), 3));
        return new THREE.Line(g, wireMat);
      }),
    [wireMat]
  );

  const tmp = useRef({ v1: new THREE.Vector3(), v2: new THREE.Vector3() });

  useFrame((state, delta) => {
    const p = THREE.MathUtils.smoothstep(THREE.MathUtils.clamp(progressRef.current, 0, 1), 0, 1);
    const t = state.clock.elapsedTime;

    // slow turntable + pointer lean + re-center as the rig explodes upward
    if (spinRef.current) {
      const narrow = state.size.width / state.size.height < 0.78;
      const targetScale = narrow ? 0.58 : 0.86;
      spinRef.current.rotation.y += delta * 0.04;
      spinRef.current.rotation.x += ((state.pointer.y * -0.05 + 0.06) - spinRef.current.rotation.x) * 0.04;
      spinRef.current.position.y = -0.9 - p * 0.55;
      const s = THREE.MathUtils.lerp(spinRef.current.scale.x, targetScale, 0.06);
      spinRef.current.scale.setScalar(s);
    }

    // board parts stair-rise
    BOARD_PARTS.forEach((part, i) => {
      const g = groupRefs.current[i];
      if (!g) return;
      const local = THREE.MathUtils.smoothstep(p, i * 0.09, Math.min(1, i * 0.09 + 0.45));
      g.position.set(
        part.home[0] + part.dir[0] * local,
        part.home[1] + part.dir[1] * local,
        part.home[2] + part.dir[2] * local
      );
    });

    // modules orbit out
    MODULES.forEach((part, i) => {
      const g = modRefs.current[i];
      if (!g) return;
      const local = THREE.MathUtils.smoothstep(p, 0.12 + i * 0.05, Math.min(1, 0.12 + i * 0.05 + 0.5));
      g.position.set(
        part.home[0] + part.dir[0] * local,
        part.home[1] + part.dir[1] * local + Math.sin(t * 0.9 + i) * 0.03,
        part.home[2] + part.dir[2] * local
      );
    });

    // slack wires: recompute the sagging arc every frame
    wireMat.opacity = THREE.MathUtils.clamp((p - 0.45) * 2.2, 0, 0.85);
    MODULES.forEach((part, i) => {
      const geo = wires[i].geometry;
      const mod = modRefs.current[i];
      if (!mod) return;
      const pad = PADS[part.id];
      const spin = spinRef.current;
      if (!spin) return;
      // module world pos (inside spin group) and pad target in spin-local space
      tmp.current.v1.setFromMatrixPosition(mod.matrix);
      tmp.current.v2.set(pad[0], 0.06, pad[1]);
      const pos = geo.attributes.position as THREE.BufferAttribute;
      for (let s = 0; s < WIRE_SEGS; s++) {
        const k = s / (WIRE_SEGS - 1);
        const x = THREE.MathUtils.lerp(tmp.current.v1.x, tmp.current.v2.x, k);
        const y = THREE.MathUtils.lerp(tmp.current.v1.y, tmp.current.v2.y, k) - Math.sin(k * Math.PI) * (0.35 + 0.25 * (1 - p));
        const z = THREE.MathUtils.lerp(tmp.current.v1.z, tmp.current.v2.z, k);
        pos.setXYZ(s, x, y, z);
      }
      pos.needsUpdate = true;
      geo.computeBoundingSphere();
    });
  });

  return (
    <group ref={spinRef} position={[0, -0.9, 0]}>
      {BOARD_PARTS.map((part, i) => (
        <group key={part.id} ref={(el) => { groupRefs.current[i] = el; }} position={part.home}>
          <PartMesh p={part} mat={mats.get(part.id)!} />
          {part.id === "pcb" && <lineSegments geometry={pcbEdges} material={pcbEdgeMat} />}
          {part.id === "can" && (
            // antenna keep-out zone etched in front of the can
            <mesh position={[-0.62, -0.02, 0.1]}>
              <boxGeometry args={[0.55, 0.05, 0.52]} />
              <meshStandardMaterial color="#8f7f3f" metalness={0.9} roughness={0.3} />
            </mesh>
          )}
          {part.label && (
            <Html position={[0, part.size[1] / 2 + 0.22, 0]} center distanceFactor={7} className="pointer-events-none select-none">
              <div style={labelStyle()} className="text-center">
                <div className="font-mono text-[9px] tracking-[0.22em] text-lime/90">{part.label}</div>
                {part.tag && <div className="font-mono text-[7.5px] tracking-[0.12em] text-dew-mute/80">{part.tag}</div>}
              </div>
            </Html>
          )}
        </group>
      ))}
      {MODULES.map((part, i) => (
        <group key={part.id} ref={(el) => { modRefs.current[i] = el; }} position={part.home}>
          <PartMesh p={part} mat={mats.get(part.id)!} />
          {part.id === "sonar" && (
            <>
              <mesh position={[-0.17, 0, 0.05]}>
                <cylinderGeometry args={[0.085, 0.085, 0.05, 16]} />
                <meshStandardMaterial color="#c8d2cd" metalness={0.9} roughness={0.25} />
              </mesh>
              <mesh position={[0.17, 0, 0.05]}>
                <cylinderGeometry args={[0.085, 0.085, 0.05, 16]} />
                <meshStandardMaterial color="#c8d2cd" metalness={0.9} roughness={0.25} />
              </mesh>
            </>
          )}
          <Html position={[0, part.size[1] / 2 + 0.2, 0]} center distanceFactor={7} className="pointer-events-none select-none">
            <div style={labelStyle()} className="text-center">
              <div className="font-mono text-[9px] tracking-[0.22em] text-hydro/95">{part.label}</div>
              {part.tag && <div className="font-mono text-[7.5px] tracking-[0.12em] text-dew-mute/80">{part.tag}</div>}
            </div>
          </Html>
        </group>
      ))}
      {MODULES.map((part, i) => (
        <primitive key={`wire-${part.id}`} object={wires[i]} />
      ))}
    </group>
  );
}

export default function BuildCanvas({ progressRef }: { progressRef: MutableRefObject<number> }) {
  return (
    <Canvas
      dpr={[1, 1.6]}
      camera={{ position: [0, 2.3, 7.4], fov: 40 }}
      gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
      onCreated={({ gl }) => { gl.toneMapping = THREE.NoToneMapping; }}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[4, 6, 3]} intensity={1.1} color="#E9FFF2" />
      <directionalLight position={[-5, 3, -2]} intensity={0.4} color="#67E8F9" />
      <pointLight position={[0, 3.5, 0]} intensity={12} color="#A6FF3F" distance={9} />
      <Rig progressRef={progressRef} />
      <Sparkles count={55} scale={[7, 4.5, 7]} size={1.8} speed={0.25} color="#67E8F9" opacity={0.35} position={[0, 0.8, 0]} />
      <EffectComposer>
        <Bloom mipmapBlur intensity={0.7} luminanceThreshold={0.18} luminanceSmoothing={0.3} />
        <Noise opacity={0.045} />
        <Vignette eskil={false} offset={0.2} darkness={0.8} />
      </EffectComposer>
    </Canvas>
  );
}
