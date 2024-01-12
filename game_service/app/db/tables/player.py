import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase


class PlayerORM(DBBase):
    __tablename__ = 'player'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column('user_id', sa.ForeignKey('user.id'))
    remaining_moves = sa.Column('remaining_moves', sa.Integer, nullable=False)
    used_moves = sa.Column('used_moves', sa.Integer, nullable=False)

    user = orm.relationship('UserORM', back_populates='players')
    games1 = orm.relationship('GameORM', back_populates='player1', foreign_keys='GameORM.player1_id', uselist=False)
    games2 = orm.relationship('GameORM', back_populates='player2', foreign_keys='GameORM.player2_id', uselist=False)
    fields = orm.relationship('FieldORM', back_populates='player')

    def __repr__(self) -> str:
        return f'PlayerORM(id={self.id}, user_id={self.user_id}, ' \
            f'remaining_moves={self.remaining_moves}, used_moves={self.used_moves})'
