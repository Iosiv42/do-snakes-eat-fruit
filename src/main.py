""" Main module """

import time

import pygame
pygame.init()

from globals import WIDTH, HEIGHT
from snake import Snake
from fruit import Fruit

if __name__ == "__main__":
    # Initilize window.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Do Snakes Eat Fruits?")
    pygame.display.set_icon(pygame.image.load("./icons/window_icon.png"))

    # Create snake and fruit entity.
    snake = Snake(frames_per_step=5)
    fruit = Fruit()

    running = True    # pylint: disable=C0103
    while running:
        start_time = time.perf_counter()

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    # pylint: disable=C0103
            elif event.type == pygame.KEYDOWN:
                snake.handle_keys(event)

        screen.fill((0, 0, 0))

        fruit.draw(screen)

        # Should to update early that draw, 'cause of remove screen jitter.
        snake.update(fruit)
        snake.draw(screen)

        pygame.display.flip()

        # Sleep enough to keep 50 fps.
        # If frame was processed longer than 1/50 s, then do not wait.
        end_time = time.perf_counter()
        dt = end_time - start_time
        time.sleep((abs(dt - 0.02) - dt + 0.02) / 2)

    pygame.quit()
