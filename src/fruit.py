""" Fruit entity. """

import random

import pygame

from globals import GRID_WIDHT, GRID_HEIGHT, SCALE_X, SCALE_Y, PROJ_MATRIX
from matrix_math import Vector


class Fruit:
    """ Fruit class. Create once and respawn when collected. """

    def __init__(self, snake):
        self.pos = snake.head_pos
        while self.pos in snake.get_part_poses():
            self.pos = Vector((
                random.randint(0, GRID_WIDHT - 1),
                random.randint(0, GRID_HEIGHT - 1),
            ))

    def is_collelcted(self, snake_head_pos: Vector) -> bool:
        """ Check if position of self equals to snake_head_pos """
        return self.pos == snake_head_pos

    def collect(self, snake) -> None:
        """ Respawn fruit. """
        Fruit.__init__(self, snake)

    def draw(self, screen: pygame.Surface) -> None:
        """ Draw fruit to specified pygame screen. """

        pygame.draw.rect(
            screen, (0, 255, 0),
            ((PROJ_MATRIX * self.pos).transpose()[0], (SCALE_X, SCALE_Y))
        )
