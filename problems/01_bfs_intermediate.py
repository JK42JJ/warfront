# MISSION: 01 | BFS | nco
# TITLE: Withdrawal Operation — BFS Mine Avoidance
# DESC: Avoid WALL and MOUNTAIN terrain and find the shortest passable path
# ALGO: BFS
# MODULE: mission_01_bfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 3
"""
┌─ BFS ───────────────────────────────────────────────────────────────────────┐
│  1. Multiple terrain types can be blocked, not just WALL                    │
│  2. Store blocked terrains in a set for O(1) lookup                         │
│  3. After filtering, add to visited AND queue in one step                   │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from collections import deque
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap — 12×12 grid
# data['start'] : (r, c)  — ALLY position
# data['goal']  : (r, c)  — TARGET position
# BLOCKED = {Terrain.WALL, Terrain.MOUNTAIN} — impassable terrains
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """BFS avoiding WALL and MOUNTAIN — return shortest path."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    BLOCKED = {Terrain.WALL, Terrain.MOUNTAIN}
    queue   = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == goal:
            return path

        for nr, nc in gmap.get_neighbors(r, c):
            terrain = gmap.grid[nr][nc].terrain
            if (nr, nc) not in visited and terrain not in BLOCKED:
                # TODO: add (nr, nc) to visited
                # TODO: append ((nr, nc), path + [(nr, nc)]) to queue
                pass

    return []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ No WALL or MOUNTAIN in path
#   ✅ Path connects start → goal
#   ✅ Shortest BFS path
#
# Expected output:
#   Path avoids M cells;  length varies with random terrain
# ─────────────────────────────────────────────────────────────────────────────
