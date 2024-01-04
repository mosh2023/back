import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase


class GameORM(DBBase):
    __tablename__ = 'game'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    description = sa.Column('description', sa.Text)
    board_size = sa.Column('board_size', sa.Integer, nullable=False)
    key = sa.Column('key', sa.VARCHAR(10), nullable=False, unique=True)

    player_id = sa.Column('player_id', sa.ForeignKey('player.id'))
    player_moves = sa.Column('player_moves', sa.Integer)
    
    admin_id = sa.Column('admin_id', sa.ForeignKey('player.id'), nullable=False)
    dt_start = sa.Column('dt_start', sa.TIMESTAMP())

    field = orm.relationship('FieldORM', back_populates='game')
    player = orm.relationship('PlayerORM', back_populates='game_player', foreign_keys=[player_id])
    admin = orm.relationship('PlayerORM', back_populates='game_admin', foreign_keys=[admin_id])

    def __repr__(self) -> str:
        return f'GameORM(id={self.id}, name={self.name}, description=..., board_size={self.board_size}, ' \
            f'key=***, player_id={self.player_id}, player_moves={self.player_moves}, ' \
            f'admin_id={self.admin_id}, dt_start={self.dt_start})'
