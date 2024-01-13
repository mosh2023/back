'''
Модуль содержит сущности для абстрактной работы с базой данных. 
Объекты содержат методы с реализованными запросами к ней.
'''

from .base import BaseRepository
from .player import Player
from .admin import Admin
from .game import Game
from .field import Field
from .boat import Boat
from .prize import Prize
