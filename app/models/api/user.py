from pydantic import BaseModel, Field
from typing import Optional


class UserModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: Optional[str] = None


class UserInfo(BaseModel):
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: Optional[str] = None


class UserEdit(BaseModel):
    id: int = Field(gt=0)
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    icon_link: Optional[str] = None

