from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_disasters():
    response = client.get("/api/v1/disasters")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4

def test_get_disaster_by_id():
    response = client.get("/api/v1/disasters/DIS-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "DIS-001"
    assert data["type"] == "wildfire"

def test_get_resources():
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 8

def test_coordination_recommendations():
    response = client.get("/api/v1/coordination/recommendations/DIS-001")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_allocations" in data
    assert len(data["recommended_allocations"]) > 0

def test_coordination_dispatch():
    rec_resp = client.get("/api/v1/coordination/recommendations/DIS-002")
    resource_id = rec_resp.json()["recommended_allocations"][0]["resource_id"]

    dispatch_resp = client.post("/api/v1/coordination/dispatch", json={
        "disaster_id": "DIS-002",
        "resource_ids": [resource_id],
        "notes": "Fast deployment via API test"
    })
    assert dispatch_resp.status_code == 200
    assert dispatch_resp.json()["success"] is True

def test_analytics_summary():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_casualties_at_risk" in data
    assert "hazard_distribution" in data

def test_simulation_endpoints():
    tick_resp = client.post("/api/v1/simulation/tick")
    assert tick_resp.status_code == 200

    telem_resp = client.get("/api/v1/simulation/telemetry")
    assert telem_resp.status_code == 200
    assert isinstance(telem_resp.json(), list)

    inject_resp = client.post("/api/v1/simulation/inject-scenario?scenario_type=severe_weather")
    assert inject_resp.status_code == 200
    assert inject_resp.json()["status"] == "injected"
