"""
collisions: frog-vs-vehicle collision detection.
"""

CELL_SIZE = 50


def check_collision(frog, vehicles):
    """
    Returns True if the frog is currently hit by any vehicle.

    Uses real rectangle overlap (the same rects that are drawn on screen)
    so a vehicle hits the frog anywhere along its full width, not just when
    its left edge happens to sit in the frog's grid column.
    """
    frog_rect = frog.get_rect(CELL_SIZE)
    for v in vehicles:
        if v.row != frog.row:
            continue
        if frog_rect.colliderect(v.get_rect(CELL_SIZE)):
            return True
    return False
