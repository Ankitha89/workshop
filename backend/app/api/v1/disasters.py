from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.models.disaster import DisasterEvent
from backend.app.services.disaster_engine import disaster_engine

router = APIRouter(prefix="/disasters", tags=["Disasters"])

@router.get("", response_model=List[DisasterEvent])
def list_disasters(
    status: Optional[str] = Query(None, description="Filter by status (active, contained, resolved)"),
    disaster_type: Optional[str] = Query(None, description="Filter by type (wildfire, earthquake, flood, etc.)")
):
    return disaster_engine.get_all(status=status, disaster_type=disaster_type)

@router.get("/{disaster_id}", response_model=DisasterEvent)
def get_disaster(disaster_id: str):
    disaster = disaster_engine.get_by_id(disaster_id)
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return disaster

@router.post("", response_model=DisasterEvent, status_code=201)
def create_disaster(event: DisasterEvent):
    return disaster_engine.create_disaster(event)

@router.patch("/{disaster_id}", response_model=DisasterEvent)
def update_disaster(disaster_id: str, updates: dict):
    updated = disaster_engine.update_disaster(disaster_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return updated
