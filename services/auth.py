
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_token_data(token: str = Depends(oauth2_scheme)) -> dict[str, int]:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="App is not ready")

    try:
        payload = jwt.decode(token, secret, algorithms=[ "HS256" ])
        user_id = payload.get("id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

        token_type = payload.get("token_type")

        if token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return {"id": user_id}
