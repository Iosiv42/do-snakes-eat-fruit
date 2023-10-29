from collections import deque
from enum import Enum
import time
import random

import pygame
from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN

from matrix_math import Matrix, Vector

pygame.init()


def gen_apple() -> Vector:
    return Vector(
        (random.randint(0, GRID_WIDHT - 1),
         random.randint(0, GRID_HEIGHT - 1))
    )


WIDTH, HEIGHT= 800, 800
GRID_WIDHT, GRID_HEIGHT = 20, 20

DIRS = {
    K_RIGHT: Vector((1, 0)),
    K_UP: Vector((0, -1)),
    K_LEFT: Vector((-1, 0)),
    K_DOWN: Vector((0, 1)),
}

RIGHT = DIRS[K_RIGHT]
UP = DIRS[K_UP]
LEFT = DIRS[K_LEFT]
DOWN = DIRS[K_DOWN]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
snake = deque((LEFT, LEFT, LEFT, UP, UP, LEFT, UP, UP, UP, UP, RIGHT, RIGHT))
head_pos = Vector((8, 8))
snake_dir = snake[0]

scale_x, scale_y = WIDTH / GRID_WIDHT, HEIGHT / GRID_HEIGHT
proj_matrix = Matrix((
    (scale_x, 0),
    (0, scale_y),
))

apple_pos = gen_apple()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in {K_RIGHT, K_UP, K_LEFT, K_DOWN}:
                snake_dir = -DIRS[event.key]

    if head_pos == apple_pos:
        snake.append(snake[-1])
        apple_pos = gen_apple()

    screen.fill((0, 0, 0))

    apple_proj_pos = proj_matrix * apple_pos
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (apple_proj_pos.transpose().data[0], (scale_x, scale_y))
    )
    
    snake.appendleft(snake[0])
    snake.pop()

    snake[0] = snake_dir

    head_pos -= snake[0]
    head_pos[0][0] %= GRID_WIDHT
    head_pos[1][0] %= GRID_HEIGHT

    pos = head_pos
    prev_poses = set()
    for idx, direction in enumerate(snake):
        if idx == 0:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        
        pos[0][0] %= GRID_WIDHT
        pos[1][0] %= GRID_HEIGHT
        projected = proj_matrix * pos

        pygame.draw.rect(
            screen,
            color,
            ((proj_matrix * pos).transpose()[0], (scale_x, scale_y))
        )

        if head_pos - snake_dir in prev_poses:
            running = False
        else:
            prev_poses.add(pos)

        pos += direction

    pygame.display.flip()

    time.sleep(0.1)

pygame.quit()
