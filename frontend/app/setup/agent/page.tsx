"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Bot, Cpu, Mail, Smile, AlignLeft, ArrowRight, Loader2, CheckCircle2 } from 'lucide-react';
import Image from 'next/image';

type Tone = "profesional" | "casual" | "friendly" | "formal";
type LlmModel = "gpt-3.5-turbo" | "gpt-4o" | "gpt-4o-mini";

export default function AgentSetupPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    name: 'CS Nusara',
    llm_provider: 'openai',
    llm_model: 'gpt-4o-mini' as LlmModel,
    tone: 'friendly' as Tone,
    fallback_to_human: '',
    base_prompt: 'Anda adalah AI Customer Service yang ramah dan siap membantu pelanggan.',
    temperature: 0.7,
    enable_ai: true,
    include_memory: true
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg(null);

    try {
      const payload = {
        ...formData,
        temperature: parseFloat(formData.temperature.toString())
      };

      const res = await fetch('/api/agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || 'Gagal menyimpan konfigurasi AI Agent.');
      }

      setSuccess(true);
      // Wait a moment so they can see the success state
      setTimeout(() => {
        router.push('/dashboard');
      }, 1500);

    } catch (err: any) {
      setErrorMsg(err.message);
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <div className="w-24 h-24 bg-green-500 text-white rounded-full flex items-center justify-center mb-6 shadow-xl shadow-green-500/40 animate-in zoom-in duration-500">
          <CheckCircle2 size={48} />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Agent Selesai Dibuat!</h2>
        <p className="text-gray-500 text-lg">Mengarahkan Anda ke Dashboard utama...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 md:p-8">
      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-xl shadow-gray-200/50 overflow-hidden flex flex-col md:flex-row">
        
        {/* Left Side: Branding / Info */}
        <div className="w-full md:w-5/12 bg-indigo-950 p-10 text-white flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-full opacity-10">
            <div className="absolute top-[-20%] left-[-20%] w-[140%] h-[140%] bg-gradient-to-br from-indigo-400 to-transparent rounded-full blur-3xl"></div>
          </div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-12">
              <div className="bg-white p-2 rounded-xl">
                <Image src="/Logo.png" alt="Nusara Logo" width={32} height={32} className="object-contain" />
              </div>
              <span className="font-bold text-2xl tracking-wide font-mono">NUSARA</span>
            </div>

            <h1 className="text-4xl font-bold mb-6 leading-tight">Konfigurasi <span className="text-indigo-400">AI Agent</span></h1>
            <p className="text-indigo-200 text-lg leading-relaxed mb-8">
              Tentukan bagaimana AI Anda akan berinteraksi dan melayani pelanggan secara cerdas.
            </p>

            <ul className="space-y-4">
              <li className="flex items-center gap-3 text-indigo-100/50">
                <div className="w-8 h-8 rounded-full border border-indigo-800 flex items-center justify-center text-green-400">
                  <CheckCircle2 size={16} />
                </div>
                Setup Profil Bisnis
              </li>
              <li className="flex items-center gap-3 text-indigo-100">
                <div className="w-8 h-8 rounded-full bg-indigo-900 flex items-center justify-center text-indigo-400">2</div>
                Setup Agent Customer Service
              </li>
            </ul>
          </div>
        </div>

        {/* Right Side: Form */}
        <div className="w-full md:w-7/12 p-8 md:p-12 bg-white">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Profil Agent AI</h2>
          <p className="text-gray-500 mb-8">Pengaturan dasar asisten cerdas Anda.</p>

          {errorMsg && (
            <div className="p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl mb-6 text-sm font-medium">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Agent Name */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5">Nama AI Agent <span className="text-red-500">*</span></label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <Bot size={18} className="text-gray-400" />
                </div>
                <input 
                  type="text" 
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  placeholder="Misal: CS Cerdas"
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none"
                />
              </div>
            </div>

            {/* Model & Tone row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1.5">Model AI</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <Cpu size={18} className="text-gray-400" />
                  </div>
                  <select 
                    name="llm_model"
                    value={formData.llm_model}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none appearance-none"
                  >
                    <option value="gpt-4o-mini">GPT-4o Mini (Cepat)</option>
                    <option value="gpt-4o">GPT-4o (Akurat)</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1.5">Gaya Bahasa</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                    <Smile size={18} className="text-gray-400" />
                  </div>
                  <select 
                    name="tone"
                    value={formData.tone}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none appearance-none"
                  >
                    <option value="friendly">Friendly (Ramah)</option>
                    <option value="formal">Formal</option>
                    <option value="profesional">Profesional</option>
                    <option value="casual">Casual (Santai)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Fallback Email/Contact */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5">Kontak Human Fallback <span className="text-red-500">*</span></label>
              <p className="text-xs text-gray-500 mb-2">Email atau telepon Anda jika AI tidak bisa menjawab.</p>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <Mail size={18} className="text-gray-400" />
                </div>
                <input 
                  type="text" 
                  name="fallback_to_human"
                  value={formData.fallback_to_human}
                  onChange={handleChange}
                  required
                  placeholder="Misal: cs@bisnis.com"
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none"
                />
              </div>
            </div>

            {/* Base Prompt */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5">Instruksi Dasar (Prompt) <span className="text-red-500">*</span></label>
              <div className="relative">
                <div className="absolute top-3.5 left-3.5 pointer-events-none">
                  <AlignLeft size={18} className="text-gray-400" />
                </div>
                <textarea 
                  name="base_prompt"
                  value={formData.base_prompt}
                  onChange={handleChange}
                  required
                  rows={3}
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none resize-none"
                ></textarea>
              </div>
            </div>

            <div className="pt-4 flex gap-4">
              <button 
                type="button"
                onClick={() => router.push('/dashboard')}
                className="w-1/3 py-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-xl transition-all"
              >
                Nanti Saja
              </button>
              <button 
                type="submit" 
                disabled={isLoading}
                className="w-2/3 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <Loader2 size={20} className="animate-spin" /> Menyimpan...
                  </>
                ) : (
                  <>
                    Simpan & Mulai <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>
  );
}
