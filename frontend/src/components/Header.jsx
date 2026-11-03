import React, { useState, useEffect } from 'react';
import { ShieldAlert, Activity, Radio, Cpu, RefreshCw } from 'lucide-react';

export default function Header({ analytics, onRefresh, isRefreshing }) {
  const [time, setTime] = useState(new Date().toUTCString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4 z-40 shadow-md">
      <div className="flex items-center space-x-3">
        <div className="p-2.5 bg-gradient-to-br from-red-600 to-rose-700 rounded-xl shadow-lg shadow-rose-900/30 flex items-center justify-center">
          <ShieldAlert className="w-7 h-7 text-white animate-pulse" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              AEGIS-AI
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30 uppercase tracking-wider">
                Multi-Hazard Grid
              </span>
            </h1>
          </div>
          <p className="text-xs text-slate-400 font-medium">
            AI-Powered Multi-Disaster Monitoring & Intelligent Emergency Resource Coordination System
          </p>
        </div>
      </div>

      <div className="flex items-center gap-5 text-sm">
        {/* Readiness Index */}
        <div className="hidden md:flex items-center gap-2.5 px-3.5 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
          <Cpu className="w-4 h-4 text-emerald-400" />
          <span className="text-xs text-slate-400">Fleet Readiness:</span>
          <span className="text-xs font-bold text-emerald-400">
            {analytics?.readiness_index_pct ?? 100}%
          </span>
        </div>

        {/* Live Active Incident Count */}
        <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-rose-950/40 border border-rose-900/60 text-rose-300">
          <Activity className="w-4 h-4 text-rose-400 animate-spin" />
          <span className="text-xs font-semibold uppercase tracking-wider">Active Crises:</span>
          <span className="text-sm font-bold text-rose-200">
            {analytics?.active_disasters_count ?? 0}
          </span>
        </div>

        {/* Live UTC Clock & Telemetry Indicator */}
        <div className="hidden lg:flex items-center gap-2 text-xs text-slate-400 font-mono">
          <Radio className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span>{time}</span>
        </div>

        {/* Manual Refresh Button */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg border border-slate-700 transition flex items-center gap-1.5 text-xs font-medium cursor-pointer"
          title="Refresh All Telemetry & State"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span className="hidden sm:inline">Sync</span>
        </button>
      </div>
    </header>
  );
}
