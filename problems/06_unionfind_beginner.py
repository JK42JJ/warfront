# MISSION: 06 | Union-Find | soldier
# TITLE: Frontline Reorganization — Union-Find Basics
# DESC: Determine unit connectivity and integrate the front line
# ALGO: Union-Find
# MODULE: mission_06_uf
def solve(data):
    units  = data['units']   # Unit List
    links  = data['links']   # [(u, v), ...] Connected Unit  
    parent = {u: u for u in units}
    rank   = {u: 0 for u in units}

    def find(x):
        if parent[x] != x:
            # TODO: Path Compression Add
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        # TODO: rank Based union
        parent[ra] = rb

    for u, v in links:
        union(u, v)

    groups = {}
    for u in units:
        root = find(u)
        groups.setdefault(root, []).append(u)
    return {'groups': list(groups.values()), 'count': len(groups)}

# --- Execution Block ---
