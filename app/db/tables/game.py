import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Mapped
from typing import List

from db.tables.base import Base


class GameORM(Base):
    __tablename__ = 'game'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    description = sa.Column('description', sa.Text)
    board_size = sa.Column('board_size', sa.Integer, nullable=False)
    key = sa.Column('key', sa.VARCHAR(10), nullable=False, unique=True)

    player1_id = sa.Column('player1_id', sa.ForeignKey('player.id'))
    player1_remaining_moves = sa.Column('player1_remaining_moves', sa.Integer)
    player1_used_moves = sa.Column('player1_used_moves', sa.Integer)
    
    player2_id = sa.Column('player2_id', sa.ForeignKey('player.id'))
    player2_remaining_moves = sa.Column('player2_remaining_moves', sa.Integer)
    player2_used_moves = sa.Column('player2_used_moves', sa.Integer)

    admin_id = sa.Column('admin_id', sa.ForeignKey('player.id'), nullable=False)
    datetime_start = sa.Column('datetime_start', sa.TIMESTAMP())
    datetime_end = sa.Column('datetime_end', sa.TIMESTAMP())

    field = orm.relationship('FieldORM', back_populates='game')
    player1 = orm.relationship('PlayerORM', back_populates='game_player1', foreign_keys=[player1_id])
    player2 = orm.relationship('PlayerORM', back_populates='game_player2', foreign_keys=[player2_id])
    admin = orm.relationship('PlayerORM', back_populates='game_admin', foreign_keys=[admin_id])

    def __repr__(self) -> str:
        return f'''GameORM(id={self.id}, name={self.name}, description=..., board_size={self.board_size}, key=***, 
        player1_id={self.player1_id}, player1_remaining_moves={self.player1_remaining_moves}, player1_used_moves={self.player1_used_moves}, 
        player2_id={self.player2_id}, player2_remaining_moves={self.player2_remaining_moves}, player2_used_moves={self.player2_used_moves}, 
        admin_id={self.admin_id}, datetime_start={self.datetime_start}, datetime_end={self.datetime_end}'''
