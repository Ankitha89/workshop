const API_BASE = '/api/v1';

export const api = {
  // Disasters
  async getDisasters(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/disasters${query ? '?' + query : ''}`);
    if (!res.ok) throw new Error('Failed to fetch disasters');
    return res.json();
  },

  async getDisaster(id) {
    const res = await fetch(`${API_BASE}/disasters/${id}`);
    if (!res.ok) throw new Error('Failed to fetch disaster details');
    return res.json();
  },

  // Resources
  async getResources(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/resources${query ? '?' + query : ''}`);
    if (!res.ok) throw new Error('Failed to fetch emergency resources');
    return res.json();
  },

  // AI Coordination
  async getRecommendations(disasterId) {
    const res = await fetch(`${API_BASE}/coordination/recommendations/${disasterId}`);
    if (!res.ok) throw new Error('Failed to compute recommendations');
    return res.json();
  },

  async dispatchResources(disasterId, resourceIds, notes) {
    const res = await fetch(`${API_BASE}/coordination/dispatch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ disaster_id: disasterId, resource_ids: resourceIds, notes })
    });
    if (!res.ok) throw new Error('Failed to dispatch resources');
    return res.json();
  },

  // Analytics
  async getAnalyticsSummary() {
    const res = await fetch(`${API_BASE}/analytics/summary`);
    if (!res.ok) throw new Error('Failed to fetch analytics summary');
    return res.json();
  },

  // Simulation
  async injectScenario(scenarioType) {
    const res = await fetch(`${API_BASE}/simulation/inject-scenario?scenario_type=${scenarioType}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Failed to inject scenario');
    return res.json();
  },

  async getTelemetry() {
    const res = await fetch(`${API_BASE}/simulation/telemetry`);
    if (!res.ok) throw new Error('Failed to fetch sensor telemetry');
    return res.json();
  }
};
