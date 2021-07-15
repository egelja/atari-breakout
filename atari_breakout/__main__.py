import logging

import pygame
from pygame.locals import *

log = logging.getLogger("main")

pygame.init()

if not pygame.font:
    log.warn("Warning, fonts disabled")
if not pygame.mixer:
    log.warn("Warning, sound disabled")
