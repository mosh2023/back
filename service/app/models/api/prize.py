from pydantic import BaseModel, Field
from datetime import datetime


class PrizeModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    icon_link: str = None
    admin_id: int = Field(gt=0)
    user_id: int = Field(gt=0, default=None)
    dt_won: datetime = None


class PrizeInfo(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    icon_link: str = None
    admin_id: int = Field(gt=0)


class PrizeEdit(BaseModel):
    name: str = Field(min_length=3, max_length=50, default=None)
    description: str = None
    icon_link: str = None
