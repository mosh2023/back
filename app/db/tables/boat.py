import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class BoatORM(Base):
    __tablename__ = 'boat'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    prize_id = sa.Column('prize_id', sa.ForeignKey('prize.id'))

    game = orm.relationship('GameORM')
    prize = orm.relationship('PrizeORM')

    def __repr__(self) -> str:
        return f'''BoatORM(id={self.id}, prize_id={self.prize_id})'''
