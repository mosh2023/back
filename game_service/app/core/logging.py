from medsi_fastapi.logging import CustomizeLogger
from medsi_fastapi.logging_factory import LogHandlerFactory

from app.core import config


logger = CustomizeLogger().make_logger(config.LOGGING_LEVEL, config.LOGGING_SERIALIZE)

logger_factory = LogHandlerFactory(logger)
