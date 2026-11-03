import random
from typing import List, Dict, Any
from datetime import datetime, timezone
from backend.app.models.telemetry import SensorTelemetry
from backend.app.services.disaster_engine import disaster_engine

class SimulationService:
    def __init__(self):
        self._telemetry_stream: List[SensorTelemetry] = []
        self._generate_initial_telemetry()

    def _generate_initial_telemetry(self):
        disasters = disaster_engine.get_all()
        for d in disasters:
            if d.type.value == "wildfire":
                self._telemetry_stream.append(
                    SensorTelemetry(
                        sensor_id=f"SENS-WF-{d.id}",
                        station_name=f"{d.location.region} Smoke/Thermal Node",
                        latitude=d.location.latitude + 0.02,
                        longitude=d.location.longitude + 0.02,
                        sensor_type="smoke_thermal",
                        reading=d.impact.air_quality_index or 280.0,
                        unit="AQI",
                        status="critical"
                    )
                )
            elif d.type.value == "earthquake":
                self._telemetry_stream.append(
                    SensorTelemetry(
                        sensor_id=f"SENS-SEIS-{d.id}",
                        station_name=f"{d.location.region} Seismograph 03",
                        latitude=d.location.latitude - 0.01,
                        longitude=d.location.longitude - 0.01,
                        sensor_type="seismic",
                        reading=d.impact.seismic_magnitude or 7.1,
                        unit="Richter",
                        status="critical"
                    )
                )
            elif d.type.value == "flood":
                self._telemetry_stream.append(
                    SensorTelemetry(
                        sensor_id=f"SENS-FL-{d.id}",
                        station_name=f"{d.location.region} River Depth Gauge",
                        latitude=d.location.latitude + 0.01,
                        longitude=d.location.longitude - 0.02,
                        sensor_type="water_gauge",
                        reading=d.impact.flood_depth_meters or 2.5,
                        unit="Meters",
                        status="warning"
                    )
                )

    def get_latest_telemetry(self) -> List[SensorTelemetry]:
        return self._telemetry_stream[-20:]

    def step_simulation(self) -> Dict[str, Any]:
        updated = []
        for sensor in self._telemetry_stream:
            delta = random.uniform(-0.5, 0.6)
            sensor.reading = round(max(0.1, sensor.reading + delta), 2)
            sensor.timestamp = datetime.now(timezone.utc)
            updated.append(sensor.model_dump())
        return {"updated_count": len(updated), "timestamp": datetime.now(timezone.utc).isoformat()}

simulation_service = SimulationService()
