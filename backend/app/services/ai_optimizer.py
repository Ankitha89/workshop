import math
from typing import Dict, List, Optional
from datetime import datetime, timezone
from backend.app.models.resource import EmergencyResource, ResourceStatus
from backend.app.models.disaster import DisasterEvent
from backend.app.models.allocation import OptimizationRecommendation, DispatchPlanItem, DispatchExecutionResult
from backend.app.services.disaster_engine import haversine_distance, disaster_engine
from backend.app.data.seed_data import get_initial_resources

class AiResourceOptimizer:
    def __init__(self):
        self._resources: Dict[str, EmergencyResource] = {
            r.id: r for r in get_initial_resources()
        }

    def get_all_resources(self, status: Optional[str] = None, resource_type: Optional[str] = None) -> List[EmergencyResource]:
        res_list = list(self._resources.values())
        if status:
            res_list = [r for r in res_list if r.status.value.lower() == status.lower()]
        if resource_type:
            res_list = [r for r in res_list if r.type.value.lower() == resource_type.lower()]
        return res_list

    def get_by_id(self, resource_id: str) -> Optional[EmergencyResource]:
        return self._resources.get(resource_id)

    def calculate_match_score(
        self,
        resource: EmergencyResource,
        disaster: DisasterEvent,
        distance_km: float
    ) -> float:
        req_set = set(disaster.required_capabilities)
        res_set = set(resource.capabilities)
        if req_set:
            overlap = len(req_set.intersection(res_set))
            capability_score = min(1.0, overlap / max(1, len(req_set))) * 100.0
        else:
            capability_score = 70.0

        proximity_score = 100.0 / (1.0 + (distance_km / 60.0))
        readiness_score = resource.fuel_or_battery_pct
        cap_ratio = (resource.available_units / max(1, resource.capacity_units))
        capacity_score = cap_ratio * 100.0

        total_score = (
            (capability_score * 0.45) +
            (proximity_score * 0.35) +
            (readiness_score * 0.10) +
            (capacity_score * 0.10)
        )
        return round(total_score, 1)

    def recommend_allocations(self, disaster_id: str) -> Optional[OptimizationRecommendation]:
        disaster = disaster_engine.get_by_id(disaster_id)
        if not disaster:
            return None

        candidates = [
            r for r in self._resources.values()
            if r.status in [ResourceStatus.AVAILABLE, ResourceStatus.EN_ROUTE]
            and r.id not in disaster.assigned_resources
        ]

        evaluated_items: List[DispatchPlanItem] = []
        covered_capabilities = set()

        for resource in candidates:
            dist = haversine_distance(
                resource.location.latitude,
                resource.location.longitude,
                disaster.location.latitude,
                disaster.location.longitude
            )
            eta_mins = round((dist / max(20.0, resource.speed_kmh)) * 60.0, 1)
            score = self.calculate_match_score(resource, disaster, dist)

            matches = set(disaster.required_capabilities).intersection(set(resource.capabilities))
            rationale_parts = []
            if matches:
                rationale_parts.append(f"Provides {', '.join(matches)}")
                covered_capabilities.update(matches)
            rationale_parts.append(f"ETA ~{eta_mins}m ({dist} km away)")
            if resource.fuel_or_battery_pct > 90:
                rationale_parts.append("High operational battery/fuel reserves")

            evaluated_items.append(
                DispatchPlanItem(
                    resource_id=resource.id,
                    resource_name=resource.name,
                    resource_type=resource.type,
                    agency=resource.agency,
                    distance_km=dist,
                    estimated_arrival_minutes=eta_mins,
                    match_score=score,
                    allocated_units=min(resource.available_units, 100),
                    rationale="; ".join(rationale_parts)
                )
            )

        evaluated_items.sort(key=lambda x: x.match_score, reverse=True)
        top_recommendations = evaluated_items[:5]

        unmet = [c for c in disaster.required_capabilities if c not in covered_capabilities]
        projected_hours = max(2.0, round(24.0 * (disaster.risk_score / 100.0) / max(1, len(top_recommendations)), 1))

        urgency = "HIGH"
        if disaster.risk_score >= 85:
            urgency = "CRITICAL_IMMEDIATE"
        elif disaster.risk_score <= 50:
            urgency = "STANDARD"

        return OptimizationRecommendation(
            disaster_id=disaster.id,
            disaster_title=disaster.title,
            urgency_level=urgency,
            recommended_allocations=top_recommendations,
            unmet_capabilities=unmet,
            projected_containment_hours=projected_hours,
            total_resources_needed=len(disaster.required_capabilities) * 2
        )

    def dispatch_resources(self, disaster_id: str, resource_ids: List[str], notes: Optional[str] = None) -> DispatchExecutionResult:
        disaster = disaster_engine.get_by_id(disaster_id)
        if not disaster:
            return DispatchExecutionResult(
                success=False,
                disaster_id=disaster_id,
                dispatched_count=0,
                mission_id="",
                message="Disaster event not found"
            )

        mission_id = f"MSN-{int(datetime.now(timezone.utc).timestamp())}"
        dispatched = 0

        for r_id in resource_ids:
            res = self._resources.get(r_id)
            if res:
                res.status = ResourceStatus.DEPLOYED
                res.target_disaster_id = disaster_id
                res.current_mission_id = mission_id
                res.updated_at = datetime.now(timezone.utc)
                disaster_engine.assign_resource_to_disaster(disaster_id, r_id)
                dispatched += 1

        if notes:
            disaster.notes.append(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Mission {mission_id}: {notes}")

        return DispatchExecutionResult(
            success=True,
            disaster_id=disaster_id,
            dispatched_count=dispatched,
            mission_id=mission_id,
            message=f"Successfully deployed {dispatched} emergency units under Mission {mission_id}."
        )

ai_optimizer = AiResourceOptimizer()
