# MISSION: 03 | DFS | general
# TITLE: Infiltration Operation — DFS Repeat Stack
# DESC: Implement DFS using an explicit stack to prevent overflow
# ALGO: DFS
# MODULE: mission_03_dfs
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    # Stack: (CurrentPosition, Path)
    stack   = [(start, [start])]
    visited = {start}
    while stack:
        (r, c), path = stack.pop()  # LIFO
        if (r, c) == goal:
            return path
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                # TODO: visited Add and stack push
                pass
    return []

# --- Execution Block ---
