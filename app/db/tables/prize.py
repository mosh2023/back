import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class PrizeORM(Base):
    __tablename__ = 'prize'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50))
    description = sa.Column('description', sa.Text)
    icon_link = sa.Column('icon_link', sa.Text)
    admin_id = sa.Column('admin_id', sa.ForeignKey('player.id'))
    player_id = sa.Column('player_id', sa.ForeignKey('player.id'))
    datetime = sa.Column('datetime', sa.TIMESTAMP())  # Win timestamp

    boat = orm.relationship('BoatORM')
    admin = orm.relationship('PlayerORM')
    player = orm.relationship('PlayerORM')

    def __repr__(self) -> str:
        return f'''PrizeORM(id={self.id}, name={self.name}, description=...,
        icon_link=..., admin_id={self.admin_id}, player_id={self.player_id},
        datetime={self.datetime})'''
