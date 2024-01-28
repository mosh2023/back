from pydantic import BaseModel, Field
from typing import Optional

from .boat import BoatModel
from .prize import PrizeModel


class FieldModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
    injured: bool
    player_id: Optional[int] = Field(gt=0, default=None)
    boat_id: Optional[int] = Field(gt=0, default=None)


class FieldSecureModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
    injured: bool
    player_id: Optional[int] = Field(gt=0, default=None)


class FullFieldModel(BaseModel):
    field: FieldModel
    boat: Optional[BoatModel] = None
    prize: Optional[PrizeModel] = None


class Hit(BaseModel):
    player_id: int = Field(gt=0)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
