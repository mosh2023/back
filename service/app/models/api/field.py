from pydantic import BaseModel, Field


class FieldModel(BaseModel):
    id: int = Field(gt=0)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
    injured: bool
    player_id: int = Field(gt=0, default=None)
    boat_id: int = Field(gt=0, default=None)


class Hit(BaseModel):
    player_id: int = Field(gt=0)
    game_id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
