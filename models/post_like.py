from datetime import datetime

from sqlalchemy import VARCHAR, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class PostLike(db.DBModel):
    __tablename__ = "post_likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="cascade"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

