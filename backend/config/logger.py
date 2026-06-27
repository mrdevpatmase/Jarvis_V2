"""
Centralized logging configuration for Jarvis AI.
"""

import logging
from pathlib import Path

from backend.config.settings import settings

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "jarvis.log"


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.
    """

    logger = logging.getLogger("Jarvis")

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()