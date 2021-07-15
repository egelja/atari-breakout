import logging

import pygame
from pygame.locals import *

log = logging.getLogger("main")

if not pygame.font:
    log.warn("Warning, fonts disabled")
if not pygame.mixer:
    log.warn("Warning, sound disabled")


def main() -> None:
    """Run the program."""
    # Pygame init
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Atari Breakout")
    pygame.mouse.set_visible(False)

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

    # Main loop:
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
    pygame.quit()


if __name__ == "__main__":
    main()
