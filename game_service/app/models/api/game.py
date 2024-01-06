from pydantic import BaseModel, Field
from datetime import datetime


class GameModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    board_size: int = Field(gt=0)

    ...

    admin_id: int = Field(gt=0)
    dt_start: datetime = None


class GameKey(BaseModel):
    player_id: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)
