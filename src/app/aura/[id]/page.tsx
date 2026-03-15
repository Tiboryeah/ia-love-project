"use client"

import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "framer-motion"
import { MessageSquare, Camera, Mic, Heart, ChevronLeft, MoreVertical, Send, Zap, Play, Lock, Volume2, Eye, Flame, Share2, CornerUpRight } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useState, useRef, useEffect } from "react"
import { AURA_DATABASE } from "@/lib/aura-db"

const LIVE_ACTIONS = [
    { id: 'tease', label: 'I tease you slowly', icon: <Play className="w-3 h-3 fill-white" />, level: 1 },
    { id: 'dance', label: 'Dance for me', icon: <Play className="w-3 h-3 fill-white" />, level: 2 },
    { id: 'show_butt', label: 'Show me your butt', icon: <Lock className="w-3 h-3" />, level: 3, locked: true },
    { id: 'naked', label: 'Get naked for me', icon: <Lock className="w-3 h-3" />, level: 5, locked: true },
];

export default function LiveActionPage() {
    const params = useParams();
    const auraId = params.id as string;
    const aura = AURA_DATABASE.find(a => a.id === auraId) || AURA_DATABASE[0];

    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([
        { role: 'assistant', content: `¿Qué quieres que haga por ti ahora, Tibo? *Espero tus órdenes*` }
    ]);

    return (
        <div className="flex h-screen bg-black text-white overflow-hidden font-sans">
            {/* Main Live View (Vertical Image) */}
            <div className="flex-1 relative flex items-center justify-center bg-[#050505]">
                <div className="relative h-full w-full max-w-[550px] md:h-[95vh] md:my-auto md:rounded-[48px] overflow-hidden shadow-[0_0_100px_rgba(0,0,0,0.8)] border border-white/5">
                    <Image
                        src={aura.image}
                        alt={aura.name}
                        fill
                        className="object-cover"
                        unoptimized
                        priority
                    />

                    {/* Gradient Overlays */}
                    <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-black/80 to-transparent"></div>
                    <div className="absolute inset-x-0 bottom-0 h-80 bg-gradient-to-t from-black/90 via-black/40 to-transparent"></div>

                    {/* Top UI */}
                    <div className="absolute top-8 left-8 right-8 flex justify-between items-center z-30">
                        <div className="flex items-center gap-4">
                            <Link href="/" className="w-12 h-12 rounded-full bg-black/40 backdrop-blur-2xl border border-white/10 flex items-center justify-center hover:bg-white/10 transition-all text-white">
                                <ChevronLeft className="w-7 h-7" />
                            </Link>
                            <div>
                                <h1 className="text-2xl font-black italic uppercase tracking-tighter leading-none">{aura.name}</h1>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                    <span className="text-[10px] font-bold text-white/50 uppercase tracking-widest">Live Action Beta</span>
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            {/* BOTON PARA IR AL CHAT (Candy.ai Style) */}
                            <Link
                                href={`/chat/${aura.id}`}
                                className="px-6 py-3 rounded-full bg-primary/20 backdrop-blur-2xl border border-primary/40 text-primary font-black text-xs uppercase tracking-tighter hover:bg-primary hover:text-black transition-all flex items-center gap-2 shadow-[0_0_30px_rgba(0,242,255,0.2)]"
                            >
                                <MessageSquare className="w-4 h-4" />
                                Ir al Chat
                            </Link>
                            <button className="w-12 h-12 rounded-full bg-black/40 backdrop-blur-2xl border border-white/10 flex items-center justify-center text-white/70">
                                <MoreVertical className="w-6 h-6" />
                            </button>
                        </div>
                    </div>

                    {/* Messages Overlay */}
                    <div className="absolute inset-x-8 bottom-[130px] z-20 flex flex-col gap-4 pointer-events-none max-h-[40%] overflow-hidden justify-end">
                        <AnimatePresence>
                            {messages.slice(-3).map((msg, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className="p-4 rounded-[28px] bg-black/40 backdrop-blur-2xl border border-white/10 inline-block max-w-[85%]">
                                        <p className="text-sm font-medium italic leading-relaxed text-white/90">
                                            {msg.content}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>

                    {/* Quick Input Area */}
                    <div className="absolute bottom-8 left-8 right-8 z-30">
                        <form className="relative group flex items-center gap-3">
                            <div className="flex-1 relative">
                                <input
                                    type="text"
                                    placeholder={`Pídele algo a ${aura.name}...`}
                                    className="w-full bg-black/60 backdrop-blur-3xl border border-white/10 rounded-full py-5 px-8 text-sm focus:outline-none focus:border-primary/50 transition-all placeholder:text-white/20"
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 flex gap-4 text-white/40">
                                    <Camera className="w-5 h-5 cursor-pointer hover:text-primary transition-colors" />
                                    <Mic className="w-5 h-5 cursor-pointer hover:text-secondary transition-colors" />
                                </div>
                            </div>
                            <button className="w-14 h-14 rounded-full bg-gradient-to-tr from-primary to-secondary text-white flex items-center justify-center shadow-2xl hover:scale-105 active:scale-95 transition-all">
                                <Send className="w-6 h-6" />
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            {/* Right Panel: Controls (Candy.ai Style) */}
            <div className="hidden xl:flex w-[400px] flex-col bg-[#080808] p-10 border-l border-white/5">
                <div className="mb-10">
                    <div className="flex items-center gap-3 mb-2">
                        <Flame className="w-6 h-6 text-primary fill-primary" />
                        <h2 className="text-2xl font-black italic uppercase tracking-tighter">Acciones Live</h2>
                    </div>
                    <p className="text-xs text-white/30 font-bold uppercase tracking-widest leading-relaxed">Interacciones rápidas de nivel 1 al 10.</p>
                </div>

                <div className="space-y-4 flex-1">
                    {LIVE_ACTIONS.map((action) => (
                        <button
                            key={action.id}
                            className={`w-full p-5 rounded-3xl flex items-center justify-between group transition-all border ${action.locked
                                    ? 'bg-white/[0.02] border-transparent opacity-40 cursor-not-allowed'
                                    : 'bg-white/5 border-white/5 hover:bg-white/10 hover:border-primary/50'
                                }`}
                        >
                            <div className="flex flex-col items-start">
                                <span className="text-sm font-bold uppercase tracking-tight group-hover:text-white transition-colors">{action.label}</span>
                                <span className="text-[10px] font-black text-white/30 mt-1 uppercase">Requisito: Nivel {action.level}</span>
                            </div>
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${action.locked ? 'bg-white/10' : 'bg-primary shadow-[0_0_20px_rgba(0,242,255,0.4)]'
                                }`}>
                                {action.icon}
                            </div>
                        </button>
                    ))}
                </div>

                <div className="pt-10 border-t border-white/5">
                    <div className="p-6 rounded-[32px] bg-gradient-to-br from-primary/10 to-transparent border border-primary/20 flex flex-col items-center text-center gap-3">
                        <div className="w-12 h-12 rounded-2xl bg-primary/20 flex items-center justify-center">
                            <Zap className="w-6 h-6 text-primary" />
                        </div>
                        <h4 className="font-bold text-sm uppercase tracking-tighter">Aumentar Nivel</h4>
                        <p className="text-[10px] text-white/40 leading-relaxed uppercase tracking-wider font-bold">Habla con ella en el chat privado para desbloquear acciones más profundas.</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
