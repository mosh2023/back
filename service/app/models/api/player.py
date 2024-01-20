from pydantic import BaseModel, Field
from typing import Optional


class PlayerModel(BaseModel):
    id: Optional[int] = Field(gt=0, default=None)
    user_id: int = Field(gt=0)
    remaining_moves: int = Field(gt=-1)
    used_moves: int = Field(gt=-1)


class PlayerMoves(BaseModel):
    id: int = Field(gt=0)
    moves: int = Field(gt=0)
