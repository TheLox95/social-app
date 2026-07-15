from datetime import datetime
import typing
from sqlalchemy import VARCHAR, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped
from db import db

if typing.TYPE_CHECKING:
    from user import User


class DirectMessage(db.DBModel):
    __tablename__ = "direct_message"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")

    sender_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    receiver_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    content: Mapped[str] = mapped_column(VARCHAR(), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
