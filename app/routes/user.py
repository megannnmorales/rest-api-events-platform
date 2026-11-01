from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from utils.auth import get_current_valid_user_id
from app.models.schemas import MyRsvpEventsResponse
from app.models.users import list_user_rsvps

user_router = APIRouter(prefix="/api/user")

@user_router.get("/me/events", response_model=MyRsvpEventsResponse)
def get_users_own_list_of_events(user_id: int = Depends(get_current_valid_user_id)):
    my_list_of_events = list_user_rsvps(user_id)
    
    return {"events": my_list_of_events}