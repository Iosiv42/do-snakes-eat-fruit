import time

import pygame
pygame.init()

from globals import WIDTH, HEIGHT
from snake import Snake
from fruit import Fruit

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Do Snakes Eat Fruits?")
pygame.display.set_icon(pygame.image.load("./icons/window_icon.png"))

snake = Snake(frames_per_step=5)
fruit = Fruit()

running = True
while running:
    start_time = time.perf_counter()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.handle_keys(event)

    screen.fill((0, 0, 0))

    fruit.draw(screen)

    snake.update(fruit)
    snake.draw(screen)


    pygame.display.flip()

    end_time = time.perf_counter()
    dt = end_time - start_time
    time.sleep((abs(dt - 0.02) - dt + 0.02) / 2)

pygame.quit()
