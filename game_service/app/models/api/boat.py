from pydantic import BaseModel, Field


class BoatModel(BaseModel):
    id: int = Field(gt=0)
    prize_id: int = Field(gt=0)


class BoatInfo(BaseModel):
    prize_id: int = Field(gt=0)


class BoatPlace(BaseModel):
    id: int = Field(gt=0)
    x: int = Field(gt=-1)
    y: int = Field(gt=-1)
