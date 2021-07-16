import logging

import pygame
from pygame.locals import *

from .utils import load_image

log = logging.getLogger("atari_breakout.main")

if not pygame.font:
    log.warning("Warning, fonts disabled")
if not pygame.mixer:
    log.warning("Warning, sound disabled")


def main() -> None:
    """Run the program."""
    # Pygame and screen setup
    log.info("Starting game setup!")
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    # Window setup
    pygame.display.set_caption("Atari Breakout")
    icon, _ = load_image("atari_logo.png")
    pygame.display.set_icon(icon)

    # Background setup
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0, 0, 0))

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Atari Breakout!", True, (255, 255, 255))
        textpos = text.get_rect(
            centerx=background.get_width() / 2, centery=background.get_height() / 2 - 20
        )
        background.blit(text, textpos)

    # Game object setup
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.LayeredDirty(())

    # Display the background
    all_sprites.clear(screen, background)

    # Grab the mouse
    # TODO: make this configurable later, or add a menu
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    # Main loop:
    log.info("Setup complete, starting Atari Breakout!")
    running = True
    while running:
        clock.tick(60)  # 60 FPS max

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            pass
        elif keys[K_RIGHT]:
            pass

        # Update Sprites
        all_sprites.update()

        # Redraw scene
        to_update = all_sprites.draw(screen)
        pygame.display.update(to_update)

    # Game over
    log.warning("Received quit signal, now closing gracefully.")
    pygame.quit()


if __name__ == "__main__":
    main()
