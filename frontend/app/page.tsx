"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Exo_2, Plus_Jakarta_Sans } from 'next/font/google';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowRight, Bot, Clock, MessageSquare, Zap, 
  BarChart, ShieldCheck, Smartphone, Target, 
  CheckCircle2, Users, FileText, BrainCircuit,
  TrendingUp, Layers, PlayCircle, Menu, X,
  Sparkles, Activity, Check, AlertTriangle, Lightbulb
} from 'lucide-react';

const exo2 = Exo_2({ subsets: ['latin'], weight: ['400', '600', '700', '800'] });
const jakarta = Plus_Jakarta_Sans({ subsets: ['latin'], weight: ['400', '500', '600', '700'] });

// Animation Variants
const fadeInUp = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.1, 0.25, 1.0] } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1
    }
  }
};

export default function LandingPage() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className={`min-h-screen bg-white text-slate-900 ${jakarta.className} selection:bg-blue-100 selection:text-blue-900 antialiased overflow-x-hidden`}>
      
      {/* NAVBAR */}
      <header className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-100/80 transition-all">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16 sm:h-20">
            {/* Brand Logo */}
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 group-hover:border-blue-300 transition-colors">
                <Image src="/Logo_NUSARA.png" alt="NUSARA Logo" width={26} height={26} className="object-contain" />
              </div>
              <span className={`text-xl font-bold tracking-tight text-slate-900 ${exo2.className}`}>
                NUSARA
              </span>
            </Link>
            
            {/* Desktop Nav Links */}
            <nav className="hidden md:flex items-center space-x-9">
              <Link href="#fitur" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
                Fitur
              </Link>
              <Link href="#cara-kerja" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
                Cara Kerja
              </Link>
              <Link href="#solusi" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
                Solusi
              </Link>
            </nav>

            {/* Desktop Action Buttons */}
            <div className="hidden md:flex items-center space-x-5">
              <Link href="/login" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
                Masuk
              </Link>
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Link href="/register" className="inline-flex items-center justify-center px-5 py-2.5 rounded-full bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition-all shadow-md shadow-blue-600/20 hover:shadow-lg hover:shadow-blue-600/30">
                  Coba Gratis
                </Link>
              </motion.div>
            </div>

            {/* Mobile Nav Toggle */}
            <div className="md:hidden flex items-center">
              <button 
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} 
                className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                aria-label="Toggle Menu"
              >
                {isMobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden bg-white border-b border-slate-100 px-4 py-6 space-y-4 shadow-xl overflow-hidden"
            >
              <Link 
                href="#fitur" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="block text-base font-medium text-slate-700 hover:text-blue-600"
              >
                Fitur
              </Link>
              <Link 
                href="#cara-kerja" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="block text-base font-medium text-slate-700 hover:text-blue-600"
              >
                Cara Kerja
              </Link>
              <Link 
                href="#solusi" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="block text-base font-medium text-slate-700 hover:text-blue-600"
              >
                Solusi
              </Link>
              <div className="pt-2 border-t border-slate-100 flex flex-col gap-3">
                <Link href="/login" className="block text-center text-base font-medium text-slate-700 py-2 border border-slate-200 rounded-full">
                  Masuk
                </Link>
                <Link href="/register" className="block text-center text-base font-semibold text-white bg-blue-600 py-2.5 rounded-full shadow-sm">
                  Coba Gratis Sekarang
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* HERO SECTION */}
      <section className="relative pt-32 pb-20 lg:pt-44 lg:pb-32 overflow-hidden bg-slate-50/50">
        {/* Subtle Precision Grid & Glow Background */}
        <div className="absolute inset-0 bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] [background-size:24px_24px] opacity-60"></div>
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-blue-400/20 via-sky-300/15 to-transparent rounded-full blur-[110px] pointer-events-none"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <motion.div 
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200/80 text-blue-700 text-xs sm:text-sm font-semibold mb-8 shadow-xs hover:border-blue-300 transition-colors"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
            </span>
            AI Partner untuk Bisnis Modern Indonesia
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className={`text-4xl sm:text-5xl lg:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.12] mb-6 ${exo2.className}`}
          >
            AI Customer Service yang <br className="hidden md:block" />
            <span className="text-blue-600">Memahami Bisnis Anda</span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-base sm:text-lg lg:text-xl text-slate-600 max-w-3xl mx-auto mb-10 leading-relaxed font-normal"
          >
            NUSARA membantu bisnis melayani pelanggan 24/7 dengan AI yang memahami produk, layanan, dokumen, dan kebutuhan bisnis Anda secara mendalam.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto sm:max-w-none"
          >
            <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
              <Link 
                href="/register" 
                className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-blue-600 text-white text-base font-semibold hover:bg-blue-700 transition-all shadow-lg shadow-blue-600/25 flex items-center justify-center gap-2 group"
              >
                Mulai Sekarang 
                <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
              </Link>
            </motion.div>

            <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
              <button 
                className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-white text-slate-700 border border-slate-200 text-base font-semibold hover:bg-slate-50 hover:border-slate-300 transition-all shadow-xs flex items-center justify-center gap-2"
              >
                <PlayCircle size={18} className="text-slate-500" /> Lihat Demo
              </button>
            </motion.div>
          </motion.div>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mt-8 text-xs sm:text-sm text-slate-500 font-medium tracking-wide"
          >
            Lebih dari chatbot biasa — AI partner untuk bisnis modern Indonesia.
          </motion.p>

          {/* Micro floating metrics/badges below hero */}
          <motion.div 
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="mt-14 max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 pt-8 border-t border-slate-200/60"
          >
            <div className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-xs backdrop-blur-sm">
              <div className="text-blue-600 font-bold text-xl sm:text-2xl">24/7</div>
              <div className="text-slate-500 text-xs font-medium">Melayani Nonstop</div>
            </div>
            <div className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-xs backdrop-blur-sm">
              <div className="text-blue-600 font-bold text-xl sm:text-2xl">&lt; 0.5s</div>
              <div className="text-slate-500 text-xs font-medium">Respon Instan</div>
            </div>
            <div className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-xs backdrop-blur-sm">
              <div className="text-blue-600 font-bold text-xl sm:text-2xl">98.4%</div>
              <div className="text-slate-500 text-xs font-medium">Akurasi Knowledge</div>
            </div>
            <div className="p-3.5 rounded-2xl bg-white/80 border border-slate-200/80 shadow-xs backdrop-blur-sm">
              <div className="text-blue-600 font-bold text-xl sm:text-2xl">100%</div>
              <div className="text-slate-500 text-xs font-medium">Bahasa Indonesia</div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* PROBLEM SECTION */}
      <section className="py-24 bg-white relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
            className="text-center max-w-3xl mx-auto mb-16"
          >
            <h2 className={`text-3xl sm:text-4xl font-bold text-slate-900 mb-5 ${exo2.className}`}>
              Masalah Customer Service yang Sering Dialami Bisnis
            </h2>
            <div className="inline-flex items-center gap-2 text-rose-700 bg-rose-50 border border-rose-100 py-2.5 px-5 rounded-full text-sm font-semibold shadow-xs">
              <AlertTriangle size={16} className="text-rose-600 shrink-0" />
              <span>Banyak bisnis kehilangan pelanggan karena customer service yang lambat dan tidak efisien.</span>
            </div>
          </motion.div>

          {/* Asymmetric Layout */}
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            variants={staggerContainer}
            className="grid grid-cols-1 lg:grid-cols-3 gap-6"
          >
            {/* Featured Left Card */}
            <motion.div 
              variants={fadeInUp}
              className="lg:col-span-1 bg-slate-900 text-white rounded-3xl p-8 flex flex-col justify-between relative overflow-hidden shadow-xl"
            >
              <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/20 rounded-full blur-3xl pointer-events-none"></div>
              <div>
                <div className="w-12 h-12 rounded-2xl bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-400 mb-6">
                  <Clock size={26} />
                </div>
                <span className="text-xs font-semibold uppercase tracking-wider text-rose-400 mb-2 block">Dampak Utama</span>
                <h3 className="text-2xl font-bold mb-3 text-white">Di Luar Jam Operasional</h3>
                <p className="text-slate-300 text-sm leading-relaxed mb-6">
                  Pelanggan tidak terlayani saat malam hari atau hari libur. Padahal 40%+ keputusan beli terjadi di luar jam kerja resmi admin Anda.
                </p>
              </div>
              <div className="pt-6 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span>Kehilangan leads potensial</span>
                <span className="font-semibold text-rose-400">-35% Konversi</span>
              </div>
            </motion.div>

            {/* Right Side 5 Cards in Grid */}
            <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
              {[
                { 
                  icon: Layers, 
                  title: "Chat Menumpuk", 
                  desc: "Tim CS kewalahan merespon antrian pesan yang terlalu banyak.",
                  badge: "Beban Kerja"
                },
                { 
                  icon: Zap, 
                  title: "Respon Lambat", 
                  desc: "Balasan yang lama dan tidak konsisten membuat pelanggan beralih ke kompetitor.",
                  badge: "Retensi Rendah"
                },
                { 
                  icon: TrendingUp, 
                  title: "Biaya Operasional Tinggi", 
                  desc: "Membayar banyak admin customer service menguras profit bisnis Anda.",
                  badge: "Efisiensi"
                },
                { 
                  icon: MessageSquare, 
                  title: "Pertanyaan Berulang", 
                  desc: "Waktu terbuang untuk menjawab pertanyaan yang sama setiap hari.",
                  badge: "Waktu Terbuang"
                },
                { 
                  icon: BarChart, 
                  title: "Data Terabaikan", 
                  desc: "Data percakapan berharga tidak dimanfaatkan menjadi insight bisnis.",
                  badge: "Insight Hilang"
                }
              ].map((problem, i) => (
                <motion.div 
                  key={i} 
                  variants={fadeInUp}
                  whileHover={{ y: -4 }}
                  className="group bg-slate-50/70 hover:bg-white border border-slate-200/80 hover:border-blue-200 rounded-3xl p-6 transition-all duration-300 shadow-xs hover:shadow-md"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-11 h-11 bg-white border border-slate-200 group-hover:border-blue-200 group-hover:bg-blue-50 text-slate-700 group-hover:text-blue-600 rounded-2xl flex items-center justify-center transition-all duration-300 shadow-xs group-hover:scale-105">
                      <problem.icon size={22} />
                    </div>
                    <span className="text-[11px] font-semibold text-slate-400 group-hover:text-blue-600 bg-white group-hover:bg-blue-50/50 px-2.5 py-1 rounded-full border border-slate-200/60 group-hover:border-blue-100 transition-colors">
                      {problem.badge}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">{problem.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">{problem.desc}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* SOLUTION SECTION */}
      <section id="solusi" className="py-24 bg-slate-950 text-white relative overflow-hidden">
        {/* Glow Lighting Accents */}
        <div className="absolute top-0 right-1/4 w-[500px] h-[500px] bg-blue-600/15 rounded-full blur-[140px] pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/4 w-[450px] h-[450px] bg-sky-500/10 rounded-full blur-[120px] pointer-events-none"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid lg:grid-cols-12 gap-12 lg:gap-16 items-center">
            {/* Left Content Column */}
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeInUp}
              className="lg:col-span-6"
            >
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold mb-6">
                <Sparkles size={14} /> Solusi Cerdas NUSARA
              </div>

              <h2 className={`text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight mb-6 text-white ${exo2.className}`}>
                AI Customer Service yang Bekerja untuk Bisnis Anda
              </h2>

              <p className="text-slate-300 text-base sm:text-lg mb-8 leading-relaxed">
                NUSARA memungkinkan Anda membangun otak digital untuk bisnis Anda. Masukkan knowledge bisnis Anda, dan AI akan menggunakannya sebagai konteks untuk menjawab dengan akurat.
              </p>
              
              <div className="space-y-3.5 mb-9">
                {[
                  "Tambahkan knowledge & konteks bisnis",
                  "Upload dokumen (Menu, Katalog, SOP)",
                  "Masukkan FAQ dan layanan",
                  "Integrasikan informasi produk"
                ].map((item, i) => (
                  <motion.div 
                    key={i} 
                    whileHover={{ x: 4 }}
                    className="flex items-center gap-3.5 p-3 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm"
                  >
                    <div className="w-6 h-6 rounded-full bg-blue-500/20 border border-blue-400/40 flex items-center justify-center shrink-0">
                      <Check className="text-blue-400" size={14} />
                    </div>
                    <span className="text-slate-200 text-sm font-medium">{item}</span>
                  </motion.div>
                ))}
              </div>
              
              <div className="bg-gradient-to-r from-blue-900/40 to-slate-900 border border-blue-500/30 rounded-2xl p-5 backdrop-blur-md relative">
                <p className="font-medium text-blue-200 italic text-sm sm:text-base leading-relaxed">
                  "The AI uses this business context to answer customers more accurately and naturally."
                </p>
              </div>
            </motion.div>
            
            {/* Right Bento Grid Column */}
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={staggerContainer}
              className="lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-4"
            >
              {[
                {
                  icon: Clock,
                  title: "Aktif 24/7",
                  desc: "Tidak pernah tidur, selalu siap melayani kapan saja."
                },
                {
                  icon: Zap,
                  title: "Fast Response",
                  desc: "Balasan instan membuat pelanggan tidak perlu menunggu."
                },
                {
                  icon: BrainCircuit,
                  title: "Contextual",
                  desc: "Jawaban relevan sesuai gaya bahasa dan konteks bisnis."
                },
                {
                  icon: TrendingUp,
                  title: "Scalable",
                  desc: "Tangani ribuan chat serentak tanpa tambah admin."
                }
              ].map((card, i) => (
                <motion.div 
                  key={i} 
                  variants={fadeInUp}
                  whileHover={{ y: -4 }}
                  className="bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/40 rounded-3xl p-6 transition-all duration-300 group backdrop-blur-sm"
                >
                  <div className="w-12 h-12 bg-blue-500/10 border border-blue-500/20 text-blue-400 group-hover:text-blue-300 group-hover:bg-blue-500/20 rounded-2xl flex items-center justify-center mb-5 transition-all group-hover:scale-110">
                    <card.icon size={24} />
                  </div>
                  <h4 className="font-bold text-lg text-white mb-2">{card.title}</h4>
                  <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">{card.desc}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="fitur" className="py-24 bg-slate-50/60 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center max-w-3xl mx-auto mb-16"
          >
            <h2 className={`text-3xl sm:text-4xl font-bold text-slate-900 mb-4 ${exo2.className}`}>
              Fitur Utama NUSARA
            </h2>
            <p className="text-base sm:text-lg text-slate-600">
              Sistem komprehensif yang dirancang khusus untuk memajukan pelayanan bisnis Anda.
            </p>
          </motion.div>

          {/* Bento Grid Layout for Features */}
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {[
              { 
                icon: BrainCircuit, 
                title: "Business Knowledge AI", 
                desc: "AI memahami bisnis Anda melalui knowledge base yang dapat disesuaikan tanpa coding.",
                featured: true 
              },
              { 
                icon: FileText, 
                title: "Document Knowledge", 
                desc: "Upload dokumen bisnis seperti menu, katalog, SOP, atau FAQ untuk langsung dipahami AI." 
              },
              { 
                icon: Users, 
                title: "Human Fallback System", 
                desc: "Ketika AI tidak yakin atau pelanggan mulai emosional, percakapan otomatis dialihkan ke admin manusia." 
              },
              { 
                icon: BarChart, 
                title: "Conversation Insight Engine", 
                desc: "Analisis percakapan pelanggan untuk menemukan kekurangan layanan, pola pertanyaan, dan peluang bisnis.",
                featured: true
              },
              { 
                icon: Target, 
                title: "AI Improvement Recommendation", 
                desc: "NUSARA membantu bisnis mengetahui bagian knowledge yang perlu diperbaiki berdasarkan percakapan nyata customer." 
              },
              { 
                icon: Smartphone, 
                title: "Omnichannel Integration", 
                desc: "Terhubung mulus dengan WhatsApp, website, dan platform komunikasi bisnis Anda lainnya." 
              }
            ].map((feat, i) => (
              <motion.div 
                key={i} 
                variants={fadeInUp}
                whileHover={{ y: -6 }}
                className={`group bg-white rounded-3xl p-8 border border-slate-200/80 hover:border-blue-300 shadow-xs hover:shadow-xl hover:shadow-blue-600/5 transition-all duration-300 flex flex-col justify-between ${
                  feat.featured ? 'md:col-span-2 lg:col-span-1 bg-gradient-to-b from-white to-blue-50/30' : ''
                }`}
              >
                <div>
                  <div className="w-13 h-13 bg-blue-50 border border-blue-100 group-hover:border-blue-200 group-hover:bg-blue-600 text-blue-600 group-hover:text-white rounded-2xl flex items-center justify-center mb-6 transition-all duration-300 group-hover:scale-105 shadow-xs">
                    <feat.icon size={26} />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors">{feat.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">{feat.desc}</p>
                </div>
                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center text-xs font-semibold text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity">
                  Pelajari selengkapnya <ArrowRight size={14} className="ml-1" />
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* HOW IT WORKS SECTION */}
      <section id="cara-kerja" className="py-24 bg-white border-y border-slate-100 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className={`text-3xl sm:text-4xl font-bold text-slate-900 mb-4 ${exo2.className}`}>
              Cara Kerja NUSARA
            </h2>
            <p className="text-base sm:text-lg text-slate-600">
              Mulai otomatisasi customer service Anda hanya dalam 5 langkah mudah.
            </p>
          </motion.div>

          <div className="relative">
            {/* Timeline Connector Line */}
            <div className="hidden lg:block absolute top-10 left-12 right-12 h-0.5 bg-gradient-to-r from-blue-200 via-blue-400 to-blue-200 -z-0"></div>
            
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={staggerContainer}
              className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8 relative z-10"
            >
              {[
                { step: "01", title: "Tambahkan Knowledge", desc: "Input data dan dokumen bisnis Anda." },
                { step: "02", title: "AI Melayani", desc: "AI mulai membalas customer secara otomatis." },
                { step: "03", title: "Human Fallback", desc: "Admin mengambil alih saat dibutuhkan." },
                { step: "04", title: "Analisis Data", desc: "AI menganalisis seluruh percakapan." },
                { step: "05", title: "Dapatkan Insight", desc: "Terima rekomendasi untuk perbaikan bisnis." }
              ].map((step, i) => (
                <motion.div 
                  key={i} 
                  variants={fadeInUp}
                  whileHover={{ y: -4 }}
                  className="flex flex-col items-center text-center group bg-white p-4 rounded-2xl"
                >
                  <div className="w-16 h-16 rounded-2xl bg-white border-2 border-blue-200 group-hover:border-blue-600 group-hover:bg-blue-600 text-blue-600 group-hover:text-white font-bold text-lg mb-5 shadow-md flex items-center justify-center transition-all duration-300 group-hover:scale-110">
                    {step.step}
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">{step.title}</h3>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">{step.desc}</p>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* AI INSIGHT SECTION */}
      <section className="py-24 bg-gradient-to-b from-blue-50/70 to-slate-50 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="bg-white rounded-3xl p-8 sm:p-12 lg:p-14 shadow-xl border border-blue-100 relative z-10"
          >
            <div className="grid lg:grid-cols-12 gap-12 items-center">
              {/* Text Left Column */}
              <div className="lg:col-span-5">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-200/80 text-amber-800 text-xs font-semibold mb-6">
                  <Lightbulb size={15} className="text-amber-600" /> Business Intelligence
                </div>
                
                <h2 className={`text-3xl sm:text-4xl font-bold text-slate-900 mb-6 ${exo2.className}`}>
                  Bukan Sekadar Membalas Chat
                </h2>

                <p className="text-base sm:text-lg text-slate-600 mb-8 leading-relaxed">
                  NUSARA mengubah setiap percakapan pelanggan menjadi data intelijen bisnis yang berharga. Ketahui apa yang pelanggan Anda benar-benar inginkan.
                </p>
                
                <div className="space-y-3.5 mb-8">
                  {[
                    "Pertanyaan yang paling sering muncul",
                    "Bagian layanan yang membingungkan customer",
                    "Titik kegagalan AI (Knowledge Gaps)",
                    "Rekomendasi penambahan knowledge",
                    "Kualitas pelayanan customer service"
                  ].map((point, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className="mt-1 w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                        <CheckCircle2 size={13} className="text-blue-600" />
                      </div>
                      <p className="text-slate-700 text-sm font-medium leading-snug">{point}</p>
                    </div>
                  ))}
                </div>
                
                <div className="p-4 bg-blue-600 rounded-2xl text-white font-semibold text-sm sm:text-base flex items-center gap-3.5 shadow-md shadow-blue-600/20">
                  <TrendingUp size={22} className="text-blue-200 shrink-0" />
                  <span>"Setiap percakapan membantu bisnis Anda berkembang."</span>
                </div>
              </div>
              
              {/* Realistic Interactive Dashboard Mockup */}
              <div className="lg:col-span-7">
                <div className="bg-slate-900 rounded-2xl p-4 sm:p-5 shadow-2xl border border-slate-800 text-white">
                  {/* Window Bar */}
                  <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-rose-500"></div>
                      <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                      <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                      <span className="text-xs text-slate-400 font-mono ml-2 hidden sm:inline">nusara-insight-engine / dashboard</span>
                    </div>
                    <div className="flex items-center gap-2 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                      <Activity size={12} className="animate-pulse" /> AI Engine Active
                    </div>
                  </div>

                  {/* Dashboard Metrics Grid */}
                  <div className="grid grid-cols-3 gap-3 mb-4">
                    <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
                      <div className="text-[11px] text-slate-400 font-medium">Total Chat</div>
                      <div className="text-lg sm:text-xl font-bold text-white mt-1">12,845</div>
                      <div className="text-[10px] text-emerald-400 font-semibold mt-0.5">↑ 18% bulan ini</div>
                    </div>
                    <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
                      <div className="text-[11px] text-slate-400 font-medium">Respon Rate</div>
                      <div className="text-lg sm:text-xl font-bold text-blue-400 mt-1">98.4%</div>
                      <div className="text-[10px] text-blue-300 font-semibold mt-0.5">Otoman CS</div>
                    </div>
                    <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60">
                      <div className="text-[11px] text-slate-400 font-medium">Knowledge Gap</div>
                      <div className="text-lg sm:text-xl font-bold text-amber-400 mt-1">3 Items</div>
                      <div className="text-[10px] text-amber-300 font-semibold mt-0.5">Butuh Update</div>
                    </div>
                  </div>

                  {/* Realistic Chart & Analytics Card */}
                  <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 mb-4">
                    <div className="flex justify-between items-center mb-3">
                      <div className="text-xs font-semibold text-slate-200">Volume Chat & Kategori Utama</div>
                      <div className="text-[10px] text-slate-400">7 Hari Terakhir</div>
                    </div>
                    <div className="flex items-end gap-2 h-24 pt-2">
                      {[40, 65, 85, 55, 90, 70, 95].map((val, idx) => (
                        <div key={idx} className="flex-1 flex flex-col items-center gap-1.5">
                          <div className="w-full bg-blue-600/30 rounded-t-md relative overflow-hidden" style={{ height: `${val}%` }}>
                            <div className="absolute inset-x-0 bottom-0 bg-blue-500 rounded-t-md" style={{ height: `${val * 0.7}%` }}></div>
                          </div>
                          <span className="text-[9px] text-slate-500">Hari {idx + 1}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* AI Recommendation Alert */}
                  <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-start gap-3">
                    <div className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 mt-0.5">
                      <Sparkles size={16} />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-amber-300">Rekomendasi AI Otomatis</div>
                      <div className="text-[11px] text-slate-300 mt-0.5 leading-snug">
                        Pelanggan sering bertanya tentang <span className="text-amber-200 font-semibold">"Estimasi Ongkir ke Surabaya"</span>. Tambahkan FAQ biaya kirim untuk meningkatkan kepuasan.
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* TARGET MARKET SECTION */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
          >
            <h2 className={`text-3xl sm:text-4xl font-bold text-slate-900 mb-5 ${exo2.className}`}>
              Dibangun untuk Bisnis Indonesia
            </h2>
            <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto mb-14">
              Sistem yang dirancang agar mudah digunakan, scalable, affordable, dan relevan dengan gaya komunikasi masyarakat Indonesia.
            </p>

            <div className="flex flex-wrap justify-center gap-3.5 max-w-4xl mx-auto">
              {[
                "UMKM", "Online Shop", "Food & Beverage", "Klinik & Salon", 
                "Jasa Profesional", "Startup Kecil", "Bisnis Lokal"
              ].map((market, i) => (
                <motion.span 
                  key={i} 
                  whileHover={{ scale: 1.05, y: -2 }}
                  className="px-6 py-3 bg-slate-50 border border-slate-200/90 text-slate-800 rounded-full text-sm font-semibold shadow-xs hover:border-blue-300 hover:bg-blue-50/50 hover:text-blue-700 transition-all cursor-default"
                >
                  {market}
                </motion.span>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* BENEFITS SECTION */}
      <section className="py-24 bg-slate-950 text-white relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="text-center mb-16"
          >
            <h2 className={`text-3xl sm:text-4xl font-bold text-white mb-4 ${exo2.className}`}>
              Mengapa Memilih NUSARA?
            </h2>
          </motion.div>

          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5"
          >
            {[
              "Respon pelanggan lebih cepat",
              "Layanan aktif 24/7",
              "Mengurangi beban admin",
              "AI memahami bisnis Anda",
              "Insight bisnis otomatis",
              "Skalabel untuk bisnis berkembang",
              "AI + Human collaboration",
              "Membantu meningkatkan kepuasan"
            ].map((benefit, i) => (
              <motion.div 
                key={i} 
                variants={fadeInUp}
                whileHover={{ y: -4 }}
                className="bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/40 rounded-2xl p-5 flex items-start gap-4 transition-all duration-300 group"
              >
                <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 group-hover:text-blue-300 flex items-center justify-center shrink-0">
                  <ShieldCheck size={20} />
                </div>
                <span className="font-semibold text-slate-200 text-sm leading-snug mt-2">{benefit}</span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="py-20 sm:py-24 bg-white relative overflow-hidden">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeInUp}
            className="bg-gradient-to-r from-blue-600 via-blue-600 to-blue-700 rounded-3xl p-8 sm:p-14 text-center text-white relative overflow-hidden shadow-2xl shadow-blue-600/30"
          >
            <div className="absolute top-0 right-0 -mt-12 -mr-12 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
            
            <h2 className={`text-3xl sm:text-4xl lg:text-5xl font-extrabold mb-6 text-white ${exo2.className}`}>
              Bangun Customer Service yang Lebih Cerdas
            </h2>

            <p className="text-base sm:text-xl text-blue-100 mb-10 max-w-2xl mx-auto leading-relaxed">
              Gunakan AI yang memahami bisnis Anda dan bantu pelanggan dengan lebih cepat, lebih cerdas, dan lebih efisien.
            </p>

            <motion.div whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.98 }} className="inline-block">
              <Link 
                href="/register" 
                className="inline-flex items-center gap-2.5 px-9 py-4 rounded-full bg-white text-blue-600 text-base sm:text-lg font-bold hover:bg-blue-50 transition-all shadow-xl hover:shadow-2xl"
              >
                Mulai dengan NUSARA <ArrowRight size={20} />
              </Link>
            </motion.div>

            <p className="mt-6 text-xs sm:text-sm text-blue-200/90 font-medium tracking-wide">
              Siap digunakan untuk bisnis modern Indonesia.
            </p>
          </motion.div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-white border-t border-slate-100 pt-16 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
            <div className="md:col-span-1">
              <div className="flex items-center gap-2.5 mb-4">
                <Image src="/Logo_NUSARA.png" alt="NUSARA Logo" width={26} height={26} className="object-contain" />
                <span className={`text-xl font-bold tracking-tight text-slate-900 ${exo2.className}`}>
                  NUSARA
                </span>
              </div>
              <p className="text-slate-500 text-xs sm:text-sm leading-relaxed mb-6">
                AI Customer Service untuk Bisnis Indonesia. Mengubah percakapan menjadi pengalaman pelanggan yang luar biasa.
              </p>
            </div>
            
            <div>
              <h4 className="font-bold text-slate-900 text-sm mb-4">Platform</h4>
              <ul className="space-y-3 text-xs sm:text-sm text-slate-600">
                <li><Link href="#fitur" className="hover:text-blue-600 transition-colors">Fitur</Link></li>
                <li><Link href="#solusi" className="hover:text-blue-600 transition-colors">Solusi</Link></li>
                <li><Link href="#cara-kerja" className="hover:text-blue-600 transition-colors">Cara Kerja</Link></li>
                <li><Link href="/pricing" className="hover:text-blue-600 transition-colors">Harga</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold text-slate-900 text-sm mb-4">Perusahaan</h4>
              <ul className="space-y-3 text-xs sm:text-sm text-slate-600">
                <li><Link href="/about" className="hover:text-blue-600 transition-colors">Tentang Kami</Link></li>
                <li><Link href="/blog" className="hover:text-blue-600 transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-blue-600 transition-colors">Hubungi Kami</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold text-slate-900 text-sm mb-4">Legal</h4>
              <ul className="space-y-3 text-xs sm:text-sm text-slate-600">
                <li><Link href="/privacy" className="hover:text-blue-600 transition-colors">Kebijakan Privasi</Link></li>
                <li><Link href="/terms" className="hover:text-blue-600 transition-colors">Syarat & Ketentuan</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-slate-100 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-slate-400 text-xs sm:text-sm">
              &copy; {new Date().getFullYear()} NUSARA. All rights reserved.
            </p>
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-slate-100 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-center text-slate-500 font-semibold text-xs cursor-pointer transition-colors">
                 IG
              </div>
              <div className="w-8 h-8 rounded-full bg-slate-100 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-center text-slate-500 font-semibold text-xs cursor-pointer transition-colors">
                 LI
              </div>
              <div className="w-8 h-8 rounded-full bg-slate-100 hover:bg-blue-50 hover:text-blue-600 flex items-center justify-center text-slate-500 font-semibold text-xs cursor-pointer transition-colors">
                 TW
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
