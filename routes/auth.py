from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.User import User
from db import db
from schemas.Auth import LoginRequest, RegisterRequest
from pwdlib import PasswordHash
import jwt
import os

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

        token_expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload = { "id": user.id, "token_type": "access", "exp": token_expire }
        access_token = jwt.encode(payload, secret, algorithm="HS256")

        token_expire = datetime.now(timezone.utc) + timedelta(days=7)
        payload = { "id": user.id, "token_type": "refresh", "exp": token_expire }
        refresh_token = jwt.encode(payload, secret, algorithm="HS256")

        env = os.getenv("ENV", "DEV")
        res = JSONResponse(content={"access_token": access_token})
        expires = 60 * 60 * 24 * 7 #7 days
        res.set_cookie(key="refresh_token", value=refresh_token , httponly= env != "DEV", secure=env != "DEV", samesite="lax", max_age=expires , expires=expires )

        return res

@router.post("/register")
def register(body: RegisterRequest):
    with Session(db.engine) as session:
        query = select(User).where(User.username == body.username)
        found = session.scalars(query).first()
        if found is not None:
            raise HTTPException(status_code=400, detail="User already registered")

        hashed_password = password_hash.hash(body.password.get_secret_value())
        u = User(fullname=body.fullname, email=body.email, password=hashed_password, username=body.username)

        session.add(u)
        session.commit()

        return { "success": True }
