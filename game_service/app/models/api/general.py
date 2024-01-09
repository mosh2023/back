from pydantic import BaseModel, Field


class Id(BaseModel):
    id: int = Field(gt=0)
