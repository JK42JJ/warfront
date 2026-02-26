# MISSION: 02 | Dijkstra | nco
# TITLE: UAV Reconnaissance — Dijkstra  
# DESC: Search for the minimum cost path from multiple starting points to the goal
# ALGO: Dijkstra
# MODULE: mission_02_dijkstra
import heapq
from map import Terrain

def solve(data):
    gmap   = data['gmap']
    starts = data.get('starts', [data['start']])  #  Among Start 
    goal   = data['goal']
    dist   = {}
    heap   = []
    for s in starts:
        dist[s] = 0
        heapq.heappush(heap, (0, s, [s]))
    while heap:
        cost, (r,c), path = heapq.heappop(heap)
        if (r,c) == goal: return path
        if cost > dist.get((r,c), float('inf')): continue
        for nr,nc in gmap.get_neighbors(r,c):
            if gmap.grid[nr][nc].terrain == Terrain.WALL: continue
            nc_cost = cost + gmap.get_cost(nr,nc)
            if nc_cost < dist.get((nr,nc), float('inf')):
                dist[(nr,nc)] = nc_cost
                # TODO: heappush Add
    return []

# --- Execution Block ---
