# Development log (summary of the AI-assisted session)

> NOTE: this is a *summary* of the session. The lab asks for the full chat history – export the actual
> conversation (PDF/doc or share link) and add it to this folder / the repo README.

## Prompt 0 – setup
Student: "Follow the instructions in the Lab 4 PDF for repo SETAPESU26/01_frogger and do everything."
AI: cloned the repo, read README + all 7 source files, identified the 4 tasks and the known bug.

## Prompt 1 – understand + fix the bug (Task 1)
AI found `collisions.py` only checks `int(v.x // CELL_SIZE) == frog.col`. A vehicle's body can overlap the
frog while its left edge is in a neighbouring column. Reproduced it (before video), fixed with rect overlap,
verified 0 mismatches between visual overlap and detection over 27,000 sampled states.

## Prompt 2 – lives and respawn (Task 2)
Added `lives`, `state` (playing / game_over), `_lose_life()`, HUD, Game Over banner, freeze + `R` restart.
Tested: 3 hits -> lives 2,1,0; respawn at start row; frog frozen on Game Over.

## Prompt 3 – goal and score (Task 3)
Goal row -> `STATE_WON`, +100 bonus; +10 per newly reached row (anti-farming via `best_row`).
Tested: full crossing = 7*10+100 = 170, state frozen after win.

## Prompt 4 – 30 s timer (Task 4)
`time_left` decremented by `dt`, timeout -> `_lose_life("Time's up!")`, reset per attempt, HUD turns red <=5 s.
Found and fixed my own test's off-by-one (float accumulation of 1/60 trips on frame 1801, i.e. 30.017 s).

## Review notes
- First "before" re-render accidentally used the fixed code; caught it by looking at the frame (HUD was present) and re-recorded from the original commit via `git archive 676bffe`.
- Caption overlay originally covered the Lives text; moved below the HUD.
