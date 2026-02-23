"""Centralized logging configuration.

Follows Skill 07: Observability & UX.
- File-only logging (Zero Print policy for internals).
- Structured format for easy parsing.
"""

import logging
import sys
from pathlib import Path

from platformdirs import user_log_dir

# Constants
APP_NAME = "dx-vault-atlas"
# Skill 01: Pathlib usage mandatory
LOG_DIR = Path(user_log_dir(APP_NAME, ensure_exists=True))
LOG_FILE = LOG_DIR / "app.log"


def setup_logger(name: str = "dxva") -> logging.Logger:
    """Configures the main application logger.

    Adheres to Skill 07:
    - Writes to OS-standard log directory.
    - Uses a consistent format with timestamps.
    """
    logger = logging.getLogger(name)

    # Idempotency check to prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # Fail-safe: Ensure directory exists (Skill 06: Fail Fast if IO fails)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        # Graceful fallback: warning to stderr, limit logging to console (if configured later)
        sys.stderr.write(f"WARNING: Could not create log directory {LOG_DIR}: {e}\n")
        sys.stderr.write("Logging will be restricted to console output.\n")
        # Do not exit; return a logger that might only have console handlers added later
        # or add a NullHandler to avoid "No handler found" warnings
        logger.addHandler(logging.NullHandler())
        return logger

    # Handler: Rotating File Handler (Max 5MB, keep 3 backup files)
    try:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)

        # Format: Structured-like (Pipe separated) for easy parsing
        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | %(levelname)-8s | %(name)s | "
                "%(funcName)s:%(lineno)d | %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except OSError as e:
        sys.stderr.write(f"WARNING: Could not create log file {LOG_FILE}: {e}\n")
        logger.addHandler(logging.NullHandler())

    return logger


def enable_debug_logging() -> None:
    """Enable debug logging to console (stderr)."""
    # Check if we already have a StreamHandler
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
            return

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG)

    # Simple format for console debug
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)


# Singleton instance
logger = setup_logger()
