import random
from fastapi import APIRouter
from typing import Dict, Any, List
from backend.app.services.simulation_service import simulation_service
from backend.app.services.disaster_engine import disaster_engine
from backend.app.models.disaster import DisasterEvent, DisasterType, DisasterSeverity, DisasterStatus, GeoLocation, EnvironmentalImpact
from backend.app.models.telemetry import SensorTelemetry

router = APIRouter(prefix="/simulation", tags=["Simulation Sandbox"])

@router.get("/telemetry", response_model=List[SensorTelemetry])
def get_telemetry():
    return simulation_service.get_latest_telemetry()

@router.post("/tick")
def trigger_tick() -> Dict[str, Any]:
    return simulation_service.step_simulation()

@router.post("/inject-scenario")
def inject_scenario(scenario_type: str = "severe_weather") -> Dict[str, Any]:
    new_id = f"SIM-{random.randint(100, 999)}"
    scenarios = {
        "severe_weather": DisasterEvent(
            id=new_id,
            title="Atlantic Category 4 Hurricane 'Zephyr'",
            type=DisasterType.HURRICANE,
            severity=DisasterSeverity.CRITICAL,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(latitude=25.7617, longitude=-80.1918, address="Biscayne Coast", region="South Florida"),
            radius_km=60.0,
            risk_score=91.0,
            impact=EnvironmentalImpact(estimated_casualties_at_risk=8500, structures_threatened=1800, wind_speed_kmh=155.0),
            required_capabilities=["mass_evacuation", "swift_water_rescue", "drone_surveillance", "shelter_supply"],
            notes=["Rapid intensification recorded by offshore buoys."]
        ),
        "earthquake_swarm": DisasterEvent(
            id=new_id,
            title="San Andreas Fault Rupture Event",
            type=DisasterType.EARTHQUAKE,
            severity=DisasterSeverity.CATASTROPHIC,
            status=DisasterStatus.ACTIVE,
            location=GeoLocation(latitude=34.0522, longitude=-118.2437, address="San Fernando Basin", region="Southern California"),
            radius_km=50.0,
            risk_score=96.5,
            impact=EnvironmentalImpact(estimated_casualties_at_risk=24000, structures_threatened=4500, seismic_magnitude=7.8),
            required_capabilities=["urban_search_and_rescue", "emergency_triage", "structural_inspection", "heavy_lifting"],
            notes=["Epicenter 12km NW of downtown; bridge & overpass collapses reported."]
        )
    }

    event = scenarios.get(scenario_type, scenarios["severe_weather"])
    created = disaster_engine.create_disaster(event)
    return {
        "status": "injected",
        "disaster": created.model_dump()
    }
