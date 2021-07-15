import logging
import os
import sys
from logging import handlers
from pathlib import Path

import coloredlogs


def setup() -> None:
    """Set up loggers."""
    log_level = logging.DEBUG if os.getenv("DEBUG") else logging.INFO
    format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    log_format = logging.Formatter(format_string)

    log_file = Path("logs", "game.log")
    log_file.parent.mkdir(exist_ok=True)
    file_handler = handlers.RotatingFileHandler(
        log_file, maxBytes=5242880, backupCount=7, encoding="utf8"
    )
    file_handler.setFormatter(log_format)

    root_log = logging.getLogger()
    root_log.setLevel(log_level)
    root_log.addHandler(file_handler)

    if "COLOREDLOGS_LEVEL_STYLES" not in os.environ:
        coloredlogs.DEFAULT_LEVEL_STYLES = {
            **coloredlogs.DEFAULT_LEVEL_STYLES,
            "debug": {"color": 246},
            "critical": {"background": "red"},
        }

    if "COLOREDLOGS_LOG_FORMAT" not in os.environ:
        coloredlogs.DEFAULT_LOG_FORMAT = format_string

    if "COLOREDLOGS_LOG_LEVEL" not in os.environ:
        coloredlogs.DEFAULT_LOG_LEVEL = log_level

    coloredlogs.install(logger=root_log, stream=sys.stdout)

    logging.getLogger("pygame").setLevel(logging.WARNING)
