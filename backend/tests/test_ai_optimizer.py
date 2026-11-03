from backend.app.services.ai_optimizer import AiResourceOptimizer
from backend.app.services.disaster_engine import DisasterEngine
from backend.app.models.resource import EmergencyResource, ResourceType, ResourceStatus
from backend.app.models.disaster import DisasterEvent, DisasterType, DisasterSeverity, GeoLocation

def test_ai_optimizer_recommendations():
    optimizer = AiResourceOptimizer()
    recs = optimizer.recommend_allocations("DIS-001")
    assert recs is not None
    assert recs.disaster_id == "DIS-001"
    assert len(recs.recommended_allocations) > 0

    scores = [item.match_score for item in recs.recommended_allocations]
    assert scores == sorted(scores, reverse=True)

def test_ai_optimizer_dispatch():
    optimizer = AiResourceOptimizer()
    recs = optimizer.recommend_allocations("DIS-001")
    top_resource_id = recs.recommended_allocations[0].resource_id

    result = optimizer.dispatch_resources("DIS-001", [top_resource_id], notes="Test dispatch")
    assert result.success is True
    assert result.dispatched_count == 1
    assert result.mission_id.startswith("MSN-")

    res = optimizer.get_by_id(top_resource_id)
    assert res.status == ResourceStatus.DEPLOYED
    assert res.target_disaster_id == "DIS-001"
