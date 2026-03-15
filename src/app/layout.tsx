import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "AURA.LIVE | AI Realism & Interaction",
  description: "Experience the next level of AI companionship with ultra-realistic characters and live interaction.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-black min-h-screen">
        <Sidebar />
        <div className="pl-20">
          {children}
        </div>
      </body>
    </html>
  );
}
