from datetime import datetime
import typing
from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import db

if typing.TYPE_CHECKING:
    from user import User


class UserFollowing(db.DBModel):
    __tablename__ = "users_following"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")

    following_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    followed: Mapped['User'] = relationship("User", foreign_keys=[following_user_id])
    follower_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    follower: Mapped['User'] = relationship("User", foreign_keys=[follower_user_id])


    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uix_following_follower_users", "following_user_id", "follower_user_id", unique=True
        ),
    )
