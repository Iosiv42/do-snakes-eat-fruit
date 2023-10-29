""" Fruit entity. """

import random

import pygame

from globals import GRID_WIDHT, GRID_HEIGHT, SCALE_X, SCALE_Y, PROJ_MATRIX
from matrix_math import Vector


class Fruit:
    def __init__(self):
        self.pos = Vector((
            random.randint(0, GRID_WIDHT - 1),
            random.randint(0, GRID_HEIGHT - 1),
        ))

    def is_collelcted(self, snake_head_pos: Vector) -> bool:
        return self.pos == snake_head_pos

    def collect(self) -> None:
        self = self.__init__()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen, (0, 255, 0),
            ((PROJ_MATRIX * self.pos).transpose()[0], (SCALE_X, SCALE_Y))
        )
