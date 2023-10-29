""" Snake entity. """

from collections import deque
from typing import Optional
import random

import pygame
from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN

from matrix_math import Vector
from globals import DIRS, GRID_WIDHT, GRID_HEIGHT, SCALE_X, SCALE_Y, PROJ_MATRIX
from fruit import Fruit


class Snake:
    def __init__(
        self,
        head_pos: Optional[Vector] = None,
        head_dir: Optional[Vector] = None,
        frames_per_step: Optional[int] = 10,
    ):
        if head_pos is None:
            head_pos = Vector((
                random.randint(0, GRID_WIDHT),
                random.randint(0, GRID_WIDHT),
            ))

        if head_dir is None:
            head_dir = random.choice(tuple(DIRS.values()))

        self.body = deque((head_dir, head_dir))
        self.head_pos = head_pos
        self.head_dir = head_dir
        self.alive = True
        self.frames_per_step = frames_per_step
        self.frame = 1

    def update(self, fruit: Fruit) -> None:
        if not self.alive:
            return
        if self.frame % self.frames_per_step:
            self.frame += 1
            return

        if fruit.is_collelcted(self.head_pos):
            self.body.append(self.body[-1])
            fruit.collect()

        self.body.appendleft(self.head_dir)
        self.body.pop()

        self.head_pos -= self.head_dir
        self.head_pos[0][0] %= GRID_WIDHT
        self.head_pos[1][0] %= GRID_HEIGHT

        self.frame = 1

    def handle_keys(self, event: pygame.event.Event) -> None:
        assert event.type == pygame.KEYDOWN, "Event type is not pygame.KEYDOWN"
        if event.key in {K_RIGHT, K_UP, K_LEFT, K_DOWN}:
            self.head_dir = -DIRS[event.key]

    def draw(self, screen: pygame.Surface):
        curr_pos = self.head_pos
        prev_poses = set()
        for idx, direction in enumerate(self.body):
            if idx == 0:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            
            curr_pos[0][0] %= GRID_WIDHT
            curr_pos[1][0] %= GRID_HEIGHT
            projected = PROJ_MATRIX * curr_pos

            pygame.draw.rect(
                screen, color,
                (projected.transpose()[0], (SCALE_X, SCALE_Y))
            )

            if self.head_pos - self.head_dir in prev_poses:
                self.alive = False
            else:
                prev_poses.add(curr_pos)

            curr_pos = curr_pos + direction