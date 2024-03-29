'''
Модуль с ORM репрезентациями таблиц базы данных.
'''

from .base import DBBase, get_metadata
from .user import UserORM
from .player import PlayerORM
from .game import GameORM
from .field import FieldORM
from .boat import BoatORM
from .prize import PrizeORM
from .auth import AuthORM
