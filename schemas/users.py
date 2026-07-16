
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer, field_validator

from models.app_notification import NotificationKind


class MessageUserRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def clean_content(cls, content: str) -> str:
        return content.strip()

class MessageListResponse(BaseModel):
    sender_user_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)

class NotificationsResponse(BaseModel):
    event_type: Annotated[NotificationKind, PlainSerializer(lambda v: v.name, return_type=str)]
    author_id: int
    resource_id: str
    is_read: bool

    model_config = ConfigDict(from_attributes=True)
