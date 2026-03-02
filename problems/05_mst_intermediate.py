# MISSION: 05 | MST | officer
# TITLE: Supply Network — Maximum Spanning Tree
# DESC: Build the most reliable supply network using maximum-cost edges
# ALGO: MST (Maximum Spanning Tree)
# MODULE: mission_05_mst
# TIME_COMPLEXITY: O(E log E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 4
"""
┌─ MAXIMUM SPANNING TREE ─────────────────────────────────────────────────────┐
│  1. Same as Kruskal's, but sort edges DESCENDING (highest reliability first)│
│  2. Greedy choice: always pick the highest-cost edge that doesn't form cycle│
│  3. Result: the tree that maximises total edge weight                        │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['nodes'] : list[str]
# data['edges'] : list[(cost, u, v)]
# Return: {'mst': [(u,v,cost),...], 'total': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Kruskal's for Maximum Spanning Tree — sort edges descending."""
    nodes  = data['nodes']
    edges  = data['edges']
    parent = {n: n for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        parent[find(a)] = find(b)

    mst   = []
    total = 0

    # TODO: sort edges in DESCENDING order by cost (reverse=True)
    for cost, u, v in sorted(edges, reverse=True):
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, cost))
            total += cost

    return {'mst': mst, 'total': total}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Total is MAXIMISED (not minimised)
#   ✅ len(mst) == len(nodes) - 1
# ─────────────────────────────────────────────────────────────────────────────
