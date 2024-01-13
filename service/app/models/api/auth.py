from pydantic import BaseModel, Field


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
