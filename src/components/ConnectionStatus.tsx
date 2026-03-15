"use client"

import { useState, useEffect } from "react"
import { Cpu, Zap, Image as ImageIcon, CheckCircle2, XCircle, AlertCircle } from "lucide-react"

export default function ConnectionStatus() {
    const [ollamaStatus, setOllamaStatus] = useState<'connected' | 'disconnected' | 'loading'>('loading')
    const [sdStatus, setSdStatus] = useState<'connected' | 'disconnected' | 'loading'>('loading')

    const checkStatus = async () => {
        // Check Ollama
        try {
            const res = await fetch('http://localhost:11434/api/tags')
            if (res.ok) setOllamaStatus('connected')
            else setOllamaStatus('disconnected')
        } catch {
            setOllamaStatus('disconnected')
        }

        // Check Stable Diffusion (SD.Next)
        try {
            const res = await fetch('http://127.0.0.1:7860/sdapi/v1/options')
            if (res.ok) setSdStatus('connected')
            else setSdStatus('disconnected')
        } catch {
            setSdStatus('disconnected')
        }
    }

    useEffect(() => {
        checkStatus()
        const interval = setInterval(checkStatus, 5000)
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="flex flex-col gap-3 p-4 glass rounded-2xl border border-white/5 mb-6">
            <h3 className="text-[10px] font-bold text-foreground/40 uppercase tracking-widest mb-1 flex items-center gap-2">
                <Cpu className="w-3 h-3" /> Estado del Motor Local
            </h3>

            <div className="flex items-center justify-between group">
                <div className="flex items-center gap-2">
                    <Zap className={`w-3.5 h-3.5 ${ollamaStatus === 'connected' ? 'text-primary' : 'text-foreground/20'}`} />
                    <span className="text-xs font-medium">Ollama (Chat)</span>
                </div>
                {ollamaStatus === 'connected' ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                ) : (
                    <div className="flex items-center gap-1 text-[9px] text-red-500/80 font-bold uppercase">
                        <span>Desconectado</span>
                        <AlertCircle className="w-3 h-3" />
                    </div>
                )}
            </div>

            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <ImageIcon className={`w-3.5 h-3.5 ${sdStatus === 'connected' ? 'text-secondary' : 'text-foreground/20'}`} />
                    <span className="text-xs font-medium">SD.Next (Fotos)</span>
                </div>
                {sdStatus === 'connected' ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-500" />
                ) : (
                    <div className="flex items-center gap-1 text-[9px] text-red-500/80 font-bold uppercase">
                        <span>Desconectado</span>
                        <AlertCircle className="w-3 h-3" />
                    </div>
                )}
            </div>

            {(ollamaStatus === 'disconnected' || sdStatus === 'disconnected') && (
                <p className="text-[9px] text-foreground/30 mt-2 leading-tight">
                    Asegúrate de ejecutar con <code className="text-primary/70">--api</code> activo.
                </p>
            )}
        </div>
    )
}
