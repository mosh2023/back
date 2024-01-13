from pydantic import BaseModel, Field


class UserDBModel(BaseModel):
    id: int = Field(gt=0, default=None)
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: str = None
