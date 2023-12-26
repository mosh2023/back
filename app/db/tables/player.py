import sqlalchemy as sa
from sqlalchemy import orm

from app.db.tables.base import Base


class PlayerORM(Base):
    __tablename__ = 'player'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    icon_link = sa.Column('icon_link', sa.Text)

    auth = orm.relationship('AuthORM', back_populates='player', uselist=False)
    game_admin = orm.relationship('GameORM', back_populates='admin', foreign_keys='GameORM.admin_id')
    game_player1 = orm.relationship('GameORM', back_populates='player1', foreign_keys='GameORM.player1_id')
    game_player2 = orm.relationship('GameORM', back_populates='player2', foreign_keys='GameORM.player2_id')
    field = orm.relationship('FieldORM', back_populates='player')
    prize_admin = orm.relationship('PrizeORM', back_populates='admin', foreign_keys='PrizeORM.admin_id')
    prize_player = orm.relationship('PrizeORM', back_populates='player', foreign_keys='PrizeORM.player_id')

    def __repr__(self) -> str:
        return f'''PlayerORM(id={self.id}, name={self.name}, icon_link=...)'''
