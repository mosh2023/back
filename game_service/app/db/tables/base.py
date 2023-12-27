from sqlalchemy import inspect
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm.decl_api import registry


mapper_registry = registry()
metadata = mapper_registry.metadata


@as_declarative(metadata=metadata)
class Base:
    def __iter__(self):
        obj_dict = {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }
        yield from obj_dict.items()


def get_metadata():
    """Import all project tables"""
    from app.db.tables.player import PlayerORM
    from app.db.tables.game import GameORM
    from app.db.tables.field import FieldORM
    from app.db.tables.boat import BoatORM
    from app.db.tables.prize import PrizeORM

    return mapper_registry.metadata
