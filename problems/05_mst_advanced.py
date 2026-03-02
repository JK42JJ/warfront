# MISSION: 05 | MST | general
# TITLE: Supply Network — Prim's Algorithm
# DESC: Construct MST using a heap-based Prim's algorithm starting from node 0
# ALGO: MST (Prim)
# MODULE: mission_05_mst
# TIME_COMPLEXITY: O(E log E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 5
"""
┌─ PRIM'S MST ────────────────────────────────────────────────────────────────┐
│  1. Grow the tree from a single start node using a min-heap                 │
│  2. Always add the cheapest edge connecting the tree to an unvisited node   │
│  3. adj[node] = [(cost, neighbour), ...] — adjacency list format            │
└─────────────────────────────────────────────────────────────────────────────┘
"""
import heapq

# ── Data Reference ────────────────────────────────────────────────────────────
# data['nodes'] : list[str]
# data['adj']   : dict  — {node: [(cost, neighbour), ...]}
# Return: {'mst': [(u,v,cost),...], 'total': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Prim's algorithm — grow MST from nodes[0]."""
    nodes   = data['nodes']
    adj     = data['adj']
    start   = nodes[0]
    visited = {start}
    heap    = [(c, start, nb) for c, nb in adj.get(start, [])]
    heapq.heapify(heap)
    mst   = []
    total = 0

    while heap and len(visited) < len(nodes):
        cost, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, cost))
        total += cost
        for c, nb in adj.get(v, []):
            if nb not in visited:
                # TODO: push (c, v, nb) onto the heap
                pass

    return {'mst': mst, 'total': total}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ len(mst) == len(nodes) - 1
#   ✅ Same total cost as Kruskal result
# ─────────────────────────────────────────────────────────────────────────────
