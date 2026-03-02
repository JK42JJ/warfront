# MISSION: 03 | DFS | soldier
# TITLE: Infiltration Operation — DFS Basics
# DESC: Find a path through enemy territory using recursive DFS
# ALGO: DFS
# MODULE: mission_03_dfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 2
"""
┌─ DFS ───────────────────────────────────────────────────────────────────────┐
│  1. Standard DFS: go deep, stop the moment you reach the goal (return True) │
│  2. Add to visited BEFORE recursing — do NOT remove (prevents re-visits)    │
│  3. Build path as you go deep; pop only when a branch is a dead end         │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap — 12×12 grid with periodic WALL pattern
# data['start'] : (row, col)
# data['goal']  : (row, col)
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Standard DFS — find the first reachable path to goal (O(V+E))."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    visited = {start}
    path    = [start]

    def dfs(r: int, c: int) -> bool:
        """Explore from (r, c). Return True when goal is reached."""
        if (r, c) == goal:
            return True
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                visited.add((nr, nc))     # mark before diving in
                path.append((nr, nc))
                # TODO: recurse into (nr, nc); return True immediately if found
                path.pop()               # dead end — backtrack
        return False

    dfs(start[0], start[1])
    return path if path[-1] == goal else []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ result[0] == start
#   ✅ result[-1] == goal
#   ✅ each consecutive cell is adjacent (no teleporting)
#
# NOTE: DFS does NOT guarantee the shortest path — that's BFS/Dijkstra.
#       This mission is about traversal, not optimality.
# ─────────────────────────────────────────────────────────────────────────────
