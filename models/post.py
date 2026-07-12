
from datetime import datetime
import typing
import uuid

from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID, VARCHAR

from db import db

if typing.TYPE_CHECKING:
    from .user import User
    from .post_comment import PostComment
    from .post_like import PostLike

class Post(db.DBModel):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), server_default=text("uuidv7()"), primary_key=True)
    content: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    user: Mapped['User'] = relationship("User",back_populates="posts", single_parent=True)

    comments: Mapped[list['PostComment']] = relationship("PostComment")
    likes: Mapped[list['PostLike']] = relationship("PostLike")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    class Config:
        from_attributes = True
