import React, { useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Micro-3D Viewport Primitive: Rotating Octahedron
 * Replaces standard icons with real-time WebGL interactive geometry.
 */
function MiniOctahedron({ color = "#00f0ff", speed = 1.5 }) {
  const meshRef = useRef()
  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * speed
      meshRef.current.rotation.y += delta * (speed * 1.2)
    }
  })
  return (
    <mesh ref={meshRef} scale={1.2}>
      <octahedronGeometry args={[1, 0]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.6}
        roughness={0.2}
        metalness={0.8}
        wireframe
      />
    </mesh>
  )
}

/**
 * Micro-3D Viewport Primitive: Rotating Torus Knot
 */
function MiniTorusKnot({ color = "#ff007f", speed = 1.2 }) {
  const meshRef = useRef()
  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * speed
      meshRef.current.rotation.z += delta * (speed * 0.8)
    }
  })
  return (
    <mesh ref={meshRef} scale={0.7}>
      <torusKnotGeometry args={[0.9, 0.28, 64, 16]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.5}
        roughness={0.2}
        metalness={0.9}
      />
    </mesh>
  )
}

/**
 * Micro-3D Viewport Primitive: Rotating Icosahedron Pulse
 */
function MiniIcosahedron({ color = "#a855f7", speed = 1.0 }) {
  const meshRef = useRef()
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * speed
      meshRef.current.rotation.y += delta * (speed * 1.4)
      const scale = 1.1 + Math.sin(state.clock.elapsedTime * 3) * 0.15
      meshRef.current.scale.set(scale, scale, scale)
    }
  })
  return (
    <mesh ref={meshRef}>
      <icosahedronGeometry args={[1, 0]} />
      <meshStandardMaterial
        color={color}
        emissive={color}
        emissiveIntensity={0.8}
        wireframe
      />
    </mesh>
  )
}

export default function GlassDashboard() {
  const [activeAdapter, setActiveAdapter] = useState("GRAPH_API")
  const [isSimulating, setIsSimulating] = useState(false)
  const [recentEvents, setRecentEvents] = useState([
    {
      id: "ev_101",
      user: "dev_alex",
      comment: "Send me the full course link please!",
      intent: "request_link",
      confidence: "0.99",
      target: "SYSTEMS_DESIGN_VIP",
      status: "DISPATCHED",
      latency: "240ms"
    },
    {
      id: "ev_102",
      user: "sarah_ai",
      comment: "Where can I get the prompt bundle?",
      intent: "request_course",
      confidence: "0.97",
      target: "AI_PROMPT_ENGINEERING",
      status: "DISPATCHED",
      latency: "198ms"
    }
  ])

  const handleSimulateViralSpike = () => {
    setIsSimulating(true)
    setTimeout(() => {
      setRecentEvents((prev) => [
        {
          id: `ev_${Date.now().toString().slice(-4)}`,
          user: `creator_${Math.floor(Math.random() * 899 + 100)}`,
          comment: "link for full breakdown!",
          intent: "trigger_matched",
          confidence: "0.98",
          target: "ANTIGRAVITY_EARLY_ACCESS",
          status: "DISPATCHED",
          latency: "185ms"
        },
        ...prev.slice(0, 4)
      ])
      setIsSimulating(false)
    }, 450)
  }

  return (
    <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-8 py-10 pointer-events-auto">
      
      {/* Top Kinetic Bar */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10 pb-6 border-b border-white/10">
        <div>
          <div className="flex items-center gap-4">
            {/* 3D Micro-Geometry Brand Visual Cue */}
            <div className="w-10 h-10 rounded-xl overflow-hidden glass-panel border border-neon-cyan/40">
              <Canvas camera={{ position: [0, 0, 3.2] }}>
                <ambientLight intensity={1} />
                <MiniOctahedron color="#00f0ff" speed={2.0} />
              </Canvas>
            </div>
            <div>
              <span className="font-mono text-[11px] tracking-[0.25em] text-neon-cyan uppercase block">
                [ ECOSYSTEM CORE // V3.2 ]
              </span>
              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tighter text-white font-display">
                ANTIGRAVITY
              </h1>
            </div>
          </div>
        </div>

        {/* Kinetic Status & Adapter Switcher */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="glass-panel px-4 py-2 rounded-xl border border-white/10 flex items-center gap-3">
            <div className="w-5 h-5 rounded-md overflow-hidden">
              <Canvas camera={{ position: [0, 0, 2.5] }}>
                <MiniIcosahedron color="#10b981" speed={2.5} />
              </Canvas>
            </div>
            <div>
              <span className="font-mono text-[9px] uppercase tracking-widest text-slate-400 block">
                INGESTION ENGINE
              </span>
              <span className="font-mono text-xs font-bold text-neon-emerald tracking-wide">
                WEBHOOK_ACTIVE (0.0ms)
              </span>
            </div>
          </div>

          <div className="glass-panel p-1 rounded-xl border border-white/10 flex items-center">
            <button
              onClick={() => setActiveAdapter("GRAPH_API")}
              className={`px-3 py-1.5 rounded-lg font-mono text-[10px] tracking-wider transition-all ${
                activeAdapter === "GRAPH_API"
                  ? "bg-neon-cyan text-black font-bold shadow-lg shadow-neon-cyan/20"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              META_GRAPH_API
            </button>
            <button
              onClick={() => setActiveAdapter("INSTAGRAPI")}
              className={`px-3 py-1.5 rounded-lg font-mono text-[10px] tracking-wider transition-all ${
                activeAdapter === "INSTAGRAPI"
                  ? "bg-neon-magenta text-white font-bold shadow-lg shadow-neon-magenta/20"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              INSTAGRAPI_FALLBACK
            </button>
          </div>
        </div>
      </header>

      {/* Main Grid: Telemetry, Trigger Architecture & Link-in-Bio Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Metrics & Trigger Architecture (8 Cols) */}
        <div className="lg:col-span-8 flex flex-col gap-8">
          
          {/* Real-Time Conversion & Throughput Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            
            {/* Card 1: Total DMs Dispatched */}
            <div className="glass-panel p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-4 right-4 w-12 h-12">
                <Canvas camera={{ position: [0, 0, 3] }}>
                  <ambientLight intensity={1.5} />
                  <MiniOctahedron color="#00f0ff" speed={1.2} />
                </Canvas>
              </div>
              <span className="font-mono text-[10px] tracking-[0.2em] text-slate-400 uppercase block mb-1">
                TOTAL_CONVERSIONS
              </span>
              <div className="text-4xl font-extrabold text-white font-display tracking-tight mb-2">
                48,290
              </div>
              <div className="font-mono text-[11px] text-neon-cyan flex items-center gap-1.5">
                <span>+312%</span>
                <span className="text-slate-500">VS MANUAL BIO</span>
              </div>
            </div>

            {/* Card 2: Outbound Click-Through Rate */}
            <div className="glass-panel p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-4 right-4 w-12 h-12">
                <Canvas camera={{ position: [0, 0, 3] }}>
                  <ambientLight intensity={1.5} />
                  <MiniTorusKnot color="#ff007f" speed={1.0} />
                </Canvas>
              </div>
              <span className="font-mono text-[10px] tracking-[0.2em] text-slate-400 uppercase block mb-1">
                OUTBOUND_CTR
              </span>
              <div className="text-4xl font-extrabold text-white font-display tracking-tight mb-2">
                74.8%
              </div>
              <div className="font-mono text-[11px] text-neon-magenta flex items-center gap-1.5">
                <span>HIGH_INTENT</span>
                <span className="text-slate-500">CLAUDE_SYNTHESIS</span>
              </div>
            </div>

            {/* Card 3: NLP Inference Latency */}
            <div className="glass-panel p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-4 right-4 w-12 h-12">
                <Canvas camera={{ position: [0, 0, 3] }}>
                  <ambientLight intensity={1.5} />
                  <MiniIcosahedron color="#a855f7" speed={1.4} />
                </Canvas>
              </div>
              <span className="font-mono text-[10px] tracking-[0.2em] text-slate-400 uppercase block mb-1">
                GEMINI_LATENCY
              </span>
              <div className="text-4xl font-extrabold text-white font-display tracking-tight mb-2">
                210ms
              </div>
              <div className="font-mono text-[11px] text-neon-violet flex items-center gap-1.5">
                <span>ASYNC_QUEUE</span>
                <span className="text-slate-500">ZERO_TIMEOUT</span>
              </div>
            </div>

          </div>

          {/* Active Trigger Pipelines (Superprofile/Zorcha Style) */}
          <div className="glass-panel p-7 rounded-3xl border border-white/10">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
              <div>
                <span className="font-mono text-[10px] tracking-[0.25em] text-neon-cyan uppercase">
                  AUTOMATION RULES
                </span>
                <h2 className="text-xl font-bold text-white font-display tracking-tight">
                  ACTIVE_TRIGGER_MATRICES
                </h2>
              </div>
              <button
                onClick={handleSimulateViralSpike}
                disabled={isSimulating}
                className="px-4 py-2 rounded-xl bg-neon-cyan/10 hover:bg-neon-cyan/20 border border-neon-cyan/40 font-mono text-xs font-semibold text-neon-cyan tracking-wider transition-all"
              >
                {isSimulating ? "[ INGESTING_SPIKE... ]" : "[ SIMULATE_COMMENT_SPIKE ]"}
              </button>
            </div>

            <div className="space-y-3">
              {[
                {
                  keyword: "COURSE",
                  media: "REEL #984 — Systems Architecture at Scale",
                  dest: "antigrav.link/r/sys99",
                  original: "masterclass.dev/systems",
                  clicks: 1420,
                  ctr: "81.4%"
                },
                {
                  keyword: "PROMPT",
                  media: "POST #842 — Top 10 Autonomous Coding Workflows",
                  dest: "antigrav.link/r/pr88",
                  original: "gumroad.com/l/prompts",
                  clicks: 3120,
                  ctr: "76.2%"
                },
                {
                  keyword: "VIP",
                  media: "GLOBAL_ACCOUNT_TRIGGER (All Media)",
                  dest: "antigrav.link/r/vip01",
                  original: "skool.com/antigravity-vip",
                  clicks: 890,
                  ctr: "89.1%"
                }
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
                >
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-xs font-bold px-3 py-1 rounded-lg bg-neon-cyan/10 text-neon-cyan border border-neon-cyan/30">
                      /{item.keyword}
                    </span>
                    <div>
                      <div className="text-sm font-semibold text-white tracking-tight">
                        {item.media}
                      </div>
                      <div className="font-mono text-[11px] text-slate-400">
                        {item.dest} <span className="text-slate-600">➔</span> {item.original}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-6 self-end md:self-center">
                    <div className="text-right">
                      <span className="font-mono text-[10px] text-slate-500 block uppercase">CLICKS</span>
                      <span className="font-mono text-sm font-bold text-slate-200">{item.clicks}</span>
                    </div>
                    <div className="text-right">
                      <span className="font-mono text-[10px] text-slate-500 block uppercase">CTR</span>
                      <span className="font-mono text-sm font-bold text-neon-emerald">{item.ctr}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Real-Time Ingested Event Feed */}
          <div className="glass-panel p-7 rounded-3xl border border-white/10">
            <span className="font-mono text-[10px] tracking-[0.25em] text-neon-magenta uppercase block mb-1">
              LIVE_EVENT_PIPELINE
            </span>
            <h3 className="text-lg font-bold text-white font-display mb-4">
              STREAMED_WEBHOOK_TRANSACTIONS
            </h3>

            <div className="space-y-2.5">
              {recentEvents.map((ev) => (
                <div
                  key={ev.id}
                  className="p-3.5 rounded-xl bg-slate-950/60 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-2 h-2 rounded-full bg-neon-emerald animate-ping inline-block" />
                    <div>
                      <span className="font-mono text-xs text-neon-cyan">@{ev.user}</span>
                      <p className="text-xs text-slate-300 mt-0.5 font-sans">
                        "{ev.comment}"
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 font-mono text-[10px] text-slate-400">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      CONF: {ev.confidence}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-neon-emerald/10 text-neon-emerald border border-neon-emerald/30">
                      {ev.status} ({ev.latency})
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: High-Conversion Link-in-Bio Canvas Node (4 Cols) */}
        <div className="lg:col-span-4 flex flex-col gap-8">
          
          <div className="glass-panel-neon p-7 rounded-3xl relative overflow-hidden">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-[10px] tracking-[0.25em] text-neon-cyan uppercase">
                HYBRID_NODE
              </span>
              <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/40">
                ACTIVE
              </span>
            </div>

            <h2 className="text-2xl font-extrabold text-white font-display tracking-tight mb-2">
              CREATOR_BIO_ROUTER
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed mb-6 font-normal">
              Unified link-in-bio architecture with automatic comment-to-DM link handoffs and click-telemetry wrapping.
            </p>

            <div className="space-y-3 mb-6">
              {[
                { title: "SYSTEMS_DESIGN_VIP_COMMUNITY", badge: "68% CONVERSION", desc: "Private engineering mastermind" },
                { title: "PROMPT_ENGINEERING_PLAYBOOK", badge: "HOT_PRODUCT", desc: "Production agents & evaluators" },
                { title: "BOOK_1_ON_1_ADVISORY_CALL", badge: "LIMITED_SLOTS", desc: "Direct fractional architecture" },
              ].map((link, idx) => (
                <div
                  key={idx}
                  className="glass-card p-4 rounded-2xl group cursor-pointer border border-white/10 hover:border-neon-cyan"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-[11px] font-bold text-white group-hover:text-neon-cyan transition-colors">
                      {link.title}
                    </span>
                    <span className="font-mono text-[9px] text-neon-magenta tracking-wider">
                      [{link.badge}]
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    {link.desc}
                  </p>
                </div>
              ))}
            </div>

            <div className="p-4 rounded-2xl bg-black/50 border border-white/5 font-mono text-[10px] text-slate-400 leading-relaxed">
              <span className="text-neon-cyan font-bold block mb-1">// DUAL_ENGINE_ARCHITECTURE</span>
              Comment triggers are ingested via Flask webhook ➔ Offloaded to Celery queue ➔ Classified by Gemini NLP ➔ Synthesized by Claude ➔ Dispatched via Graph API / Instagrapi.
            </div>
          </div>

        </div>

      </div>

    </div>
  )
}
