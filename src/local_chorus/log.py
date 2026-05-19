"""Loguru setup. Import `from local_chorus.logging import logger` everywhere."""

import sys

from loguru import logger

from .config import settings

logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format=(
        "<green>{time:HH:mm:ss.SSS}</green> "
        "<level>{level: <7}</level> "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> | {message}"
    ),
    colorize=True,
    backtrace=True,
    diagnose=False,  # don't leak local variables in tracebacks
)

__all__ = ["logger"]
