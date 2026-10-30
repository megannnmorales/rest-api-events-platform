from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.models.schemas import LoginRequest, Token, RegisterUser, UserRegistered
from utils.passwords import hash_password, verify_password
from app.models.users import get_user_by_email, create_user
from utils.auth import create_access_token

auth_router = APIRouter(prefix="/api/auth")

unauthorised = HTTPException(
    status_code=401,
    detail={"code": "Unauthorized", "message": "Invalid email or password"},
)

@auth_router.post("/login", response_model=Token)
def login(body: LoginRequest):

    user = get_user_by_email(body.email)

    if user is None:
        raise unauthorised
    
    if verify_password(body.password, user["hashed_password"]):
        return {
            "access_token": create_access_token(user["id"]),
            "token_type": "bearer"
        }
    
    raise unauthorised

@auth_router.post("/register", status_code=201, response_model=UserRegistered)
def register_new_user(body: RegisterUser):

    user = get_user_by_email(body.email)
    if user is not None:  
        raise HTTPException(
        status_code=409,
        detail={"code": "Conflict", "message": "Email already registered"},
        )
    
    hashed_password = hash_password(body.password)
    
    user = create_user(body.name, body.email, hashed_password)

    return {"user":user}

