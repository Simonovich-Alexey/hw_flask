from abc import ABC
import pydantic
from typing import Optional
import re


class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    email: Optional[str] = None
    password: str

    @pydantic.field_validator('password')
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f'Minimal length of password is 8')
        return v

    @pydantic.field_validator('email')
    @classmethod
    def valid_email(cls, email: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError(f'invalid email format')
        return email


class CreateUser(AbstractUser):
    name: str
    email: str
    password: str


class LoginUser(AbstractUser):
    pass


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class CreateAd(pydantic.BaseModel):
    title: str
    description: str


class UpdateAd(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
