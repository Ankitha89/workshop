import React from 'react';
import { Truck, CheckCircle2, AlertOctagon, BatteryCharging, Shield, Activity } from 'lucide-react';

const statusBadges = {
  available: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
  deployed: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
  en_route: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
  maintenance: 'bg-slate-700 text-slate-400 border-slate-600',
};

export default function ResourceFleet({ resources }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
        <div className="flex items-center gap-2">
          <Truck className="w-4 h-4 text-cyan-400" />
          <h2 className="text-sm font-bold text-white tracking-wide uppercase">Emergency Resource Fleet</h2>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          Total Fleet: <strong className="text-white">{resources.length}</strong>
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {resources.map((res) => {
          const statusClass = statusBadges[res.status] || statusBadges.available;
          return (
            <div
              key={res.id}
              className="bg-slate-950/70 border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between hover:border-slate-700 transition"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <h4 className="text-xs font-bold text-white truncate" title={res.name}>
                    {res.name}
                  </h4>
                  <span className={`text-[9px] font-semibold uppercase px-2 py-0.5 rounded-full border ${statusClass}`}>
                    {res.status}
                  </span>
                </div>
                <p className="text-[10px] text-slate-400">{res.agency}</p>
                <p className="text-[10px] text-slate-500 mt-0.5">Base: {res.location.region}</p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-400">
                <span className="flex items-center gap-1">
                  <BatteryCharging className="w-3 h-3 text-emerald-400" />
                  <span>{res.fuel_or_battery_pct}% Reserves</span>
                </span>
                <span className="font-mono text-cyan-400">
                  {res.available_units}/{res.capacity_units} Units
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
