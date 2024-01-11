import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase


class PrizeORM(DBBase):
    __tablename__ = 'prize'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.VARCHAR(50), nullable=False)
    description = sa.Column('description', sa.Text)
    icon_link = sa.Column('icon_link', sa.Text)
    admin_id = sa.Column('admin_id', sa.ForeignKey('user.id'), nullable=False)
    user_id = sa.Column('user_id', sa.ForeignKey('user.id'))
    dt_won = sa.Column('dt_won', sa.TIMESTAMP())

    boat = orm.relationship('BoatORM', back_populates='prize', uselist=False)
    admin = orm.relationship('UserORM', back_populates='prize_admin', foreign_keys=[admin_id])
    player = orm.relationship('UserORM', back_populates='prize_user', foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f'PrizeORM(id={self.id}, name={self.name}, description=..., icon_link=..., ' \
            f'admin_id={self.admin_id}, user_id={self.user_id}, dt_won={self.dt_won})'
