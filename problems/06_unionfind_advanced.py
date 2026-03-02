# MISSION: 06 | Union-Find | general
# TITLE: Frontline Reorganization — Path Compression + Union-by-Rank
# DESC: Achieve near-O(1) operations with path compression and union-by-rank
# ALGO: Union-Find
# MODULE: mission_06_uf
# TIME_COMPLEXITY: O(α(n))
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 5
"""
┌─ UNION-FIND (OPTIMISED) ────────────────────────────────────────────────────┐
│  1. Path compression (two-pass): flatten tree while finding root            │
│  2. Union-by-rank: always attach the shorter tree under the taller one      │
│  3. Combined: amortised O(α(n)) per operation (nearly constant)             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['units'] : list[str]
# data['links'] : list[(str, str)]
# Return: {'groups': [[...],[...]], 'count': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Optimised Union-Find with path compression and union-by-rank."""
    units  = data['units']
    links  = data['links']
    parent = {u: u for u in units}
    rank   = {u: 0 for u in units}

    def find(x: str) -> str:
        # Two-pass iterative path compression
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: str, b: str) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    components = len(units)
    for u, v in links:
        if union(u, v):
            components -= 1

    groups = {}
    for u in units:
        groups.setdefault(find(u), []).append(u)

    return {'groups': list(groups.values()), 'count': components}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Same results as basic version but faster
#   ✅ count == number of connected components
# ─────────────────────────────────────────────────────────────────────────────
