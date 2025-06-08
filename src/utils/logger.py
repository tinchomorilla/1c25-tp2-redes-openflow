import logging
import sys


def setup_logger(name=None):
    """
    Configure and return a logger with the specified name.
    If no name is provided, returns the root logger.

    Args:
        name: Optional name for the logger. If None, returns root logger.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Get logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Show all levels including DEBUG

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Add handler
    logger.addHandler(console_handler)

    return logger
