import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class FieldORM(Base):
    __tablename__ = 'field'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    game_id = sa.Column('game_id', sa.ForeignKey('game.id'))
    x = sa.Column('x', sa.Integer)
    y = sa.Column('y', sa.Integer)
    injured = sa.Column('injured', sa.Boolean)
    player_id = sa.Column('player_id', sa.ForeignKey('player.id'))
    boat_id = sa.Column('boat_id', sa.ForeignKey('boat.id'))

    game = orm.relationship('GameORM')
    player = orm.relationship('PlayerORM')
    boat = orm.relationship('BoatORM')

    def __repr__(self) -> str:
        return f'''FieldORM(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y}, 
        injured={self.injured}, player_id={self.player_id}, boat_id={self.boat_id})'''
