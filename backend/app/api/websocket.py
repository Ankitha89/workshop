import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from backend.app.services.simulation_service import simulation_service
from backend.app.services.disaster_engine import disaster_engine

router = APIRouter(tags=["WebSocket Realtime Stream"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            simulation_service.step_simulation()
            payload = {
                "type": "TELEMETRY_UPDATE",
                "telemetry": [t.model_dump() for t in simulation_service.get_latest_telemetry()],
                "active_disasters_count": len(disaster_engine.get_all(status="active"))
            }
            await websocket.send_text(json.dumps(payload, default=str))
            await asyncio.sleep(3.0)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
