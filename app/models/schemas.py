from pydantic import BaseModel, EmailStr
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterUser(BaseModel):
  name: str
  email: str
  password: str

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class UserRegistered(BaseModel):
    user: User


class Rsvp(BaseModel):
    id: int
    attendee_id: int
    event_id: int
    created_at: datetime

class RsvpResponse(BaseModel):
    rsvp: Rsvp

class CreateEvent(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int


class Event(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int
    organiser_id: int
    created_at: datetime

class EventCreated(BaseModel):
    event: Event