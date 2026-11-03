import React from 'react';
import { BarChart3, Users, Home, ShieldCheck, Flame, Zap } from 'lucide-react';

export default function AnalyticsPanel({ analytics }) {
  if (!analytics) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {/* Total Casualties at Risk */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3.5">
        <div className="p-3 bg-rose-500/10 text-rose-400 rounded-xl border border-rose-500/20">
          <Users className="w-5 h-5" />
        </div>
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Casualties at Risk</span>
          <h3 className="text-xl font-bold text-white mt-0.5">
            {analytics.total_casualties_at_risk?.toLocaleString() || 0}
          </h3>
        </div>
      </div>

      {/* Threatened Structures */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3.5">
        <div className="p-3 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/20">
          <Home className="w-5 h-5" />
        </div>
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Structures Threatened</span>
          <h3 className="text-xl font-bold text-white mt-0.5">
            {analytics.total_structures_threatened?.toLocaleString() || 0}
          </h3>
        </div>
      </div>

      {/* Deployed Emergency Units */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3.5">
        <div className="p-3 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20">
          <Zap className="w-5 h-5" />
        </div>
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Active Deployments</span>
          <h3 className="text-xl font-bold text-cyan-400 mt-0.5">
            {analytics.resources_summary?.deployed || 0} Units
          </h3>
        </div>
      </div>

      {/* Readiness Rating */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3.5">
        <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Reserve Readiness</span>
          <h3 className="text-xl font-bold text-emerald-400 mt-0.5">
            {analytics.readiness_index_pct || 100}%
          </h3>
        </div>
      </div>
    </div>
  );
}
