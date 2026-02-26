# MISSION: 03 | DFS | soldier
# TITLE: Infiltration Operation — DFS Basics
# DESC: Search all paths within enemy lines using recursive DFS
# ALGO: DFS
# MODULE: mission_03_dfs
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    result = []

    def dfs(r, c, path, visited):
        if (r, c) == goal:
            result.append(path[:])
            return
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                visited.add((nr, nc))
                path.append((nr, nc))
                # TODO: Recursion Call Add
                path.pop()
                visited.remove((nr, nc))

    dfs(start[0], start[1], [start], {start})
    # Shortest path Return
    return min(result, key=len) if result else []

# --- Execution Block ---
