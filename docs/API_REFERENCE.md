# AEGIS-AI REST & WebSocket API Reference

Base Endpoint URL: `http://localhost:8000/api/v1`

---

## 1. Disasters & Hazard Tracking (`/api/v1/disasters`)

### `GET /api/v1/disasters`
List all tracked disaster incidents. Supports filtering by hazard category and status.

- **Query Parameters:**
  - `hazard_type` (optional, string): e.g., `wildfire`, `earthquake`, `flood`, `hurricane`, `hazmat`, `landslide`
  - `status` (optional, string): e.g., `active`, `escalating`, `stabilized`, `resolved`

- **Response:** `200 OK`
```json
[
  {
    "id": "DIS-001",
    "name": "Sierra Foothills Wildfire Complex",
    "hazard_type": "wildfire",
    "severity_level": "critical",
    "status": "escalating",
    "location": {
      "latitude": 39.12,
      "longitude": -120.95,
      "city": "Placer & El Dorado Counties",
      "region": "Northern California",
      "country": "USA"
    },
    "risk_score": 88.5,
    "affected_radius_km": 35.0,
    "estimated_casualties_at_risk": 4200,
    "structures_threatened": 1850,
    "assigned_resources": ["RES-001"],
    "timestamp": "2026-11-03T09:40:00Z"
  }
]
```

### `GET /api/v1/disasters/{disaster_id}`
Retrieve granular telemetry and status for a single incident.

### `POST /api/v1/disasters`
Create a new active disaster incident.

---

## 2. Emergency Resources Fleet (`/api/v1/resources`)

### `GET /api/v1/resources`
List emergency response resources and fleet capabilities.

- **Query Parameters:**
  - `resource_type` (optional, string): e.g., `aerial`, `ground_crew`, `medical`, `marine`, `search_rescue`, `hazmat`
  - `status` (optional, string): e.g., `available`, `deployed`, `en_route`, `maintenance`

- **Response:** `200 OK`
```json
[
  {
    "id": "RES-001",
    "name": "Air-Crane Helitanker Helitack 101",
    "type": "aerial",
    "status": "available",
    "home_base": "Sacramento Cal Fire Air Base",
    "location": {
      "latitude": 38.58,
      "longitude": -121.49,
      "region": "California",
      "country": "USA"
    },
    "capabilities": ["aerial_drop", "firebreak_creation", "thermal_imaging"],
    "capacity_total": 3000,
    "capacity_available": 3000,
    "speed_kmh": 220.0,
    "fuel_or_battery_percent": 95.0
  }
]
```

### `POST /api/v1/resources`
Register a new emergency response unit or asset.

---

## 3. Intelligent Resource Coordination (`/api/v1/coordination`)

### `GET /api/v1/coordination/recommendations/{disaster_id}`
Run the AI optimization model to recommend and rank optimal assets for a target disaster.

- **Path Parameters:**
  - `disaster_id` (string): Target incident identifier

- **Response:** `200 OK`
```json
{
  "disaster_id": "DIS-001",
  "disaster_name": "Sierra Foothills Wildfire Complex",
  "urgency_level": "critical_immediate",
  "total_units_required": 3,
  "recommendations": [
    {
      "resource_id": "RES-001",
      "resource_name": "Air-Crane Helitanker Helitack 101",
      "resource_type": "aerial",
      "current_base": "Sacramento Cal Fire Air Base",
      "distance_km": 75.3,
      "estimated_eta_minutes": 20.5,
      "suitability_score": 94.2,
      "matching_capabilities": ["aerial_drop", "firebreak_creation"],
      "recommended_units": 1,
      "priority_rank": 1,
      "rationale": "Direct capability alignment with wildfire suppression. Rapid aerial transit."
    }
  ],
  "recommended_at": "2026-11-03T09:40:00Z"
}
```

### `POST /api/v1/coordination/dispatch`
Execute deployment orders for one or more resources to a disaster site.

- **Request Body:**
```json
{
  "disaster_id": "DIS-001",
  "resource_ids": ["RES-001"],
  "dispatch_note": "Immediate aerial retardant drops on northern flank",
  "commander_callsign": "CHIEF-01"
}
```

- **Response:** `200 OK`
```json
{
  "allocation_id": "DISPATCH-c8e411b9",
  "disaster_id": "DIS-001",
  "disaster_name": "Sierra Foothills Wildfire Complex",
  "dispatched_resources": [
    {
      "resource_id": "RES-001",
      "resource_name": "Air-Crane Helitanker Helitack 101",
      "units_allocated": 1,
      "status": "deployed"
    }
  ],
  "dispatched_at": "2026-11-03T09:45:00Z",
  "commander_callsign": "CHIEF-01",
  "status": "active"
}
```

---

## 4. Analytics & Overview (`/api/v1/analytics`)

### `GET /api/v1/analytics/overview`
Provides high-level system indicators (active crises, casualties exposed, threatened structures, fleet readiness).

---

## 5. Crisis Simulation Sandbox (`/api/v1/simulation`)

### `POST /api/v1/simulation/scenarios`
Inject preconfigured multi-hazard scenarios into the live grid:
- `hurricane_fl`: Category 4 Hurricane with storm surge
- `quake_pnw`: 7.8 Magnitude Subduction Earthquake
- `wildfire_sierra`: Severe Wildfire Complex

### `POST /api/v1/simulation/telemetry`
Simulate environmental sensor spikes (wind speed, river height, seismic tremor).

---

## 6. WebSocket Live Stream (`/ws/stream`)

Connect via `ws://localhost:8000/ws/stream` to receive real-time push events:
- `DISASTER_UPDATED` / `DISASTER_CREATED`
- `RESOURCE_DISPATCHED`
- `TELEMETRY_UPDATED`
