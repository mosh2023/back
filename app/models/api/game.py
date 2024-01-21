from pydantic import BaseModel, Field
from .player import PlayerModel
from datetime import datetime
from typing import Optional


class GameAPIModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    board_size: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)

    player1: Optional[PlayerModel] = None
    player2: Optional[PlayerModel] = None

    admin_id: int = Field(gt=0)
    dt_start: Optional[datetime] = None


class GameModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    board_size: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)

    player1_id: Optional[int] = Field(gt=0, default=None)
    player2_id: Optional[int] = Field(gt=0, default=None)
    
    admin_id: int = Field(gt=0)
    dt_start: Optional[datetime] = None


class GameInfo(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = None
    board_size: int = Field(gt=0)
    admin_id: int = Field(gt=0)

    # Ключ создается в бизнес логике автоматом. Его надо возвращать.


class GameEdit(BaseModel):
    id: int = Field(gt=0)
    name: Optional[str] = Field(min_length=3, max_length=50, default=None)
    description: Optional[str] = None
    board_size: Optional[int] = Field(gt=0, default=None)


class GameKey(BaseModel):
    user_id: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)

