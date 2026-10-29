from fastapi import Depends, HTTPException
from datetime import datetime, timezone, timedelta
from utils.config import get_secret, ALGORITHM
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


def create_access_token(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc)+timedelta(hours=1)
    }

    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_valid_user_id(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):

    unauthorised = HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorised

    try:
        payload = jwt.decode(credentials.credentials, get_secret(), [ALGORITHM])
        user_id = int(payload["sub"])
    except:
        raise unauthorised
    return user_id