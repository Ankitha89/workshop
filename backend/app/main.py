from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1 import disasters, resources, coordination, analytics, simulation
from backend.app.api import websocket

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-Powered Multi-Disaster Monitoring & Intelligent Emergency Resource Allocation API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(disasters.router, prefix=settings.api_prefix)
app.include_router(resources.router, prefix=settings.api_prefix)
app.include_router(coordination.router, prefix=settings.api_prefix)
app.include_router(analytics.router, prefix=settings.api_prefix)
app.include_router(simulation.router, prefix=settings.api_prefix)
app.include_router(websocket.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": settings.app_name,
        "version": settings.version
    }
