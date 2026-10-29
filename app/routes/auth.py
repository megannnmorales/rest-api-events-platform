from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.models.schemas import LoginRequest
from utils.passwords import verify_password
from app.models.users import get_user
from utils.auth import create_access_token

auth_router = APIRouter(prefix="/api/auth")

@auth_router.post("/login")
def login(body: LoginRequest):

    user = get_user(body.email)

    if verify_password(body.password, user["hashed_password"]):
        return {
            "access_token": create_access_token(user["id"]),
            "token_type": "bearer"
        }
    return "hello"