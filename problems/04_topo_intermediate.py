# MISSION: 04 | Topological Sort | officer
# TITLE: Operation Plan — Cycle Detection
# DESC: Detect and report cyclic dependencies during topological sort
# ALGO: Topological Sort
# MODULE: mission_04_topo
from collections import deque

def solve(data):
    graph    = data['graph']
    indegree = dict(data['indegree'])
    queue    = deque([n for n,d in indegree.items() if d==0])
    order, processed = [], 0
    while queue:
        node = queue.popleft()
        order.append(node)
        processed += 1
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    # TODO: Cycle Detection Add Condition
    has_cycle = False  # processed != len(indegree) If Cycle
    return {'order': order, 'has_cycle': has_cycle}

# --- Execution Block ---
