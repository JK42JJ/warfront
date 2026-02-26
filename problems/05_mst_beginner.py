# MISSION: 05 | MST | soldier
# TITLE: Supplywith   —   Basics
# DESC: Build a supply network connecting all bases with minimum cost
# ALGO: MST (Kruskal)
# MODULE: mission_05_mst
def solve(data):
    nodes = data['nodes']  # Base List
    edges = data['edges']  # [(cost, u, v), ...]

    # Union-Find
    parent = {n: n for n in nodes}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)

    mst, total = [], 0
    for cost, u, v in sorted(edges):
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, cost))
            total += cost
            # TODO: All Node Connect  Early End
    return {'mst': mst, 'total': total}

# --- Execution Block ---
