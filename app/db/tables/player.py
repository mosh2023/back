import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class PlayerORM(Base):
    __tablename__ = 'player'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50))
    icon_link = sa.Column('icon_link', sa.Text)

    auth = orm.relationship('AuthORM')
    game = orm.relationship('GameORM')
    field = orm.relationship('FieldORM')
    prize = orm.relationship('PrizeORM')

    def __repr__(self) -> str:
        return f'''PlayerORM(id={self.id}, name={self.name}, icon_link={self.icon_link})'''
