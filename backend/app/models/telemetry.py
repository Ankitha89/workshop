from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime, timezone

class SensorTelemetry(BaseModel):
    sensor_id: str
    station_name: str
    latitude: float
    longitude: float
    sensor_type: str
    reading: float
    unit: str
    status: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
