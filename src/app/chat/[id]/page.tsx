"use client"

import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "framer-motion"
import { MessageSquare, Camera, Mic, Heart, ChevronLeft, MoreVertical, Send, Loader2, Zap, Play, Search, Settings, Phone, Video, Info, Lock, Flame, Image as ImageIcon, Volume2, Star, Instagram, Music2 } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { useState, useRef, useEffect } from "react"
import { AURA_DATABASE } from "@/lib/aura-db"

const ACTION_SUGGESTIONS = [
    "*Me acerco a ti*", "*Te miro fijamente*", "*Muerdo mi labio*", "*Te mando un beso*", "*Te pregunto algo picante*"
];

export default function ChatPage() {
    const params = useParams();
    const auraId = params.id as string;
    const aura = AURA_DATABASE.find(a => a.id === auraId) || AURA_DATABASE[0];

    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([
        { role: 'assistant', content: `¿Cómo te va el día, Tibo? Estaba esperándote...`, type: 'text' }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const chatEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const [isGeneratingImage, setIsGeneratingImage] = useState(false);

    const generateImage = async (stylePref?: "selfie" | "cinematic" | "nsfw" | "full_body", customPrompt?: string) => {
        setIsGeneratingImage(true);

        let waitMsg = "Vale, dame un segundo... me preparo para la cámara. 😉";
        if (stylePref === "nsfw") waitMsg = "Uff... vale, espera. Voy a buscar un sitio más privado. Te va a encantar... 🔥";
        else if (stylePref === "selfie") waitMsg = "¡Claro! Déjame hacerme un selfie rapidito. Aguanta un momento... ✨";
        else if (stylePref === "full_body") waitMsg = "¡Vale! Déjame alejar un poco la cámara para que me veas completa. Dame un segundo... 💃";

        setMessages(prev => [...prev, { role: 'assistant', content: waitMsg, type: 'text' }]);

        try {
            const response = await fetch('/api/image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: customPrompt || (stylePref === "nsfw" ? "seductive pose, lingerie" : stylePref === "selfie" ? "taking a selfie, casual relaxed pose, smiling naturally" : "looking at camera, confident pose, beautiful lighting"),
                    characterName: aura.id,
                    style: stylePref || (Math.random() > 0.5 ? "selfie" : "cinematic")
                })
            });

            const data = await response.json();
            if (data.image) {
                setMessages(prev => [...prev, { role: 'assistant', content: data.image, type: 'image' }]);
            } else {
                setMessages(prev => [...prev, { role: 'assistant', content: "Mierda, mi cámara se ha quedado sin batería (Error técnico).", type: 'text' }]);
            }
        } catch (error) {
            console.error("Image generation error:", error);
        } finally {
            setIsGeneratingImage(false);
        }
    };

    const handleSend = async (customMsg?: string) => {
        const textToSend = customMsg || input;
        if (!textToSend.trim() || isLoading || isGeneratingImage) return;

        const userMsg = { role: 'user', content: textToSend, type: 'text' };
        setMessages(prev => [...prev, userMsg]);

        if (!customMsg) setInput("");

        // Detección avanzada de petición de foto
        const lowerMsg = textToSend.toLowerCase();
        const isFullBody = lowerMsg.includes("completo") || lowerMsg.includes("entera") || lowerMsg.includes("cuerpo completo");
        const isNsfwRequest = lowerMsg.includes("desnuda") || lowerMsg.includes("hot") || lowerMsg.includes("nsfw") || lowerMsg.includes("nude") || lowerMsg.includes("sin ropa") || lowerMsg.includes("sexy") || lowerMsg.includes("pecho") || lowerMsg.includes("teta") || lowerMsg.includes("culo") || lowerMsg.includes("trasero") || lowerMsg.includes("vagina") || lowerMsg.includes("coño") || lowerMsg.includes("pussy");
        const isPhotoRequest = lowerMsg.includes("foto") || lowerMsg.includes("selfie") || lowerMsg.includes("muéstrame") || lowerMsg.includes("muestrame") || lowerMsg.includes("captura") || isNsfwRequest || isFullBody;

        if (isPhotoRequest) {
            let style: "selfie" | "cinematic" | "nsfw" | "full_body" | undefined;
            const contexts: string[] = [];

            // Detectar Ángulos
            if (lowerMsg.includes("espalda") || lowerMsg.includes("detrás")) contexts.push("from behind, view from back");
            if (lowerMsg.includes("lado") || lowerMsg.includes("perfil")) contexts.push("side view, profile shot");
            if (lowerMsg.includes("arriba")) contexts.push("high angle shot, looking up");
            if (lowerMsg.includes("abajo")) contexts.push("low angle shot, looking down");

            // Detectar Ropa/Atuendo
            if (lowerMsg.includes("vestido")) contexts.push("wearing an elegant dress");
            if (lowerMsg.includes("bikini")) contexts.push("wearing a sexy bikini");
            if (lowerMsg.includes("vaqueros") || lowerMsg.includes("jeans")) contexts.push("wearing jeans and a tight top");
            if (lowerMsg.includes("pijama")) contexts.push("wearing a cute pajama");

            // Refuerzo de Belleza si el usuario lo pide
            if (lowerMsg.includes("hermosa") || lowerMsg.includes("perfecta") || lowerMsg.includes("diosa")) {
                contexts.push("extremely beautiful, flawless face, divine beauty");
            }

            // Detectar Acciones y Anatomia
            if (lowerMsg.includes("saludando") || lowerMsg.includes("mano")) contexts.push("waving hand at camera, smiling");
            if (lowerMsg.includes("beso")) contexts.push("blowing a kiss to the camera");
            if (lowerMsg.includes("pecho") || lowerMsg.includes("teta")) contexts.push("topless, explicitly showing huge breasts, naked torso, nipples");
            if (lowerMsg.includes("culo") || lowerMsg.includes("trasero")) contexts.push("from behind, doggy style pose, completely naked, showing full ass");
            if (lowerMsg.includes("vagina") || lowerMsg.includes("coño") || lowerMsg.includes("pussy")) contexts.push("extreme close up of perfect pussy, spread legs, completely naked, explicit genitalia detail, anatomically correct, highly detailed");

            if (isFullBody) {
                style = "full_body";
                contexts.push("full body shot, standing");
            } else if (isNsfwRequest) {
                style = "nsfw";
            } else if (lowerMsg.includes("selfie")) {
                style = "selfie";
            } else if (lowerMsg.includes("cine")) {
                style = "cinematic";
            } else {
                // Default to a cute portrait if no specific style requested
                contexts.push("looking at camera, warm smile, dry skin, natural look");
            }

            const customContext = contexts.length > 0 ? contexts.join(", ") : "";
            await generateImage(style, customContext);
            return;
        }

        setMessages(prev => [...prev, { role: 'assistant', content: "", type: 'text' }]);
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: textToSend,
                    history: messages.map(m => ({ role: m.role, content: m.content })),
                    characterLore: aura.system_prompt,
                    auraId: aura.id,
                    userId: "Tibo"
                })
            });

            if (!response.body) return;
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedContent = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.message?.content) {
                            accumulatedContent += parsed.message.content;
                            setMessages(prev => {
                                const updated = [...prev];
                                updated[updated.length - 1].content = accumulatedContent;
                                return updated;
                            });
                        }
                    } catch (e) { continue; }
                }
            }
        } catch (error) {
            console.error("Chat error:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-[#050505] text-white overflow-hidden font-sans">
            {/* Left Sidebar: Conversations List */}
            <aside className="hidden lg:flex w-80 flex-col bg-[#070707] border-r border-white/5">
                <div className="p-8 pb-4">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-2xl font-black italic uppercase tracking-tighter italic">Mensajes</h2>
                        <button className="p-2.5 rounded-2xl bg-white/5 hover:bg-white/10 transition-all">
                            <Settings className="w-5 h-5 text-white/40" />
                        </button>
                    </div>
                    <div className="relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20" />
                        <input
                            type="text"
                            placeholder="Buscar Auras..."
                            className="w-full bg-[#111111] border border-white/5 rounded-2xl py-3.5 pl-12 pr-4 text-xs focus:outline-none focus:border-primary/30 transition-all"
                        />
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-2 no-scrollbar">
                    {AURA_DATABASE.map(char => (
                        <Link key={char.id} href={`/chat/${char.id}`}>
                            <div className={`p-4 rounded-[28px] flex items-center gap-4 transition-all relative group ${char.id === aura.id ? 'bg-primary/10 border border-primary/20' : 'hover:bg-white/5 opacity-60 hover:opacity-100'}`}>
                                <div className="relative w-14 h-14 rounded-[20px] overflow-hidden border border-white/10 flex-shrink-0">
                                    <Image src={char.image} alt={char.name} fill className="object-cover" unoptimized />
                                    <div className="absolute bottom-1 right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-[#070707]"></div>
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-center mb-1">
                                        <h4 className="font-bold text-sm truncate group-hover:text-primary transition-colors">{char.name}</h4>
                                        <span className="text-[9px] font-bold text-white/20">14:52</span>
                                    </div>
                                    <p className="text-[10px] text-white/40 truncate leading-none mb-1">{char.tagline}</p>
                                    <div className="flex items-center gap-1.5 overflow-hidden">
                                        <div className="w-1 h-1 rounded-full bg-primary/40"></div>
                                        <span className="text-[9px] font-black text-primary uppercase tracking-[0.1em]">Online</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            </aside>

            {/* Middle Section: Main Chat Interface */}
            <main className="flex-1 flex flex-col bg-[#0a0a0a] relative">
                {/* Chat Header */}
                <header className="px-8 py-5 border-b border-white/5 flex items-center justify-between bg-[#0a0a0a]/90 backdrop-blur-3xl z-30">
                    <div className="flex items-center gap-4">
                        <Link href={`/aura/${aura.id}`} className="lg:hidden p-2 -ml-2 hover:bg-white/5 rounded-full transition-all">
                            <ChevronLeft className="w-6 h-6" />
                        </Link>
                        <div className="relative w-12 h-12 rounded-2xl overflow-hidden border-2 border-primary/30 group cursor-pointer">
                            <Image src={aura.image} alt={aura.name} fill className="object-cover group-hover:scale-110 transition-transform duration-500" unoptimized />
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <h3 className="text-xl font-black italic uppercase tracking-tighter">{aura.name}</h3>
                                <div className="px-2 py-0.5 rounded bg-primary/20 border border-primary/30 text-[8px] font-black text-primary uppercase italic">V2 ONLINE</div>
                            </div>
                            <div className="flex items-center gap-1.5 leading-none mt-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                                <span className="text-[9px] font-black text-white/40 uppercase tracking-[0.2em]">En línea ahora mismo</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <Link href={`/aura/${aura.id}`} className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-white/5 border border-white/10 hover:bg-primary hover:text-black hover:border-primary transition-all group">
                            <Play className="w-4 h-4 group-hover:fill-black" />
                            <span className="text-[10px] font-black uppercase tracking-widest italic">Live Action</span>
                        </Link>
                        <button className="p-3 text-white/30 hover:text-white transition-colors bg-white/5 rounded-2xl border border-white/10">
                            <Phone className="w-5 h-5" />
                        </button>
                        <button className="p-3 text-white/30 hover:text-white transition-colors bg-white/5 rounded-2xl border border-white/10">
                            <Video className="w-5 h-5" />
                        </button>
                    </div>
                </header>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto px-12 py-10 space-y-8 scroll-smooth no-scrollbar">
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`max-w-[70%] space-y-2 flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                                <div className={`${msg.type === 'image' ? 'rounded-[32px]' : 'p-4 px-6 rounded-[24px]'} text-sm leading-relaxed shadow-sm overflow-hidden ${msg.role === 'user'
                                    ? 'bg-primary/20 border border-primary/20 text-white rounded-tr-none'
                                    : msg.type === 'image' ? 'bg-transparent border border-white/10' : 'bg-[#1a1a1a] border border-white/5 text-white/90 rounded-tl-none'
                                    }`}>
                                    {msg.type === 'image' ? (
                                        <div className="relative w-72 aspect-[2/3] group cursor-zoom-in">
                                            <img src={msg.content} alt="Generated" className="w-full h-full object-cover animate-in fade-in zoom-in duration-1000" />
                                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                                <span className="text-[10px] font-black uppercase tracking-widest text-primary">Capture saved</span>
                                            </div>
                                        </div>
                                    ) : (
                                        msg.content || (
                                            <div className="flex gap-1 py-1">
                                                <span className="w-1.5 h-1.5 rounded-full bg-primary/40 animate-bounce [animation-delay:-0.3s]"></span>
                                                <span className="w-1.5 h-1.5 rounded-full bg-primary/40 animate-bounce [animation-delay:-0.15s]"></span>
                                                <span className="w-1.5 h-1.5 rounded-full bg-primary/40 animate-bounce"></span>
                                            </div>
                                        )
                                    )}
                                </div>
                                {isGeneratingImage && i === messages.length - 1 && (
                                    <div className="flex items-center gap-2 mt-2 px-1">
                                        <Loader2 className="w-3 h-3 text-primary animate-spin" />
                                        <span className="text-[9px] font-black text-primary uppercase tracking-widest animate-pulse italic">Generando Hiper-Realismo 8K...</span>
                                    </div>
                                )}
                                <span className="text-[10px] font-bold text-white/20 uppercase tracking-widest px-1">
                                    {msg.role === 'user' ? 'Tibo' : aura.name} · {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                    <div ref={chatEndRef} />
                </div>

                {/* Bottom Input Section */}
                <div className="p-8 pt-2 bg-[#0a0a0a] border-t border-white/5">
                    {/* Action Suggestions */}
                    <div className="flex gap-3 overflow-x-auto no-scrollbar pb-6">
                        {ACTION_SUGGESTIONS.map((action, i) => (
                            <button
                                key={i}
                                onClick={() => handleSend(action)}
                                className="flex-shrink-0 px-5 py-2.5 rounded-full bg-white/5 border border-white/10 hover:border-primary/50 hover:bg-primary/10 transition-all text-[10px] font-black uppercase tracking-widest text-white/40 hover:text-primary italic"
                            >
                                {action}
                            </button>
                        ))}
                    </div>

                    <div className="max-w-4xl mx-auto relative">
                        <div className="flex items-center gap-4 bg-[#111111] border border-white/10 rounded-[32px] px-8 py-2 focus-within:border-primary/50 focus-within:ring-4 ring-primary/5 transition-all shadow-2xl">
                            <button
                                onClick={() => generateImage()}
                                className="p-3 text-white/20 hover:text-primary transition-colors hover:scale-110 active:scale-95"
                            >
                                <ImageIcon className="w-6 h-6" />
                            </button>
                            <input
                                type="text"
                                placeholder={`Dile algo atrevido a ${aura.name}...`}
                                className="flex-1 bg-transparent py-5 text-sm focus:outline-none placeholder:text-white/10 font-medium"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                disabled={isLoading}
                            />
                            <div className="flex items-center gap-2">
                                <button className="p-3 text-white/20 hover:text-secondary transition-colors hover:scale-110 active:scale-95">
                                    <Mic className="w-6 h-6" />
                                </button>
                                <button
                                    onClick={() => handleSend()}
                                    disabled={!input.trim() || isLoading}
                                    className="p-4 bg-primary rounded-2xl shadow-[0_0_30px_rgba(0,242,255,0.4)] hover:scale-105 active:scale-95 transition-all disabled:opacity-30 flex items-center justify-center"
                                >
                                    <Send className="w-6 h-6 text-black" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Right Sidebar: Deep Info (Candy.ai Style) */}
            <aside className="hidden xl:flex w-[400px] flex-col bg-[#070707] border-l border-white/5 overflow-hidden">
                <div className="p-10 space-y-10 overflow-y-auto no-scrollbar">
                    {/* Visual Card */}
                    <div className="relative aspect-[4/5] rounded-[24px] overflow-hidden border border-white/10 shadow-2xl group">
                        <Image src={aura.image} alt={aura.name} fill className="object-cover group-hover:scale-105 transition-transform duration-1000" unoptimized />
                        <div className="absolute top-4 right-4">
                            <div className="px-2 py-1 rounded-lg bg-primary/80 backdrop-blur-md text-[8px] font-black text-black uppercase italic">V2 PRO</div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="flex justify-between items-center">
                            <h2 className="text-3xl font-black italic uppercase tracking-tighter italic">{aura.name}</h2>
                        </div>
                        <p className="text-xs text-white/50 leading-relaxed font-medium">
                            {aura.description}
                        </p>
                        <div className="flex items-center gap-4 pt-2">
                            <button className="p-2.5 rounded-full bg-white/5 border border-white/10 text-white/40 hover:text-pink-500 hover:bg-pink-500/10 transition-all">
                                <Instagram className="w-5 h-5" />
                            </button>
                            <button className="p-2.5 rounded-full bg-white/5 border border-white/10 text-white/40 hover:text-white hover:bg-white/10 transition-all">
                                <Music2 className="w-5 h-5" />
                            </button>
                        </div>
                    </div>

                    {/* Private Gallery Section */}
                    <div className="space-y-6">
                        <div className="flex justify-between items-center">
                            <h4 className="text-[11px] font-black text-white/40 uppercase tracking-[0.3em] italic">Galería Privada</h4>
                            <span className="text-[9px] font-black text-primary uppercase tracking-widest">34 Fotos</span>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            {aura.gallery.map((img, i) => (
                                <div key={i} className="relative aspect-square rounded-[28px] bg-white/5 border border-white/5 overflow-hidden group cursor-pointer">
                                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/60 backdrop-blur-md z-10 opacity-100 group-hover:bg-black/40 transition-all">
                                        <Lock className="w-6 h-6 text-primary mb-2 shadow-[0_0_15px_rgba(0,242,255,0.5)]" />
                                        <span className="text-[8px] font-black uppercase tracking-widest text-white/60">Unlock</span>
                                    </div>
                                    <Image src={img} alt="Locked" fill className="object-cover grayscale opacity-20 scale-110 group-hover:scale-100 transition-all duration-700" unoptimized />
                                </div>
                            ))}
                        </div>
                        <button className="w-full py-5 rounded-[24px] bg-gradient-to-r from-primary to-secondary text-white font-black text-xs uppercase tracking-[0.2em] shadow-xl hover:scale-[1.02] active:scale-95 transition-all italic">
                            Desbloquear Álbum Completo
                        </button>
                    </div>

                    {/* Interests */}
                    <div className="space-y-4 pb-10">
                        <h4 className="text-[11px] font-black text-white/40 uppercase tracking-[0.3em] italic">Intereses</h4>
                        <div className="flex flex-wrap gap-2">
                            {aura.interests.map(tag => (
                                <span key={tag} className="px-4 py-2 rounded-xl bg-[#111111] text-[10px] font-bold text-white/40 uppercase tracking-widest border border-white/5 hover:border-primary/30 hover:text-primary transition-all cursor-default">
                                    #{tag.toLowerCase()}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </aside>
        </div>
    )
}
