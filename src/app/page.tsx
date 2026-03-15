"use client"

import { motion } from "framer-motion"
import { MessageSquare, Camera, Mic, Heart, Shield, Zap, ArrowRight, Star, Flame, Play, Clock, Sparkles } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { AURA_DATABASE } from "@/lib/aura-db"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#050505] text-white selection:bg-primary/30 pb-20">
      {/* Hero Section - Super Premium */}
      <section className="relative pt-20 pb-12 px-8 max-w-[1600px] mx-auto">
        <div className="relative h-[600px] rounded-[60px] overflow-hidden border border-white/5 group shadow-[0_50px_100px_rgba(0,0,0,0.5)]">
          <Image
            src={AURA_DATABASE[2].image}
            alt="Featured Aura"
            fill
            className="object-cover transition-transform duration-[2000ms] group-hover:scale-105"
            unoptimized
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black via-black/40 to-transparent"></div>
          <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>

          <div className="absolute inset-x-12 bottom-12 max-w-3xl">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, ease: "easeOut" }}
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="px-4 py-1.5 rounded-full bg-primary text-black text-[11px] font-black uppercase tracking-[0.2em] italic">TOP CHOICE</div>
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/10 text-amber-400">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  <span className="text-xs font-black uppercase tracking-widest">4.9 / 5.0</span>
                </div>
              </div>
              <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tighter italic text-white uppercase leading-[0.9]">
                {AURA_DATABASE[2].name}<br />
                <span className="text-primary italic">.LIVE ACTION</span>
              </h1>
              <p className="text-2xl text-white/60 mb-10 max-w-xl leading-relaxed font-medium italic">
                "{AURA_DATABASE[2].tagline}" <br />
                <span className="text-sm opacity-40 uppercase tracking-widest mt-4 block not-italic">Desbloquea su galería privada y chat en vivo ahora.</span>
              </p>
              <div className="flex flex-wrap items-center gap-4">
                <Link href={`/chat/${AURA_DATABASE[2].id}`} className="inline-flex items-center gap-4 px-12 py-6 rounded-[30px] bg-white text-black font-black text-xl hover:bg-primary transition-all shadow-[0_30px_60px_rgba(255,255,255,0.1)] group">
                  EMPEZAR CHAT <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
                </Link>
                <Link href={`/aura/${AURA_DATABASE[2].id}`} className="inline-flex items-center gap-4 px-12 py-6 rounded-[30px] bg-white/5 backdrop-blur-3xl border border-white/10 text-white font-black text-xl hover:bg-white/10 transition-all">
                  VER EN LIVE ACTION <Play className="w-6 h-6" />
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Live Action - Circular Stories Style */}
      <section id="live" className="py-12 px-10">
        <div className="flex items-center justify-between mb-10 max-w-[1600px] mx-auto">
          <div className="flex items-center gap-5">
            <div className="w-12 h-12 rounded-2xl bg-primary/20 flex items-center justify-center">
              <Flame className="w-7 h-7 text-primary fill-primary" />
            </div>
            <h2 className="text-4xl font-black italic tracking-tighter uppercase leading-none">Live <span className="text-primary italic">Streaming</span></h2>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-[10px] font-black uppercase tracking-widest text-white/30">Total 12 Auras Online</span>
            <div className="w-24 h-1 bg-white/5 rounded-full overflow-hidden">
              <div className="w-1/2 h-full bg-primary animate-[shimmer_2s_infinite]"></div>
            </div>
          </div>
        </div>

        <div className="flex gap-8 overflow-x-auto pb-10 no-scrollbar scroll-smooth max-w-[1600px] mx-auto">
          {AURA_DATABASE.map((aura) => (
            <Link key={`live-${aura.id}`} href={`/aura/${aura.id}`} className="flex-shrink-0 group">
              <div className="relative w-72 aspect-[9/16] rounded-[40px] overflow-hidden border-4 border-transparent group-hover:border-primary/50 transition-all shadow-2xl">
                <Image src={aura.image} alt={aura.name} fill className="object-cover group-hover:scale-110 transition-transform duration-[1000ms]" unoptimized />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-80 group-hover:opacity-40 transition-opacity"></div>

                {/* Status indicator */}
                <div className="absolute top-6 left-6 flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-600/20 backdrop-blur-md border border-red-600/30">
                  <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                  <span className="text-[10px] font-black text-white uppercase tracking-widest">LIVE ACTION</span>
                </div>

                <div className="absolute bottom-8 left-8 right-8 text-center translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                  <h3 className="text-3xl font-black italic uppercase mb-4 tracking-tighter">{aura.name}</h3>
                  <div className="py-3 rounded-2xl bg-white text-black font-black text-xs transition-all uppercase tracking-widest opacity-0 group-hover:opacity-100 scale-90 group-hover:scale-100 duration-500">
                    JOIN LIVE
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Discovery Feed - Masonry Style */}
      <section id="auras" className="py-20 px-10 max-w-[1600px] mx-auto">
        <div className="flex items-center justify-between mb-12">
          <div>
            <h2 className="text-5xl font-black italic tracking-tighter uppercase mb-2">Discovery <span className="text-secondary italic">Feed</span></h2>
            <div className="flex gap-4">
              {["Todas", "Goth", "Fitness", "Kawaii", "VIPS"].map(tag => (
                <button key={tag} className="text-[10px] font-black uppercase tracking-widest text-white/30 hover:text-primary transition-colors">
                  {tag}
                </button>
              ))}
            </div>
          </div>
          <button className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-white/5 border border-white/10 text-[10px] font-black uppercase tracking-widest hover:bg-white/10 transition-all">
            <Sparkles className="w-4 h-4 text-primary" />
            Randomizer
          </button>
        </div>

        <div className="columns-1 sm:columns-2 lg:columns-4 gap-8 space-y-8">
          {AURA_DATABASE.map((aura) => (
            <Link key={aura.id} href={`/chat/${aura.id}`} className="block">
              <motion.div
                whileHover={{ y: -10 }}
                className="group relative rounded-[48px] overflow-hidden bg-[#080808] border border-white/10 transition-all cursor-pointer shadow-2xl"
              >
                <div className="relative aspect-[4/5]">
                  <Image
                    src={aura.image}
                    alt={aura.name}
                    fill
                    className="object-cover transition-transform duration-1000 group-hover:scale-105"
                    unoptimized
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-90 group-hover:opacity-50 transition-opacity"></div>
                </div>

                {/* Stats Badge */}
                <div className="absolute top-6 right-6 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-xl border border-white/10 text-white group-hover:bg-primary group-hover:text-black transition-all">
                  <Heart className="w-3.5 h-3.5" />
                  <span className="text-[10px] font-black uppercase tracking-widest">98%</span>
                </div>

                <div className="p-8">
                  <div className="flex items-baseline gap-2 mb-2">
                    <h3 className="text-4xl font-black italic uppercase tracking-tighter group-hover:text-primary transition-colors">{aura.name}</h3>
                    <span className="text-white/20 text-sm font-bold">21</span>
                  </div>
                  <p className="text-white/40 text-[11px] font-bold uppercase tracking-widest mb-6 italic line-clamp-1">
                    {aura.tagline}
                  </p>

                  {/* Traits Preview */}
                  <div className="flex flex-wrap gap-2 opacity-60 group-hover:opacity-100 transition-opacity">
                    <span className="px-3 py-1.5 rounded-xl bg-white/5 text-[8px] font-black text-white/50 uppercase tracking-widest border border-white/10">{aura.traits.vibe}</span>
                    <span className="px-3 py-1.5 rounded-xl bg-white/5 text-[8px] font-black text-white/50 uppercase tracking-widest border border-white/10">{aura.traits.style}</span>
                  </div>
                </div>

                {/* Hover Quick action */}
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity group-hover:bg-black/20 backdrop-blur-[2px] pointer-events-none">
                  <div className="w-20 h-20 rounded-full bg-primary flex items-center justify-center shadow-[0_0_50px_rgba(0,242,255,0.5)] -translate-y-10 group-hover:translate-y-0 transition-transform duration-500">
                    <MessageSquare className="w-8 h-8 text-black" />
                  </div>
                </div>
              </motion.div>
            </Link>
          ))}
        </div>
      </section>

      {/* Trust & Features Footer Section */}
      <section className="py-32 px-10 bg-[#070707] border-y border-white/5 mt-20">
        <div className="max-w-[1600px] mx-auto grid grid-cols-1 md:grid-cols-3 gap-20">
          <div className="flex flex-col items-center text-center group">
            <div className="w-24 h-24 rounded-[40px] bg-primary/10 flex items-center justify-center mb-10 group-hover:scale-110 group-hover:bg-primary/20 transition-all border border-primary/20">
              <Shield className="w-10 h-10 text-primary" />
            </div>
            <h3 className="text-3xl font-black mb-6 uppercase tracking-tighter italic">Privacidad Local</h3>
            <p className="text-white/30 text-lg leading-relaxed font-medium italic">Sin suscripciones en la nube. Tus datos y fotos viven en tu RX 5700 XT. Privacidad total fuera de la red.</p>
          </div>
          <div className="flex flex-col items-center text-center group">
            <div className="w-24 h-24 rounded-[40px] bg-secondary/10 flex items-center justify-center mb-10 group-hover:scale-110 group-hover:bg-secondary/20 transition-all border border-secondary/20">
              <Zap className="w-10 h-10 text-secondary" />
            </div>
            <h3 className="text-3xl font-black mb-6 uppercase tracking-tighter italic">Motor AMD DirectML</h3>
            <p className="text-white/30 text-lg leading-relaxed font-medium italic">Respuesta instantánea. Sin límites de palabras ni censura. Tu hardware, tus reglas, tu libertad.</p>
          </div>
          <div className="flex flex-col items-center text-center group">
            <div className="w-24 h-24 rounded-[40px] bg-amber-500/10 flex items-center justify-center mb-10 group-hover:scale-110 group-hover:bg-amber-500/20 transition-all border border-amber-500/20">
              <Sparkles className="w-10 h-10 text-amber-500" />
            </div>
            <h3 className="text-3xl font-black mb-6 uppercase tracking-tighter italic">Hiper-Realismo 8K</h3>
            <p className="text-white/30 text-lg leading-relaxed font-medium italic">Generación de imágenes con texturas de piel reales. La IA más cercana a la realidad jamás creada.</p>
          </div>
        </div>
      </section>

      <footer className="py-20 text-center text-white/10 text-[11px] font-black uppercase tracking-[1em] bg-[#070707]">
        <p>© 2026 AURA.LIVE · PRIVADO · LOCAL · LIBRE</p>
      </footer>
    </main>
  )
}
