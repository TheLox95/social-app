
from pydantic import UUID7, BaseModel, Field, field_validator

class SuccessResponse(BaseModel):
    success: bool = True

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

