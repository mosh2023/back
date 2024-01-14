from pydantic import BaseModel, Field


class BoatDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    prize_id: int = Field(gt=0)
