from functools import lru_cache
import asyncio

from medsi_kafka.producer import UniversalProducer

from app.core import config


@lru_cache(maxsize=20)
def _get_producer(loop):
    from app.main import app

    producer = UniversalProducer(
        loop=loop,
        logger=app.logger,
        bootstrap=config.KAFKA_BOOTSTRAP_SERVER,
    )
    return producer


def get_producer():
    loop = asyncio.get_running_loop()
    return _get_producer(loop)
