from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from backend.app.models.disaster import GeoLocation

class ResourceType(str, Enum):
    MEDICAL_EVAC = "medical_evac"
    FIREFIGHTING = "firefighting"
    SEARCH_AND_RESCUE = "search_and_rescue"
    HAZMAT_CONTAINMENT = "hazmat_containment"
    AIRBORNE_DRONE = "airborne_drone"
    SHELTER_SUPPLY = "shelter_supply"
    WATER_RESCUE = "water_rescue"

class ResourceStatus(str, Enum):
    AVAILABLE = "available"
    EN_ROUTE = "en_route"
    DEPLOYED = "deployed"
    MAINTENANCE = "maintenance"
    EXHAUSTED = "exhausted"

class EmergencyResource(BaseModel):
    id: str
    name: str
    type: ResourceType
    agency: str
    status: ResourceStatus = ResourceStatus.AVAILABLE
    location: GeoLocation
    speed_kmh: float = 60.0
    capacity_units: int = 100
    available_units: int = 100
    capabilities: List[str] = Field(default_factory=list)
    current_mission_id: Optional[str] = None
    target_disaster_id: Optional[str] = None
    fuel_or_battery_pct: float = Field(100.0, ge=0.0, le=100.0)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
