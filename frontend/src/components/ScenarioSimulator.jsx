import React, { useState } from 'react';
import { PlayCircle, AlertTriangle, Wind, Zap } from 'lucide-react';
import { api } from '../services/api';

export default function ScenarioSimulator({ onScenarioInjected }) {
  const [injecting, setInjecting] = useState(false);

  const handleInject = async (type) => {
    setInjecting(true);
    try {
      await api.injectScenario(type);
      onScenarioInjected();
    } catch (err) {
      console.error('Failed to inject scenario:', err);
    } finally {
      setInjecting(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-purple-500/10 text-purple-400 rounded-xl border border-purple-500/20">
          <PlayCircle className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">Multi-Crisis Scenario Sandbox</h3>
          <p className="text-[11px] text-slate-400">Inject real-time multi-hazard stress scenarios into the coordination grid</p>
        </div>
      </div>

      <div className="flex items-center gap-2.5">
        <button
          onClick={() => handleInject('severe_weather')}
          disabled={injecting}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 text-xs font-medium rounded-lg flex items-center gap-1.5 transition cursor-pointer"
        >
          <Wind className="w-3.5 h-3.5 text-teal-400" />
          <span>Category 4 Hurricane</span>
        </button>

        <button
          onClick={() => handleInject('earthquake_swarm')}
          disabled={injecting}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 text-xs font-medium rounded-lg flex items-center gap-1.5 transition cursor-pointer"
        >
          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
          <span>7.8 Magnitude Quake</span>
        </button>
      </div>
    </div>
  );
}
