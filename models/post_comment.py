from datetime import datetime

from sqlalchemy import VARCHAR, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class PostComment(db.DBModel):
    __tablename__ = "post_comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(VARCHAR(256), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="cascade"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"), nullable=False)
    parent_comment_id: Mapped[int | None] = mapped_column(ForeignKey("post_comments.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

