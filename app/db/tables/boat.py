import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase


class BoatORM(DBBase):
    __tablename__ = 'boat'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    prize_id = sa.Column('prize_id', sa.ForeignKey('prize.id'), unique=True, nullable=False)

    field = orm.relationship('FieldORM', back_populates='boat', uselist=False)
    prize = orm.relationship('PrizeORM', back_populates='boat')

    def __repr__(self) -> str:
        return f'BoatORM(id={self.id}, prize_id={self.prize_id})'
