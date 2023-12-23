import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class AuthORM(Base):
    __tablename__ = 'auth'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    player_id = sa.Column('player_id', sa.ForeignKey('player.id'))
    login = sa.Column('login', sa.VARCHAR(100))
    password = sa.Column('password', sa.VARCHAR(50))
    is_admin = sa.Column('is_admin', sa.Boolean)
    datetime = sa.Column('datetime', sa.TIMESTAMP())

    player = orm.relationship('PlayerORM')

    def __repr__(self) -> str:
        return f'''AuthORM(id={self.id}, player_id={self.player_id}, login={self.login}, 
        password=***, is_admin={self.is_admin}, datetime={self.datetime})'''
