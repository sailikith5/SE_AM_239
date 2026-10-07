"""Headless tests for the four Lab 4 tasks.  Run from the frogger/ folder:
    SDL_VIDEODRIVER=dummy python3 -m unittest discover -s tests -v
"""
import os, sys, random, unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from game.game_engine import (GameEngine, START_LIVES, TIME_LIMIT, ROW_POINTS, GOAL_BONUS,
                              STATE_PLAYING, STATE_WON, STATE_GAME_OVER)
from game.collisions import check_collision
from game.renderer import START_ROW

pygame.init()
pygame.display.set_mode((600, 400))


def make_engine(parked=False, seed=1):
    random.seed(seed)
    e = GameEngine()
    if parked:                       # move all traffic off-screen for deterministic tests
        for v in e.vehicles:
            v.speed, v.x = 0, -500
    return e


def put_frog_under_vehicle(e):
    v = e.vehicles[0]
    e.frog.row, e.frog.col = v.row, int(v.x + v.width / 2) // 50


class Task1Collision(unittest.TestCase):
    def test_detects_overlap_anywhere_along_vehicle_width(self):
        e = make_engine()
        v = e.vehicles[0]
        e.frog.row, e.frog.col = v.row, 5
        v.speed = 0
        v.x = 5 * 50 - v.width + 20        # vehicle's LEFT edge is in col 4, its body overlaps col 5
        self.assertTrue(check_collision(e.frog, e.vehicles))

    def test_no_collision_when_clear(self):
        e = make_engine(parked=True)
        e.frog.row, e.frog.col = 3, 5
        self.assertFalse(check_collision(e.frog, e.vehicles))


class Task2Lives(unittest.TestCase):
    def test_three_lives_respawn_and_game_over(self):
        e = make_engine()
        self.assertEqual(e.lives, START_LIVES)
        for expected in (2, 1):
            put_frog_under_vehicle(e); e.update()
            self.assertEqual((e.lives, e.frog.row, e.state), (expected, START_ROW, STATE_PLAYING))
        put_frog_under_vehicle(e); e.update()
        self.assertEqual((e.lives, e.state), (0, STATE_GAME_OVER))

    def test_frozen_after_game_over_and_r_restarts(self):
        e = make_engine(); e.lives = 1
        put_frog_under_vehicle(e); e.update()
        pos = (e.frog.col, e.frog.row); e.handle_keydown(pygame.K_UP)
        self.assertEqual((e.frog.col, e.frog.row), pos)
        e.handle_keydown(pygame.K_r)
        self.assertEqual((e.lives, e.state, e.score), (START_LIVES, STATE_PLAYING, 0))


class Task3GoalScore(unittest.TestCase):
    def test_reaching_goal_wins_and_scores(self):
        e = make_engine(parked=True)
        for _ in range(7):
            e.handle_keydown(pygame.K_UP); e.update()
        self.assertEqual(e.state, STATE_WON)
        self.assertEqual(e.score, 7 * ROW_POINTS + GOAL_BONUS)

    def test_no_score_farming_and_score_survives_death(self):
        e = make_engine(parked=True)
        e.handle_keydown(pygame.K_UP); e.handle_keydown(pygame.K_DOWN); e.handle_keydown(pygame.K_UP)
        self.assertEqual(e.score, ROW_POINTS)
        e._lose_life()
        self.assertEqual(e.score, ROW_POINTS)


class Task4Timer(unittest.TestCase):
    def test_timeout_costs_a_life_and_resets_timer(self):
        e = make_engine(parked=True)
        e.update(TIME_LIMIT - 0.01); self.assertEqual(e.lives, START_LIVES)
        e.update(0.02)
        self.assertEqual((e.lives, e.time_left, e.frog.row), (START_LIVES - 1, TIME_LIMIT, START_ROW))

    def test_timer_stops_on_game_over_and_win(self):
        e = make_engine(parked=True); e.lives = 1
        e.update(TIME_LIMIT + 1)
        self.assertEqual(e.state, STATE_GAME_OVER)
        t = e.time_left; e.update(5); self.assertEqual(e.time_left, t)

    def test_collision_respawn_resets_timer(self):
        e = make_engine(); e.time_left = 10
        put_frog_under_vehicle(e); e.update(0.0)
        self.assertEqual(e.time_left, TIME_LIMIT)


if __name__ == "__main__":
    unittest.main()
