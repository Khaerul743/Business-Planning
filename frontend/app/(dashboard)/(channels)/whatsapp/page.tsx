"use client";

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Smartphone, QrCode, CheckCircle2, AlertCircle, RefreshCw, 
  Unplug, Activity, Server, Hash, Clock, XCircle, LogOut, Link2
} from 'lucide-react';
import Image from 'next/image';

type SessionStatus = 
  | "loading"
  | "not_connected"
  | "pending_qr"
  | "authenticating"
  | "connected"
  | "disconnected"
  | "error";

interface WsEvent {
  id: string;
  time: string;
  event: string;
  message: string;
}

function useWhatsAppSession() {
  const [status, setStatus] = useState<SessionStatus>("loading");
  const [businessId, setBusinessId] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [qrCode, setQrCode] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<any>(null);
  const [events, setEvents] = useState<WsEvent[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const addEvent = useCallback((event: string, message: string) => {
    setEvents(prev => {
      const newEvent = {
        id: Math.random().toString(36).substring(7),
        time: new Date().toLocaleTimeString(),
        event,
        message
      };
      return [newEvent, ...prev].slice(0, 20); // Max 20 events
    });
  }, []);

  const connectWebSocket = useCallback((bId: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    const ws = new WebSocket(`${wsUrl}/ws/channels/${bId}`);

    ws.onopen = () => {
      addEvent("ws_open", "WebSocket connected to server");
    };

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        addEvent(payload.event, payload.message || `Received event: ${payload.event}`);

        if (payload.event === "qr") {
          setStatus("pending_qr");
          if (payload.qr_code) setQrCode(payload.qr_code);
        } else if (payload.event === "authenticated") {
          setStatus("authenticating");
          setQrCode(null);
        } else if (payload.event === "ready") {
          setStatus("connected");
          setQrCode(null);
          if (payload.metadata) setMetadata(payload.metadata);
          if (payload.session_id) setSessionId(payload.session_id);
        } else if (payload.event === "disconnected") {
          setStatus("disconnected");
        }
      } catch (err) {
        console.error("Failed to parse WS message", err);
      }
    };

    ws.onclose = () => {
      addEvent("ws_close", "WebSocket disconnected");
      // Auto reconnect socket
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = setTimeout(() => {
        connectWebSocket(bId);
      }, 3000);
    };

    ws.onerror = (err) => {
      console.error("WS error", err);
      addEvent("ws_error", "WebSocket encountered an error");
    };

    wsRef.current = ws;
  }, [addEvent]);

  const initData = useCallback(async () => {
    try {
      setStatus("loading");
      
      const bRes = await fetch("/api/business/me");
      const bData = await bRes.json();
      if (!bRes.ok || !bData.data?.id) {
        throw new Error(bData.message || "Failed to get business ID");
      }
      const bId = bData.data.id;
      setBusinessId(bId);

      const sRes = await fetch("/api/wa-session");
      const sData = await sRes.json();
      
      if (sRes.ok && sData.data) {
        const state = sData.data.status;
        if (state === "destroyed" || !state) {
          setStatus("not_connected");
        } else {
          setStatus(state);
          setSessionId(sData.data.session_id);
          if (sData.data.qr_code) setQrCode(sData.data.qr_code);
          if (sData.data.metadata) setMetadata(sData.data.metadata);
        }
      } else {
        setStatus("not_connected");
      }

      connectWebSocket(bId);
    } catch (err: any) {
      setStatus("error");
      setErrorMsg(err.message);
    }
  }, [connectWebSocket]);

  useEffect(() => {
    initData();

    return () => {
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
    };
  }, [initData]);

  const createSession = async () => {
    try {
      setStatus("loading");
      const res = await fetch("/api/wa-session", { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message);
      
      setStatus("pending_qr");
      if (data.data?.qr_code) setQrCode(data.data.qr_code);
      if (data.data?.session_id) setSessionId(data.data.session_id);
    } catch (err: any) {
      setStatus("error");
      setErrorMsg(err.message);
    }
  };

  const deleteSession = async () => {
    try {
      setStatus("loading");
      const res = await fetch("/api/wa-session", { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to disconnect");
      
      setStatus("not_connected");
      setSessionId(null);
      setMetadata(null);
      setQrCode(null);
      addEvent("api_delete", "Session deleted by user");
    } catch (err: any) {
      alert(err.message);
      initData(); // Revert state
    }
  };

  const reconnectSession = async () => {
    try {
      setStatus("loading");
      const res = await fetch("/api/wa-session/reconnect", { method: "POST" });
      if (!res.ok) throw new Error("Failed to reconnect");
      addEvent("api_reconnect", "Reconnect requested");
    } catch (err: any) {
      alert(err.message);
      initData(); // Revert state
    }
  };

  return {
    status,
    businessId,
    sessionId,
    qrCode,
    metadata,
    events,
    errorMsg,
    createSession,
    deleteSession,
    reconnectSession,
    initData
  };
}

export default function WhatsAppChannelsPage() {
  const {
    status,
    businessId,
    sessionId,
    qrCode,
    metadata,
    events,
    errorMsg,
    createSession,
    deleteSession,
    reconnectSession,
    initData
  } = useWhatsAppSession();

  const [isModalOpen, setIsModalOpen] = useState(false);

  // Auto close modal when connected
  useEffect(() => {
    if (status === "connected" && isModalOpen) {
      setTimeout(() => setIsModalOpen(false), 2000);
    }
  }, [status, isModalOpen]);

  const handleConnect = async () => {
    setIsModalOpen(true);
    await createSession();
  };

  const renderStatusBadge = () => {
    switch(status) {
      case "connected":
        return <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full flex items-center gap-1"><CheckCircle2 size={14}/> Connected</span>;
      case "disconnected":
        return <span className="px-3 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-full flex items-center gap-1"><Unplug size={14}/> Disconnected</span>;
      case "pending_qr":
        return <span className="px-3 py-1 bg-amber-100 text-amber-700 text-xs font-semibold rounded-full flex items-center gap-1"><QrCode size={14}/> Waiting QR</span>;
      case "authenticating":
        return <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full flex items-center gap-1"><RefreshCw size={14} className="animate-spin"/> Authenticating</span>;
      case "error":
        return <span className="px-3 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-full flex items-center gap-1"><AlertCircle size={14}/> Error</span>;
      case "loading":
        return <span className="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-semibold rounded-full flex items-center gap-1"><RefreshCw size={14} className="animate-spin"/> Loading</span>;
      default:
        return <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-semibold rounded-full">Not Connected</span>;
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 pb-12 pt-8">
      {/* 1. Header Section */}
      <div className="flex flex-col items-center text-center space-y-4 mb-8">
        <div className="w-16 h-16 bg-gradient-to-tr from-green-400 to-green-600 rounded-2xl flex items-center justify-center shadow-lg shadow-green-500/30 text-white">
          <Smartphone size={32} />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">WhatsApp Channels</h1>
          <p className="text-gray-500 text-lg max-w-lg mx-auto">
            Kelola koneksi WhatsApp bisnis Anda untuk mengaktifkan AI Customer Service.
          </p>
        </div>
      </div>

      {/* 2. Connection Status Card */}
      <div className="bg-white rounded-3xl border border-gray-200 shadow-xl shadow-gray-200/40 overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/80 backdrop-blur-sm">
          <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
            <Link2 size={20} className="text-gray-400" /> Status Koneksi
          </h2>
          {renderStatusBadge()}
        </div>
        
        <div className="p-8 md:p-12 relative overflow-hidden">
          {/* Subtle background glow based on status */}
          {status === "connected" && <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-green-400/10 rounded-full blur-3xl pointer-events-none"></div>}
          {status === "not_connected" && <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-gray-400/10 rounded-full blur-3xl pointer-events-none"></div>}
          {status === "error" || status === "disconnected" ? <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-red-400/10 rounded-full blur-3xl pointer-events-none"></div> : null}

          {status === "loading" && (
            <div className="flex flex-col items-center justify-center py-12 text-gray-400">
              <RefreshCw size={40} className="animate-spin mb-4 text-indigo-500" />
              <p className="text-lg font-medium">Memuat status koneksi...</p>
            </div>
          )}

          {status === "error" && (
            <div className="flex flex-col items-center justify-center py-8 text-center relative z-10">
              <div className="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mb-6 shadow-sm border border-red-100">
                <AlertCircle size={40} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Terjadi Kesalahan</h3>
              <p className="text-red-600 mb-8 max-w-md">{errorMsg || "Gagal memuat data sesi WhatsApp."}</p>
              <button onClick={initData} className="px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white font-semibold rounded-xl transition-all shadow-md flex items-center gap-2">
                <RefreshCw size={18} /> Coba Lagi
              </button>
            </div>
          )}

          {status === "not_connected" && (
            <div className="flex flex-col items-center justify-center py-8 text-center relative z-10">
              <div className="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mb-6 border border-gray-100 shadow-inner">
                <Unplug size={40} className="text-gray-400" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">WhatsApp Belum Terhubung</h3>
              <p className="text-gray-500 mb-10 max-w-md text-lg leading-relaxed">
                Tautkan perangkat WhatsApp Business Anda sekarang untuk mulai melayani pelanggan secara otomatis 24/7.
              </p>
              <button 
                onClick={handleConnect}
                className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white text-lg font-bold rounded-2xl transition-all shadow-lg shadow-green-600/30 flex items-center gap-3 hover:-translate-y-1"
              >
                <QrCode size={22} /> Connect WhatsApp
              </button>
            </div>
          )}

          {status === "pending_qr" && (
            <div className="flex flex-col items-center justify-center py-6 text-center relative z-10">
              <h3 className="text-xl font-bold text-gray-900 mb-2">Scan QR Code</h3>
              <p className="text-gray-500 mb-8 max-w-md">
                Buka WhatsApp di HP Anda &gt; Tautkan Perangkat &gt; Arahkan kamera ke QR Code di bawah.
              </p>
              <div className="p-6 bg-white border-2 border-dashed border-gray-200 rounded-3xl mb-8 shadow-sm">
                {qrCode ? (
                   <img src={qrCode} alt="WhatsApp QR Code" className="w-64 h-64 object-contain" />
                ) : (
                   <div className="w-64 h-64 flex items-center justify-center bg-gray-50 text-gray-400 rounded-2xl">
                     <RefreshCw className="animate-spin" size={32}/>
                   </div>
                )}
              </div>
              <button 
                onClick={deleteSession}
                className="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl transition-colors"
              >
                Batalkan
              </button>
            </div>
          )}

          {status === "authenticating" && (
            <div className="flex flex-col items-center justify-center py-16 text-center relative z-10">
              <RefreshCw size={48} className="animate-spin text-blue-500 mb-6" />
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Sedang Memverifikasi...</h3>
              <p className="text-gray-500 text-lg max-w-sm">Mohon tunggu sebentar sementara sistem mensinkronkan sesi WhatsApp Anda.</p>
            </div>
          )}

          {status === "connected" && (
            <div className="flex flex-col py-6 relative z-10">
              <div className="flex flex-col md:flex-row items-center gap-6 mb-10 p-8 bg-gradient-to-br from-green-50 to-emerald-50/30 border border-green-100/60 rounded-3xl shadow-sm">
                <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-md text-green-600 font-bold text-3xl">
                  {metadata?.display_name?.charAt(0) || "W"}
                </div>
                <div className="text-center md:text-left">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{metadata?.display_name || "WhatsApp Business"}</h3>
                  <div className="inline-flex items-center gap-2 px-3 py-1 bg-white rounded-lg border border-green-100">
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    <p className="text-green-700 font-bold font-mono tracking-wide">{metadata?.phone_number || "+62 xxx"}</p>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-center md:justify-end border-t border-gray-100 pt-8">
                <button 
                  onClick={deleteSession}
                  className="px-8 py-3.5 bg-red-50 hover:bg-red-100 text-red-600 font-bold rounded-xl transition-colors flex items-center gap-2 border border-red-100 hover:border-red-200"
                >
                  <LogOut size={20} /> Disconnect Device
                </button>
              </div>
            </div>
          )}

          {status === "disconnected" && (
            <div className="flex flex-col items-center justify-center py-8 text-center relative z-10">
              <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mb-6 border border-red-100 shadow-sm">
                <XCircle size={40} className="text-red-500" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Koneksi Terputus</h3>
              <p className="text-gray-500 mb-10 max-w-md text-lg">
                Sesi WhatsApp Anda terputus. Pastikan perangkat Anda menyala dan memiliki koneksi internet yang stabil.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button 
                  onClick={reconnectSession}
                  className="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-2xl transition-all shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 hover:-translate-y-1"
                >
                  <RefreshCw size={20} /> Reconnect
                </button>
                <button 
                  onClick={deleteSession}
                  className="px-8 py-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-2xl transition-colors"
                >
                  Reset Sesi
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 3. QR Modal (Onboarding Flow) */}
      {isModalOpen && (status === "pending_qr" || status === "authenticating" || status === "connected" || status === "loading") && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-[2rem] shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200 border border-white/20">
            <div className="p-8 text-center relative">
              {status !== "authenticating" && status !== "connected" && (
                <button 
                  onClick={() => setIsModalOpen(false)}
                  className="absolute top-6 right-6 text-gray-400 hover:text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-full p-1 transition-colors"
                >
                  <XCircle size={24} />
                </button>
              )}
              
              {status === "loading" && (
                <div className="py-12">
                  <div className="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6">
                    <RefreshCw size={40} className="animate-spin text-indigo-500" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">Menyiapkan Sesi...</h3>
                  <p className="text-gray-500 mt-2">Membuat sesi aman untuk perangkat Anda.</p>
                </div>
              )}

              {status === "pending_qr" && (
                <div className="py-2">
                  <div className="w-16 h-16 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 rotate-3">
                    <Smartphone size={32} />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Tautkan Perangkat</h3>
                  <p className="text-gray-500 text-sm mb-8 px-2">
                    Buka WhatsApp di HP Anda <br/> <span className="font-medium text-gray-700">Setelan &gt; Perangkat Tertaut &gt; Tautkan</span> <br/> dan arahkan kamera ke layar.
                  </p>
                  
                  <div className="inline-block p-4 bg-white border-2 border-gray-100 rounded-[2rem] shadow-sm mb-6 relative">
                    <div className="absolute -inset-1 bg-gradient-to-r from-green-400 to-indigo-500 rounded-[2.2rem] blur opacity-20 -z-10"></div>
                    {qrCode ? (
                       <img src={qrCode} alt="QR Code" className="w-56 h-56 object-contain rounded-xl" />
                    ) : (
                       <div className="w-56 h-56 flex items-center justify-center bg-gray-50 text-gray-400 rounded-xl">
                         <RefreshCw className="animate-spin" size={32}/>
                       </div>
                    )}
                  </div>
                  
                  <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-50 text-amber-700 rounded-full text-xs font-bold uppercase tracking-wider">
                    <RefreshCw size={14} className="animate-spin" /> QR Diperbarui Otomatis
                  </div>
                </div>
              )}

              {status === "authenticating" && (
                <div className="py-12">
                  <div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">
                    <RefreshCw size={40} className="animate-spin text-blue-500" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Memverifikasi...</h3>
                  <p className="text-gray-500">Kredensial sedang dicocokkan. Mohon tunggu beberapa detik.</p>
                </div>
              )}

              {status === "connected" && (
                <div className="py-12">
                  <div className="w-24 h-24 bg-gradient-to-tr from-green-400 to-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-green-500/40">
                    <CheckCircle2 size={48} />
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900 mb-3">Terhubung!</h3>
                  <p className="text-gray-500 text-lg">Sesi WhatsApp Anda telah aktif.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
