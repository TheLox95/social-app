
from pydantic import BaseModel, ConfigDict, field_validator


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
