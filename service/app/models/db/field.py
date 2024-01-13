from pydantic import BaseModel, Field


class FieldDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
    injured: bool
    player_id: int = Field(gt=0, default=None)
    boat_id: int = Field(gt=0, default=None)
