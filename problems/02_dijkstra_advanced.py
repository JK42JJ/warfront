# MISSION: 02 | Dijkstra | general
# TITLE: UAV Reconnaissance — Dijkstra All-Shortest-Paths
# DESC: Find shortest paths from start to ALL reachable cells
# ALGO: Dijkstra (SSSP)
# MODULE: mission_02_dijkstra
# TIME_COMPLEXITY: O((V+E) log V)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 5
"""
┌─ DIJKSTRA (SSSP) ───────────────────────────────────────────────────────────┐
│  1. Single-Source Shortest Path: one source → distances to all nodes        │
│  2. Remove early exit — process every reachable node                        │
│  3. Return a dist dict {(r,c): min_cost, ...} covering the whole grid       │
└─────────────────────────────────────────────────────────────────────────────┘
"""
import heapq
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap
# data['start'] : (r, c)  — single source
# Return: dict[(r,c): int] — minimum cost from start to each reachable cell
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Dijkstra SSSP — return minimum-cost distance from start to every cell."""
    gmap  = data['gmap']
    start = data['start']

    dist    = {start: 0}
    heap    = [(0, start)]
    visited = set()

    while heap:
        cost, (r, c) = heapq.heappop(heap)

        if (r, c) in visited:
            continue
        visited.add((r, c))

        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) in visited or gmap.grid[nr][nc].terrain == Terrain.WALL:
                continue
            # TODO: new_cost = cost + gmap.get_cost(nr, nc)
            # TODO: if new_cost < dist.get((nr,nc), inf):
            #           dist[(nr,nc)] = new_cost
            #           heapq.heappush(heap, (new_cost, (nr,nc)))
            pass

    return dist


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ dist[start] == 0
#   ✅ every reachable cell has an entry
#   ✅ unreachable cells are absent from the dict
#
# Expected output:
#   {(0,0): 0, (0,1): 1, (1,0): 1, ..., (11,11): 18}
# ─────────────────────────────────────────────────────────────────────────────
