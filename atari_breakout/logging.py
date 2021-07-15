import logging
import os
import sys
from logging import Logger, handlers
from pathlib import Path
from typing import Any

import coloredlogs


class StreamToLogger:
    """Fake file-like stream object that redirects writes to a logger instance."""

    def __init__(self, logger: Logger, log_level: int = logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf: str = ""

    def write(self, buf: Any) -> None:
        """Write a line to the stream."""
        temp_linebuf = self.linebuf + buf
        self.linebuf = ""
        for line in temp_linebuf.splitlines(True):
            # From the io.TextIOWrapper docs:
            #   On output, if newline is None, any '\n' characters written
            #   are translated to the system default line separator.
            # By default sys.stdout.write() expects '\n' newlines and then
            # translates them so this is still cross platform.
            if line[-1] == "\n":
                self.logger.log(self.log_level, line.rstrip())
            else:
                self.linebuf += line

    def flush(self) -> None:
        """Output the log."""
        if self.linebuf != "":
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ""


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

    coloredlogs.install(logger=root_log, stream=sys.__stdout__)

    logging.getLogger("pygame").setLevel(logging.WARNING)

    stdout_logger = logging.getLogger("STDOUT")
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)

    stderr_logger = logging.getLogger("STDERR")
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
