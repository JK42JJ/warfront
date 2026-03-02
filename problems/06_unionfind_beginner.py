# MISSION: 06 | Union-Find | soldier
# TITLE: Frontline Reorganization — Union-Find Basics
# DESC: Determine unit connectivity and integrate the front line
# ALGO: Union-Find
# MODULE: mission_06_uf
# TIME_COMPLEXITY: O(α(n))
# SPACE_COMPLEXITY: O(n)
# DIFFICULTY: 2
"""
┌─ UNION-FIND ────────────────────────────────────────────────────────────────┐
│  1. parent[x] = x initially — every node is its own root                   │
│  2. find(x): follow parent pointers until reaching the root                 │
│  3. union(a, b): merge the two groups by pointing one root to the other     │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['units'] : list[str]         — unit names
# data['links'] : list[(str, str)]  — (unit_a, unit_b) connections
# Return: {'groups': [[...],[...]], 'count': int}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Union-Find — group connected units and return component count."""
    units  = data['units']
    links  = data['links']
    parent = {u: u for u in units}
    rank   = {u: 0 for u in units}

    def find(x: str) -> str:
        if parent[x] != x:
            # TODO: path compression — parent[x] = find(parent[x])
            parent[x] = find(parent[x])
        return parent[x]

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        # TODO: union-by-rank — attach lower-rank root under higher-rank root
        parent[ra] = rb

    for u, v in links:
        union(u, v)

    groups = {}
    for u in units:
        groups.setdefault(find(u), []).append(u)

    return {'groups': list(groups.values()), 'count': len(groups)}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Units in the same group are all connected
#   ✅ count == number of distinct components
# ─────────────────────────────────────────────────────────────────────────────
