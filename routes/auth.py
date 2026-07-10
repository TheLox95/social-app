from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import User
from db import db
from schemas.auth import LoginRequest, RegisterRequest
from pwdlib import PasswordHash
from services.user import find_users, FindUsersParams
import asyncio
import jwt
import os

REFRESH_TOKEN_EXPIRE_MINUTES = 15

router = APIRouter(tags=["auth"])

password_hash = PasswordHash.recommended()


@router.post("/login")
def login(body: LoginRequest):
    with Session(db.engine) as session:
        query = select(User).where(User.email == body.email)
        user = session.scalars(query).first()
        if not user:
            raise HTTPException(status_code=404, detail="Credentials not found")

        if not password_hash.verify(body.password.get_secret_value(), user.password):
            raise HTTPException(status_code=401, detail="Credentials not found")

        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise HTTPException(status_code=500, detail="App is not ready")

        token_expire = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
        payload = {"id": user.id, "token_type": "access", "exp": token_expire}
        access_token = jwt.encode(payload, secret, algorithm="HS256")

        token_expire = datetime.now(timezone.utc) + timedelta(days=7)
        payload = {"id": user.id, "token_type": "refresh", "exp": token_expire}
        refresh_token = jwt.encode(payload, secret, algorithm="HS256")

        env = os.getenv("ENV", "DEV")
        res = JSONResponse(content={"access_token": access_token})
        expires = 60 * 60 * 24 * 7  # 7 days
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=env != "DEV",
            secure=env != "DEV",
            samesite="lax",
            max_age=expires,
            expires=expires,
        )

        return res


@router.post("/register")
async def register(body: RegisterRequest):
    session = next(db.get_db())
    task = [
        find_users(FindUsersParams(username=body.username), session),
        find_users(FindUsersParams(email=body.email), session),
    ]

    results = await asyncio.gather(*task)
    by_username = results[0].first()
    if by_username is not None:
        raise HTTPException(status_code=400, detail="Username already used")

    by_email = results[1].first()
    if by_email is not None:
        raise HTTPException(status_code=400, detail="Email already used")

    hashed_password = password_hash.hash(body.password.get_secret_value())
    u = User(
        fullname=body.fullname,
        email=body.email,
        password=hashed_password,
        username=body.username,
    )

    session.add(u)
    session.commit()

    return {"success": True}


@router.get("/refresh")
def refresh_token(refresh_token: Annotated[str | None, Cookie()] = None):
    secret = os.getenv("JWT_SECRET")
    if secret is None:
        raise HTTPException(status_code=500, detail="App is not ready")
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Missing refresh_token")

    try:
        usr = jwt.decode(refresh_token, secret, algorithms="HS256")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    token_expire = datetime.now(timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )
    payload = {"id": usr.get("id"), "token_type": "access", "exp": token_expire}
    access_token = jwt.encode(payload, secret, algorithm="HS256")

    res = JSONResponse(content={"access_token": access_token})
    return res
