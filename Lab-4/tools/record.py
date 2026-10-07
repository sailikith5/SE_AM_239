"""Headless recorder: runs the Frogger game with scripted input and writes an mp4.
usage: SEED=31 record.py <game_dir> <out.mp4> <bug|after|timeout> <caption>
"""
import os, sys, random, subprocess
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
game_dir, out, scenario, caption = sys.argv[1:5]
sys.path.insert(0, game_dir); os.chdir(game_dir)
import pygame, imageio_ffmpeg
from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.SysFont("consolas", 20)
cap_font = pygame.font.SysFont("consolas", 14, bold=True)
SEED = int(os.environ.get("SEED", "7"))
random.seed(SEED)
if scenario == "timeout":
    import game.game_engine as ge
    ge.TIME_LIMIT = 3.0          # demo only: shorten the timer so timeout fits in 10 s
engine = GameEngine()
U, D, L, R, RS = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_r

events = {}

def clear_ahead(e):
    f = e.frog
    nr = f.row - 1
    fx0, fx1 = f.col * 50, f.col * 50 + 50
    for v in e.vehicles:
        if v.row == nr:
            # look-ahead: vehicle within 70px horizontally of the target cell
            if v.x < fx1 + 70 and v.x + v.width > fx0 - 70:
                return False
    return True

ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}",
    "-r", "60", "-i", "-", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "23", out],
    stdin=subprocess.PIPE)

FRAMES = 60 * 10
for i in range(FRAMES):
    if scenario == "bug":
        # keep the frog standing in lane row 5 (a right-moving lane) so the bug is visible
        if i >= 30 and i % 12 == 0 and engine.frog.row > 5:
            engine.handle_keydown(U)
    elif scenario == "after":
        if getattr(engine, "state", "playing") == "playing":
            if engine.lives == 3:                      # phase 1: reckless -> get hit once
                if i >= 20 and i % 8 == 0: engine.handle_keydown(U)
            elif i % 15 == 0 and clear_ahead(engine):  # phase 2: careful -> reach the goal
                engine.handle_keydown(U)
    elif scenario == "timeout":
        pass                                           # idle: let the timer run out

    from game.collisions import check_collision
    fr = engine.frog.get_rect(50)
    overlap_nohit = (not check_collision(engine.frog, engine.vehicles)) and \
        any(v.get_rect(50).colliderect(fr) for v in engine.vehicles if v.row == engine.frog.row)
    engine.update()
    engine.draw(screen, font)
    if scenario == "bug" and overlap_nohit:
        t = cap_font.render("OVERLAP - BUT NO HIT DETECTED!", True, (255, 255, 255), (200, 0, 0))
        screen.blit(t, (10, 34))
    cap = cap_font.render(caption, True, (255, 255, 0), (0, 0, 0))
    screen.blit(cap, (WINDOW_SIZE[0] - cap.get_width() - 6, 34))   # free strip under the HUD
    ff.stdin.write(pygame.image.tostring(screen, "RGB"))
ff.stdin.close(); ff.wait()
print("wrote", out)
