"use client";

import {
    AnalyticInsightResponse,
    CategoryPercentageResponse,
    KnowledgeGapResponse
} from '@/lib/services/analytic/types';
import {
    AlertCircle, Lightbulb, TrendingUp, TrendingDown,
    MessageSquare, Tag, Target, Zap, RefreshCcw, Activity, PieChart,
    Info, BookX, Sparkles, ArrowRight, ShieldAlert, CheckCircle2,
    Layers, BookOpenCheck, HelpCircle, AlertTriangle
} from 'lucide-react';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Link from 'next/link';

export default function InsightPage() {
    const [insightData, setInsightData] = useState<AnalyticInsightResponse | null>(null);
    const [categoryData, setCategoryData] = useState<CategoryPercentageResponse | null>(null);
    const [knowledgeGapData, setKnowledgeGapData] = useState<KnowledgeGapResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchInsights = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const [insightRes, categoryRes, gapRes] = await Promise.all([
                fetch('/api/analytic/insight'),
                fetch('/api/analytic/category-percentage'),
                fetch('/api/analytic/knowlage_gap')
            ]);

            const [insightResult, categoryResult, gapResult] = await Promise.all([
                insightRes.json(),
                categoryRes.json(),
                gapRes.json()
            ]);

            if (!insightRes.ok) throw new Error(insightResult.message || "Failed to fetch Insight Data");
            if (!categoryRes.ok) throw new Error(categoryResult.message || "Failed to fetch Category Percentage Data");
            if (!gapRes.ok) throw new Error(gapResult.message || "Failed to fetch Knowledge Gap Data");

            setInsightData(insightResult.data);
            setCategoryData(categoryResult.data);
            setKnowledgeGapData(gapResult.data);
        } catch (err: any) {
            console.error("Insight fetch error:", err);
            setError(err.message || 'An unexpected error occurred while loading insights.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchInsights();
    }, []);

    const parseChange = (changeStr: string) => {
        const isPositive = changeStr.startsWith('+');
        const isNegative = changeStr.startsWith('-');
        const value = changeStr.replace(/[\+\-]/g, '');
        return { isPositive, isNegative, value };
    };

    const getMaxTotal = () => {
        if (!categoryData || !categoryData.summary) return 1;
        return Math.max(...categoryData.summary.map(s => s.total), 1);
    };

    return (
        <div className="max-w-7xl mx-auto space-y-8 pb-12">
            {/* Header Area */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                   <div className="flex items-center gap-3">
                     <div className="p-2.5 bg-amber-50 text-amber-600 rounded-xl border border-amber-200/60 shadow-xs">
                       <Lightbulb size={24} />
                     </div>
                     <h1 className="text-3xl font-bold text-gray-900">AI Intelligence Insights</h1>
                   </div>
                   <p className="text-gray-500 mt-2 text-base sm:text-lg">Analisis otomatis perilaku pelanggan, pola percakapan, dan rekomendasi AI untuk bisnis Anda.</p>
                </div>
                
                <button 
                  onClick={fetchInsights}
                  disabled={isLoading}
                  className="inline-flex items-center gap-2 p-2.5 px-4 text-gray-700 hover:text-indigo-600 bg-white border border-gray-200 rounded-xl hover:border-indigo-200 transition-colors shadow-xs disabled:opacity-50 font-medium text-sm"
                >
                  <RefreshCcw size={16} className={isLoading ? 'animate-spin' : ''} />
                  <span>Refresh Insights</span>
                </button>
            </div>

            {error ? (
                <div className="bg-red-50 border border-red-200 rounded-2xl p-8 flex flex-col items-center justify-center text-center min-h-[300px]">
                   <AlertCircle size={48} className="text-red-400 mb-4" />
                   <h3 className="text-xl font-semibold text-gray-900">Gagal Memuat Insight</h3>
                   <p className="text-red-600 mt-2 font-medium">{error}</p>
                   <button 
                     onClick={fetchInsights}
                     className="mt-6 px-6 py-2 bg-white border border-red-200 text-red-600 hover:bg-red-50 rounded-xl shadow-xs font-medium transition-colors"
                   >
                     Coba Lagi
                   </button>
                </div>
            ) : isLoading ? (
                <div className="space-y-6">
                   <div className="h-64 bg-gray-100 animate-pulse rounded-3xl border border-gray-200"></div>
                   <div className="h-80 bg-gray-100 animate-pulse rounded-3xl border border-gray-200"></div>
                   <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                       <div className="h-80 bg-gray-100 animate-pulse rounded-3xl border border-gray-200"></div>
                       <div className="h-80 bg-gray-100 animate-pulse rounded-3xl border border-gray-200"></div>
                   </div>
                </div>
            ) : (
                <div className="space-y-8">
                    {/* Executive Summary & Business Insight */}
                    {insightData && (
                        <div className="bg-white rounded-3xl shadow-sm border border-slate-200/80 overflow-hidden">
                            {/* Banner Overview Header */}
                            <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-8 relative overflow-hidden">
                                <div className="absolute -top-12 -right-12 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
                                <div className="relative z-10">
                                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-semibold mb-4">
                                        <Sparkles size={14} /> Executive AI Intelligence Report
                                    </div>
                                    <h2 className="text-2xl sm:text-3xl font-bold mb-3 text-white flex items-center gap-2.5">
                                        Executive Summary
                                    </h2>
                                    <div className="text-slate-200 text-sm sm:text-base leading-relaxed prose prose-invert max-w-none prose-p:my-1">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{insightData.overview}</ReactMarkdown>
                                    </div>
                                </div>
                            </div>
                            
                            {/* 4 Cards Grid */}
                            <div className="p-6 sm:p-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                {/* Card 1: Key Insight */}
                                <div className="bg-blue-50/50 hover:bg-blue-50 border border-blue-100 hover:border-blue-300 rounded-2xl p-6 transition-all duration-300 shadow-xs flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center shadow-xs shrink-0">
                                                <Activity size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-blue-600">Temuan Utama</span>
                                                <h4 className="font-bold text-gray-900 text-base">Key Insight</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{insightData.insight}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Card 2: Reasoning */}
                                <div className="bg-amber-50/50 hover:bg-amber-50 border border-amber-100 hover:border-amber-300 rounded-2xl p-6 transition-all duration-300 shadow-xs flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shadow-xs shrink-0">
                                                <HelpCircle size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-amber-600">Latar Belakang</span>
                                                <h4 className="font-bold text-gray-900 text-base">Reasoning</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{insightData.reason}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Card 3: Impact */}
                                <div className="bg-emerald-50/50 hover:bg-emerald-50 border border-emerald-100 hover:border-emerald-300 rounded-2xl p-6 transition-all duration-300 shadow-xs flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-xs shrink-0">
                                                <TrendingUp size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-600">Estimasi Efek</span>
                                                <h4 className="font-bold text-gray-900 text-base">Business Impact</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{insightData.impact}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Card 4: Recommendation */}
                                <div className="bg-purple-50/50 hover:bg-purple-50 border border-purple-100 hover:border-purple-300 rounded-2xl p-6 transition-all duration-300 shadow-xs flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-purple-600 text-white flex items-center justify-center shadow-xs shrink-0">
                                                <Zap size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-purple-600">Langkah Strategis</span>
                                                <h4 className="font-bold text-gray-900 text-base">Recommendation</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none whitespace-pre-line">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{insightData.recommendation}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Knowledge Gap Insight Section */}
                    {knowledgeGapData && (
                        <div className="bg-gradient-to-br from-rose-50/60 via-amber-50/30 to-white rounded-3xl border border-rose-200/80 shadow-md p-6 sm:p-8 space-y-6 relative overflow-hidden">
                            <div className="absolute top-0 right-0 -mt-12 -mr-12 w-64 h-64 bg-rose-400/10 rounded-full blur-3xl pointer-events-none"></div>

                            {/* Header Row */}
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-rose-200/60 relative z-10">
                                <div>
                                    <div className="flex items-center gap-2 mb-2">
                                        <span className="px-3 py-1 rounded-full bg-rose-100 text-rose-700 text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 border border-rose-200">
                                            <AlertTriangle size={14} className="text-rose-600" /> Perhatian Diperlukan
                                        </span>
                                        <div className="group relative flex items-center cursor-help">
                                            <Info size={16} className="text-slate-400 hover:text-slate-600 transition-colors" />
                                            <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-72 bg-slate-900 text-white text-xs p-3 rounded-xl shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-20 font-normal">
                                                Knowledge Gap menunjukkan informasi penting bisnis yang belum diketahui oleh AI Customer Service. Melengkapi data ini membuat AI makin responsif & akurat.
                                                <div className="absolute right-0 left-0 -bottom-1 mx-auto w-2 h-2 bg-slate-900 rotate-45 transform"></div>
                                            </div>
                                        </div>
                                    </div>
                                    <h2 className="text-2xl font-extrabold text-slate-900 flex items-center gap-2.5">
                                        <BookX className="text-rose-600" size={26} />
                                        Knowledge Gap Insight
                                    </h2>
                                    <p className="text-slate-600 text-sm sm:text-base mt-1.5 max-w-2xl leading-relaxed">
                                        AI mendeteksi beberapa pertanyaan pelanggan yang belum ada pada dokumentasi bisnis Anda. Tambahkan informasi ini untuk meningkatkan akurasi balasan.
                                    </p>
                                </div>

                                <div className="shrink-0">
                                    <Link 
                                        href="/business" 
                                        className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-2xl transition-all shadow-md shadow-blue-600/20 hover:shadow-lg"
                                    >
                                        <BookOpenCheck size={18} />
                                        <span>Tambah Knowledge Baru</span>
                                        <ArrowRight size={16} />
                                    </Link>
                                </div>
                            </div>
                            
                            {/* 3 Detail Cards */}
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
                                {/* Card 1: Defisit Insight */}
                                <div className="bg-white rounded-2xl p-6 border border-rose-200/80 shadow-xs hover:shadow-md hover:border-rose-300 transition-all flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-rose-100 border border-rose-200 text-rose-600 flex items-center justify-center shrink-0">
                                                <ShieldAlert size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-rose-600">Temuan Gap</span>
                                                <h4 className="font-bold text-slate-900 text-base">Insight Kekurangan</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{knowledgeGapData.insight}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Card 2: Gap Pengetahuan Teridentifikasi */}
                                <div className="bg-white rounded-2xl p-6 border border-amber-200/80 shadow-xs hover:shadow-md hover:border-amber-300 transition-all flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-amber-100 border border-amber-200 text-amber-700 flex items-center justify-center shrink-0">
                                                <Layers size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-amber-600">Informasi Kosong</span>
                                                <h4 className="font-bold text-slate-900 text-base">Gap Teridentifikasi</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{knowledgeGapData.knowladge_business_gap}</ReactMarkdown>
                                        </div>
                                    </div>
                                </div>

                                {/* Card 3: Tindakan Perbaikan Disarankan */}
                                <div className="bg-white rounded-2xl p-6 border border-indigo-200/80 shadow-xs hover:shadow-md hover:border-indigo-300 transition-all flex flex-col justify-between">
                                    <div>
                                        <div className="flex items-center gap-3 mb-4">
                                            <div className="w-10 h-10 rounded-xl bg-indigo-100 border border-indigo-200 text-indigo-600 flex items-center justify-center shrink-0">
                                                <Zap size={20} />
                                            </div>
                                            <div>
                                                <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600">Solusi AI</span>
                                                <h4 className="font-bold text-slate-900 text-base">Rekomendasi Aksi</h4>
                                            </div>
                                        </div>
                                        <div className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none whitespace-pre-line">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{knowledgeGapData.recommendation}</ReactMarkdown>
                                        </div>
                                    </div>

                                    <div className="mt-5 pt-4 border-t border-slate-100">
                                        <Link 
                                            href="/business" 
                                            className="text-xs font-bold text-indigo-600 hover:text-indigo-700 inline-flex items-center gap-1 group"
                                        >
                                            <span>Buka Business Knowledge</span>
                                            <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Bottom Section: Category Distribution & Sample Messages */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Categories Summary */}
                        {categoryData && categoryData.summary && (
                            <div className="bg-white rounded-3xl shadow-sm border border-slate-200/80 p-6 sm:p-8">
                                <h3 className="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2.5">
                                    <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
                                        <PieChart size={20} />
                                    </div>
                                    Category Distribution
                                </h3>
                                <p className="text-sm text-slate-500 mb-6">Distribusi volume topik dan tren perubahan pertanyaan pelanggan.</p>
                                
                                <div className="space-y-4">
                                    {categoryData.summary.map((item, idx) => {
                                        const change = parseChange(item.change);
                                        const percentage = (item.total / getMaxTotal()) * 100;
                                        return (
                                            <div key={idx} className="group p-4 rounded-2xl border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/30 transition-all">
                                                <div className="flex justify-between items-center mb-2.5">
                                                    <div className="flex items-center gap-2">
                                                        <Tag size={16} className="text-slate-400 group-hover:text-indigo-600 transition-colors" />
                                                        <span className="font-bold text-slate-800 capitalize text-sm">{item.category_type}</span>
                                                    </div>
                                                    <div className="flex items-center gap-3">
                                                        <span className="text-base font-extrabold text-slate-900">{item.total}</span>
                                                        <div className={`flex items-center text-xs font-semibold px-2.5 py-1 rounded-full ${
                                                            change.isPositive ? 'bg-emerald-100 text-emerald-700' : 
                                                            change.isNegative ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-700'
                                                        }`}>
                                                            {change.isPositive ? <TrendingUp size={12} className="mr-1" /> : 
                                                             change.isNegative ? <TrendingDown size={12} className="mr-1" /> : null}
                                                            {item.change}
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                                                    <div 
                                                        className="bg-gradient-to-r from-blue-500 to-indigo-600 h-full rounded-full transition-all duration-1000 ease-out" 
                                                        style={{ width: `${Math.max(percentage, 6)}%` }}
                                                    />
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {/* Sample Messages */}
                        {categoryData && categoryData.samples && (
                            <div className="bg-white rounded-3xl shadow-sm border border-slate-200/80 p-6 sm:p-8 flex flex-col h-full max-h-[620px]">
                                <h3 className="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2.5">
                                    <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
                                        <MessageSquare size={20} />
                                    </div>
                                    Sample Inquiries
                                </h3>
                                <p className="text-sm text-slate-500 mb-6">Contoh pertanyaan nyata pelanggan berdasarkan kategori topik.</p>
                                
                                <div className="flex-1 overflow-y-auto pr-2 space-y-6 scrollbar-thin scrollbar-thumb-slate-200">
                                    {categoryData.samples.map((sample, idx) => (
                                        <div key={idx} className="space-y-3">
                                            <h4 className="text-xs font-bold text-indigo-700 uppercase tracking-wider px-3 py-1 bg-indigo-50 rounded-lg w-fit border border-indigo-100">
                                                {sample.category_type}
                                            </h4>
                                            <div className="flex flex-col gap-2 pl-1">
                                                {sample.sample_messages.map((msg, mIdx) => (
                                                    <div key={mIdx} className="bg-slate-50 border border-slate-200/80 text-slate-800 text-sm px-4 py-3 rounded-2xl rounded-tl-xs max-w-[95%] shadow-2xs leading-relaxed">
                                                        "{msg}"
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
