from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.models.events import list_events, get_one_event

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