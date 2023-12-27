import typing as t

from pydantic import BaseModel
from pydantic import PrivateAttr
from sqlalchemy.orm.base import DEFAULT_STATE_ATTR


class SQLAlchemyBaseModel(BaseModel):
    __slots__ = {DEFAULT_STATE_ATTR, "__weakref__"}
    __abstract__ = True
    __annotations__ = {DEFAULT_STATE_ATTR: t.Any}
    __private_attributes__ = {DEFAULT_STATE_ATTR: PrivateAttr()}

    def dict(
        self,
        *,
        include: t.Union[
            t.AbstractSet[t.Union[int, str]], t.Mapping[t.Union[int, str], t.Any], None
        ] = None,
        exclude: t.Union[
            t.AbstractSet[t.Union[int, str]], t.Mapping[t.Union[int, str], t.Any], None
        ] = None,
        by_alias: bool = False,
        skip_defaults: t.Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> t.Dict[str, t.Any]:
        _exclude = {"__fields_set__"}

        if exclude:
            _exclude = _exclude.union(exclude)  # type: ignore

        return super().dict(
            include=include,
            exclude=_exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
