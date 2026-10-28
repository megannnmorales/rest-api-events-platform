from pydantic import BaseModel, EmailStr

class UserAuthenticate(BaseModel):
    email: EmailStr
    password: str