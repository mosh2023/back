from pydantic import BaseModel, Field


class Hit(BaseModel):
    player_id: int = Field(gt=0)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
