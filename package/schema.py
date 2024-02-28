from abc import ABC
import pydantic
from typing import Optional


class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    email: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f'Minimal length of password is 8')
        return v


class CreateUser(AbstractUser):
    name: str
    email: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class CreateAd(pydantic.BaseModel):
    title: str
    description: str
    owner: int


class UpdateAd(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[int] = None
