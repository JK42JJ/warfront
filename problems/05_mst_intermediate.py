# MISSION: 05 | MST | officer
# TITLE: Supplywith   — Maximum   Tree
# DESC: Build a supply network using the maximum reliability path
# ALGO: MST (Maximum Spanning Tree)
# MODULE: mission_05_mst
def solve(data):
    nodes  = data['nodes']
    edges  = data['edges']  # [(cost, u, v)]
    parent = {n:n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        parent[find(a)] = find(b)

    mst, total = [], 0
    # TODO: Maximum   Tree = Cost Descending Sort
    for cost, u, v in sorted(edges, reverse=True):
        if find(u) != find(v):
            union(u,v)
            mst.append((u,v,cost))
            total += cost
    return {'mst': mst, 'total': total}

# --- Execution Block ---
