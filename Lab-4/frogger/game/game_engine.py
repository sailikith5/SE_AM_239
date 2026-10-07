"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.

Features: collision detection (Task 1), 3 lives with respawn and Game Over
(Task 2).
"""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GRID_ROWS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)
from game import renderer

START_LIVES = 3

STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]   # one entry per road row, alternating direction


class GameEngine:
    def __init__(self):
        self._build_entities()

    def _build_entities(self):
        self.lives = START_LIVES
        self.state = STATE_PLAYING
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)

        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70   # mix of cars and wider trucks
            spacing = 300
            count = 2

            # Try a few random phases and keep the first one that doesn't
            # already overlap the frog's starting column - guarantees a
            # safe first lane instead of leaving it to chance.
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break

            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self._build_entities()
            return
        if self.state != STATE_PLAYING:
            return   # frog is frozen once the game is over

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def _lose_life(self):
        """Take one life; respawn at the start, or end the game on the last one."""
        self.lives -= 1
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            self.frog.reset()

    def update(self):
        if self.state != STATE_PLAYING:
            return   # world is frozen on the Game Over screen

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if check_collision(self.frog, self.vehicles):
            self._lose_life()
            return

        if self.frog.row == GOAL_ROW:
            self.frog.reset()

    def draw(self, surface, font):
        renderer.draw_scene(surface, self.frog, self.vehicles)
        renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))
        renderer.draw_text_right(surface, font, f"Lives: {self.lives}", WIDTH - 10, 12)

        if self.state == STATE_GAME_OVER:
            renderer.draw_banner(surface, font, "GAME OVER", "Press R to restart", color=(255, 90, 80))
