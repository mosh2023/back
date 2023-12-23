import sqlalchemy as sa
from sqlalchemy import orm

from db.tables.base import Base


class GameORM(Base):
    __tablename__ = 'game'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50))
    description = sa.Column('description', sa.Text)
    board_size = sa.Column('board_size', sa.Integer)
    key = sa.Column('key', sa.VARCHAR(10))

    player1_id = sa.Column('player1_id', sa.ForeignKey('player.id'))
    player1_remaining_moves = sa.Column('player1_remaining_moves', sa.Integer)
    player1_used_moves = sa.Column('player1_used_moves', sa.Integer)
    
    player2_id = sa.Column('player2_id', sa.ForeignKey('player.id'))
    player2_remaining_moves = sa.Column('player2_remaining_moves', sa.Integer)
    player2_used_moves = sa.Column('player2_used_moves', sa.Integer)

    admin_id = sa.Column('admin_id', sa.ForeignKey('player.id'))
    datetime_start = sa.Column('datetime_start', sa.TIMESTAMP())
    datetime_end = sa.Column('datetime_end', sa.TIMESTAMP())

    player1 = orm.relationship('PlayerORM')
    player2 = orm.relationship('PlayerORM')
    admin = orm.relationship('PlayerORM')
    field = orm.relationship('FieldORM')

    def __repr__(self) -> str:
        return f'''GameORM(id={self.id}, name={self.name}, description=..., board_size={self.board_size}, key=***, 
        player1_id={self.player1_id}, player1_remaining_moves={self.player1_remaining_moves}, player1_used_moves={self.player1_used_moves}, 
        player2_id={self.player2_id}, player2_remaining_moves={self.player2_remaining_moves}, player2_used_moves={self.player2_used_moves}, 
        admin_id={self.admin_id}, datetime_start={self.datetime_start}, datetime_end={self.datetime_end}'''
