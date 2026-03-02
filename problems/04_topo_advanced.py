# MISSION: 04 | Topological Sort | general
# TITLE: Operation Plan — DFS-Based Topological Sort
# DESC: Implement topological sort using DFS post-order traversal
# ALGO: Topological Sort (DFS)
# MODULE: mission_04_topo
# TIME_COMPLEXITY: O(V+E)
# SPACE_COMPLEXITY: O(V+E)
# DIFFICULTY: 5
"""
┌─ TOPOLOGICAL SORT (DFS) ────────────────────────────────────────────────────┐
│  1. DFS post-order: append a node AFTER all its descendants are processed   │
│  2. Reverse the result at the end to get topological order                  │
│  3. Unlike Kahn's, this works recursively by finishing deep nodes first     │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ── Data Reference ────────────────────────────────────────────────────────────
# data['graph']    : dict  — {node: [next_node, ...]}
# data['indegree'] : dict  — keys give the full node list
# Return: list[str] in topological order
# ─────────────────────────────────────────────────────────────────────────────

def solve(data: dict) -> list:
    """DFS post-order topological sort."""
    graph   = data['graph']
    nodes   = list(data['indegree'].keys())
    visited = set()
    result  = []

    def dfs(node: str) -> None:
        visited.add(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                dfs(nxt)
        # TODO: append node to result AFTER all descendants are processed
        pass

    for n in nodes:
        if n not in visited:
            dfs(n)

    return result[::-1]   # reverse post-order = topological order


# ─────────────────────────────────────────────────────────────────────────────
# WARFRONT checks:
#   ✅ Same valid ordering as Kahn's algorithm
#   ✅ Every prerequisite appears before its dependent
# ─────────────────────────────────────────────────────────────────────────────
