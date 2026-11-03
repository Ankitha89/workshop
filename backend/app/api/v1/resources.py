from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.models.resource import EmergencyResource
from backend.app.services.ai_optimizer import ai_optimizer

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("", response_model=List[EmergencyResource])
def list_resources(
    status: Optional[str] = Query(None, description="Filter by status (available, en_route, deployed, etc.)"),
    resource_type: Optional[str] = Query(None, description="Filter by type")
):
    return ai_optimizer.get_all_resources(status=status, resource_type=resource_type)

@router.get("/{resource_id}", response_model=EmergencyResource)
def get_resource(resource_id: str):
    res = ai_optimizer.get_by_id(resource_id)
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    return res
