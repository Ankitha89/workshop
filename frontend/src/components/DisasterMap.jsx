import React from 'react';
import { Flame, Waves, Activity, Wind, Biohazard, ShieldAlert, Navigation } from 'lucide-react';

const hazardIcons = {
  wildfire: Flame,
  flood: Waves,
  earthquake: Activity,
  hurricane: Wind,
  hazmat_spill: Biohazard,
  tsunami: Waves,
};

const hazardColors = {
  wildfire: 'border-amber-500/80 bg-amber-500/10 text-amber-400',
  flood: 'border-blue-500/80 bg-blue-500/10 text-blue-400',
  earthquake: 'border-red-500/80 bg-red-500/10 text-red-400',
  hurricane: 'border-teal-500/80 bg-teal-500/10 text-teal-400',
  hazmat_spill: 'border-emerald-500/80 bg-emerald-500/10 text-emerald-400',
};

export default function DisasterMap({ disasters, resources, selectedDisaster, onSelectDisaster }) {
  // Normalize US coordinates for clean tactical radar visualization
  // Lat range: 24 to 50, Lon range: -125 to -65
  const projectCoords = (lat, lon) => {
    const x = ((lon - (-125)) / (-65 - (-125))) * 100;
    const y = ((50 - lat) / (50 - 24)) * 100;
    return {
      left: `${Math.min(95, Math.max(5, x))}%`,
      top: `${Math.min(95, Math.max(5, y))}%`
    };
  };

  return (
    <div className="relative w-full h-[460px] bg-slate-950/90 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl flex flex-col">
      {/* Map Control Bar */}
      <div className="px-5 py-3 bg-slate-900/90 border-b border-slate-800/80 flex items-center justify-between text-xs z-10">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          <span className="font-semibold text-slate-200 tracking-wide uppercase">Tactical Geospatial Radar</span>
          <span className="text-slate-500 font-mono">CONUS Sector View</span>
        </div>
        <div className="flex items-center gap-4 text-slate-400">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Hazards ({disasters.length})</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Emergency Assets ({resources.length})</span>
        </div>
      </div>

      {/* Interactive Tactical Radar Grid */}
      <div className="relative flex-1 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 overflow-hidden">
        {/* Radar Ring Background Effect */}
        <div className="absolute inset-0 opacity-15 pointer-events-none flex items-center justify-center">
          <div className="w-[500px] h-[500px] rounded-full border border-cyan-500/30"></div>
          <div className="absolute w-[350px] h-[350px] rounded-full border border-cyan-500/20"></div>
          <div className="absolute w-[200px] h-[200px] rounded-full border border-cyan-500/10"></div>
          <div className="absolute w-full h-[1px] bg-cyan-500/20"></div>
          <div className="absolute h-full w-[1px] bg-cyan-500/20"></div>
        </div>

        {/* Resources / Assets Rendered on Tactical Map */}
        {resources.map((res) => {
          const pos = projectCoords(res.location.latitude, res.location.longitude);
          const isDeployed = res.status === 'deployed';
          return (
            <div
              key={res.id}
              style={{ left: pos.left, top: pos.top }}
              className="absolute -translate-x-1/2 -translate-y-1/2 group cursor-pointer z-10 transition-transform duration-300 hover:scale-125"
              title={`${res.name} (${res.agency}) - Status: ${res.status}`}
            >
              <div className={`p-1.5 rounded-full border ${isDeployed ? 'bg-cyan-500/30 border-cyan-400 text-cyan-300' : 'bg-slate-800 border-slate-600 text-slate-300'}`}>
                <Navigation className="w-3.5 h-3.5 rotate-45" />
              </div>
              <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-full mb-1 left-1/2 -translate-x-1/2 px-2 py-1 bg-slate-900/95 border border-slate-700 text-[11px] rounded whitespace-nowrap shadow-xl pointer-events-none text-slate-200 z-30">
                <p className="font-semibold text-cyan-400">{res.name}</p>
                <p className="text-slate-400">{res.agency}</p>
                <p className="text-slate-500 text-[9px] uppercase tracking-wider">Status: {res.status}</p>
              </div>
            </div>
          );
        })}

        {/* Disasters Rendered on Tactical Map */}
        {disasters.map((disaster) => {
          const pos = projectCoords(disaster.location.latitude, disaster.location.longitude);
          const Icon = hazardIcons[disaster.type] || ShieldAlert;
          const isSelected = selectedDisaster?.id === disaster.id;
          const colorClass = hazardColors[disaster.type] || 'border-rose-500 bg-rose-500/20 text-rose-400';

          return (
            <div
              key={disaster.id}
              style={{ left: pos.left, top: pos.top }}
              onClick={() => onSelectDisaster(disaster)}
              className={`absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer z-20 group transition-all duration-300 ${isSelected ? 'scale-125' : 'hover:scale-110'}`}
            >
              {/* Radius ring simulation */}
              <div
                style={{
                  width: `${Math.max(40, disaster.radius_km * 2)}px`,
                  height: `${Math.max(40, disaster.radius_km * 2)}px`
                }}
                className={`absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full border border-dashed pointer-events-none transition-all duration-700 ${isSelected ? 'border-rose-400/60 bg-rose-500/10 animate-pulse' : 'border-rose-500/20'}`}
              ></div>

              {/* Marker Icon */}
              <div className={`p-2.5 rounded-xl border backdrop-blur-md shadow-lg flex items-center justify-center transition-all ${colorClass} ${isSelected ? 'ring-2 ring-white ring-offset-2 ring-offset-slate-950 shadow-rose-900/50' : ''}`}>
                <Icon className="w-5 h-5 animate-pulse" />
              </div>

              {/* Label */}
              <div className="absolute top-full mt-1.5 left-1/2 -translate-x-1/2 bg-slate-900/90 border border-slate-700 px-2 py-0.5 rounded text-[10px] font-medium text-slate-200 whitespace-nowrap shadow-md pointer-events-none">
                {disaster.title.split(' ')[0]} (Risk: {disaster.risk_score})
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Disaster Quick HUD Bar */}
      {selectedDisaster && (
        <div className="px-5 py-2.5 bg-slate-900/95 border-t border-slate-800 flex items-center justify-between text-xs">
          <div className="flex items-center gap-3">
            <span className="font-bold text-rose-400">{selectedDisaster.title}</span>
            <span className="text-slate-400">| {selectedDisaster.location.region}</span>
            <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-semibold uppercase text-[10px]">
              Risk Score: {selectedDisaster.risk_score} / 100
            </span>
          </div>
          <div className="text-slate-400 text-[11px]">
            <span>Casualties Exposed: <strong className="text-white">{selectedDisaster.impact.estimated_casualties_at_risk.toLocaleString()}</strong></span>
            <span className="ml-4">Affected Radius: <strong className="text-white">{selectedDisaster.radius_km} km</strong></span>
          </div>
        </div>
      )}
    </div>
  );
}
