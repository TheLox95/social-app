import re

from typing_extensions import Self
from pydantic import BaseModel, EmailStr, SecretStr, field_validator, model_validator, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator("email", mode="before")
    @classmethod
    def clean_email(cls, email: EmailStr) -> EmailStr:
        return email.strip().lower()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: SecretStr
    confirmPassword: SecretStr
    fullname: str = Field(max_length=12)
    username: str = Field(max_length=12)

    @field_validator('fullname', mode='before')
    @classmethod
    def sanitize_fullname(cls, fullname: str) -> str:
        return fullname.strip()

    @field_validator('username', mode='before')
    @classmethod
    def sanitize_username(cls, username: str) -> str:
        return username.strip()

    @field_validator('email', mode='before')
    @classmethod
    def sanitize_email(cls, email: EmailStr) -> EmailStr:
        return email.strip().lower()

    @field_validator('password', mode='after')
    @classmethod
    def valid_password(cls, password: SecretStr) -> SecretStr:
        raw_password = password.get_secret_value()

        if not re.search(r'[A-Z]', raw_password) or not re.search(r'[0-9]', raw_password):
            raise ValueError('Password must contain uppercase letter and a number')

        return password

    @model_validator(mode='after')
    def password_match(self) -> Self:
        if self.password.get_secret_value() != self.confirmPassword.get_secret_value():
            raise ValueError("Password does not match")

        return self
