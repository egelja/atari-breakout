import logging
import sys
from pathlib import Path

import pygame
from pygame import Surface
from pygame.locals import *

DATA_PATH = Path("data")

log = logging.getLogger(__name__)


def load_image(name: str, colorkey: int = None) -> list[Surface, Rect]:
    """Load an image from the data folder.

    Args:
        name (str): The name of the image.
        colorkey (int, optional): A colorkey for alpha coloring. Defaults to None.
            Set to -1 for auto-detection.

    Returns:
        list[Surface, Rect]: The image surface and its containing rectangle.
    """
    path = DATA_PATH / name
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
        return NoneSound()

    path = DATA_PATH / name
    try:
        sound = pygame.mixer.Sound(path)
    except Exception as e:
        log.critical(f"Cannot load sound: {path}", exc_info=True)
        sys.exit(e)
    return sound
