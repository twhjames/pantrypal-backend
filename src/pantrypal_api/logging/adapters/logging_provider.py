import logging
import os
from typing import Dict, Optional

from src.core.logging.ports.logging_provider import ILoggingProvider

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("pantrypal")
logger.setLevel(logging.WARNING)  # Only WARNING and above will be logged

# Prevent duplicate handlers if already configured
if not logger.handlers:
    # File handler only
    file_handler = logging.FileHandler("logs/pantrypal.log")
    file_formatter = logging.Formatter("[%(levelname)s] %(asctime)s — %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

STACK_LEVEL = 2


class AppLoggingProvider(ILoggingProvider):
    def _format_message(
        self, message: str, extra_data: Optional[Dict], tag: Optional[str]
    ) -> str:
        extra_data = extra_data or {}
        tag_prefix = f"[{tag}] " if tag else ""
        return (
            f"{tag_prefix}{message} | Extra: {extra_data}"
            if extra_data
            else f"{tag_prefix}{message}"
        )

    def debug(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ):
        logger.debug(
            self._format_message(message, extra_data, tag), stacklevel=STACK_LEVEL
        )

    def info(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ):
        logger.info(
            self._format_message(message, extra_data, tag), stacklevel=STACK_LEVEL
        )

    def warning(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ):
        logger.warning(
            self._format_message(message, extra_data, tag), stacklevel=STACK_LEVEL
        )

    def error(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ):
        logger.error(
            self._format_message(message, extra_data, tag), stacklevel=STACK_LEVEL
        )

    def critical(
        self, message: str, extra_data: Optional[Dict] = None, tag: Optional[str] = None
    ):
        logger.critical(
            self._format_message(message, extra_data, tag), stacklevel=STACK_LEVEL
        )
