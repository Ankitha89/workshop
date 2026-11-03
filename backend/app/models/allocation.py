from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from backend.app.models.resource import ResourceType

class DispatchPlanItem(BaseModel):
    resource_id: str
    resource_name: str
    resource_type: ResourceType
    agency: str
    distance_km: float
    estimated_arrival_minutes: float
    match_score: float
    allocated_units: int
    rationale: str

class OptimizationRecommendation(BaseModel):
    disaster_id: str
    disaster_title: str
    urgency_level: str
    recommended_allocations: List[DispatchPlanItem]
    unmet_capabilities: List[str] = Field(default_factory=list)
    projected_containment_hours: float
    total_resources_needed: int
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DispatchRequest(BaseModel):
    disaster_id: str
    resource_ids: List[str]
    notes: Optional[str] = None

class DispatchExecutionResult(BaseModel):
    success: bool
    disaster_id: str
    dispatched_count: int
    mission_id: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
