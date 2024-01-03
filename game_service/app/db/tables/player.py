import sqlalchemy as sa
from sqlalchemy import orm

from app.db.tables.base import DBBase


class PlayerORM(DBBase):
    __tablename__ = 'player'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    auth_id = sa.Column('auth_id', sa.Integer, nullable=False, unique=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    icon_link = sa.Column('icon_link', sa.Text)

    game_admin = orm.relationship('GameORM', back_populates='admin', foreign_keys='GameORM.admin_id')
    game_player = orm.relationship('GameORM', back_populates='player', foreign_keys='GameORM.player_id')
    field = orm.relationship('FieldORM', back_populates='player')
    prize_admin = orm.relationship('PrizeORM', back_populates='admin', foreign_keys='PrizeORM.admin_id')
    prize_player = orm.relationship('PrizeORM', back_populates='player', foreign_keys='PrizeORM.player_id')

    def __repr__(self) -> str:
        return f'PlayerORM(id={self.id}, auth_id={self.auth_id}, name={self.name}, icon_link=...)'
