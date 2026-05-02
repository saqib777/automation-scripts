# Custom logger for automation-scripts
# Writes to both console and rotating log file

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def get_logger(name: str, log_dir: str = "logs", level: str = "INFO") -> logging.Logger:
    """
    Create and return a configured logger.

    Features:
    - Console handler with colour-coded output
    - Rotating file handler (max 5MB, keeps 3 backups)
    - Timestamped log entries
    - Named loggers (one per module)

    Usage:
        from utilities.logger import get_logger
        log = get_logger(__name__)
        log.info("Test started")
        log.error("Something failed")
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger   # already configured — avoid duplicate handlers

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── Console Handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # ── File Handler ──────────────────────────────────────────────────────────
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"test_run_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


def get_test_logger() -> logging.Logger:
    """Convenience function — returns logger named 'test_suite'."""
    return get_logger("test_suite")


# ── Module-level default logger ───────────────────────────────────────────────
log = get_logger("automation")


if __name__ == "__main__":
    test_log = get_logger("demo", level="DEBUG")
    test_log.debug("Debug message")
    test_log.info("Info message")
    test_log.warning("Warning message")
    test_log.error("Error message")
    test_log.critical("Critical message")
