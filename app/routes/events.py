from fastapi import APIRouter
from db.queries import list_events, get_one_event

events_router = APIRouter(prefix="/events")

@events_router.get("/")
def get_events():
    events = list_events()

    return {"events": events}


@events_router.get("/{id}")
def get_events(id):
    event = get_one_event(id)

    return {"event": event}