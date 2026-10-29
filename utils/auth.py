from datetime import datetime, timezone, timedelta
from utils.config import get_secret, ALGORITHM
import jwt


def create_access_token(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc)+timedelta(hours=1)
    }

    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)