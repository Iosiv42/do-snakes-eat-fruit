""" Game global values. """

from typing import Final

from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN

from matrix_math import Matrix, Vector

WIDTH: Final = 800
HEIGHT: Final = 800

GRID_WIDHT: Final = 20
GRID_HEIGHT: Final = 20

DIRS: Final = {
    K_RIGHT: Vector((1, 0)),
    K_UP: Vector((0, -1)),
    K_LEFT: Vector((-1, 0)),
    K_DOWN: Vector((0, 1)),
}

RIGHT: Final = DIRS[K_RIGHT]
UP: Final = DIRS[K_UP]
LEFT: Final = DIRS[K_LEFT]
DOWN: Final = DIRS[K_DOWN]

SCALE_X: Final = WIDTH / GRID_WIDHT
SCALE_Y: Final = HEIGHT / GRID_HEIGHT

PROJ_MATRIX: Final = Matrix((
    (SCALE_X, 0),
    (0, SCALE_Y),
))
