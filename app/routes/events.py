from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.models.events import list_events, get_one_event
from utils.auth import get_current_valid_user_id
from app.models.schemas import RsvpResponse
from app.models.rsvps import create_rsvp, get_rsvp

events_router = APIRouter(prefix="/api/events")

@events_router.get("/")
def get_events():
    events = list_events()

    return {"events": events}


@events_router.get("/{event_id}")
def get_event(event_id:int):
    event = get_one_event(event_id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "Event not found"},
        )

    return {"event": event}


@events_router.post("/{event_id}/rsvp", status_code=201, response_model=RsvpResponse)
def user_rsvp_to_event(event_id:int, user_id: int = Depends(get_current_valid_user_id)):
    event = get_one_event(event_id)
    if event is None:
        raise HTTPException(
        status_code=404,
        detail={"code": "Not Found", "message": "Event not found"},
        )

    rsvp = get_rsvp(user_id, event_id)
    if rsvp is not None:  
        raise HTTPException(
        status_code=409,
        detail={"code": "Conflict", "message": "Duplicate RSVP"},
        )
    
    rsvp = create_rsvp(user_id, event_id)
    return {"rsvp":rsvp}