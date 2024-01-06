from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    id: int = Field(gt=0)
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: str = None


class PlayerInfo(BaseModel):
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: str = None


class PlayerEdit(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=50)
    icon_link: str = None

