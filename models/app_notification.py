from datetime import datetime
import enum
from sqlalchemy import Boolean, ForeignKey, Index, String, func, Enum
from sqlalchemy.orm import mapped_column, Mapped
from db import db

class NotificationKind(enum.Enum):
    POST=0
    COMMENT=1
    LIKE=2
    DM=3
    FOLLOW=4


class AppNotification(db.DBModel):
    __tablename__ = "app_notification"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")

    event_type: Mapped[str] = mapped_column(Enum(NotificationKind), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    resource_id: Mapped[str] = mapped_column(String())
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    is_read: Mapped[bool] = mapped_column(Boolean, default=True, server_default="false")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uix_author_event_resource", "event_type", "author_id", "resource_id",unique=True
        ),
    )

