import React, { useState, useEffect } from 'react';
import { Cpu, Send, CheckCircle2, Clock, MapPin, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export default function AiDispatchConsole({ selectedDisaster, onDispatchSuccess }) {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedResourceIds, setSelectedResourceIds] = useState([]);
  const [dispatching, setDispatching] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  useEffect(() => {
    if (!selectedDisaster) {
      setRecommendations(null);
      setSelectedResourceIds([]);
      return;
    }

    const fetchRecommendations = async () => {
      setLoading(true);
      setStatusMessage(null);
      try {
        const data = await api.getRecommendations(selectedDisaster.id);
        setRecommendations(data);
        // Pre-select top 2 recommendations
        if (data.recommended_allocations && data.recommended_allocations.length > 0) {
          setSelectedResourceIds(data.recommended_allocations.slice(0, 2).map(r => r.resource_id));
        } else {
          setSelectedResourceIds([]);
        }
      } catch (err) {
        console.error('Error fetching recommendations:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [selectedDisaster]);

  const handleToggleResource = (id) => {
    setSelectedResourceIds(prev =>
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  const handleDispatch = async () => {
    if (!selectedDisaster || selectedResourceIds.length === 0) return;
    setDispatching(true);
    setStatusMessage(null);
    try {
      const res = await api.dispatchResources(
        selectedDisaster.id,
        selectedResourceIds,
        `Coordinated AI tactical dispatch for ${selectedDisaster.title}`
      );
      setStatusMessage({ type: 'success', text: res.message });
      onDispatchSuccess();
      // Re-fetch recommendations after state changes
      const updated = await api.getRecommendations(selectedDisaster.id);
      setRecommendations(updated);
      setSelectedResourceIds([]);
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.message || 'Dispatch failed' });
    } finally {
      setDispatching(false);
    }
  };

  if (!selectedDisaster) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center text-center h-[560px] text-slate-400 shadow-xl">
        <Cpu className="w-12 h-12 text-slate-600 mb-3 animate-pulse" />
        <h3 className="text-base font-semibold text-slate-200">No Disaster Incident Selected</h3>
        <p className="text-xs text-slate-500 max-w-xs mt-1">
          Select an active hazard from the radar map or incident feed to calculate AI multi-criteria resource allocations.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[560px] shadow-xl overflow-hidden">
      {/* Console Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-rose-500/20 text-rose-400 rounded-lg border border-rose-500/30">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-white tracking-wide uppercase">AI Resource Allocation Engine</h2>
            <p className="text-[11px] text-slate-400">Target: <strong className="text-slate-200">{selectedDisaster.title}</strong></p>
          </div>
        </div>

        {recommendations && (
          <span className="text-[10px] font-bold px-2.5 py-1 rounded bg-rose-950/60 text-rose-300 border border-rose-800/60 uppercase">
            {recommendations.urgency_level}
          </span>
        )}
      </div>

      {/* Main Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {loading ? (
          <div className="flex flex-col items-center justify-center h-48 space-y-2 text-slate-400">
            <Cpu className="w-6 h-6 animate-spin text-rose-500" />
            <span className="text-xs">Computing optimal deployment vectors...</span>
          </div>
        ) : recommendations && recommendations.recommended_allocations.length > 0 ? (
          <>
            {/* Projected Metrics */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800/80">
                <span className="text-slate-400 text-[10px] uppercase font-semibold">Projected Containment</span>
                <p className="text-base font-bold text-cyan-400 mt-0.5">
                  ~{recommendations.projected_containment_hours} hrs
                </p>
              </div>
              <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800/80">
                <span className="text-slate-400 text-[10px] uppercase font-semibold">Recommended Deployment</span>
                <p className="text-base font-bold text-white mt-0.5">
                  {recommendations.recommended_allocations.length} Units Available
                </p>
              </div>
            </div>

            {/* Allocation Candidate List */}
            <div className="space-y-2.5">
              <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                Ranked AI Allocation Recommendations
              </h4>

              {recommendations.recommended_allocations.map((item) => {
                const isChecked = selectedResourceIds.includes(item.resource_id);

                return (
                  <div
                    key={item.resource_id}
                    onClick={() => handleToggleResource(item.resource_id)}
                    className={`p-3 rounded-xl border transition-all cursor-pointer ${
                      isChecked
                        ? 'bg-slate-800/90 border-cyan-500 ring-1 ring-cyan-500/40 shadow-md'
                        : 'bg-slate-950/50 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-start gap-2.5">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {}} // handled by container click
                          className="mt-1 rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-0 cursor-pointer"
                        />
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-white">{item.resource_name}</span>
                            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono">
                              {item.agency}
                            </span>
                          </div>
                          <p className="text-[11px] text-slate-400 mt-0.5">{item.rationale}</p>
                        </div>
                      </div>

                      <div className="text-right flex flex-col items-end">
                        <div className="flex items-center gap-1 text-emerald-400 font-bold text-xs">
                          <span>Match:</span>
                          <span>{item.match_score}%</span>
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-slate-400 mt-1">
                          <Clock className="w-3 h-3 text-cyan-400" />
                          <span>ETA {item.estimated_arrival_minutes}m</span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <div className="text-center py-10 text-xs text-slate-400">
            No suitable or available resources remaining for dispatch.
          </div>
        )}

        {statusMessage && (
          <div className={`p-3 rounded-xl text-xs flex items-center gap-2 ${
            statusMessage.type === 'success'
              ? 'bg-emerald-950/60 border border-emerald-800 text-emerald-300'
              : 'bg-rose-950/60 border border-rose-800 text-rose-300'
          }`}>
            {statusMessage.type === 'success' ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
            <span>{statusMessage.text}</span>
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="p-4 border-t border-slate-800 bg-slate-900 flex items-center justify-between">
        <span className="text-xs text-slate-400">
          Selected Units: <strong className="text-white">{selectedResourceIds.length}</strong>
        </span>

        <button
          onClick={handleDispatch}
          disabled={dispatching || selectedResourceIds.length === 0}
          className="px-4 py-2 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 disabled:opacity-40 text-white font-semibold text-xs rounded-xl shadow-lg shadow-rose-900/40 flex items-center gap-2 cursor-pointer transition"
        >
          <Send className="w-3.5 h-3.5" />
          <span>{dispatching ? 'Deploying...' : 'Execute Dispatch'}</span>
        </button>
      </div>
    </div>
  );
}
