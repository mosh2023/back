from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    remaining_moves: int = Field(gt=-1)
    used_moves: int = Field(gt=-1)
