# MISSION: 06 | Union-Find | officer
# TITLE: Frontline Reorganization — Merge / Query Operations
# DESC: Process real-time merge and connectivity queries using Union-Find
# ALGO: Union-Find
# MODULE: mission_06_uf
# TIME_COMPLEXITY: O(α(n))
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 4
"""
┌─ UNION-FIND ────────────────────────────────────────────────────────────────┐
│  1. 'merge' query: call union(a, b)                                         │
│  2. 'connected' query: return find(a) == find(b)                            │
│  3. Two-pass path compression (iterative) avoids recursion overhead         │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['units']   : list[str]
# data['queries'] : list[('merge'|'connected', str, str)]
# Return: list[bool]  — one entry per 'connected' query
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Handle merge/connected queries and return results for 'connected' ops."""
    units   = data['units']
    queries = data['queries']
    parent  = {u: u for u in units}
    rank    = {u: 0 for u in units}

    def find(x: str) -> str:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    results = []
    for q in queries:
        if q[0] == 'merge':
            # TODO: call union(q[1], q[2])
            pass
        elif q[0] == 'connected':
            # TODO: append (find(q[1]) == find(q[2])) to results
            pass

    return results


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Each 'connected' query produces exactly one bool in results
#   ✅ Merges are reflected in subsequent connected queries
# ─────────────────────────────────────────────────────────────────────────────
