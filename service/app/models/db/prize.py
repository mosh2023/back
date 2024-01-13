from pydantic import BaseModel, Field
from datetime import datetime


class PrizeDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    icon_link: str = None
    admin_id: int = Field(gt=0)
    user_id: int = Field(gt=0, default=None)
    dt_won: datetime = None
