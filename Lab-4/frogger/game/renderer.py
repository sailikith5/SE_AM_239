"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

CELL_SIZE = 50
GRID_COLS = 12
GRID_ROWS = 8

WIDTH = CELL_SIZE * GRID_COLS
HEIGHT = CELL_SIZE * GRID_ROWS
WINDOW_SIZE = (WIDTH, HEIGHT)

GOAL_ROW = 0
ROAD_ROWS = list(range(1, GRID_ROWS - 1))   # rows 1..6
START_ROW = GRID_ROWS - 1                     # row 7

COLOR_BG = (20, 20, 25)
COLOR_GOAL = (40, 130, 60)
COLOR_ROAD = (45, 45, 50)
COLOR_START = (40, 90, 60)
COLOR_LANE_LINE = (90, 90, 90)
COLOR_FROG = (80, 220, 100)
COLOR_VEHICLE = (220, 80, 70)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, frog, vehicles):
    surface.fill(COLOR_BG)

    for row in range(GRID_ROWS):
        rect = pygame.Rect(0, row * CELL_SIZE, WIDTH, CELL_SIZE)
        if row == GOAL_ROW:
            pygame.draw.rect(surface, COLOR_GOAL, rect)
        elif row == START_ROW:
            pygame.draw.rect(surface, COLOR_START, rect)
        else:
            pygame.draw.rect(surface, COLOR_ROAD, rect)
            pygame.draw.line(surface, COLOR_LANE_LINE, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 1)

    for v in vehicles:
        pygame.draw.rect(surface, COLOR_VEHICLE, v.get_rect(CELL_SIZE), border_radius=6)

    pygame.draw.rect(surface, COLOR_FROG, frog.get_rect(CELL_SIZE), border_radius=8)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_text_right(surface, font, text, right_x, y, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    surface.blit(surf, (right_x - surf.get_width(), y))


def draw_text_centered(surface, font, text, center_x, y, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    surface.blit(surf, (center_x - surf.get_width() // 2, y))


def draw_banner(surface, font, text, subtext=None, color=(255, 220, 80)):
    """Centered message on a dark translucent panel so it is readable over the scene."""
    w, h = surface.get_size()
    panel_h = 90 if subtext else 56
    panel = pygame.Surface((w, panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 190))
    surface.blit(panel, (0, h // 2 - panel_h // 2))

    title = font.render(text, True, color)
    if subtext:
        surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 16)))
        sub = font.render(subtext, True, COLOR_TEXT)
        surface.blit(sub, sub.get_rect(center=(w // 2, h // 2 + 18)))
    else:
        surface.blit(title, title.get_rect(center=(w // 2, h // 2)))
