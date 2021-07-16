import logging
import sys
from pathlib import Path

import pygame
from pygame import Surface
from pygame.locals import *

log = logging.getLogger(__name__)

MODULE_DIR = Path(__file__).resolve().parent
DATA_DIR = MODULE_DIR / "data"

log.trace(f"__file__: {__file__}")
log.trace(f"MODULE_DIR: {MODULE_DIR}")
log.trace(f"DATA_DIR: {DATA_DIR}")


def load_image(name: str, colorkey: int = None) -> list[Surface, Rect]:
    """Load an image from the data folder.

    Args:
        name (str): The name of the image.
        colorkey (int, optional): A colorkey for alpha coloring. Defaults to None.
            Set to -1 for auto-detection.

    Returns:
        list[Surface, Rect]: The image surface and its containing rectangle.
    """
    path = DATA_DIR / name
    log.debug(f"Loading image data/{name}")
    log.trace(f"Image path: {path}")
    try:
        image = pygame.image.load(path)
    except Exception as e:
        log.critical(f"Cannot load image: {name}", exc_info=True)
        sys.exit(e)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name: str) -> pygame.mixer.Sound:
    """Load a sound from the data folder.

    Args:
        name (str): The name of the sound file.

    Returns:
        pygame.mixer.Sound: A pygame sound object.
    """

    class NoneSound:
        def play(self) -> None:
            pass

    if not pygame.mixer:
        log.debug(f"Mixer not init-ed, replacing sound {name} with an empty wrapper.")
        return NoneSound()

    path = DATA_DIR / name
    log.debug(f"Loading sound data/{name}")
    log.trace(f"Sound path: {path}")
    try:
        sound = pygame.mixer.Sound(path)
    except Exception as e:
        log.critical(f"Cannot load sound: {path}", exc_info=True)
        sys.exit(e)
    return sound
