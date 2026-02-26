# MISSION: 02 | Dijkstra | soldier
# TITLE: UAV Reconnaissance — Dijkstra Basics
# DESC: Find the minimum fuel path for a drone considering terrain costs
# ALGO: Dijkstra
# MODULE: mission_02_dijkstra
import heapq
from map import Terrain

def solve(data):
    gmap, start, goal = data['gmap'], data['start'], data['goal']
    dist = {start: 0}
    heap = [(0, start, [start])]  # (Cost, Position, Path)
    while heap:
        cost, (r, c), path = heapq.heappop(heap)
        if (r, c) == goal:
            return path
        if cost > dist.get((r, c), float('inf')):
            continue
        for nr, nc in gmap.get_neighbors(r, c):
            if gmap.grid[nr][nc].terrain == Terrain.WALL:
                continue
            # TODO: next cell Cost  gmap.get_cost(nr, nc) with Calculateto heappush
            pass
    return []

# --- Execution Block ---
