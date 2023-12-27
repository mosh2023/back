import sqlalchemy as sa
from sqlalchemy import orm

from app.db.tables.base import Base


class AuthORM(Base):
    __tablename__ = 'auth'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    login = sa.Column('login', sa.VARCHAR(100), nullable=False, unique=True)
    password = sa.Column('password', sa.VARCHAR(50), nullable=False)
    is_admin = sa.Column('is_admin', sa.Boolean, nullable=False, default=False)
    datetime = sa.Column('datetime', sa.TIMESTAMP())

    def __repr__(self) -> str:
        return f'''AuthORM(id={self.id}, login={self.login}, \
password=***, is_admin={self.is_admin}, datetime={self.datetime})'''
