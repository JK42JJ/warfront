# MISSION: 01 | BFS | nco
# TITLE: Withdrawal Operation — BFS Mine Avoidance
# DESC: Avoid WALL + MOUNTAIN (3x cost) and search for the shortest path
# ALGO: BFS
# MODULE: mission_01_bfs
from collections import deque
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    # Impassable terrain List
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
                # TODO: visited Add and queue to (Position, Path) push
                pass
    return []

# --- Execution Block ---
