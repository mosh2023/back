import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase


class UserORM(DBBase):
    __tablename__ = 'user'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    auth_id = sa.Column('auth_id', sa.Integer, nullable=False, unique=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    icon_link = sa.Column('icon_link', sa.Text)

    players = orm.relationship('PlayerORM', back_populates='user', foreign_keys='PlayerORM.user_id')
    admin_games = orm.relationship('GameORM', back_populates='admin', foreign_keys='GameORM.admin_id', uselist=False)
    admin_prizes = orm.relationship('PrizeORM', back_populates='admin', foreign_keys='PrizeORM.admin_id')
    user_prizes = orm.relationship('PrizeORM', back_populates='user', foreign_keys='PrizeORM.user_id')

    def __repr__(self) -> str:
        return f'UserORM(id={self.id}, auth_id={self.auth_id}, name={self.name}, icon_link=...)'
