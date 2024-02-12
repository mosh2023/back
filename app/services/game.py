from random import randint
from string import ascii_uppercase, digits

from app.core import config


key_symbols = ascii_uppercase + digits


def generate_key() -> str:
    r = len(key_symbols) - 1
    key = ''
    for _ in range(config.GAME_KEY_LENGTH):
        key += key_symbols[randint(0, r)]
    return key
