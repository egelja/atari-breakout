import logging
import os
import sys
from distutils.util import strtobool
from logging import Logger, handlers
from pathlib import Path
from typing import Any

import coloredlogs

TRACE_LEVEL = 5
try:
    DEBUG_MODE = strtobool(os.getenv("DEBUG", "False"))  # TODO: move to constants file?
except ValueError:
    DEBUG_MODE = False


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
    logging.TRACE = TRACE_LEVEL
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    Logger.trace = _monkeypatch_trace

    # TODO: verbose logging
    log_level = TRACE_LEVEL if DEBUG_MODE else logging.INFO
    format_string = "%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s"
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
            "trace": {"color": 246},
            "critical": {"background": "red"},
            "debug": coloredlogs.DEFAULT_LEVEL_STYLES["info"],
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


def _monkeypatch_trace(self: logging.Logger, msg: str, *args, **kwargs) -> None:
    """
    Log 'msg % args' with severity 'TRACE'.

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.
    logger.trace("Houston, we have an %s", "interesting problem", exc_info=1)
    """
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, msg, args, **kwargs)
