from backend.app.services.disaster_engine import DisasterEngine, haversine_distance
from backend.app.models.disaster import DisasterEvent, DisasterType, DisasterSeverity, GeoLocation, EnvironmentalImpact

def test_haversine_distance():
    dist = haversine_distance(37.7749, -122.4194, 37.8044, -122.2712)
    assert 10.0 <= dist <= 16.0

def test_calculate_risk_score_scaling():
    engine = DisasterEngine()
    low_event = DisasterEvent(
        id="TEST-LOW",
        title="Minor Brush Fire",
        type=DisasterType.WILDFIRE,
        severity=DisasterSeverity.LOW,
        location=GeoLocation(latitude=37.0, longitude=-120.0),
        radius_km=1.0,
        impact=EnvironmentalImpact(estimated_casualties_at_risk=0)
    )
    high_event = DisasterEvent(
        id="TEST-HIGH",
        title="Catastrophic Quake",
        type=DisasterType.EARTHQUAKE,
        severity=DisasterSeverity.CATASTROPHIC,
        location=GeoLocation(latitude=37.0, longitude=-120.0),
        radius_km=50.0,
        impact=EnvironmentalImpact(estimated_casualties_at_risk=50000, seismic_magnitude=8.2)
    )
    score_low = engine.calculate_risk_score(low_event)
    score_high = engine.calculate_risk_score(high_event)
    assert score_low < score_high
    assert score_high >= 90.0

def test_crud_disaster():
    engine = DisasterEngine()
    initial_count = len(engine.get_all())
    new_event = DisasterEvent(
        id="TEST-NEW",
        title="Testing Flood Event",
        type=DisasterType.FLOOD,
        severity=DisasterSeverity.MODERATE,
        location=GeoLocation(latitude=30.0, longitude=-90.0),
        radius_km=10.0,
        required_capabilities=["swift_water_rescue"]
    )
    engine.create_disaster(new_event)
    assert len(engine.get_all()) == initial_count + 1

    updated = engine.update_disaster("TEST-NEW", {"title": "Updated Flood Event", "radius_km": 15.0})
    assert updated.title == "Updated Flood Event"
    assert updated.radius_km == 15.0
