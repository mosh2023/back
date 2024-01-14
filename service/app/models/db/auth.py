import enum
from pydantic import BaseModel, Field


class Roles(enum.Enum):
    user = 1
    admin = 2


class AuthDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: Roles
