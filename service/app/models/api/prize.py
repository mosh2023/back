from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PrizeModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    icon_link: Optional[str] = None
    admin_id: int = Field(gt=0)
    user_id: Optional[int] = Field(gt=0, default=None)
    dt_won: Optional[datetime] = None


class PrizeInfo(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    icon_link: Optional[str] = None
    admin_id: int = Field(gt=0)


class PrizeEdit(BaseModel):
    id: int = Field(gt=0)
    name: Optional[str] = Field(min_length=3, max_length=50, default=None)
    description: Optional[str] = None
    icon_link: Optional[str] = None
