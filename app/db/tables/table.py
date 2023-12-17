import sqlalchemy as sa

from app.db.tables.base import Base


__all__ = ("ExampleTableORM",)


class ExampleTableORM(Base):
    __tablename__ = "example_table"

    id = sa.Column("id", sa.Integer, primary_key=True, autoincrement=True)
