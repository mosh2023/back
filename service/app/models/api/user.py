from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: int = Field(gt=0)
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: str = None


class UserInfo(BaseModel):
    # To respolve repo.get_repo we need `id` field
    auth_id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    icon_link: str = None


class UserEdit(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(default=None, min_length=3, max_length=50)
    icon_link: str = None

