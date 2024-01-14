from pydantic import BaseModel, Field
from datetime import datetime


class GameDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    name: str = Field(min_length=3, max_length=50)
    description: str = None
    board_size: int = Field(gt=0)
    key: str = Field(min_length=4, max_length=10)

    player1_id: int = Field(gt=0, default=None)
    player2_id: int = Field(gt=0, default=None)

    admin_id: int = Field(gt=0)
    dt_start: datetime = None
