# MISSION: 02 | Dijkstra | soldier
# TITLE: UAV Reconnaissance — Dijkstra Basics
# DESC: Find the minimum-fuel path for a drone considering terrain movement costs
# ALGO: Dijkstra
# MODULE: mission_02_dijkstra
# TIME_COMPLEXITY: O((V+E) log V)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 2
"""
┌─ DIJKSTRA ──────────────────────────────────────────────────────────────────┐
│  1. Use a min-heap (heapq) — always process the lowest-cost cell next       │
│  2. dist[node] = best known cost; skip if we already found a cheaper path   │
│  3. Cost per cell: gmap.get_cost(r, c) — Plain=1, Forest=2, River=4, Mt=5  │
└─────────────────────────────────────────────────────────────────────────────┘
"""
import heapq
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap — terrain with movement costs
# data['start'] : (r, c)
# data['goal']  : (r, c)
# gmap.get_cost(r, c) → int  — movement cost of entering cell (r, c)
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Dijkstra — return minimum-cost path from start to goal."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    dist = {start: 0}
    heap = [(0, start, [start])]   # (total_cost, position, path)

    while heap:
        cost, (r, c), path = heapq.heappop(heap)

        if (r, c) == goal:
            return path

        if cost > dist.get((r, c), float('inf')):
            continue   # stale entry — skip

        for nr, nc in gmap.get_neighbors(r, c):
            if gmap.grid[nr][nc].terrain == Terrain.WALL:
                continue
            # TODO: new_cost = cost + gmap.get_cost(nr, nc)
            # TODO: if new_cost < dist.get((nr,nc), inf):
            #           dist[(nr,nc)] = new_cost
            #           heapq.heappush(heap, (new_cost, (nr,nc), path+[(nr,nc)]))
            pass

    return []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Returns minimum-cost path (not just shortest hop count)
#   ✅ Forest(2), River(4), Mountain(5) are more expensive than Plain(1)
#
# Expected output:
#   Path prefers Plains over Mountains;  total cost printed in viz panel
# ─────────────────────────────────────────────────────────────────────────────
