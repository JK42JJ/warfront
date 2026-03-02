# MISSION: 01 | BFS | soldier
# TITLE: Withdrawal Operation — BFS Basics
# DESC: Escape the encircled Ally (@) to the Base (★) via the shortest path
# ALGO: BFS
# MODULE: mission_01_bfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 2
"""
┌─ BFS ───────────────────────────────────────────────────────────────────────┐
│  1. Use a queue (FIFO) — deque from collections                             │
│  2. Mark cells visited before adding to queue to avoid cycles               │
│  3. The first time you reach the goal, the path is the shortest             │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from collections import deque
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap — 12×12 grid
# data['start'] : (r, c)  — start cell
# data['goal']  : (r, c)  — target cell
# gmap.get_neighbors(r, c) → [(nr, nc), ...]
# gmap.grid[r][c].terrain  → Terrain.PLAIN / .WALL / .FOREST / .RIVER / .MOUNTAIN
# ─────────────────────────────────────────────────────────────────────────────

def is_passable(gmap, r: int, c: int) -> bool:
    """Return True if the cell (r, c) can be traversed."""
    # TODO: return False if terrain is Terrain.WALL
    return True


def solve(data: dict) -> list:
    """BFS — return shortest path from start to goal.

    Returns:
        list[(row, col)] from start to goal inclusive, or [] if no path.
    """
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    queue   = deque([(start, [start])])   # (position, path so far)
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == goal:
            return path

        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and is_passable(gmap, nr, nc):
                # TODO: mark (nr, nc) as visited
                # TODO: append ((nr, nc), path + [(nr, nc)]) to queue
                pass

    return []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ returns list[(row, col)]
#   ✅ result[0] == start,  result[-1] == goal
#   ✅ each step is a valid 4-directional move
#   ✅ no WALL cells in path
#
# Expected output:
#   Path  : [(0,0), (0,1), (1,1), ..., (11,11)]
#   Length: ~15–20 steps depending on wall layout
# ─────────────────────────────────────────────────────────────────────────────
