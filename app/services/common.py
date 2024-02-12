from random import randint
from string import ascii_letters, digits


key_symbols = ascii_letters + digits


def generate_str(length: int = 8) -> str:
    r = len(key_symbols) - 1
    return ''.join(
        [key_symbols[randint(0, r)] for _ in range(length)]
    )
