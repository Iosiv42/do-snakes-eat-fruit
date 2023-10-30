""" Snake entity. """

from collections import deque
from typing import Optional
import random

import pygame
from pygame.locals import K_RIGHT, K_UP, K_LEFT, K_DOWN

from matrix_math import Vector
from globals import (
    DIRS, GRID_WIDHT, GRID_HEIGHT, SCALE_X, SCALE_Y, PROJ_MATRIX, master_volume
)
from fruit import Fruit


class Snake:
    """ Snake entity. Choice random head_pos or head_dir if not specified """

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

        # self.body start is head and end is tail.
        # It contains direction for next cell (part) of snake body.
        self.body = deque((head_dir, head_dir))
        self.part_poses = []
        self.head_pos = head_pos
        self.head_dir = head_dir
        self.alive = True

        # Specify how many steps needed to go one step forward.
        self.frames_per_step = frames_per_step
        self.frame = 1

        self.sfx_channel = pygame.mixer.Channel(1)
        self.sfx_channel.set_volume(master_volume)
        self.create_sfxs()

    def update(self, fruit: Fruit) -> None:
        """ Update entity. """

        if not self.alive:
            return
        if self.frame % self.frames_per_step:
            self.frame += 1
            return

        if fruit.is_collelcted(self.head_pos):
            self.power_up()
            fruit.collect(self)

        # Go one step forward if enough frames elapsed.

        self.body.appendleft(self.head_dir)
        self.body.pop()

        # There's toroidal surface, so we should to use
        # Z/nZ and Z/mZ, where n = GRID_WIDHT and m = GRID_HEIGHT.
        self.head_pos -= self.head_dir
        self.head_pos[0][0] %= GRID_WIDHT
        self.head_pos[1][0] %= GRID_HEIGHT

        self.frame = 1

    def handle_keys(self, event: pygame.event.Event) -> None:
        """ Handle key event to proceed snake movement. """

        assert event.type == pygame.KEYDOWN, "Event type is not pygame.KEYDOWN"
        if (event.key in {K_RIGHT, K_UP, K_LEFT, K_DOWN}
            and DIRS[event.key] != self.head_dir):
            self.head_dir = -DIRS[event.key]

    def power_up(self) -> None:
        self.body.append(self.body[-1])

        self.sfx_channel.play(self.power_up_sfx)
        while self.sfx_channel.get_busy():
            pass

    def draw(self, screen: pygame.Surface):
        """ Draw entity. """

        for idx, pos in enumerate(self.get_part_poses()):
            color = (255, 0, 0) if idx == 0 else (255,) * 3
            window_pos = PROJ_MATRIX * pos

            pygame.draw.rect(
                screen, color,
                (window_pos.transpose()[0], (SCALE_X, SCALE_Y))
            )

    def get_part_poses(self) -> bool:
        curr_pos = self.head_pos
        next_head_pos = self.head_pos - self.head_dir
        for idx, direction in enumerate(self.body):
            curr_pos[0][0] %= GRID_WIDHT
            curr_pos[1][0] %= GRID_HEIGHT

            if curr_pos == next_head_pos and idx != 0:
                self.die()

            yield curr_pos
            curr_pos += direction

    def create_sfxs(self) -> None:
        self.power_up_sfx = pygame.mixer.Sound("sfx/snake/power_up.wav")
        self.death_sfx = pygame.mixer.Sound("sfx/snake/death.wav")

    def die(self) -> None:
        # Dead inside cannot die.
        if self.alive:
            self.alive = False
            self.sfx_channel.queue(self.death_sfx)
