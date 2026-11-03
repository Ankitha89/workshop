#!/usr/bin/env bash
# AEGIS-AI Automated Demo Runner

set -e

echo "=========================================================="
echo " Starting AEGIS-AI: Multi-Disaster Command System"
echo "=========================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down AEGIS-AI processes..."
    kill $(lsof -t -i :8000) 2>/dev/null || true
    kill $(lsof -t -i :3000) 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Kill any existing processes on port 8000 and 3000
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :3000) 2>/dev/null || true

# 2. Launch FastAPI Backend
echo "[1/2] Starting FastAPI backend on http://localhost:8000..."
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend healthcheck
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo " Backend operational at http://localhost:8000"
        echo " API documentation at http://localhost:8000/docs"
        break
    fi
    sleep 0.5
done

# 3. Launch Frontend
echo "[2/2] Starting Vite Frontend on http://localhost:3000..."
cd "$ROOT_DIR/frontend"
npm run preview -- --host 0.0.0.0 --port 3000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo " Frontend dashboard ready at http://localhost:3000"
        break
    fi
    sleep 0.5
done

echo ""
echo "=========================================================="
echo " AEGIS-AI Command Grid is LIVE!"
echo " Web Dashboard: http://localhost:3000"
echo " REST API Docs: http://localhost:8000/docs"
echo " Press Ctrl+C to terminate all services."
echo "=========================================================="

# Keep running
wait
