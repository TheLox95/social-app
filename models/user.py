from datetime import datetime
import typing
from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import db

from .post import Post

class User(db.DBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    fullname: Mapped[str] = mapped_column(String(35))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(String(18), unique=True)

    posts: Mapped[list['Post']] = relationship("Post",back_populates="user", passive_deletes=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

