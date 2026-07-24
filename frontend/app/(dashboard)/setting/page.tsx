"use client";

import React, { useEffect, useState } from 'react';
import { 
  Building2, User, Phone, MapPin, FileText, Calendar, 
  Save, CheckCircle2, AlertCircle, RefreshCcw, Settings, Clock
} from 'lucide-react';

interface BusinessData {
  name: string;
  owner_name: string;
  phone_number: string;
  description: string;
  address: string;
  created_at: string;
  updated_at: string;
}

export default function SettingPage() {
  const [formData, setFormData] = useState<Partial<BusinessData>>({
    name: '',
    owner_name: '',
    phone_number: '',
    description: '',
    address: '',
  });

  const [initialData, setInitialData] = useState<BusinessData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const fetchBusinessData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/business/me');
      const json = await res.json();

      if (!res.ok) {
        throw new Error(json.message || 'Gagal mengambil data bisnis.');
      }

      if (json.data) {
        setInitialData(json.data);
        setFormData({
          name: json.data.name || '',
          owner_name: json.data.owner_name || '',
          phone_number: json.data.phone_number || '',
          description: json.data.description || '',
          address: json.data.address || '',
        });
      }
    } catch (err: any) {
      console.error("Fetch business error:", err);
      setError(err.message || 'Terjadi kesalahan saat memuat detail bisnis.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBusinessData();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const res = await fetch('/api/business/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const json = await res.json();

      if (!res.ok) {
        throw new Error(json.message || 'Gagal memperbarui detail bisnis.');
      }

      if (json.data) {
        setInitialData(json.data);
        setFormData({
          name: json.data.name || '',
          owner_name: json.data.owner_name || '',
          phone_number: json.data.phone_number || '',
          description: json.data.description || '',
          address: json.data.address || '',
        });
        setSuccessMessage('Detail bisnis berhasil diperbarui!');
        setTimeout(() => setSuccessMessage(null), 4000);
      }
    } catch (err: any) {
      console.error("Update business error:", err);
      setError(err.message || 'Gagal memperbarui detail bisnis.');
    } finally {
      setIsSaving(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '-';
    try {
      return new Date(dateString).toLocaleDateString('id-ID', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl">
              <Settings size={24} />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Pengaturan Bisnis</h1>
          </div>
          <p className="text-gray-500 mt-1 text-sm sm:text-base">
            Kelola detail dan informasi profil bisnis Anda yang digunakan oleh sistem AI NUSARA.
          </p>
        </div>

        <button
          onClick={fetchBusinessData}
          disabled={isLoading}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors shadow-xs disabled:opacity-50"
        >
          <RefreshCcw size={16} className={isLoading ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Alert Error / Success */}
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-3 text-rose-800">
          <AlertCircle size={20} className="text-rose-600 shrink-0 mt-0.5" />
          <div className="text-sm font-medium">{error}</div>
        </div>
      )}

      {successMessage && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-center gap-3 text-emerald-800">
          <CheckCircle2 size={20} className="text-emerald-600 shrink-0" />
          <div className="text-sm font-medium">{successMessage}</div>
        </div>
      )}

      {isLoading ? (
        <div className="bg-white rounded-2xl border border-gray-200 p-8 space-y-6">
          <div className="h-6 w-1/4 bg-gray-100 animate-pulse rounded-lg"></div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="h-12 bg-gray-100 animate-pulse rounded-xl"></div>
            <div className="h-12 bg-gray-100 animate-pulse rounded-xl"></div>
            <div className="h-12 bg-gray-100 animate-pulse rounded-xl"></div>
            <div className="h-12 bg-gray-100 animate-pulse rounded-xl"></div>
          </div>
          <div className="h-24 bg-gray-100 animate-pulse rounded-xl"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Main Form Edit */}
          <div className="lg:col-span-8 bg-white rounded-2xl border border-gray-200 shadow-xs p-6 sm:p-8">
            <div className="flex items-center gap-2 mb-6 border-b border-gray-100 pb-4">
              <Building2 size={20} className="text-indigo-600" />
              <h2 className="text-lg font-bold text-gray-900">Informasi & Profil Bisnis</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Nama Bisnis */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Nama Bisnis <span className="text-rose-500">*</span>
                </label>
                <div className="relative">
                  <Building2 size={18} className="absolute left-3.5 top-3 text-gray-400" />
                  <input
                    type="text"
                    name="name"
                    value={formData.name || ''}
                    onChange={handleChange}
                    placeholder="Masukkan nama bisnis Anda"
                    required
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                  />
                </div>
              </div>

              {/* Nama Pemilik & Telepon */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Nama Pemilik
                  </label>
                  <div className="relative">
                    <User size={18} className="absolute left-3.5 top-3 text-gray-400" />
                    <input
                      type="text"
                      name="owner_name"
                      value={formData.owner_name || ''}
                      onChange={handleChange}
                      placeholder="Nama pemilik bisnis"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Nomor Telepon
                  </label>
                  <div className="relative">
                    <Phone size={18} className="absolute left-3.5 top-3 text-gray-400" />
                    <input
                      type="text"
                      name="phone_number"
                      value={formData.phone_number || ''}
                      onChange={handleChange}
                      placeholder="Contoh: 081234567890"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                    />
                  </div>
                </div>
              </div>

              {/* Alamat Bisnis */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Alamat Bisnis
                </label>
                <div className="relative">
                  <MapPin size={18} className="absolute left-3.5 top-3 text-gray-400" />
                  <input
                    type="text"
                    name="address"
                    value={formData.address || ''}
                    onChange={handleChange}
                    placeholder="Alamat lengkap lokasi bisnis"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                  />
                </div>
              </div>

              {/* Deskripsi Bisnis */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Deskripsi Bisnis
                </label>
                <div className="relative">
                  <FileText size={18} className="absolute left-3.5 top-3.5 text-gray-400" />
                  <textarea
                    name="description"
                    rows={4}
                    value={formData.description || ''}
                    onChange={handleChange}
                    placeholder="Jelaskan produk, layanan, atau bidang bisnis Anda secara ringkas..."
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                  />
                </div>
                <p className="mt-1.5 text-xs text-gray-500">
                  Deskripsi ini dapat digunakan oleh AI sebagai referensi utama dalam memahami profil usaha Anda.
                </p>
              </div>

              {/* Submit Button */}
              <div className="pt-4 border-t border-gray-100 flex justify-end">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl transition-all shadow-md shadow-indigo-600/20 disabled:opacity-50 cursor-pointer"
                >
                  <Save size={18} className={isSaving ? 'animate-bounce' : ''} />
                  {isSaving ? 'Menyimpan...' : 'Simpan Perubahan'}
                </button>
              </div>
            </form>
          </div>

          {/* Sidebar Summary & Timeline Metadata */}
          <div className="lg:col-span-4 space-y-6">
            {/* Quick Preview Card */}
            <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-2xl p-6 shadow-md relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none"></div>
              
              <div className="w-10 h-10 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center text-indigo-300 mb-4">
                <Building2 size={20} />
              </div>

              <h3 className="text-lg font-bold text-white leading-tight">
                {formData.name || 'Nama Bisnis'}
              </h3>
              <p className="text-slate-300 text-xs mt-1">
                {formData.owner_name ? `Pemilik: ${formData.owner_name}` : 'Pemilik belum diisi'}
              </p>

              <div className="mt-4 pt-4 border-t border-white/10 space-y-2 text-xs text-slate-300">
                <div className="flex items-center gap-2">
                  <Phone size={14} className="text-indigo-400 shrink-0" />
                  <span>{formData.phone_number || 'Belum ada nomor telepon'}</span>
                </div>
                <div className="flex items-start gap-2">
                  <MapPin size={14} className="text-indigo-400 shrink-0 mt-0.5" />
                  <span className="line-clamp-2">{formData.address || 'Belum ada alamat'}</span>
                </div>
              </div>
            </div>

            {/* System Info Metadata */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6 space-y-4 shadow-xs">
              <h4 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-3 flex items-center gap-2">
                <Clock size={16} className="text-indigo-600" /> Informasi Riwayat System
              </h4>

              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-gray-400 block mb-0.5">Tanggal Dibuat</span>
                  <div className="font-semibold text-gray-700 flex items-center gap-1.5">
                    <Calendar size={14} className="text-gray-400" />
                    {formatDate(initialData?.created_at)}
                  </div>
                </div>

                <div>
                  <span className="text-gray-400 block mb-0.5">Terakhir Diperbarui</span>
                  <div className="font-semibold text-gray-700 flex items-center gap-1.5">
                    <Clock size={14} className="text-gray-400" />
                    {formatDate(initialData?.updated_at)}
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
