# MISSION: 03 | DFS | general
# TITLE: Infiltration Operation — DFS Iterative Stack
# DESC: Implement path-finding DFS using an explicit stack (no recursion)
# ALGO: DFS
# MODULE: mission_03_dfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 5
"""
┌─ DFS ───────────────────────────────────────────────────────────────────────┐
│  1. Explicit stack:  stack.pop() → LIFO (last in, first out)                │
│  2. Push (position, path) pairs — no recursion needed                      │
│  3. DFS may return a LONGER path than BFS — it explores deep first         │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap
# data['start'] : (r, c)
# data['goal']  : (r, c)
# stack stores (position, path) tuples — use .pop() not .popleft()
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Iterative DFS — return any valid path from start to goal."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    stack   = [(start, [start])]   # (position, path)
    visited = {start}

    while stack:
        (r, c), path = stack.pop()   # LIFO — depth-first

        if (r, c) == goal:
            return path

        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                # TODO: add (nr, nc) to visited
                # TODO: push ((nr, nc), path + [(nr, nc)]) onto stack
                pass

    return []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Returns a valid path (may not be shortest)
#   ✅ Uses stack.pop() not queue.popleft()
#   ✅ No recursion
#
# Expected output:
#   Path: [(0,0), ..., (11,11)]  — longer than BFS path is normal
# ─────────────────────────────────────────────────────────────────────────────
