import React, { useState } from 'react';
import { Flame, Waves, Activity, Wind, Biohazard, AlertTriangle, Filter, Users, ShieldAlert } from 'lucide-react';

const hazardIcons = {
  wildfire: Flame,
  flood: Waves,
  earthquake: Activity,
  hurricane: Wind,
  hazmat_spill: Biohazard,
  tsunami: Waves,
};

const severityStyles = {
  catastrophic: 'bg-rose-500/20 text-rose-300 border-rose-500/50',
  critical: 'bg-red-500/20 text-red-300 border-red-500/50',
  high: 'bg-orange-500/20 text-orange-300 border-orange-500/50',
  moderate: 'bg-amber-500/20 text-amber-300 border-amber-500/50',
  low: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50',
};

export default function DisasterFeed({ disasters, selectedDisaster, onSelectDisaster }) {
  const [filterType, setFilterType] = useState('all');

  const filteredDisasters = filterType === 'all'
    ? disasters
    : disasters.filter(d => d.type === filterType);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[560px] shadow-xl overflow-hidden">
      {/* Feed Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-rose-400" />
          <h2 className="text-sm font-bold text-white tracking-wide uppercase">Active Incident Feed</h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            {filteredDisasters.length}
          </span>
        </div>

        {/* Filter Dropdown */}
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <Filter className="w-3.5 h-3.5" />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1 text-xs focus:outline-none focus:border-rose-500"
          >
            <option value="all">All Hazards</option>
            <option value="wildfire">Wildfire</option>
            <option value="earthquake">Earthquake</option>
            <option value="flood">Flood</option>
            <option value="hazmat_spill">Hazmat Spill</option>
            <option value="hurricane">Hurricane</option>
          </select>
        </div>
      </div>

      {/* Incident List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
        {filteredDisasters.map((d) => {
          const Icon = hazardIcons[d.type] || ShieldAlert;
          const isSelected = selectedDisaster?.id === d.id;
          const severityClass = severityStyles[d.severity] || severityStyles.high;

          return (
            <div
              key={d.id}
              onClick={() => onSelectDisaster(d)}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                isSelected
                  ? 'bg-slate-800/90 border-rose-500 ring-1 ring-rose-500/50 shadow-lg shadow-rose-950/40'
                  : 'bg-slate-950/60 border-slate-800 hover:border-slate-700 hover:bg-slate-800/40'
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-lg bg-slate-800 border border-slate-700 text-rose-400">
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-white leading-tight">{d.title}</h3>
                    <p className="text-[11px] text-slate-400">{d.location.region} • {d.location.address}</p>
                  </div>
                </div>

                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase ${severityClass}`}>
                  {d.severity}
                </span>
              </div>

              {/* Metrics & Capabilities preview */}
              <div className="mt-2.5 grid grid-cols-2 gap-2 text-[11px] bg-slate-900/60 p-2 rounded-lg border border-slate-800/60">
                <div className="flex items-center gap-1.5 text-slate-300">
                  <Users className="w-3.5 h-3.5 text-slate-400" />
                  <span>Casualties: <strong className="text-white">{d.impact.estimated_casualties_at_risk.toLocaleString()}</strong></span>
                </div>
                <div className="flex items-center justify-end gap-1.5 text-slate-300">
                  <span className="text-[10px] text-slate-400 uppercase">Risk:</span>
                  <span className="font-bold text-rose-400">{d.risk_score}</span>
                  <span className="text-[10px] text-slate-500">/ 100</span>
                </div>
              </div>

              {/* Assigned Resources badge count */}
              <div className="mt-2 flex items-center justify-between text-[10px]">
                <span className="text-slate-400">
                  Units Assigned: <span className="text-cyan-400 font-semibold">{d.assigned_resources?.length || 0}</span>
                </span>
                <span className="text-xs text-rose-400 font-semibold hover:underline">
                  {isSelected ? 'Targeted' : 'Inspect & Coordinate →'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
