# MISSION: 02 | Dijkstra | general
# TITLE: UAV Reconnaissance — Dijkstra Optimization
# DESC: Optimize memory by separating distance and parent tracking
# ALGO: Dijkstra
# MODULE: mission_02_dijkstra
import heapq
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    dist   = {start: 0}
    parent = {start: None}
    heap   = [(0, start)]
    while heap:
        cost, (r, c) = heapq.heappop(heap)
        if (r, c) == goal:
            # TODO: parent backtracking Path Reconstruction
            path, cur = [], goal
            while cur:
                path.append(cur); cur = parent[cur]
            return path[::-1]
        if cost > dist.get((r, c), float('inf')):
            continue
        for nr, nc in gmap.get_neighbors(r, c):
            if gmap.grid[nr][nc].terrain == Terrain.WALL:
                continue
            new_cost = cost + gmap.get_cost(nr, nc)
            if new_cost < dist.get((nr, nc), float('inf')):
                dist[(nr, nc)]   = new_cost
                parent[(nr, nc)] = (r, c)
                # TODO: heappush Add
    return []

# --- Execution Block ---
