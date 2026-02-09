import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from project.config.settings import LOG_FILE, LOG_LEVEL

def setup_logger(name: str = "archival_bot") -> logging.Logger:
    """
    Sets up a logger with console and daily rotating file handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Daily Rotation)
    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30, # Keep 30 days of logs
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
