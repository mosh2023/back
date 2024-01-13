from sqlalchemy import Column, Integer, String
from .base import DBBase


class AuthORM(DBBase):

    __tablename__ = 'auth'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    login = Column('login', String(50), unique=True, nullable=False)
    password = Column('password', String(128), nullable=False)
    role = Column('role', String(50), nullable=False)

    def __repr__(self) -> str:
        return f'AuthORM(id={self.id}, login={self.login}, password={self.password}, role={self.role})'
