import React from 'react'
import ThreeCanvas from './components/ThreeCanvas'
import GlassDashboard from './components/GlassDashboard'

export default function App() {
  return (
    <div className="relative min-h-screen w-full bg-void overflow-x-hidden selection:bg-neon-cyan selection:text-black">
      {/* Global Interactive Three.js Background Canvas */}
      <ThreeCanvas />

      {/* Foreground Frosted Dark-Mode Glassmorphic Interface */}
      <GlassDashboard />
    </div>
  )
}
