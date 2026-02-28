"""Structured logging configuration using python-json-logger."""

import logging
import sys

# Try to import, but don't fail if unavailable at runtime
try:
    from pythonjsonlogger import jsonlogger
    HAS_JSON_LOGGER = True
except ImportError:
    HAS_JSON_LOGGER = False


def setup_logging(app=None):
    """Configure structured JSON logging for the application."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    if HAS_JSON_LOGGER:
        # Use JSON formatter
        formatter = jsonlogger.JsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
    else:
        # Fallback to standard formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_logger(name):
    """Get a logger with the given name."""
    return logging.getLogger(name)
