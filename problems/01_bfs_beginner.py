# MISSION: 01 | BFS | soldier
# TITLE: Withdrawal Operation — BFS Basics
# DESC: Escape the encircled Ally (@) to the Base (★) via the Shortest Path (implement Wall condition)
# ALGO: BFS
# MODULE: mission_01_bfs
from collections import deque
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    queue   = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == goal:
            return path
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited:
                # TODO: Terrain.WALL Add Condition
                pass
    return []

# --- Execution Block ---
