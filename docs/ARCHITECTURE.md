# AEGIS-AI Architecture & System Design Document

**AI-Powered Multi-Disaster Monitoring and Intelligent Resource Coordination System**

---

## 1. System Vision & Objectives

Natural and human-made disasters often occur concurrently or trigger secondary catastrophic cascades (e.g., an offshore earthquake inducing a tsunami, followed by coastal flooding and petrochemical plant fires). Traditional emergency management systems operate in rigid silos with delayed manual coordination, suboptimal resource allocation, and high response latency.

**AEGIS-AI** is an emergency command, disaster monitoring, and intelligent resource coordination system engineered to:
1. **Aggregate Multi-Hazard Telemetry:** Continuously monitor wildfires, earthquakes, floods, hurricanes, industrial hazmat leaks, and landslides across distributed geographic sectors.
2. **Compute Compound Multi-Factor Risk:** Quantify disaster urgency via dynamic severity indicators (Richter magnitude, Saffir-Simpson category, fire front velocity, water surge, structural vulnerability, and casualty exposure).
3. **Optimize Multi-Criteria Emergency Resource Allocation:** Leverage automated heuristics and mathematical optimization to match specialized emergency teams (Search & Rescue, Helitankers, Swiftwater teams, Mobile Trauma Hospitals, HAZMAT units) to active crises based on capability alignment, transit ETA (Haversine geospatial modeling), deployment readiness, and cross-incident priority.
4. **Facilitate High-Fidelity Tactical Command & Simulation:** Enable incident commanders to visualize crisis radars in real-time, test stress scenarios, and trigger one-click coordinated multi-unit dispatches.

---

## 2. Clean Architecture & Directory Hierarchy

The project adheres to domain-driven design (DDD), separating core mathematical optimization logic, persistence schemas, RESTful & WebSocket communications, and responsive tactical presentation interfaces.

```
aegis-ai/
├── backend/                             # Python 3.12 / FastAPI Core
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── analytics.py         # Systemwide telemetry & status counters
│   │   │       ├── coordination.py      # AI recommendations & dispatch execution
│   │   │       ├── disasters.py          # Incident CRUD & geospatial queries
│   │   │       ├── resources.py          # Fleet inventory & unit tracking
│   │   │       └── simulation.py         # Scenario injections & telemetry triggers
│   │   ├── core/
│   │   │   ├── config.py                # Environment configs & global constants
│   │   │   └── websocket.py             # Event bus broadcasting live state
│   │   ├── data/
│   │   │   └── seed_data.py             # Default CONUS emergency incidents & resources
│   │   ├── models/
│   │   │   ├── allocation.py            # AI recommendation & dispatch models
│   │   │   ├── disaster.py              # Multi-hazard schema & severity models
│   │   │   ├── resource.py              # Fleet asset models & capability definitions
│   │   │   └── telemetry.py             # Dynamic environmental sensor feeds
│   │   ├── services/
│   │   │   ├── ai_optimizer.py          # Multi-criteria optimization engine
│   │   │   ├── disaster_engine.py       # Haversine distance & composite risk scoring
│   │   │   └── simulation_service.py    # State persistence & telemetry mutation
│   │   └── main.py                      # FastAPI application entrypoint
│   └── tests/                           # Pytest unit & integration test suites
│       ├── test_ai_optimizer.py         # AI scoring & allocation validation
│       ├── test_api.py                  # API endpoint integration testing
│       └── test_disaster_engine.py      # Distance calculations & risk scores
├── frontend/                            # Vite / React / Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── AiDispatchConsole.jsx    # Recommendation review & dispatch trigger
│   │   │   ├── AnalyticsPanel.jsx       # Real-time casualty/threat metrics
│   │   │   ├── DisasterFeed.jsx         # Hazard cards with filter selectors
│   │   │   ├── DisasterMap.jsx          # Tactical radar geospatial projection
│   │   │   ├── Header.jsx               # Navigation bar & live status indicator
│   │   │   ├── ResourceFleet.jsx        # Fleet inventory status cards
│   │   │   └── ScenarioSimulator.jsx    # Real-time incident stress-testing
│   │   ├── services/
│   │   │   └── api.js                   # Unified Axios API client
│   │   ├── App.jsx                      # Primary dashboard orchestration
│   │   ├── index.css                    # Tailwind utility and tactical styling
│   │   └── main.jsx                     # React DOM bootstrap
│   ├── index.html                       # Application shell
│   ├── package.json                     # Node dependencies & build scripts
│   ├── tailwind.config.js               # Theme configuration
│   └── vite.config.js                   # Vite dev & preview proxy configuration
├── docs/
│   ├── ARCHITECTURE.md                  # Detailed architectural design & algorithms
│   └── API_REFERENCE.md                 # OpenAPI REST endpoint contracts
├── run_demo.sh                          # One-step automated start script
├── requirements.txt                     # Backend Python dependencies
└── README.md                            # Quickstart & user documentation
```

---

## 3. Mathematical Models & AI Optimization Algorithm

### 3.1 Composite Disaster Risk Scoring ($S_{risk}$)

Disaster risk is quantified as a normalized score from $0$ to $100$, derived from baseline hazard severity, casualty exposure, structural threats, and secondary hazard cascade multipliers:

$$S_{risk} = \min\left(100, \left(W_{base} \cdot V_{hazard} + W_{cas} \cdot \log_{10}(N_{cas} + 10) \cdot 18 + W_{str} \cdot \log_{10}(N_{str} + 10) \cdot 12\right) \times M_{sec}\right)$$

Where:
- $V_{hazard} \in [1, 5]$ is hazard severity.
- $N_{cas}$ is estimated population at risk.
- $N_{str}$ is threatened infrastructure count.
- $M_{sec}$ is the secondary cascade multiplier ($\ge 1.0$).
- Weights $W_{base} = 0.45$, $W_{cas} = 0.35$, $W_{str} = 0.20$.

### 3.2 AI Resource Capability & Suitability Engine

Each disaster type defines required operational capabilities:
- **Wildfire:** `wildfire_suppression`, `aerial_drop`, `evacuation_support`, `firebreak_creation`.
- **Flood / Tsunami:** `swiftwater_rescue`, `waterborne_evac`, `flood_barrier`, `airlift`.
- **Earthquake / Landslide:** `urban_search_rescue`, `heavy_extrication`, `structural_stabilization`, `trauma_care`.
- **Hazmat / Chemical:** `hazmat_containment`, `chemical_decon`, `vapor_suppression`, `casualty_triage`.

For each available emergency resource $R_j$ evaluated against disaster $D_i$:

1. **Capability Alignment ($C_{score} \in [0, 1]$):**
   $$C_{score} = \frac{|\text{Capabilities}(R_j) \cap \text{Required}(D_i)|}{|\text{Required}(D_i)|}$$

2. **Transit Time & Proximity ($P_{score} \in [0, 1]$):**
   $$\text{Distance}_{km} = \text{Haversine}(\text{Coord}(R_j), \text{Coord}(D_i))$$
   $$\text{ETA}_{hours} = \frac{\text{Distance}_{km}}{V_{speed}(R_j)} \times F_{terrain}$$
   $$P_{score} = \max\left(0, 1.0 - \frac{\text{ETA}_{hours}}{\text{MaxWindow}}\right)$$

3. **Asset Readiness ($R_{score} \in [0, 1]$):**
   $$R_{score} = \text{OperationalCapacity}(R_j) \times \text{FuelSuppliesFactor}$$

4. **Composite Recommendation Score ($S_{alloc} \in [0, 100]$):**
   $$S_{alloc} = \left(0.40 \cdot C_{score} + 0.35 \cdot P_{score} + 0.25 \cdot R_{score}\right) \times 100$$

Units with $S_{alloc} \ge 35$ and at least one matching capability are ranked and proposed in the AI Dispatch Console with computed ETAs, required mission roles, and recommended unit sizes.

---

## 4. Real-Time Telemetry & Event Streaming

The system incorporates a bidirectional WebSocket event bus (`/ws/stream`) and REST telemetry push endpoints:
- **Telemetry Ingestion:** Live sensors (seismographs, Doppler radar, river level gauges, infrared air patrol) post continuous telemetry updates.
- **Dynamic Re-Scoring:** Significant parameter shifts (e.g. earthquake aftershocks or wind speed spikes) automatically recalculate incident risk ratings.
- **WebSocket Broadcast:** Changes in disaster coordinates, risk scores, or fleet dispatch events are pushed instantly to connected clients.
