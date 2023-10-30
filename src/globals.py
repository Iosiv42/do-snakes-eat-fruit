""" Game global values. """

from typing import Final

from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN    # pylint: disable=E0401

from matrix_math import Matrix, Vector

master_volume = 100

# Window size.
WIDTH: Final = 800
HEIGHT: Final = 800

# Game grid size.
GRID_WIDHT: Final = 10
GRID_HEIGHT: Final = 10

# Map pressed keys to directions.
# 'Cause of y axis goes downwards down and up dirs. are opposite.
DIRS: Final = {
    K_RIGHT: Vector((1, 0)),
    K_UP: Vector((0, -1)),
    K_LEFT: Vector((-1, 0)),
    K_DOWN: Vector((0, 1)),
}

# Scale coeff. to scale grid coordinates to window ones.
SCALE_X: Final = WIDTH / GRID_WIDHT
SCALE_Y: Final = HEIGHT / GRID_HEIGHT

# Projection matrix for grid to window coordinates conversion.
PROJ_MATRIX: Final = Matrix((
    (SCALE_X, 0),
    (0, SCALE_Y),
))
