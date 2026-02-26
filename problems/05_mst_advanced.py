# MISSION: 05 | MST | general
# TITLE: Supplywith   —    
# DESC: Construct MST using heap-based Prims algorithm
# ALGO: MST (Prim)
# MODULE: mission_05_mst
import heapq

def solve(data):
    nodes    = data['nodes']
    adj      = data['adj']   # {node: [(cost, neighbor), ...]}
    start    = nodes[0]
    visited  = {start}
    heap     = [(c, start, nb) for c, nb in adj.get(start, [])]
    heapq.heapify(heap)
    mst, total = [], 0
    while heap and len(visited) < len(nodes):
        cost, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, cost))
        total += cost
        for c, nb in adj.get(v, []):
            if nb not in visited:
                # TODO: heappush
                pass
    return {'mst': mst, 'total': total}

# --- Execution Block ---
