from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from db import db

router = APIRouter()

@router.get("/login", tags=["auth"])
def login():
    with Session(db.engine) as session:
        u = User.User(name="joe", fullname="joe doe")

        session.add(u)
        session.commit()


        query = select(User.User).order_by(User.User.id)
        rows = session.scalars(query).all()

        return rows
