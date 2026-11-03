from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

class DisasterType(str, Enum):
    WILDFIRE = "wildfire"
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    HURRICANE = "hurricane"
    HAZMAT_SPILL = "hazmat_spill"
    TSUNAMI = "tsunami"

class DisasterSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"

class DisasterStatus(str, Enum):
    DETECTED = "detected"
    ACTIVE = "active"
    CONTAINED = "contained"
    RESOLVED = "resolved"

class GeoLocation(BaseModel):
    latitude: float
    longitude: float
    address: str = ""
    region: str = ""

class EnvironmentalImpact(BaseModel):
    estimated_casualties_at_risk: int = 0
    structures_threatened: int = 0
    air_quality_index: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    flood_depth_meters: Optional[float] = None
    seismic_magnitude: Optional[float] = None
    radiation_or_ppm: Optional[float] = None

class DisasterEvent(BaseModel):
    id: str
    title: str
    type: DisasterType
    severity: DisasterSeverity
    status: DisasterStatus = DisasterStatus.ACTIVE
    location: GeoLocation
    radius_km: float = Field(..., ge=0.1)
    risk_score: float = Field(0.0, ge=0.0, le=100.0)
    impact: EnvironmentalImpact = Field(default_factory=EnvironmentalImpact)
    required_capabilities: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_resources: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
