from logging import Logger, StreamHandler, DEBUG

import colorlog


def setup_logger(name: str = "app") -> Logger:
    handler = StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
    )
    logger = colorlog.getLogger(name)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    logger.setLevel(DEBUG)  # Показывает все уровни логов
    return logger
