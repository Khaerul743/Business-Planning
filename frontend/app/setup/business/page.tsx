"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Building2, User, Phone, MapPin, AlignLeft, ArrowRight, Loader2, CheckCircle2 } from 'lucide-react';
import Image from 'next/image';

export default function BusinessSetupPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        owner_name: '',
        phone_number: '',
        description: '',
        address: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setErrorMsg(null);

        try {
            const res = await fetch('/api/business', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.message || 'Gagal menyimpan data bisnis.');
            }

            setSuccess(true);
            // Wait a moment so they can see the success state
            setTimeout(() => {
                router.push('/setup/agent');
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
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Setup Selesai!</h2>
                <p className="text-gray-500 text-lg">Mengarahkan Anda ke Setup Agent...</p>
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

                        <h1 className="text-4xl font-bold mb-6 leading-tight">Selamat Datang di <span className="text-indigo-400">NUSARA</span></h1>
                        <p className="text-indigo-200 text-lg leading-relaxed mb-8">
                            Lengkapi profil bisnis Anda untuk mulai mengotomatisasi layanan pelanggan dengan AI.
                        </p>

                        <ul className="space-y-4">
                            <li className="flex items-center gap-3 text-indigo-100">
                                <div className="w-8 h-8 rounded-full bg-indigo-900 flex items-center justify-center text-indigo-400">1</div>
                                Setup Profil Bisnis
                            </li>
                            <li className="flex items-center gap-3 text-indigo-100/50">
                                <div className="w-8 h-8 rounded-full border border-indigo-800 flex items-center justify-center">2</div>
                                Setup Agent Customer Service
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Right Side: Form */}
                <div className="w-full md:w-7/12 p-8 md:p-12 bg-white">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Informasi Bisnis</h2>
                    <p className="text-gray-500 mb-8">Data ini akan membantu AI memahami konteks bisnis Anda.</p>

                    {errorMsg && (
                        <div className="p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl mb-6 text-sm font-medium">
                            {errorMsg}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Business Name */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1.5">Nama Bisnis / Toko <span className="text-red-500">*</span></label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                                    <Building2 size={18} className="text-gray-400" />
                                </div>
                                <input
                                    type="text"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    required
                                    placeholder="Misal: Kopi Kenangan"
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none"
                                />
                            </div>
                        </div>

                        {/* Owner Name */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1.5">Nama Pemilik</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                                    <User size={18} className="text-gray-400" />
                                </div>
                                <input
                                    type="text"
                                    name="owner_name"
                                    value={formData.owner_name}
                                    onChange={handleChange}
                                    placeholder="Nama Anda"
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none"
                                />
                            </div>
                        </div>

                        {/* Phone Number */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1.5">Nomor Telepon Bisnis <span className="text-red-500">*</span></label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                                    <Phone size={18} className="text-gray-400" />
                                </div>
                                <input
                                    type="tel"
                                    name="phone_number"
                                    value={formData.phone_number}
                                    onChange={handleChange}
                                    required
                                    placeholder="Misal: 08123456789"
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none"
                                />
                            </div>
                        </div>

                        {/* Address */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1.5">Alamat Lengkap <span className="text-red-500">*</span></label>
                            <div className="relative">
                                <div className="absolute top-3.5 left-3.5 pointer-events-none">
                                    <MapPin size={18} className="text-gray-400" />
                                </div>
                                <textarea
                                    name="address"
                                    value={formData.address}
                                    onChange={handleChange}
                                    required
                                    rows={2}
                                    placeholder="Alamat kantor atau toko offline"
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none resize-none"
                                ></textarea>
                            </div>
                        </div>

                        {/* Description */}
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1.5">Deskripsi Singkat <span className="text-red-500">*</span></label>
                            <div className="relative">
                                <div className="absolute top-3.5 left-3.5 pointer-events-none">
                                    <AlignLeft size={18} className="text-gray-400" />
                                </div>
                                <textarea
                                    name="description"
                                    value={formData.description}
                                    onChange={handleChange}
                                    required
                                    rows={3}
                                    placeholder="Jelaskan secara singkat produk atau layanan yang Anda tawarkan..."
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors outline-none resize-none"
                                ></textarea>
                            </div>
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isLoading ? (
                                    <>
                                        <Loader2 size={20} className="animate-spin" /> Menyimpan...
                                    </>
                                ) : (
                                    <>
                                        Simpan & Lanjutkan <ArrowRight size={20} />
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
