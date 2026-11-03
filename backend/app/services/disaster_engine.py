import math
from typing import Dict, List, Optional
from datetime import datetime, timezone
from backend.app.models.disaster import DisasterEvent, DisasterSeverity, DisasterStatus, DisasterType, GeoLocation, EnvironmentalImpact
from backend.app.data.seed_data import get_initial_disasters

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

class DisasterEngine:
    def __init__(self):
        self._disasters: Dict[str, DisasterEvent] = {
            d.id: d for d in get_initial_disasters()
        }

    def get_all(self, status: Optional[str] = None, disaster_type: Optional[str] = None) -> List[DisasterEvent]:
        events = list(self._disasters.values())
        if status:
            events = [e for e in events if e.status.value.lower() == status.lower()]
        if disaster_type:
            events = [e for e in events if e.type.value.lower() == disaster_type.lower()]
        return sorted(events, key=lambda x: x.risk_score, reverse=True)

    def get_by_id(self, disaster_id: str) -> Optional[DisasterEvent]:
        return self._disasters.get(disaster_id)

    def calculate_risk_score(self, event: DisasterEvent) -> float:
        severity_weights = {
            DisasterSeverity.LOW: 20.0,
            DisasterSeverity.MODERATE: 40.0,
            DisasterSeverity.HIGH: 65.0,
            DisasterSeverity.CRITICAL: 85.0,
            DisasterSeverity.CATASTROPHIC: 95.0,
        }
        base_score = severity_weights.get(event.severity, 50.0)

        casualties = event.impact.estimated_casualties_at_risk
        cas_factor = 0.0
        if casualties > 0:
            cas_factor = min(15.0, round(math.log10(casualties + 1) * 3.5, 2))

        rad_factor = min(10.0, (event.radius_km / 50.0) * 10.0)

        hazard_factor = 0.0
        if event.type == DisasterType.WILDFIRE:
            if event.impact.wind_speed_kmh and event.impact.wind_speed_kmh > 40:
                hazard_factor += 5.0
            if event.impact.air_quality_index and event.impact.air_quality_index > 250:
                hazard_factor += 5.0
        elif event.type == DisasterType.EARTHQUAKE:
            if event.impact.seismic_magnitude and event.impact.seismic_magnitude >= 7.0:
                hazard_factor += 10.0
            elif event.impact.seismic_magnitude and event.impact.seismic_magnitude >= 6.0:
                hazard_factor += 6.0
        elif event.type == DisasterType.FLOOD:
            if event.impact.flood_depth_meters and event.impact.flood_depth_meters >= 2.0:
                hazard_factor += 8.0
        elif event.type == DisasterType.HAZMAT_SPILL:
            if event.impact.radiation_or_ppm and event.impact.radiation_or_ppm > 100:
                hazard_factor += 8.0

        final_score = min(100.0, max(5.0, base_score + cas_factor + rad_factor + hazard_factor))
        return round(final_score, 1)

    def create_disaster(self, event: DisasterEvent) -> DisasterEvent:
        event.risk_score = self.calculate_risk_score(event)
        event.created_at = datetime.now(timezone.utc)
        event.updated_at = datetime.now(timezone.utc)
        self._disasters[event.id] = event
        return event

    def update_disaster(self, disaster_id: str, updates: dict) -> Optional[DisasterEvent]:
        disaster = self._disasters.get(disaster_id)
        if not disaster:
            return None
        disaster_dict = disaster.model_dump()
        for k, v in updates.items():
            if k in disaster_dict and v is not None:
                disaster_dict[k] = v
        disaster_dict["updated_at"] = datetime.now(timezone.utc)
        updated = DisasterEvent(**disaster_dict)
        updated.risk_score = self.calculate_risk_score(updated)
        self._disasters[disaster_id] = updated
        return updated

    def assign_resource_to_disaster(self, disaster_id: str, resource_id: str) -> bool:
        disaster = self._disasters.get(disaster_id)
        if not disaster:
            return False
        if resource_id not in disaster.assigned_resources:
            disaster.assigned_resources.append(resource_id)
            disaster.updated_at = datetime.now(timezone.utc)
        return True

disaster_engine = DisasterEngine()
