import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import DisasterMap from './components/DisasterMap';
import DisasterFeed from './components/DisasterFeed';
import AiDispatchConsole from './components/AiDispatchConsole';
import ResourceFleet from './components/ResourceFleet';
import AnalyticsPanel from './components/AnalyticsPanel';
import ScenarioSimulator from './components/ScenarioSimulator';
import { api } from './services/api';

export default function App() {
  const [disasters, setDisasters] = useState([]);
  const [resources, setResources] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [selectedDisaster, setSelectedDisaster] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    setIsRefreshing(true);
    try {
      const [disastersData, resourcesData, analyticsData] = await Promise.all([
        api.getDisasters(),
        api.getResources(),
        api.getAnalyticsSummary()
      ]);
      setDisasters(disastersData);
      setResources(resourcesData);
      setAnalytics(analyticsData);

      // Default select first disaster if none selected
      if (!selectedDisaster && disastersData.length > 0) {
        setSelectedDisaster(disastersData[0]);
      } else if (selectedDisaster) {
        // sync currently selected disaster
        const found = disastersData.find(d => d.id === selectedDisaster.id);
        if (found) setSelectedDisaster(found);
      }
    } catch (err) {
      console.error('Failed to load system data:', err);
    } finally {
      setIsRefreshing(false);
    }
  }, [selectedDisaster]);

  useEffect(() => {
    loadData();

    // Setup periodic polling
    const interval = setInterval(() => {
      loadData();
    }, 10000);

    return () => clearInterval(interval);
  }, [loadData]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header analytics={analytics} onRefresh={loadData} isRefreshing={isRefreshing} />

      <main className="flex-1 p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Top KPI Metric Cards */}
        <AnalyticsPanel analytics={analytics} />

        {/* Tactical Map */}
        <DisasterMap
          disasters={disasters}
          resources={resources}
          selectedDisaster={selectedDisaster}
          onSelectDisaster={setSelectedDisaster}
        />

        {/* Live Incident Feed & AI Allocation Dispatch Console */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DisasterFeed
            disasters={disasters}
            selectedDisaster={selectedDisaster}
            onSelectDisaster={setSelectedDisaster}
          />
          <AiDispatchConsole
            selectedDisaster={selectedDisaster}
            onDispatchSuccess={loadData}
          />
        </div>

        {/* Scenario Injection Sandbox */}
        <ScenarioSimulator onScenarioInjected={loadData} />

        {/* Emergency Resources Inventory */}
        <ResourceFleet resources={resources} />
      </main>

      <footer className="py-4 border-t border-slate-900 text-center text-xs text-slate-500">
        AEGIS Multi-Disaster Command System • AI-Powered Resource Coordination Engine
      </footer>
    </div>
  );
}
