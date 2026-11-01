from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.models.events import list_events, get_one_event, create_event, change_event, get_event_organiser, list_attendees
from utils.auth import get_current_valid_user_id
from app.models.schemas import RsvpResponse, CreateEvent, EventCreated, ChangeEvent, EventChanged, AttendeesResponse
from app.models.rsvps import create_rsvp, get_rsvp, delete_rsvp

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

@events_router.delete("/{event_id}/rsvp/me", status_code=204)
def user_cancels_rsvp(event_id:int, user_id: int = Depends(get_current_valid_user_id)):
    deleted = delete_rsvp(user_id, event_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "RSVP not found"},
        )
    return None

@events_router.post("/", status_code=201, response_model=EventCreated)
def user_creates_event(body:CreateEvent, organiser_id: int = Depends(get_current_valid_user_id)): 

    event = create_event(
        body.title, 
        body.description, 
        body.starts_at, 
        body.ends_at, 
        body.venue_id, 
        organiser_id
    )

    return {"event": event}


@events_router.patch("/{event_id}", response_model=EventChanged)
def user_changes_event(event_id: int, body: ChangeEvent, user_id: int = Depends(get_current_valid_user_id)):
    event = get_one_event(event_id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "Event not found"},
        )
    
    
    event_organiser = get_event_organiser(event_id)

    if event_organiser["organiser_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail={"code": "Forbidden", "message": "You do not have access to change this event"},
        ) 

    if body.starts_at is not None and body.ends_at is not None and body.starts_at >= body.ends_at: 
         raise HTTPException(
            status_code=400,
            detail={"code": "Bad Request", "message": "Start time cannot be after end time"},
        )

    if body.starts_at is not None and body.ends_at is None and body.starts_at >= event["ends_at"]:
        raise HTTPException(
            status_code=400,
            detail={"code": "Bad Request", "message": "Start time cannot be after end time"},
        )
    if body.starts_at is None and body.ends_at is not None and event["starts_at"] >= body.ends_at:
        raise HTTPException(
            status_code=400,
            detail={"code": "Bad Request", "message": "Start time cannot be after end time"},
        )
       
    updated_event = change_event(event_id, body.description, body.starts_at, body.ends_at)

    return {"event": updated_event} 


@events_router.get("/{event_id}/attendees", response_model=AttendeesResponse)
def get_event_attendees(event_id:int, user_id: int = Depends(get_current_valid_user_id)):
    
    event_organiser = get_event_organiser(event_id)
    
    if event_organiser["organiser_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail={"code": "Forbidden", "message": "You do not have access to this attendee list"},
        )

    attendees = list_attendees(event_id) 

    return {"attendees": attendees}