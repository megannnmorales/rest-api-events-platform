from datetime import datetime, timezone, timedelta
from utils.config import get_secret
import jwt

ALGORITHM = "HS256"

def create_access_token(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc)+timedelta(hours=1)
    }

    jwt.encode(payload, get_secret(), algorithm=ALGORITHM)