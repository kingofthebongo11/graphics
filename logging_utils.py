import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    """Настраивает корневой логгер с единым форматом."""
    logging.basicConfig(level=level, format=LOG_FORMAT)


def get_logger(name: str) -> logging.Logger:
    """Возвращает логгер модуля с общим префиксом."""
    return logging.getLogger(name)
