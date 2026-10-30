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



