# MISSION: 01 | BFS | general
# TITLE: Withdrawal Operation — BFS Optimization
# DESC: Track parents using dict and optimize path reconstruction
# ALGO: BFS
# MODULE: mission_01_bfs
from collections import deque
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    parent = {start: None}
    queue  = deque([start])
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            # TODO: parent Dictionarywith Path  
            path = []
            cur  = goal
            while cur is not None:
                break  # TODO: path.append(cur); cur = parent[cur]
            return path[::-1]
        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in parent and gmap.grid[nr][nc].terrain != Terrain.WALL:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []

# --- Execution Block ---
