# MISSION: 01 | BFS | general
# TITLE: Withdrawal Operation — BFS Parent-Pointer Reconstruction
# DESC: Track parents with a dict and reconstruct the path without copying lists
# ALGO: BFS
# MODULE: mission_01_bfs
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V)
# DIFFICULTY: 5
"""
┌─ BFS ───────────────────────────────────────────────────────────────────────┐
│  1. Store parent[node] = prev instead of copying the path each step         │
│  2. Backtrack from goal → start using the parent dict, then reverse         │
│  3. This reduces space from O(V·P) to O(V) where P = path length           │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from collections import deque
from map import Terrain

# ── Data Reference ────────────────────────────────────────────────────────────
# data['gmap']  : GameMap
# data['start'] : (r, c)
# data['goal']  : (r, c)
# parent dict:  parent[node] = predecessor  (parent[start] = None)
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """BFS with parent-pointer path reconstruction."""
    gmap  = data['gmap']
    start = data['start']
    goal  = data['goal']

    parent = {start: None}   # node → predecessor (None for start)
    queue  = deque([start])

    while queue:
        r, c = queue.popleft()

        if (r, c) == goal:
            # TODO: reconstruct path by following parent pointers
            #   path = []
            #   cur  = goal
            #   while cur is not None:
            #       path.append(cur)
            #       cur = parent[cur]
            #   return path[::-1]
            path = []
            cur  = goal
            while cur is not None:
                path.append(cur)
                # TODO: advance cur to parent[cur]
                break   # ← remove this break once implemented
            return path[::-1]

        for nr, nc in gmap.get_neighbors(r, c):
            if (nr, nc) not in parent and gmap.grid[nr][nc].terrain != Terrain.WALL:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    return []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Identical path to standard BFS
#   ✅ No list copying per step  (O(V) space)
#
# Expected output:
#   Same path as beginner version but implemented with parent pointers
# ─────────────────────────────────────────────────────────────────────────────
