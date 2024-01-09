from pydantic import BaseModel, Field
from datetime import datetime


class GameModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    board_size: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)

    player_id: int = Field(gt=0, default=None)
    player_moves: int = Field(gt=-1, default=None)

    admin_id: int = Field(gt=0)
    dt_start: datetime = None


class GameInfo(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    board_size: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)  # Генерируется на фронте?
    admin_id: int = Field(gt=0)


class GameEdit(BaseModel):
    name: str = Field(min_length=3, max_length=50, default=None)
    description: str = None
    board_size: int = Field(gt=0, default=None)


class GameKey(BaseModel):
    player_id: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)


class GameMoves(BaseModel):
    id: int = Field(gt=0)
    player_id: int = Field(gt=0)
    add_moves: int = Field(gt=0)
