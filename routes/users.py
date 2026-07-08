from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from db import db
from models.User import User
from services.auth import get_token_data

router = APIRouter(tags=["auth"])

@router.get("/profile")
def login(usr: dict[str, int] = Depends(get_token_data), driver: Session = Depends(db.get_db)):
    user = driver.query(User).where(User.id == usr.get("id")).first()

    return user
