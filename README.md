# AEGIS-AI: Multi-Disaster Monitoring & Intelligent Resource Coordination System

[![Backend Tests](https://img.shields.io/badge/pytest-13%20passed-brightgreen.svg)](#)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](#)
[![React](https://img.shields.io/badge/frontend-React%20%7C%20TailwindCSS-61DAFB.svg)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](#)

AEGIS-AI is a multi-hazard emergency command and automated resource dispatch system. It provides real-time situational awareness across concurrent disaster domains (wildfires, earthquakes, floods, hurricanes, industrial hazmat incidents, landslides) and leverages mathematical multi-criteria optimization to coordinate emergency response fleets.

---

## 🌟 Key Features

- **Multi-Hazard Grid Telemetry:** Continuous aggregation of seismic, atmospheric, hydrologic, and chemical sensor feeds.
- **Dynamic Risk Evaluation:** Normalized multi-factor risk scoring ($0-100$) factoring in population exposure, infrastructure vulnerability, and secondary hazard cascade multipliers.
- **AI Resource Optimization Engine:** Heuristic matching of emergency assets (Helitankers, Urban USAR teams, Mobile Trauma Hospitals, HAZMAT units, Swiftwater flotillas) based on capability synergy, Haversine geospatial proximity, transit ETAs, and asset readiness.
- **Interactive Tactical Radar:** Real-time geospatial incident and asset mapping with radar distance rings and status overlays.
- **One-Click Coordinated Dispatch:** Review AI-generated recommendations, inspect operational rationales, and execute coordinated fleet dispatches.
- **Multi-Crisis Scenario Sandbox:** Inject dynamic stress tests (e.g. Category 4 Hurricane, 7.8 Magnitude Subduction Quake) to validate response resilience.
- **WebSocket Event Bus:** Bi-directional real-time push streaming for instant incident status updates and dispatch confirmations.

---

## 📁 System Architecture & File Structure

```
.
├── backend/                       # Python FastAPI Backend
│   ├── app/
│   │   ├── api/v1/                # REST API routers (disasters, resources, coordination, analytics, simulation)
│   │   ├── core/                  # Configurations, constants, WebSocket connection hub
│   │   ├── data/                  # Seed disaster and asset data
│   │   ├── models/                # Pydantic data schemas
│   │   ├── services/              # Optimization engine, distance math, telemetry simulation
│   │   └── main.py                # FastAPI entry point
│   └── tests/                     # Comprehensive Pytest suite
├── frontend/                      # Modern React + Vite Dashboard
│   ├── src/
│   │   ├── components/            # Tactical radar, disaster feed, dispatch console, fleet inventory
│   │   ├── services/              # API clients
│   │   ├── App.jsx                # Main interface orchestrator
│   │   └── index.css              # Cyber-tactical Tailwind theme
│   └── vite.config.js
├── docs/                          # Architecture & API documentation
│   ├── ARCHITECTURE.md            # Deep dive into algorithms & design decisions
│   └── API_REFERENCE.md           # REST & WebSocket endpoint contracts
├── run_demo.sh                    # Automated single-command launch script
└── requirements.txt               # Backend requirements
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Automated Launch
To start both backend and frontend with a single script:
```bash
chmod +x run_demo.sh
./run_demo.sh
```
The interface will be accessible at `http://localhost:3000` (backed by `http://localhost:8000`).

### 2. Manual Launch

**Backend Setup:**
```bash
pip install -r requirements.txt
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API docs: `http://localhost:8000/docs`

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```
Command Dashboard: `http://localhost:3000`

---

## 🧪 Testing

Run backend unit and integration tests:
```bash
python3 -m pytest -v backend/tests/
```

Verify frontend build:
```bash
cd frontend && npm run build
```

---

## 📖 Documentation
- [Architecture & Optimization Engine Design](docs/ARCHITECTURE.md)
- [REST & WebSocket API Reference](docs/API_REFERENCE.md)

---
Developed for mission-critical emergency coordination & disaster resilience.
