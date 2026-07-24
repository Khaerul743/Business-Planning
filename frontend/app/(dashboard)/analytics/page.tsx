"use client";

import {
    MessageTrendHumanVsAiResponse,
    MessageUsageTrendResponse,
    SentimentAnalysisResponse,
    TokenUsageTrendResponse
} from '@/lib/services/analytic/types';
import { 
    AlertCircle, RefreshCcw, TrendingUp, Smile, Meh, Frown, 
    MessageSquare, HeartHandshake, ThumbsUp, ThumbsDown, MinusCircle 
} from 'lucide-react';
import { useEffect, useState } from 'react';
import {
    Bar, BarChart, CartesianGrid, Legend, Line, LineChart,
    ResponsiveContainer, Tooltip, XAxis, YAxis, PieChart, Pie, Cell
} from 'recharts';

export default function AnalyticPage() {
  const [tokenData, setTokenData] = useState<TokenUsageTrendResponse[]>([]);
  const [messageData, setMessageData] = useState<MessageUsageTrendResponse[]>([]);
  const [humanVsAiData, setHumanVsAiData] = useState<MessageTrendHumanVsAiResponse[]>([]);
  const [sentimentData, setSentimentData] = useState<SentimentAnalysisResponse | null>(null);
  
  const [humanVsAiPeriod, setHumanVsAiPeriod] = useState<string>('weekly');
  const [isHumanVsAiLoading, setIsHumanVsAiLoading] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const formatDataDate = (data: any[]) => data.map(item => ({
    ...item, 
    _formattedDate: item.date.includes(' ') 
      ? new Date(item.date.replace(' ', 'T')).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })
      : new Date(item.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  }));

  const fetchHumanVsAi = async (period = humanVsAiPeriod) => {
    setIsHumanVsAiLoading(true);
    try {
        const url = `/api/analytic/humanvsai?period=${period}`;

        const res = await fetch(url);
        const result = await res.json();
        if (!res.ok) throw new Error(result.message || "Failed to fetch Human vs AI Data");
        
        setHumanVsAiData(formatDataDate(result.data || []));
    } catch (err: any) {
        console.error("Human Vs AI fetch error:", err);
    } fontinally: {
        setIsHumanVsAiLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Fetch concurrently
      const [tokenRes, messageRes, sentimentRes] = await Promise.all([
        fetch('/api/analytic/token'),
        fetch('/api/analytic/message'),
        fetch('/api/analytic/sentiment-analysis')
      ]);

      const [tokenResult, messageResult, sentimentResult] = await Promise.all([
        tokenRes.json(),
        messageRes.json(),
        sentimentRes.json()
      ]);

      if (!tokenRes.ok) throw new Error(tokenResult.message || "Failed to fetch Token Usage Data");
      if (!messageRes.ok) throw new Error(messageResult.message || "Failed to fetch Message Trend Data");

      setTokenData(formatDataDate(tokenResult.data));
      setMessageData(formatDataDate(messageResult.data));

      if (sentimentRes.ok && sentimentResult.data) {
        setSentimentData(sentimentResult.data);
      }
      
      // Also fetch human vs ai independently to sync up
      await fetchHumanVsAi(humanVsAiPeriod);

    } catch (err: any) {
      console.error("Analytic fetch error:", err);
      setError(err.message || 'An unexpected error occurred while loading analytics.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-100 rounded-lg shadow-lg text-sm">
          <p className="font-semibold text-gray-800 mb-1">{label}</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
              <span className="text-gray-600 capitalize">{entry.name}:</span>
              <span className="font-semibold" style={{ color: entry.color }}>
                {entry.value.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  // Prepare Sentiment Pie Chart Data
  const sentimentChartData = sentimentData ? [
    { name: 'Positif', value: sentimentData.positif, color: '#10b981' },
    { name: 'Netral', value: sentimentData.netral, color: '#6366f1' },
    { name: 'Negatif', value: sentimentData.negatif, color: '#ef4444' },
  ] : [];

  const totalSentiment = sentimentData?.total || (
    (sentimentData?.positif || 0) + (sentimentData?.netral || 0) + (sentimentData?.negatif || 0)
  );

  return (
    <div className="max-w-7xl mx-auto space-y-8 pb-12">
      
      {/* Header Area */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
           <div className="flex items-center gap-3">
             <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl">
               <TrendingUp size={24} />
             </div>
             <h1 className="text-3xl font-bold text-gray-900">Analytics Hub</h1>
           </div>
           <p className="text-gray-500 mt-2 text-lg">Monitor token consumption, traffic volume, agent performance, and customer sentiment over time.</p>
        </div>
        
        <button 
          onClick={fetchAnalytics}
          disabled={isLoading}
          className="flex items-center gap-2 p-2.5 px-4 text-gray-600 hover:text-indigo-600 bg-white border border-gray-200 rounded-xl hover:border-indigo-200 transition-colors shadow-sm disabled:opacity-50"
        >
          <RefreshCcw size={18} className={isLoading ? 'animate-spin' : ''} />
          <span className="font-medium text-sm">Refresh Data</span>
        </button>
      </div>

      {error ? (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex flex-col items-center justify-center text-center min-h-[300px]">
           <AlertCircle size={48} className="text-red-400 mb-4" />
           <h3 className="text-xl font-semibold text-gray-900">Failed to load analytics</h3>
           <p className="text-red-600 mt-2 font-medium">{error}</p>
           <button 
             onClick={fetchAnalytics}
             className="mt-6 px-6 py-2 bg-white border border-red-200 text-red-600 hover:bg-red-50 rounded-lg shadow-sm font-medium transition-colors"
           >
             Try Again
           </button>
        </div>
      ) : isLoading ? (
        <div className="space-y-6">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <div className="h-80 bg-gray-100 animate-pulse rounded-2xl border border-gray-200"></div>
             <div className="h-80 bg-gray-100 animate-pulse rounded-2xl border border-gray-200"></div>
           </div>
           <div className="h-[400px] bg-gray-100 animate-pulse rounded-2xl border border-gray-200"></div>
           <div className="h-[350px] bg-gray-100 animate-pulse rounded-2xl border border-gray-200"></div>
        </div>
      ) : (
        <>
          {/* Top Row: Token Trend & Message Trend */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Tokens Chart */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col">
               <h3 className="text-lg font-bold text-gray-900 mb-1">Token Usage Trend</h3>
               <p className="text-sm text-gray-500 mb-6">Aggregate token consumption per day</p>
               
               <div className="flex-1 min-h-[250px] w-full">
                 <ResponsiveContainer width="100%" height="100%">
                   <LineChart data={tokenData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                     <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                     <XAxis dataKey="_formattedDate" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} dy={10} />
                     <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} />
                     <Tooltip content={<CustomTooltip />} />
                     <Line 
                        type="monotone" 
                        dataKey="token" 
                        name="Tokens"
                        stroke="#6366f1" 
                        strokeWidth={4}
                        dot={{ r: 4, fill: '#6366f1', strokeWidth: 2, stroke: '#fff' }}
                        activeDot={{ r: 6, strokeWidth: 0 }}
                      />
                   </LineChart>
                 </ResponsiveContainer>
               </div>
            </div>

            {/* Total Messages Chart */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col">
               <h3 className="text-lg font-bold text-gray-900 mb-1">Total Message Volume</h3>
               <p className="text-sm text-gray-500 mb-6">Daily inbound and outbound messages</p>
               
               <div className="flex-1 min-h-[250px] w-full">
                 <ResponsiveContainer width="100%" height="100%">
                   <LineChart data={messageData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                     <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                     <XAxis dataKey="_formattedDate" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} dy={10} />
                     <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} />
                     <Tooltip content={<CustomTooltip />} />
                     <Line 
                        type="monotone" 
                        dataKey="total_message" 
                        name="Messages"
                        stroke="#10b981" 
                        strokeWidth={4}
                        dot={{ r: 4, fill: '#10b981', strokeWidth: 2, stroke: '#fff' }}
                        activeDot={{ r: 6, strokeWidth: 0 }}
                      />
                   </LineChart>
                 </ResponsiveContainer>
               </div>
            </div>
            
          </div>

          {/* Sentiment Analysis Section */}
          {sentimentData && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 space-y-6">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <div className="p-1.5 bg-emerald-50 text-emerald-600 rounded-lg">
                    <HeartHandshake size={20} />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900">Sentiment Analysis</h3>
                </div>
                <p className="text-sm text-gray-500">Analisis sentimen pesan pelanggan dari percakapan AI.</p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                
                {/* Donut Chart Visual */}
                <div className="lg:col-span-5 flex flex-col items-center justify-center p-4 bg-slate-50/70 border border-slate-100 rounded-2xl">
                  <div className="w-full h-[220px] relative flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={sentimentChartData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={85}
                          paddingAngle={4}
                          dataKey="value"
                        >
                          {sentimentChartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                    <div className="absolute flex flex-col items-center justify-center text-center pointer-events-none">
                      <span className="text-2xl font-bold text-slate-800">{totalSentiment}</span>
                      <span className="text-xs font-medium text-slate-500">Total Chat</span>
                    </div>
                  </div>

                  {/* Legends & Percentages */}
                  <div className="grid grid-cols-3 gap-2 w-full pt-2 text-center">
                    <div className="p-2 bg-emerald-50/80 border border-emerald-100 rounded-xl">
                      <div className="text-xs font-semibold text-emerald-700">Positif</div>
                      <div className="text-base font-bold text-emerald-800">{sentimentData.positif}</div>
                      <div className="text-[10px] text-emerald-600">
                        {totalSentiment > 0 ? ((sentimentData.positif / totalSentiment) * 100).toFixed(0) : 0}%
                      </div>
                    </div>
                    <div className="p-2 bg-indigo-50/80 border border-indigo-100 rounded-xl">
                      <div className="text-xs font-semibold text-indigo-700">Netral</div>
                      <div className="text-base font-bold text-indigo-800">{sentimentData.netral}</div>
                      <div className="text-[10px] text-indigo-600">
                        {totalSentiment > 0 ? ((sentimentData.netral / totalSentiment) * 100).toFixed(0) : 0}%
                      </div>
                    </div>
                    <div className="p-2 bg-rose-50/80 border border-rose-100 rounded-xl">
                      <div className="text-xs font-semibold text-rose-700">Negatif</div>
                      <div className="text-base font-bold text-rose-800">{sentimentData.negatif}</div>
                      <div className="text-[10px] text-rose-600">
                        {totalSentiment > 0 ? ((sentimentData.negatif / totalSentiment) * 100).toFixed(0) : 0}%
                      </div>
                    </div>
                  </div>
                </div>

                {/* Sample Messages Preview */}
                <div className="lg:col-span-7 space-y-3">
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">Contoh Sample Percakapan Sentimen:</h4>

                  {/* Positif Sample */}
                  {sentimentData.samples?.positif && (
                    <div className="p-3.5 bg-emerald-50/50 border border-emerald-200/80 rounded-xl flex items-start gap-3">
                      <div className="p-1.5 bg-emerald-100 text-emerald-700 rounded-lg shrink-0 mt-0.5">
                        <Smile size={18} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-emerald-800 uppercase tracking-wide">Sentimen Positif</span>
                          <span className="text-[11px] font-semibold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full">
                            {sentimentData.positif} pesan
                          </span>
                        </div>
                        <p className="text-sm text-slate-700 italic mt-1 bg-white/70 p-2 rounded-lg border border-emerald-100">
                          "{sentimentData.samples.positif}"
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Netral Sample */}
                  {sentimentData.samples?.netral && (
                    <div className="p-3.5 bg-indigo-50/50 border border-indigo-200/80 rounded-xl flex items-start gap-3">
                      <div className="p-1.5 bg-indigo-100 text-indigo-700 rounded-lg shrink-0 mt-0.5">
                        <Meh size={18} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-indigo-800 uppercase tracking-wide">Sentimen Netral</span>
                          <span className="text-[11px] font-semibold bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded-full">
                            {sentimentData.netral} pesan
                          </span>
                        </div>
                        <p className="text-sm text-slate-700 italic mt-1 bg-white/70 p-2 rounded-lg border border-indigo-100">
                          "{sentimentData.samples.netral}"
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Negatif Sample */}
                  {sentimentData.samples?.negatif && (
                    <div className="p-3.5 bg-rose-50/50 border border-rose-200/80 rounded-xl flex items-start gap-3">
                      <div className="p-1.5 bg-rose-100 text-rose-700 rounded-lg shrink-0 mt-0.5">
                        <Frown size={18} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-rose-800 uppercase tracking-wide">Sentimen Negatif</span>
                          <span className="text-[11px] font-semibold bg-rose-100 text-rose-800 px-2 py-0.5 rounded-full">
                            {sentimentData.negatif} pesan
                          </span>
                        </div>
                        <p className="text-sm text-slate-700 italic mt-1 bg-white/70 p-2 rounded-lg border border-rose-100">
                          "{sentimentData.samples.negatif}"
                        </p>
                      </div>
                    </div>
                  )}
                </div>

              </div>
            </div>
          )}

          {/* Bottom Row: Human vs AI comparison */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
             <div className="mb-6 flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-1">Human vs AI Handled Messages</h3>
                  <p className="text-sm text-gray-500">Compare the volume of messages intercepted by the AI versus those handed off to humans.</p>
                </div>
                
                <div className="flex flex-col sm:flex-row items-center gap-2">
                  <select 
                    value={humanVsAiPeriod}
                    onChange={(e) => {
                        const newPeriod = e.target.value;
                        setHumanVsAiPeriod(newPeriod);
                        fetchHumanVsAi(newPeriod);
                    }}
                    className="border border-gray-200 bg-white rounded-lg px-3 py-1.5 text-sm text-gray-700 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 cursor-pointer"
                  >
                    <option value="day">Last 1 Day</option>
                    <option value="weekly">Last 7 Days</option>
                    <option value="monthly">Last 1 Month</option>
                  </select>
                  <button 
                    onClick={() => fetchHumanVsAi()}
                    disabled={isHumanVsAiLoading}
                    className="ml-2 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 p-1.5 rounded-lg transition-colors disabled:opacity-50"
                  >
                    <RefreshCcw size={16} className={isHumanVsAiLoading ? 'animate-spin' : ''} />
                  </button>
                </div>
             </div>
             
             <div className="w-full h-[350px]">
               <ResponsiveContainer width="100%" height="100%">
                 <BarChart data={humanVsAiData} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
                   <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                   <XAxis dataKey="_formattedDate" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} dy={10} />
                   <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6b7280' }} />
                   <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f9fafb' }} />
                   <Legend wrapperStyle={{ paddingTop: '20px' }} iconType="circle" />
                   
                   <Bar 
                     dataKey="ai" 
                     name="AI Agent" 
                     fill="#6366f1" 
                     radius={[4, 4, 0, 0]} 
                     barSize={32}
                   />
                   <Bar 
                     dataKey="human" 
                     name="Human Fallback" 
                     fill="#f59e0b" 
                     radius={[4, 4, 0, 0]} 
                     barSize={32}
                   />
                 </BarChart>
               </ResponsiveContainer>
             </div>
          </div>
        </>
      )}
    </div>
  );
}
