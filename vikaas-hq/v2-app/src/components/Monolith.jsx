import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sparkles } from '@react-three/drei';
import * as THREE from 'three';

/* ---------- the drawer monolith ---------- */
function DrawerMonolith({ scrollRef }) {
  const group = useRef();
  const cam = useRef({ z: 7.5 });
  useFrame(({ camera, pointer }) => {
    // mouse parallax
    camera.position.x += (pointer.x * 0.6 - camera.position.x) * 0.05;
    camera.position.y += (0.4 + pointer.y * 0.3 - camera.position.y) * 0.05;
    camera.lookAt(0, 0.2, 0);
    if (group.current) {
      group.current.rotation.y += (pointer.x * 0.15 - group.current.rotation.y) * 0.04;
      group.current.rotation.x += (pointer.y * 0.08 - group.current.rotation.x) * 0.04;
    }
  });
  return (
    <group ref={group} position={[0, -0.2, 0]}>
      {/* the drawer body */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[2.6, 1.6, 2.2]} />
        <meshStandardMaterial color="#12171a" metalness={0.85} roughness={0.3} />
      </mesh>
      {/* glowing edges */}
      <lineSegments>
        <edgesGeometry args={[new THREE.BoxGeometry(2.6, 1.6, 2.2)]} />
        <lineBasicMaterial color="#2ede82" transparent opacity={0.5} />
      </lineSegments>
      {/* the VIKAAS front panel */}
      <mesh position={[0, 0, 1.11]}>
        <planeGeometry args={[2.1, 0.7]} />
        <meshBasicMaterial color="#b9ff3f" />
      </mesh>
      {/* lid hint */}
      <mesh position={[0, 0.9, 0]}>
        <boxGeometry args={[2.8, 0.18, 2.4]} />
        <meshStandardMaterial color="#1d2622" metalness={0.7} roughness={0.4} />
      </mesh>
      {/* floating e-waste items orbiting */}
      <Float speed={1.6} rotationIntensity={0.4} floatIntensity={0.9}>
        <mesh position={[1.7, 0.5, 0.4]} rotation={[0.4, 0.6, 0.2]}>
          <boxGeometry args={[0.55, 0.9, 0.06]} />
          <meshStandardMaterial color="#1b2420" emissive="#2ede82" emissiveIntensity={0.25} metalness={0.3} roughness={0.4} />
        </mesh>
      </Float>
      <Float speed={1.2} rotationIntensity={0.5} floatIntensity={1.1}>
        <mesh position={[-1.9, 0.3, 0.2]} rotation={[0.2, 0.3, 0.8]}>
          <boxGeometry args={[0.5, 0.28, 0.9]} />
          <meshStandardMaterial color="#2a2f33" metalness={0.5} roughness={0.5} />
        </mesh>
      </Float>
      <Float speed={1.9} rotationIntensity={0.3} floatIntensity={0.8}>
        <mesh position={[0.4, 1.4, 0.8]} rotation={[0.8, 0.1, 0.4]}>
          <boxGeometry args={[0.42, 0.42, 0.12]} />
          <meshStandardMaterial color="#1c2125" metalness={0.6} roughness={0.45} />
        </mesh>
      </Float>
    </group>
  );
}

/* ---------- the reflective grid floor ---------- */
function GridFloor() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.4, 0]}>
      <planeGeometry args={[24, 24]} />
      <meshStandardMaterial color="#0a0f0c" metalness={0.8} roughness={0.25} />
    </mesh>
  );
}

/* ---------- the hero canvas ---------- */
export default function Monolith() {
  return (
    <Canvas
      dpr={[1, 1.5]}
      camera={{ position: [0, 0.4, 7.5], fov: 42 }}
      gl={{ antialias: true, alpha: true }}
      style={{ position: 'absolute', inset: 0 }}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[4, 7, 5]} intensity={1.2} />
      <pointLight position={[-3, 1.5, 3]} intensity={8} color="#b9ff3f" />
      <pointLight position={[3, -1, 4]} intensity={5} color="#2ede82" />
      <DrawerMonolith />
      <GridFloor />
      <Sparkles count={140} scale={[10, 5, 8]} size={1.6} speed={0.35} color="#b9ff3f" opacity={0.5} />
    </Canvas>
  );
}
