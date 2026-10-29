from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.models.events import list_events, get_one_event
from utils.auth import get_current_valid_user_id
from app.models.schemas import RsvpResponse
from app.models.rsvps import create_rsvp

events_router = APIRouter(prefix="/api/events")

@events_router.get("/")
def get_events():
    events = list_events()

    return {"events": events}


@events_router.get("/{id}")
def get_event(id:int):
    event = get_one_event(id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "Event not found"},
        )

    return {"event": event}


@events_router.post("/{id}/rsvp", dependencies=[Depends(get_current_valid_user_id)], response_model=RsvpResponse)
def user_rsvp_to_event(id:int, user_id: int = Depends(get_current_valid_user_id,)):
    rsvp = create_rsvp(user_id, id)
    
    return {"rsvp":rsvp}