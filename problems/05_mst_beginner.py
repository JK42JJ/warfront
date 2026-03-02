# MISSION: 05 | MST | soldier
# TITLE: Supply Network — MST Basics (Kruskal)
# DESC: Connect all bases with minimum total supply route cost
# ALGO: MST (Kruskal)
# MODULE: mission_05_mst
# TIME_COMPLEXITY: O(E log E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 2
"""
┌─ KRUSKAL'S MST ─────────────────────────────────────────────────────────────┐
│  1. Sort all edges by cost (ascending)                                      │
│  2. Add an edge only if it connects two different components (no cycle)     │
│  3. Use Union-Find to detect whether two nodes are already connected        │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['nodes'] : list[str]              — base names e.g. ['A','B','C',...]
# data['edges'] : list[(cost, u, v)]     — sorted (cost, node1, node2)
# Return: {'mst': [(u,v,cost),...], 'total': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Kruskal's algorithm — build minimum spanning tree."""
    nodes = data['nodes']
    edges = data['edges']

    parent = {n: n for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path compression
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        parent[find(a)] = find(b)

    mst   = []
    total = 0

    for cost, u, v in sorted(edges):
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, cost))
            total += cost
            # TODO: early exit if len(mst) == len(nodes) - 1 (MST complete)

    return {'mst': mst, 'total': total}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ len(mst) == len(nodes) - 1
#   ✅ All nodes are connected through the MST edges
#   ✅ total is minimised
# ─────────────────────────────────────────────────────────────────────────────
