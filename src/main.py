""" Main module """

import time

import pygame

from globals import WIDTH, HEIGHT, master_volume
from snake import Snake
from fruit import Fruit

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

if __name__ == "__main__":
    bg_music = pygame.mixer.Channel(0)
    bg_music.set_volume(master_volume)
    bg_music.queue(pygame.mixer.Sound("./sfx/music/ZUN - A Sacred Lot.mp3"))

    # Initilize window.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Do Snakes Eat Fruit?")
    pygame.display.set_icon(pygame.image.load("./icons/window_icon.png"))

    # Create snake and fruit entity.
    snake = Snake(frames_per_step=5)
    fruit = Fruit(snake)

    running = True    # pylint: disable=C0103
    while running:
        start_time = time.perf_counter()

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    # pylint: disable=C0103
            elif event.type == pygame.KEYDOWN:
                snake.handle_keys(event)

        if not snake.alive:
            bg_music.stop()

        screen.fill((0, 0, 0))

        fruit.draw(screen)

        snake.draw(screen)
        snake.update(fruit)

        pygame.display.flip()

        # Sleep enough to keep 50 fps.
        # If frame was processed longer than 1/50 s, then do not wait.
        end_time = time.perf_counter()
        dt = end_time - start_time
        wait_time = (abs(dt - 0.02) - dt + 0.02) / 2
        time.sleep(abs(wait_time))

    pygame.quit()
