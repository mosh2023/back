import sqlalchemy as sa
from sqlalchemy import orm

from app.db.tables.base import Base


class FieldORM(Base):
    __tablename__ = 'field'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    game_id = sa.Column('game_id', sa.ForeignKey('game.id'), nullable=False)
    x = sa.Column('x', sa.Integer, nullable=False)
    y = sa.Column('y', sa.Integer, nullable=False)
    injured = sa.Column('injured', sa.Boolean, nullable=False, default=False)
    player_id = sa.Column('player_id', sa.ForeignKey('player.id'))
    boat_id = sa.Column('boat_id', sa.ForeignKey('boat.id'))

    game = orm.relationship('GameORM', back_populates='field', foreign_keys=[game_id])
    player = orm.relationship('PlayerORM', back_populates='field', foreign_keys=[player_id])
    boat = orm.relationship('BoatORM', back_populates='field', foreign_keys=[boat_id])

    def __repr__(self) -> str:
        return f'''FieldORM(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y}, \
injured={self.injured}, player_id={self.player_id}, boat_id={self.boat_id})'''
