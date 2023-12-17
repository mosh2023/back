from typing import Iterator
from typing import List
from typing import TypeVar


T = TypeVar("T")


def get_batch(data: List[T], batch_size: int) -> Iterator[List[T]]:
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]
