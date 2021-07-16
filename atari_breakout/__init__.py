import logging as py_logging

from . import logging

__version__ = "0.1.0"

logging.setup()
log = py_logging.getLogger("atari_breakout.init")

try:
    from dotenv import load_dotenv

    log.info("Found .env file, loading environment variables from it.")
    load_dotenv(override=True)
except ModuleNotFoundError:
    log.warning("No python-dotenv, not loading .env file.")
