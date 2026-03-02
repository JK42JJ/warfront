# MISSION: 04 | Topological Sort | officer
# TITLE: Operation Plan — Cycle Detection
# DESC: Detect and report cyclic dependencies during topological sort
# ALGO: Topological Sort
# MODULE: mission_04_topo
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 4
"""
┌─ TOPOLOGICAL SORT ──────────────────────────────────────────────────────────┐
│  1. If processed count < total nodes → a cycle was detected                 │
│  2. Return both the valid order AND a has_cycle boolean                     │
│  3. Nodes inside a cycle never reach in-degree 0                            │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from collections import deque

# ── Data Reference ────────────────────────────────────────────────────────────
# data['graph']    : dict  — {node: [next_node, ...]}
# data['indegree'] : dict  — {node: prerequisite_count}
# Return: {'order': list, 'has_cycle': bool}
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> dict:
    """Kahn's with cycle detection — return order and cycle flag."""
    graph    = data['graph']
    indegree = dict(data['indegree'])

    queue     = deque([n for n, d in indegree.items() if d == 0])
    order     = []
    processed = 0

    while queue:
        node = queue.popleft()
        order.append(node)
        processed += 1
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    # TODO: has_cycle = True if processed != len(indegree)
    has_cycle = False

    return {'order': order, 'has_cycle': has_cycle}


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ has_cycle == True when graph contains a circular dependency
#   ✅ order contains only nodes before the cycle
# ─────────────────────────────────────────────────────────────────────────────
