import React, { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Float, MeshDistortMaterial, ContactShadows } from '@react-three/drei'
import * as THREE from 'three'

/**
 * Reactive Soft Body Mesh
 * Distorts in response to mouse coordinates, casting dynamic neon reflections.
 */
function ReactiveSoftBody() {
  const meshRef = useRef()
  const materialRef = useRef()

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    const { x, y } = state.pointer

    if (meshRef.current) {
      meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, y * 0.4, 0.05)
      meshRef.current.rotation.y = THREE.MathUtils.lerp(meshRef.current.rotation.y, x * 0.4 + t * 0.15, 0.05)
      meshRef.current.position.y = THREE.MathUtils.lerp(meshRef.current.position.y, Math.sin(t * 1.2) * 0.2, 0.05)
    }

    if (materialRef.current) {
      // Dynamic distortion reactivity based on cursor movement
      const speed = Math.hypot(x, y)
      materialRef.current.distort = THREE.MathUtils.lerp(materialRef.current.distort, 0.35 + speed * 0.4, 0.08)
    }
  })

  return (
    <Float speed={1.5} rotationIntensity={0.6} floatIntensity={0.8}>
      <mesh ref={meshRef} position={[2.2, 0.2, -1]} scale={1.8}>
        <icosahedronGeometry args={[1, 16]} />
        <MeshDistortMaterial
          ref={materialRef}
          color="#080e1a"
          emissive="#00f0ff"
          emissiveIntensity={0.25}
          roughness={0.15}
          metalness={0.9}
          distort={0.4}
          speed={2.2}
          wireframe={false}
        />
      </mesh>
    </Float>
  )
}

/**
 * Interactive Orbiting Particle Field
 */
function ParticleField({ count = 800 }) {
  const pointsRef = useRef()

  const [positions, scales] = useMemo(() => {
    const pos = new Float32Array(count * 3)
    const sc = new Float32Array(count)
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 18
      pos[i * 3 + 1] = (Math.random() - 0.5) * 14
      pos[i * 3 + 2] = (Math.random() - 0.5) * 12 - 2
      sc[i] = Math.random() * 0.8 + 0.2
    }
    return [pos, sc]
  }, [count])

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    if (pointsRef.current) {
      pointsRef.current.rotation.y = t * 0.02 + state.pointer.x * 0.05
      pointsRef.current.rotation.x = state.pointer.y * 0.03
    }
  })

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        size={0.045}
        color="#00f0ff"
        transparent
        opacity={0.4}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

/**
 * Dynamic Pointer Light following cursor in world space
 */
function CursorLight() {
  const lightRef = useRef()

  useFrame(({ pointer, viewport }) => {
    if (lightRef.current) {
      const x = (pointer.x * viewport.width) / 2
      const y = (pointer.y * viewport.height) / 2
      lightRef.current.position.set(x, y, 2)
    }
  })

  return <pointLight ref={lightRef} intensity={2.2} distance={8} color="#00f0ff" />
}

export default function ThreeCanvas() {
  return (
    <div className="fixed inset-0 w-full h-full pointer-events-none z-0">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[6, 8, 4]} intensity={1.5} color="#ffffff" />
        <pointLight position={[-4, 2, -1]} intensity={3.0} color="#ff007f" />
        <pointLight position={[4, -2, -1]} intensity={3.5} color="#00f0ff" />
        <CursorLight />

        <ReactiveSoftBody />
        <ParticleField count={900} />

        <ContactShadows
          position={[2.2, -2.5, -1]}
          opacity={0.4}
          scale={6}
          blur={2.5}
          far={4}
          color="#00f0ff"
        />
      </Canvas>
    </div>
  )
}
