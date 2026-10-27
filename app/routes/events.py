from fastapi import APIRouter
from db.queries import list_events

events_router = APIRouter(prefix="/events")

@events_router.get("/")
def get_events():
    events = list_events()

    return {"events": events}
    