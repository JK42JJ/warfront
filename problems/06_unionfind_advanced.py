# MISSION: 06 | Union-Find | general
# TITLE: Frontline Reorganization — PathCompression +   Optimization
# DESC: Achieve O(1) operations using path compression and union-by-rank
# ALGO: Union-Find
# MODULE: mission_06_uf
def solve(data):
    units  = data['units']
    links  = data['links']
    parent = {u: u for u in units}
    rank   = {u: 0 for u in units}

    def find(x):
        # TODO: Repeat  Based Path Compression (Recursion  )
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        if rank[ra] < rank[rb]: ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]: rank[ra] += 1
        return True

    components = len(units)
    for u, v in links:
        if union(u, v):
            components -= 1

    groups = {}
    for u in units:
        groups.setdefault(find(u), []).append(u)
    return {'groups': list(groups.values()), 'count': components}

# --- Execution Block ---
