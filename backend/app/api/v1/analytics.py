from fastapi import APIRouter
from typing import Dict, Any
from backend.app.services.disaster_engine import disaster_engine
from backend.app.services.ai_optimizer import ai_optimizer

router = APIRouter(prefix="/analytics", tags=["Analytics & Situational Intelligence"])

@router.get("/summary")
def get_situational_summary() -> Dict[str, Any]:
    disasters = disaster_engine.get_all()
    resources = ai_optimizer.get_all_resources()

    total_casualties_at_risk = sum(d.impact.estimated_casualties_at_risk for d in disasters)
    total_structures_threatened = sum(d.impact.structures_threatened for d in disasters)
    active_disasters_count = sum(1 for d in disasters if d.status.value == "active")

    resources_available = sum(1 for r in resources if r.status.value == "available")
    resources_deployed = sum(1 for r in resources if r.status.value == "deployed")
    resources_en_route = sum(1 for r in resources if r.status.value == "en_route")

    hazard_distribution = {}
    for d in disasters:
        hazard_distribution[d.type.value] = hazard_distribution.get(d.type.value, 0) + 1

    agency_participation = {}
    for r in resources:
        agency_participation[r.agency] = agency_participation.get(r.agency, 0) + 1

    return {
        "active_disasters_count": active_disasters_count,
        "total_disasters_tracked": len(disasters),
        "total_casualties_at_risk": total_casualties_at_risk,
        "total_structures_threatened": total_structures_threatened,
        "resources_summary": {
            "total": len(resources),
            "available": resources_available,
            "deployed": resources_deployed,
            "en_route": resources_en_route
        },
        "hazard_distribution": hazard_distribution,
        "agency_participation": agency_participation,
        "readiness_index_pct": round((resources_available / max(1, len(resources))) * 100, 1)
    }
