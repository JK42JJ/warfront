# MISSION: 04 | Topological Sort | soldier
# TITLE: Operation Plan — Topological Sort Basics
# DESC: Determine execution order while respecting task dependencies (Kahn's algorithm)
# ALGO: Topological Sort
# MODULE: mission_04_topo
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 2
"""
┌─ TOPOLOGICAL SORT (KAHN'S) ─────────────────────────────────────────────────┐
│  1. Compute in-degree for every node (how many prerequisites it has)        │
│  2. Enqueue all nodes with in-degree = 0 (no prerequisites)                 │
│  3. Process queue: dequeue, add to order, reduce in-degree of neighbours    │
└─────────────────────────────────────────────────────────────────────────────┘
"""
from collections import deque

# ── Data Reference ────────────────────────────────────────────────────────────
# data['graph']    : dict  — {node: [next_node, ...]}
# data['indegree'] : dict  — {node: prerequisite_count}
# Return: list[str] in topological order, or [] if cycle detected
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """Kahn's algorithm — return valid execution order or [] if cyclic."""
    graph    = data['graph']
    indegree = dict(data['indegree'])   # mutable copy

    queue = deque([n for n, d in indegree.items() if d == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            # TODO: if indegree[nxt] == 0: add nxt to queue
            pass

    # If order length != total nodes, a cycle exists
    return order if len(order) == len(indegree) else []


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ All nodes appear exactly once in the result
#   ✅ Every dependency appears before the node that needs it
#   ✅ Returns [] when a cycle is present
# ─────────────────────────────────────────────────────────────────────────────
