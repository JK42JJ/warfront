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
│  1. Recursive DFS: explore deep before backtracking                         │
│  2. Add to visited BEFORE recursing to prevent infinite loops               │
│  3. Remove from visited on backtrack if you want ALL paths (exhaustive)     │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap — 12×12 grid with periodic WALL pattern
# data['start'] : (r, c)
# data['goal']  : (r, c)
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Recursive DFS — collect all paths, return the shortest."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    all_paths = []

    def dfs(r: int, c: int, path: list, visited: set) -> None:
        if (r, c) == goal:
            all_paths.append(path[:])
            return
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                visited.add((nr, nc))
                path.append((nr, nc))
                # TODO: recurse — call dfs(nr, nc, path, visited)
                path.pop()
                visited.remove((nr, nc))

    dfs(start[0], start[1], [start], {start})
    return min(all_paths, key=len) if all_paths else []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ result[0] == start,  result[-1] == goal
#   ✅ returns shortest among all found DFS paths
#
# Expected output:
#   Path: [(0,0), ..., (11,11)]  — may differ from BFS path
# ─────────────────────────────────────────────────────────────────────────────
