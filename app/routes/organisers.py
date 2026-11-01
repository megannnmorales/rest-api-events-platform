from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.models.schemas import OrganiserStatsResponse
from app.models.organisers import get_organiser_stats


organisers_router = APIRouter(prefix="/api/organisers")

@organisers_router.get("/{organiser_id}/stats", response_model=OrganiserStatsResponse)
def get_organisers(organiser_id:int):

    stats = get_organiser_stats(organiser_id)
    if stats is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "User does not exist or has no events"},
        )
    
    return {"stats": stats}