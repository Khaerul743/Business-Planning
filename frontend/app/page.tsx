"use client";

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Exo_2 } from 'next/font/google';
import { 
  ArrowRight, Bot, Clock, MessageSquare, Zap, 
  BarChart, ShieldCheck, Smartphone, Target, 
  CheckCircle2, Users, FileText, BrainCircuit,
  TrendingUp, Layers, LifeBuoy, PlayCircle, Menu, X
} from 'lucide-react';
import { useState } from 'react';

const exo2 = Exo_2({ subsets: ['latin'], weight: ['400', '600', '700', '800'] });

export default function LandingPage() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* NAVBAR */}
      <nav className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Image src="/Logo_NUSARA.png" alt="NUSARA Logo" width={32} height={32} className="object-contain" />
              <span className={`text-xl font-bold tracking-wide text-indigo-950 ${exo2.className}`}>
                NUSARA
              </span>
            </div>
            
            {/* Desktop Nav */}
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#fitur" className="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors">Fitur</Link>
              <Link href="#cara-kerja" className="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors">Cara Kerja</Link>
              <Link href="#solusi" className="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors">Solusi</Link>
              <div className="h-4 w-px bg-gray-300"></div>
              <Link href="/login" className="text-sm font-medium text-gray-600 hover:text-indigo-600 transition-colors">Masuk</Link>
              <Link href="/register" className="px-4 py-2 rounded-full bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 transition-all shadow-sm hover:shadow-md">
                Coba Gratis
              </Link>
            </div>

            {/* Mobile Nav Toggle */}
            <div className="md:hidden flex items-center">
              <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-gray-600 hover:text-gray-900">
                {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden bg-white border-b border-gray-100 px-4 py-4 space-y-3">
            <Link href="#fitur" className="block text-base font-medium text-gray-700">Fitur</Link>
            <Link href="#cara-kerja" className="block text-base font-medium text-gray-700">Cara Kerja</Link>
            <Link href="#solusi" className="block text-base font-medium text-gray-700">Solusi</Link>
            <hr className="border-gray-100" />
            <Link href="/login" className="block text-base font-medium text-gray-700">Masuk</Link>
            <Link href="/register" className="block text-base font-medium text-indigo-600">Coba Gratis Sekarang</Link>
          </div>
        )}
      </nav>

      {/* HERO SECTION */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay"></div>
        <div className="absolute top-0 inset-x-0 h-full bg-gradient-to-b from-indigo-50/50 to-slate-50/20 -z-10"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100/50 border border-indigo-200 text-indigo-700 text-sm font-medium mb-8">
            <span className="flex h-2 w-2 rounded-full bg-indigo-600"></span>
            AI Partner untuk Bisnis Modern Indonesia
          </div>
          
          <h1 className={`text-4xl md:text-5xl lg:text-7xl font-bold text-gray-900 tracking-tight leading-tight mb-6 ${exo2.className}`}>
            AI Customer Service yang <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Memahami Bisnis Anda</span>
          </h1>
          
          <p className="mt-4 text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            NUSARA membantu bisnis melayani pelanggan 24/7 dengan AI yang memahami produk, layanan, dokumen, dan kebutuhan bisnis Anda secara mendalam.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/register" className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-indigo-600 text-white text-base font-semibold hover:bg-indigo-700 transition-all shadow-lg hover:shadow-indigo-200 flex items-center justify-center gap-2">
              Mulai Sekarang <ArrowRight size={18} />
            </Link>
            <button className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-white text-gray-700 border border-gray-200 text-base font-semibold hover:bg-gray-50 transition-all flex items-center justify-center gap-2">
              <PlayCircle size={18} className="text-gray-500" /> Lihat Demo
            </button>
          </div>
          
          <p className="mt-8 text-sm text-gray-500 font-medium">
            Lebih dari chatbot biasa — AI partner untuk bisnis modern Indonesia.
          </p>
        </div>
      </section>

      {/* PROBLEM SECTION */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className={`text-3xl md:text-4xl font-bold text-gray-900 mb-6 ${exo2.className}`}>
              Masalah Customer Service yang Sering Dialami Bisnis
            </h2>
            <p className="text-lg text-red-600/90 font-medium bg-red-50 py-3 px-6 rounded-2xl inline-block">
              Banyak bisnis kehilangan pelanggan karena customer service yang lambat dan tidak efisien.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: Clock, title: "Di Luar Jam Operasional", desc: "Pelanggan tidak terlayani saat malam hari atau hari libur." },
              { icon: Layers, title: "Chat Menumpuk", desc: "Tim CS kewalahan merespon antrian pesan yang terlalu banyak." },
              { icon: Zap, title: "Respon Lambat", desc: "Balasan yang lama dan tidak konsisten membuat pelanggan beralih ke kompetitor." },
              { icon: TrendingUp, title: "Biaya Operasional Tinggi", desc: "Membayar banyak admin customer service menguras profit bisnis Anda." },
              { icon: MessageSquare, title: "Pertanyaan Berulang", desc: "Waktu terbuang untuk menjawab pertanyaan yang sama setiap hari." },
              { icon: BarChart, title: "Data Terabaikan", desc: "Data percakapan berharga tidak dimanfaatkan menjadi insight bisnis." }
            ].map((problem, i) => (
              <div key={i} className="bg-slate-50 border border-slate-100 rounded-2xl p-6 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mb-4">
                  <problem.icon size={24} />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{problem.title}</h3>
                <p className="text-gray-600 leading-relaxed">{problem.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SOLUTION SECTION */}
      <section id="solusi" className="py-24 bg-slate-900 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-indigo-600 rounded-full blur-[128px] opacity-20"></div>
        <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-96 h-96 bg-purple-600 rounded-full blur-[128px] opacity-20"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className={`text-3xl md:text-4xl font-bold leading-tight mb-6 ${exo2.className}`}>
                AI Customer Service yang Bekerja untuk Bisnis Anda
              </h2>
              <p className="text-slate-300 text-lg mb-8 leading-relaxed">
                NUSARA memungkinkan Anda membangun otak digital untuk bisnis Anda. Masukkan knowledge bisnis Anda, dan AI akan menggunakannya sebagai konteks untuk menjawab dengan akurat.
              </p>
              
              <ul className="space-y-4 mb-8">
                {[
                  "Tambahkan knowledge & konteks bisnis",
                  "Upload dokumen (Menu, Katalog, SOP)",
                  "Masukkan FAQ dan layanan",
                  "Integrasikan informasi produk"
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-slate-200">
                    <CheckCircle2 className="text-indigo-400" size={20} />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
              
              <div className="bg-white/10 border border-white/20 rounded-2xl p-6 backdrop-blur-sm">
                <p className="font-medium text-indigo-200 italic">
                  "The AI uses this business context to answer customers more accurately and naturally."
                </p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <Clock className="text-indigo-400 mb-4" size={32} />
                <h4 className="font-bold text-lg mb-2">Aktif 24/7</h4>
                <p className="text-slate-400 text-sm">Tidak pernah tidur, selalu siap melayani kapan saja.</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mt-8">
                <Zap className="text-indigo-400 mb-4" size={32} />
                <h4 className="font-bold text-lg mb-2">Fast Response</h4>
                <p className="text-slate-400 text-sm">Balasan instan membuat pelanggan tidak perlu menunggu.</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <BrainCircuit className="text-indigo-400 mb-4" size={32} />
                <h4 className="font-bold text-lg mb-2">Contextual</h4>
                <p className="text-slate-400 text-sm">Jawaban relevan sesuai gaya bahasa dan konteks bisnis.</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mt-8">
                <TrendingUp className="text-indigo-400 mb-4" size={32} />
                <h4 className="font-bold text-lg mb-2">Scalable</h4>
                <p className="text-slate-400 text-sm">Tangani ribuan chat serentak tanpa tambah admin.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="fitur" className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className={`text-3xl md:text-4xl font-bold text-gray-900 mb-4 ${exo2.className}`}>
              Fitur Utama NUSARA
            </h2>
            <p className="text-lg text-gray-600">Sistem komprehensif yang dirancang khusus untuk memajukan pelayanan bisnis Anda.</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: BrainCircuit, title: "Business Knowledge AI", desc: "AI memahami bisnis Anda melalui knowledge base yang dapat disesuaikan tanpa coding." },
              { icon: FileText, title: "Document Knowledge", desc: "Upload dokumen bisnis seperti menu, katalog, SOP, atau FAQ untuk langsung dipahami AI." },
              { icon: Users, title: "Human Fallback System", desc: "Ketika AI tidak yakin atau pelanggan mulai emosional, percakapan otomatis dialihkan ke admin manusia." },
              { icon: BarChart, title: "Conversation Insight Engine", desc: "Analisis percakapan pelanggan untuk menemukan kekurangan layanan, pola pertanyaan, dan peluang bisnis." },
              { icon: Target, title: "AI Improvement Recommendation", desc: "NUSARA membantu bisnis mengetahui bagian knowledge yang perlu diperbaiki berdasarkan percakapan nyata customer." },
              { icon: Smartphone, title: "Omnichannel Integration", desc: "Terhubung mulus dengan WhatsApp, website, dan platform komunikasi bisnis Anda lainnya." }
            ].map((feat, i) => (
              <div key={i} className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mb-6">
                  <feat.icon size={28} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feat.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS SECTION */}
      <section id="cara-kerja" className="py-24 bg-white border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className={`text-3xl md:text-4xl font-bold text-gray-900 mb-4 ${exo2.className}`}>
              Cara Kerja NUSARA
            </h2>
            <p className="text-lg text-gray-600">Mulai otomatisasi customer service Anda hanya dalam 5 langkah mudah.</p>
          </div>

          <div className="relative">
            <div className="hidden lg:block absolute top-12 left-0 right-0 h-0.5 bg-indigo-100 -z-10"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8">
              {[
                { step: "01", title: "Tambahkan Knowledge", desc: "Input data dan dokumen bisnis Anda." },
                { step: "02", title: "AI Melayani", desc: "AI mulai membalas customer secara otomatis." },
                { step: "03", title: "Human Fallback", desc: "Admin mengambil alih saat dibutuhkan." },
                { step: "04", title: "Analisis Data", desc: "AI menganalisis seluruh percakapan." },
                { step: "05", title: "Dapatkan Insight", desc: "Terima rekomendasi untuk perbaikan bisnis." }
              ].map((step, i) => (
                <div key={i} className="relative flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-full bg-white border-4 border-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-xl mb-6 shadow-sm">
                    {step.step}
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{step.title}</h3>
                  <p className="text-sm text-gray-600">{step.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* AI INSIGHT SECTION */}
      <section className="py-24 bg-indigo-50 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-indigo-100/50 relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-100 text-orange-700 text-sm font-medium mb-6">
                  <LightbulbIcon size={16} /> Business Intelligence
                </div>
                <h2 className={`text-3xl md:text-4xl font-bold text-gray-900 mb-6 ${exo2.className}`}>
                  Bukan Sekadar Membalas Chat
                </h2>
                <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                  NUSARA mengubah setiap percakapan pelanggan menjadi data intelijen bisnis yang berharga. Ketahui apa yang pelanggan Anda benar-benar inginkan.
                </p>
                
                <div className="space-y-4">
                  {[
                    "Pertanyaan yang paling sering muncul",
                    "Bagian layanan yang membingungkan customer",
                    "Titik kegagalan AI (Knowledge Gaps)",
                    "Rekomendasi penambahan knowledge",
                    "Kualitas pelayanan customer service"
                  ].map((point, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className="mt-1 w-5 h-5 rounded-full bg-indigo-100 flex items-center justify-center shrink-0">
                        <CheckCircle2 size={12} className="text-indigo-600" />
                      </div>
                      <p className="text-gray-700 font-medium">{point}</p>
                    </div>
                  ))}
                </div>
                
                <div className="mt-8 p-4 bg-indigo-600 rounded-xl text-white font-semibold flex items-center gap-3">
                  <TrendingUp size={24} className="text-indigo-200" />
                  "Setiap percakapan membantu bisnis Anda berkembang."
                </div>
              </div>
              
              <div className="relative">
                <div className="aspect-square md:aspect-auto md:h-[500px] bg-gradient-to-br from-slate-100 to-indigo-50 rounded-2xl border border-gray-200 shadow-inner flex items-center justify-center p-8 relative overflow-hidden">
                  <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
                  
                  {/* Mockup Dashboard UI */}
                  <div className="w-full bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-10 transform rotate-2 hover:rotate-0 transition-transform duration-500">
                    <div className="bg-gray-50 border-b border-gray-100 p-3 flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-400"></div>
                      <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                      <div className="w-3 h-3 rounded-full bg-green-400"></div>
                      <div className="text-xs text-gray-400 ml-2 font-mono">nusara-insight-engine</div>
                    </div>
                    <div className="p-6 space-y-4">
                      <div className="h-4 w-1/3 bg-indigo-100 rounded"></div>
                      <div className="h-8 w-2/3 bg-indigo-50 rounded"></div>
                      <div className="flex gap-4 pt-4">
                        <div className="flex-1 bg-green-50 p-4 rounded-lg border border-green-100">
                          <div className="h-3 w-1/2 bg-green-200 rounded mb-2"></div>
                          <div className="h-6 w-3/4 bg-green-300 rounded"></div>
                        </div>
                        <div className="flex-1 bg-amber-50 p-4 rounded-lg border border-amber-100">
                          <div className="h-3 w-1/2 bg-amber-200 rounded mb-2"></div>
                          <div className="h-6 w-3/4 bg-amber-300 rounded"></div>
                        </div>
                      </div>
                      <div className="h-24 w-full bg-slate-50 rounded-lg border border-slate-100 mt-4"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TARGET MARKET SECTION */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className={`text-3xl md:text-4xl font-bold text-gray-900 mb-6 ${exo2.className}`}>
            Dibangun untuk Bisnis Indonesia
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-16">
            Sistem yang dirancang agar mudah digunakan, scalable, affordable, dan relevan dengan gaya komunikasi masyarakat Indonesia.
          </p>

          <div className="flex flex-wrap justify-center gap-4 max-w-4xl mx-auto">
            {["UMKM", "Online Shop", "Food & Beverage", "Klinik & Salon", "Jasa Profesional", "Startup Kecil", "Bisnis Lokal"].map((market, i) => (
              <span key={i} className="px-6 py-3 bg-white border-2 border-slate-100 text-slate-700 rounded-full font-bold shadow-sm hover:border-indigo-200 hover:text-indigo-700 transition-colors cursor-default">
                {market}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* BENEFITS SECTION */}
      <section className="py-24 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className={`text-3xl md:text-4xl font-bold text-white mb-4 ${exo2.className}`}>
              Mengapa Memilih NUSARA?
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
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
              <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-6 flex items-start gap-4">
                <ShieldCheck className="text-indigo-400 shrink-0" size={24} />
                <span className="font-medium text-slate-200">{benefit}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="py-24 bg-gradient-to-br from-indigo-600 to-purple-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay"></div>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
          <h2 className={`text-4xl md:text-5xl font-bold text-white mb-6 ${exo2.className}`}>
            Bangun Customer Service yang Lebih Cerdas
          </h2>
          <p className="text-xl text-indigo-100 mb-10 leading-relaxed">
            Gunakan AI yang memahami bisnis Anda dan bantu pelanggan dengan lebih cepat, lebih cerdas, dan lebih efisien.
          </p>
          <Link href="/register" className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-white text-indigo-600 text-lg font-bold hover:bg-gray-50 transition-all shadow-xl hover:-translate-y-1">
            Mulai dengan NUSARA <ArrowRight size={20} />
          </Link>
          <p className="mt-6 text-sm text-indigo-200/80 font-medium tracking-wide">
            Siap digunakan untuk bisnis modern Indonesia.
          </p>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-white border-t border-gray-100 pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div className="md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <Image src="/Logo_NUSARA.png" alt="NUSARA Logo" width={28} height={28} className="object-contain" />
                <span className={`text-xl font-bold tracking-wide text-indigo-950 ${exo2.className}`}>
                  NUSARA
                </span>
              </div>
              <p className="text-gray-500 text-sm leading-relaxed mb-6">
                AI Customer Service untuk Bisnis Indonesia. Mengubah percakapan menjadi pengalaman pelanggan yang luar biasa.
              </p>
            </div>
            
            <div>
              <h4 className="font-bold text-gray-900 mb-4">Platform</h4>
              <ul className="space-y-3 text-sm text-gray-600">
                <li><Link href="#fitur" className="hover:text-indigo-600">Fitur</Link></li>
                <li><Link href="#solusi" className="hover:text-indigo-600">Solusi</Link></li>
                <li><Link href="#cara-kerja" className="hover:text-indigo-600">Cara Kerja</Link></li>
                <li><Link href="/pricing" className="hover:text-indigo-600">Harga</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold text-gray-900 mb-4">Perusahaan</h4>
              <ul className="space-y-3 text-sm text-gray-600">
                <li><Link href="/about" className="hover:text-indigo-600">Tentang Kami</Link></li>
                <li><Link href="/blog" className="hover:text-indigo-600">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-indigo-600">Hubungi Kami</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-bold text-gray-900 mb-4">Legal</h4>
              <ul className="space-y-3 text-sm text-gray-600">
                <li><Link href="/privacy" className="hover:text-indigo-600">Kebijakan Privasi</Link></li>
                <li><Link href="/terms" className="hover:text-indigo-600">Syarat & Ketentuan</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-100 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-400 text-sm">
              &copy; {new Date().getFullYear()} NUSARA. All rights reserved.
            </p>
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-gray-100 hover:bg-indigo-100 hover:text-indigo-600 flex items-center justify-center text-gray-400 cursor-pointer transition-colors">
                 IG
              </div>
              <div className="w-8 h-8 rounded-full bg-gray-100 hover:bg-indigo-100 hover:text-indigo-600 flex items-center justify-center text-gray-400 cursor-pointer transition-colors">
                 LI
              </div>
              <div className="w-8 h-8 rounded-full bg-gray-100 hover:bg-indigo-100 hover:text-indigo-600 flex items-center justify-center text-gray-400 cursor-pointer transition-colors">
                 TW
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function LightbulbIcon({ size }: { size?: number }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size || 24} height={size || 24} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.9 1.2 1.5 1.5 2.5" />
      <path d="M9 18h6" />
      <path d="M10 22h4" />
    </svg>
  );
}
