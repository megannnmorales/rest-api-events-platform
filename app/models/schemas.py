from pydantic import BaseModel, EmailStr
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Rsvp(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime

class RsvpResponse(BaseModel):
    rsvp: Rsvp



