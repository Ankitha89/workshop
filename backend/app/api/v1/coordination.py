from fastapi import APIRouter, HTTPException
from backend.app.models.allocation import OptimizationRecommendation, DispatchRequest, DispatchExecutionResult
from backend.app.services.ai_optimizer import ai_optimizer

router = APIRouter(prefix="/coordination", tags=["Coordination & Dispatch"])

@router.get("/recommendations/{disaster_id}", response_model=OptimizationRecommendation)
def get_recommendations(disaster_id: str):
    recommendation = ai_optimizer.recommend_allocations(disaster_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Disaster not found or unavailable")
    return recommendation

@router.post("/dispatch", response_model=DispatchExecutionResult)
def dispatch_resources(request: DispatchRequest):
    result = ai_optimizer.dispatch_resources(
        disaster_id=request.disaster_id,
        resource_ids=request.resource_ids,
        notes=request.notes
    )
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result
