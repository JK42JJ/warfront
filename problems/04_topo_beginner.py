# MISSION: 04 | Topological Sort | soldier
# TITLE: Operation Plan — Topological Sort Basics
# DESC: Determine execution order while respecting dependencies (Kahns algorithm)
# ALGO: Topological Sort
# MODULE: mission_04_topo
from collections import deque

def solve(data):
    graph   = data['graph']    # {node: [next, ...]}
    indegree= data['indegree'] # {node: count}
    queue   = deque([n for n, d in indegree.items() if d == 0])
    order   = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            # TODO: indegree  0    queue to Add
    return order if len(order) == len(indegree) else []  # Cycle Detection

# --- Execution Block ---
