from pydantic import BaseModel
import orjson
from typing import Optional


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UserAllInfo(BaseSchema):
    login: str
    password: str
    is_admin: bool


class UserAuth(BaseSchema):
    login: str
    password: str


class UserGet(BaseSchema):
    id: int
    login: str
    password: str
    is_admin: bool


class UserEdit(BaseSchema):
    login: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool]


class CheckEmail(BaseSchema):
    login: str


class CheckAnswer(BaseSchema):
    answer: bool
