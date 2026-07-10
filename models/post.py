
from datetime import datetime
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID, VARCHAR

from db import db


class Post(db.DBModel):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    content: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped['User'] = relationship(back_populates="posts", single_parent=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    class Config:
        from_attributes = True
