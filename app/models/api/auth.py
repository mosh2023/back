from pydantic import BaseModel, Field
from typing import Optional
import enum


class Roles(enum.Enum):
    user = "user"
    admin = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: Roles

    class Config:
        use_enum_values = True


class AuthInfo(BaseModel):
    login: str = Field(min_length=3, max_length=50, example="user123", description="Логин пользователя")
    password: str = Field(min_length=8, max_length=128, example="strongpassword", description="Пароль пользователя")
    role: Roles

    class Config:
        use_enum_values = True


class AuthRequest(BaseModel):
    login: str = Field(min_length=3, max_length=50, example="user123", description="Логин пользователя")
    password: str = Field(min_length=8, max_length=128, example="strongpassword", description="Пароль пользователя")

    class Config:
        use_enum_values = True


class AuthResponse(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    user_id: int = Field(..., example=1, description="User ID пользователя")
    login: str = Field(min_length=3, max_length=50, example="user123", description="Логин пользователя")
    role: Roles

    class Config:
        use_enum_values = True
        from_attributes = True
