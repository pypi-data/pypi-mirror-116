import logging as _logging
import typing as _typing

__version__ = "1.0.1"
__author__ = "Carneiro, Claudio F."
__date__ = "Wed, 11 Aug 2021 14:49:24 +0000"


def get_logger(
    name=__file__,
    level: int = _logging.WARNING,
    handlers: _typing.Optional[_typing.List[_logging.Handler]] = None,
) -> _logging.Logger:
    """Returns a logger object"""

    logger = _logging.getLogger(name)

    if not len(logger.handlers) and not handlers:
        formatter = _logging.Formatter(
            "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
        )
        logger.setLevel(level)
        console = _logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger
