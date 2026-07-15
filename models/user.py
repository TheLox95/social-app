from datetime import datetime
from typing import List
from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import db

from .post import Post
from .user_following import UserFollowing
from .user_blocking import UserBlocking

class User(db.DBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    fullname: Mapped[str] = mapped_column(String(35))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(String(18), unique=True)

    posts: Mapped[list['Post']] = relationship("Post",back_populates="user", passive_deletes=True)
    followed_by: Mapped[List['UserFollowing']] = relationship("UserFollowing", foreign_keys=[UserFollowing.follower_user_id])
    following: Mapped[List['UserFollowing']] = relationship("UserFollowing", foreign_keys=[UserFollowing.following_user_id])

    blocked_by: Mapped[List['UserBlocking']] = relationship("UserBlocking", foreign_keys=[UserBlocking.blocking_user_id])

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

