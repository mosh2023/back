from pydantic import BaseModel, Field
import enum


class Roles(enum.Enum):
    user = 1
    admin = 2


class AuthModel(BaseModel):
    id: int = Field(gt=0, default=None)
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: Roles


class AuthCreateRequest(BaseModel):
    login: str = Field(..., example="user123", description="Логин пользователя")
    password: str = Field(..., example="strongpassword", description="Пароль пользователя")
    role: str = Field(..., example="user", description="Роль пользователя")


class AuthRequest(BaseModel):
    login: str = Field(..., example="user123", description="Логин пользователя")
    password: str = Field(..., example="strongpassword", description="Пароль пользователя")


class AuthResponse(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    login: str = Field(..., example="user123", description="Логин пользователя")
    role: str = Field(..., example="user", description="Роль пользователя")

    class Config:
        orm_mode = True
