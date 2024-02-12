from pydantic import BaseModel, Field
from typing import Optional


class BoatModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    prize_id: int = Field(gt=0)


class BoatInfo(BaseModel):
    prize_id: int = Field(gt=0)


class BoatPlace(BaseModel):
    boat_id: int = Field(gt=0)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
