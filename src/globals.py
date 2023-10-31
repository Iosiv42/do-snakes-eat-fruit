""" Game global values. """

from typing import Final
from enum import IntEnum

from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN    # pylint: disable=E0401

from matrix_math import Matrix, Vector

master_volume = 100

class MovementKeys(IntEnum):
    """ Keys to control snake movement. """
    RIGHT = K_RIGHT
    UP =  K_UP
    LEFT = K_LEFT
    DOWN = K_DOWN

# Window size.
WIDTH: Final = 768
HEIGHT: Final = 768

# Game grid size.
GRID_WIDHT: Final = 16
GRID_HEIGHT: Final = 16

# Map pressed keys to directions.
# 'Cause of y axis goes downwards down and up dirs. are opposite.
DIRS: Final = {
    MovementKeys.RIGHT: Vector((1, 0)),
    MovementKeys.UP: Vector((0, -1)),
    MovementKeys.LEFT: Vector((-1, 0)),
    MovementKeys.DOWN: Vector((0, 1)),
}

# Scale coeff. to scale grid coordinates to window ones.
SCALE_X: Final = WIDTH / GRID_WIDHT
SCALE_Y: Final = HEIGHT / GRID_HEIGHT

# Projection matrix for grid to window coordinates conversion.
PROJ_MATRIX: Final = Matrix((
    (SCALE_X, 0),
    (0, SCALE_Y),
))
