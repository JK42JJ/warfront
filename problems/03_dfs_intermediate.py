# MISSION: 03 | DFS | officer
# TITLE: Infiltration Operation — DFS Connected Component Search
# DESC: Identify the largest connected passable region using iterative DFS
# ALGO: DFS
# MODULE: mission_03_dfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 4
"""
┌─ DFS ───────────────────────────────────────────────────────────────────────┐
│  1. Iterative DFS uses an explicit stack (avoids Python recursion limit)    │
│  2. Scan all cells — start a new DFS whenever you find an unvisited cell    │
│  3. Each DFS call discovers one connected component                         │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap
# data['start'] : (r, c)  — (not directly used; scan all cells)
# Return: list[(r,c)] — cells of the LARGEST connected passable region
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Find the largest connected passable region using iterative DFS."""
    gmap    = data['gmap']
    visited = set()
    regions = []

    def dfs_iterative(start_r: int, start_c: int) -> list:
        stack  = [(start_r, start_c)]
        region = []
        visited.add((start_r, start_c))
        while stack:
            cr, cc = stack.pop()
            region.append((cr, cc))
            for nr, nc in gmap.get_neighbors(cr, cc):
                if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                    visited.add((nr, nc))
                    # TODO: push (nr, nc) onto stack
        return region

    for r in range(gmap.rows):
        for c in range(gmap.cols):
            if (r, c) not in visited and gmap.grid[r][c].terrain != Terrain.WALL:
                regions.append(dfs_iterative(r, c))

    return max(regions, key=len) if regions else []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Returns a list of (r,c) cells all connected to each other
#   ✅ No WALL cells included
#   ✅ It is the LARGEST region by cell count
#
# Expected output:
#   Largest region: ~80–100 cells (depends on WALL density)
# ─────────────────────────────────────────────────────────────────────────────
