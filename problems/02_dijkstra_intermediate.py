# MISSION: 02 | Dijkstra | nco
# TITLE: UAV Reconnaissance — Dijkstra with Cost Tracking
# DESC: Return both the minimum path and total fuel cost
# ALGO: Dijkstra
# MODULE: mission_02_dijkstra
# TIME_COMPLEXITY: O((V+E) log V)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 3
"""
┌─ DIJKSTRA ──────────────────────────────────────────────────────────────────┐
│  1. Track both the path and the cumulative cost                              │
│  2. Return a dict with 'path' and 'cost' keys                               │
│  3. The visited set prevents re-processing cheaper-already-known nodes       │
└─────────────────────────────────────────────────────────────────────────────┘
"""
import heapq
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap
# data['start'] : (r, c)
# data['goal']  : (r, c)
# Return: {'path': [(r,c),...], 'cost': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Dijkstra — return optimal path and total fuel cost."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    visited = set()
    heap    = [(0, start, [start])]

    while heap:
        cost, (r, c), path = heapq.heappop(heap)

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if (r, c) == goal:
            # TODO: return {'path': path, 'cost': cost}
            return {'path': [], 'cost': 0}

        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in visited and gmap.grid[nr][nc].terrain != Terrain.WALL:
                # TODO: calculate new_cost, push to heap
                pass

    return {'path': [], 'cost': -1}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ result['path'][0] == start,  result['path'][-1] == goal
#   ✅ result['cost'] == sum of terrain costs along path
#
# Expected output:
#   {'path': [(0,0),...,(11,11)], 'cost': 18}  ← cost varies with terrain
# ─────────────────────────────────────────────────────────────────────────────
