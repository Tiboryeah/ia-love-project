"use client"

import { Home, Compass, MessageSquare, Image, Zap, Heart, Settings, LayoutGrid } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

export default function Sidebar() {
    const pathname = usePathname();

    const menuItems = [
        { icon: <Home className="w-6 h-6" />, label: "Inicio", href: "/" },
        { icon: <Compass className="w-6 h-6" />, label: "Descubrir", href: "/#auras" },
        { icon: <MessageSquare className="w-6 h-6" />, label: "Chats", href: "/chat/fitness-vicky" },
        { icon: <LayoutGrid className="w-6 h-6" />, label: "Live Action", href: "/#live" },
        { icon: <Image className="w-6 h-6" />, label: "Galería", href: "#" },
        { icon: <Zap className="w-6 h-6" />, label: "Generar", href: "#" },
    ];

    return (
        <aside className="fixed left-0 top-0 h-screen w-20 flex flex-col items-center py-8 bg-[#050505] border-r border-white/5 z-50">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center mb-12 shadow-[0_0_20px_rgba(0,242,255,0.4)]">
                <span className="text-white font-black text-xl italic">A</span>
            </div>

            <nav className="flex-1 flex flex-col gap-8">
                {menuItems.map((item, i) => (
                    <Link
                        key={i}
                        href={item.href}
                        className={`group relative p-3 rounded-2xl transition-all ${pathname === item.href ? 'bg-primary/20 text-primary shadow-lg shadow-primary/10' : 'text-white/30 hover:text-white hover:bg-white/5'
                            }`}
                    >
                        {item.icon}
                        {/* Tooltip */}
                        <span className="absolute left-full ml-4 px-3 py-1.5 rounded-lg bg-white text-black text-[10px] font-black uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-[100]">
                            {item.label}
                        </span>
                    </Link>
                ))}
            </nav>

            <div className="mt-auto flex flex-col gap-6">
                <button className="p-3 rounded-2xl text-white/30 hover:text-primary transition-all">
                    <Heart className="w-6 h-6" />
                </button>
                <button className="p-3 rounded-2xl text-white/30 hover:text-white transition-all">
                    <Settings className="w-6 h-6" />
                </button>
                <div className="w-10 h-10 rounded-full border-2 border-primary/20 overflow-hidden cursor-pointer hover:border-primary transition-all">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Tibo" alt="User" className="w-full h-full object-cover" />
                </div>
            </div>
        </aside>
    )
}
