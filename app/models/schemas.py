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


class ChangeEvent(BaseModel):
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None

class EventChanged(BaseModel):
    event: Event


class Attendee(BaseModel):
    id: int
    name: str
    email: EmailStr

class AttendeesResponse(BaseModel):
    attendees: list[Attendee]

class MyRsvpEvent(BaseModel):
    id: int
    title: str
    starts_at: datetime
    rsvp_date: datetime
    event_rank: int
    total_rsvps: int

class MyRsvpEventsResponse(BaseModel):
    events: list[MyRsvpEvent]


class OrganiserStats(BaseModel):
    organiser_id: int
    name: str
    total_events: int
    avg_attendance: float
    best_attended_count: int
    organiser_rank: int

class OrganiserStatsResponse(BaseModel):
    stats: OrganiserStats