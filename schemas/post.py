
from typing import List

from pydantic import UUID7, BaseModel, ConfigDict, Field, field_validator

class SuccessResponse(BaseModel):
    success: bool = True

class LikeResponse(BaseModel):
    id: int

class PostListResponse(BaseModel):
    id: UUID7
    content: str
    likes: List[LikeResponse]
    comments: List[LikeResponse]

    model_config = ConfigDict(from_attributes=True)


class CreatePostRequest(BaseModel):
    content: str = Field()
    
    @field_validator("content")
    @classmethod
    def clean_content(cls, content: str) -> str:
        return content.strip()


class UpdatePostRequest(BaseModel):
    content: str
    id: UUID7
    
    @field_validator("content")
    @classmethod
    def clean_content(cls, content: str) -> str:
        return content.strip()

class DeletePostRequest(BaseModel):
    id: UUID7

class LikePostRequest(BaseModel):
    post_id: UUID7

class CommentPostRequest(BaseModel):
    post_id: UUID7
    content: str

    @field_validator("content")
    @classmethod
    def clean_content(cls, content: str):
        return content.strip()

