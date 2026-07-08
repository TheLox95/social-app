
import os

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import db
from models.User import User
from services.auth import get_token_data

router = APIRouter(tags=["auth"])

@router.get("/profile")
def login(usr: dict[str, int] = Depends(get_token_data)):
    with Session(db.engine) as session:
        query = select(User).where(User.id == usr.get("id"))

        user = session.scalars(query).first()

        return user
