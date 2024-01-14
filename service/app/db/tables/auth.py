import sqlalchemy as sa
from sqlalchemy import orm

from .base import DBBase
from app.models.db import Roles


class AuthORM(DBBase):
    __tablename__ = 'auth'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    login = sa.Column('login', sa.String(50), unique=True, nullable=False)
    password = sa.Column('password', sa.String(128), nullable=False)
    role = sa.Column('role', sa.Enum(Roles), nullable=False)

    user = orm.relationship('UserORM', back_populates='auth', uselist=False)

    def __repr__(self) -> str:
        return f'AuthORM(id={self.id}, login={self.login}, password=***, role={self.role})'
